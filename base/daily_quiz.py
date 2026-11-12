"""Daily Quiz for the homepage: 10 fresh questions a day per category, the same for every student.

Questions come from the test-series content engine, seeded by the date, so there is nothing to store or seed:
each day (Asia/Kolkata) gets a new quiz automatically and every visitor sees the same one.
"""
import datetime

from django.core.cache import cache
from django.utils import timezone

from base.templatetags.question_tags import question_html

QUIZ_SIZE = 10

# key, label, Font Awesome icon, topic prefixes (or exact keys) to draw from
CATEGORIES = [
    ('mixed', 'Mixed Bag', 'shuffle', None),
    ('gk', 'General Knowledge', 'earth-asia', ('ga.', 'environment.')),
    ('maths', 'Maths & Aptitude', 'calculator', ('quant.',)),
    ('reasoning', 'Reasoning', 'brain', ('reasoning.',)),
    ('english', 'English', 'spell-check', ('english.',)),
    ('science', 'Science', 'flask', ('physics.', 'chemistry.', 'biology.', 'ga.science')),
    ('computer', 'Computer', 'laptop-code', ('cs.',)),
]
CATEGORY_KEYS = [key for key, *_ in CATEGORIES]

# Long passages and data tables don't suit a quick quiz; numerical-only and kids' topics don't fit either.
SKIP = {'english.comprehension', 'english.kids', 'quant.di', 'quant.tita'}

# The Mixed Bag quiz: how many questions to take from each category.
MIX = [('gk', 3), ('maths', 2), ('reasoning', 2), ('english', 2), ('science', 1)]


def _topics():
    from testseries.content import load_all
    return load_all()


def _pool(category, topics):
    prefixes = dict((key, prefixes) for key, _, _, prefixes in CATEGORIES)[category]
    return sorted(k for k in topics if k not in SKIP and k.startswith(prefixes))


def _draw(pool, n, rng, used, topics):
    """n single-answer questions, each from a different topic where the pool allows."""
    from testseries.content.core import draw
    order = pool[:]
    rng.shuffle(order)
    out, seen, tries = [], set(), 0
    while len(out) < n and tries < n * 6:
        key = order[tries % len(order)]
        tries += 1
        for q in draw(key, 1, rng, used):
            text = q.text.strip().lower()
            if q.kind == 'mcq_single' and len(q.options) == 4 and len(q.text) <= 600 and text not in seen:
                seen.add(text)
                out.append((topics[key].label, q))
    return out[:n]


def build_quiz(day, category):
    """The quiz for a date and category as plain data (cached for the day)."""
    cache_key = f'daily-quiz:v1:{day.isoformat()}:{category}'
    quiz = cache.get(cache_key)
    if quiz is not None:
        return quiz
    from testseries.content.core import seeded
    topics = _topics()
    rng = seeded('daily-quiz', day.isoformat(), category)
    used = set()
    if category == 'mixed':
        picked = []
        for part, n in MIX:
            picked += _draw(_pool(part, topics), n, rng, used, topics)
        rng.shuffle(picked)
    else:
        picked = _draw(_pool(category, topics), QUIZ_SIZE, rng, used, topics)
    quiz = {
        'date': day.isoformat(),
        'category': category,
        'questions': [
            {
                'topic': label,
                'html': str(question_html(q.text)),
                'options': [str(o) for o in q.options],
                'answer': q.answer,
                'explanation': q.explanation or '',
            }
            for label, q in picked
        ],
    }
    cache.set(cache_key, quiz, 60 * 60 * 26)
    return quiz


def seconds_to_next_quiz(now=None):
    now = timezone.localtime(now)
    tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time.min, tzinfo=now.tzinfo)
    return max(1, int((tomorrow - now).total_seconds()))


CATEGORY_LABELS = {key: label for key, label, _, _ in CATEGORIES}
CATEGORY_ICONS = {key: icon for key, _, icon, _ in CATEGORIES}


# ---------------------------------------------------------------- saving attempts (logged-in students only)


def record_attempt(user, category, picks, day=None):
    """Score `picks` against the day's quiz on the server and save it. Returns the attempt.

    The first try is what counts in stats; retakes bump `attempts`, keep the best score and the latest picks.
    """
    from base.models import DailyQuizAttempt
    day = day or timezone.localdate()
    questions = build_quiz(day, category)['questions']
    if len(picks) != len(questions) or not all(isinstance(p, int) and 0 <= p < 4 for p in picks):
        raise ValueError('picks must give one option (0-3) per question')
    score = sum(1 for pick, q in zip(picks, questions) if pick == q['answer'])
    attempt, created = DailyQuizAttempt.objects.get_or_create(
        user=user, quiz_date=day, category=category,
        defaults={'score': score, 'best_score': score, 'total': len(questions), 'picks': picks},
    )
    if not created:
        attempt.attempts += 1
        attempt.best_score = max(attempt.best_score, score)
        attempt.picks = picks
        attempt.save(update_fields=['attempts', 'best_score', 'picks', 'updated_at'])
    attempt.latest_score = score
    return attempt


def _streaks(dates, today):
    """(current, best) runs of consecutive days in `dates`; the current one may end today or yesterday."""
    days = sorted(set(dates))
    best = run = 0
    previous = None
    for d in days:
        run = run + 1 if previous and (d - previous).days == 1 else 1
        best = max(best, run)
        previous = d
    have = set(days)
    current = 0
    d = today if today in have else today - datetime.timedelta(days=1)
    while d in have:
        current += 1
        d -= datetime.timedelta(days=1)
    return current, best


def today_state(user, day=None):
    """What the homepage widget needs for a logged-in student: today's plays and the current streak."""
    from base.models import DailyQuizAttempt
    day = day or timezone.localdate()
    dates = DailyQuizAttempt.objects.filter(user=user).values_list('quiz_date', flat=True).distinct()
    current, _ = _streaks(dates, day)
    today = {
        a.category: {'score': a.score, 'best': a.best_score, 'total': a.total, 'picks': a.picks}
        for a in DailyQuizAttempt.objects.filter(user=user, quiz_date=day)
    }
    return {'today': today, 'streak': current}


def user_stats(user, recent=30):
    """Daily Quiz totals, streaks, per-category accuracy, the last 14 days and recent plays for My Results / Profile."""
    from base.models import DailyQuizAttempt
    today = timezone.localdate()
    attempts = list(DailyQuizAttempt.objects.filter(user=user).order_by('-quiz_date', '-created_at'))
    answered = sum(a.total for a in attempts)
    correct = sum(a.score for a in attempts)
    current, best = _streaks([a.quiz_date for a in attempts], today)

    per_cat = {}
    for a in attempts:
        c = per_cat.setdefault(a.category, {'played': 0, 'correct': 0, 'answered': 0})
        c['played'] += 1
        c['correct'] += a.score
        c['answered'] += a.total
    categories = [
        {
            'key': key, 'label': label, 'icon': icon, 'played': per_cat[key]['played'],
            'accuracy': round(per_cat[key]['correct'] * 100 / per_cat[key]['answered']) if per_cat[key]['answered'] else 0,
        }
        for key, label, icon, _ in CATEGORIES if key in per_cat
    ]

    played_on = {}
    for a in attempts:
        played_on[a.quiz_date] = played_on.get(a.quiz_date, 0) + 1
    last_14 = [
        {'date': d, 'count': played_on.get(d, 0)}
        for d in (today - datetime.timedelta(days=i) for i in range(13, -1, -1))
    ]

    for a in attempts[:recent]:
        a.category_label = CATEGORY_LABELS.get(a.category, a.category)
        a.category_icon = CATEGORY_ICONS.get(a.category, 'bolt')
    return {
        'taken': len(attempts),
        'retakes': sum(a.attempts - 1 for a in attempts),
        'answered': answered,
        'correct': correct,
        'accuracy': round(correct * 100 / answered) if answered else 0,
        'perfect': sum(1 for a in attempts if a.score == a.total),
        'current_streak': current,
        'best_streak': best,
        'days_active': len(played_on),
        'played_today': played_on.get(today, 0),
        'categories': categories,
        'last_14': last_14,
        'recent': attempts[:recent],
    }


def homepage_context(user):
    """Everything the homepage section needs. Logged-out visitors get no questions (and no answers) at all."""
    today = timezone.localdate()
    context = {
        'date': today,
        'categories': [{'key': key, 'label': label, 'icon': icon} for key, label, icon, _ in CATEGORIES],
        'next_in': seconds_to_next_quiz(),
        'locked': not user.is_authenticated,
    }
    if user.is_authenticated:
        context['initial'] = build_quiz(today, 'mixed')
        context['me'] = today_state(user, today)
    return context
