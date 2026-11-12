"""Create the NIOS Secondary and Senior Secondary test series from cbse_data.nios.

Only plain model fields are used (no custom save()/update_stats()), so the same code runs from the
`seed_nios` management command and from a data migration with historical models. It never deletes anything:
existing series and tests are kept (purchases and attempts stay intact) and only missing tests are added.
"""
import math
import random
from decimal import Decimal
from itertools import zip_longest

from django.utils.text import slugify

from testseries.boards import STATE_BOARDS
from testseries.management.cbse_data import nios

DEMO_TITLE = 'Free Demo Test'
DEMO_QUESTIONS = 10


def _shuffled(text, opts, answer):
    """Shuffle options the same way on every run so the right answer isn't always 'a'."""
    correct = opts['abcd'.index(answer)]
    order = list(opts)
    random.Random(text).shuffle(order)
    return dict(zip('abcd', order)), 'abcd'[order.index(correct)]


def _refresh_test(test, Question):
    questions = list(Question.objects.filter(test=test).values_list('marks', 'difficulty'))
    test.total_questions = len(questions)
    test.total_marks = round(sum(m for m, _ in questions))
    for level in ('easy', 'medium', 'hard'):
        setattr(test, f'{level}_questions', sum(1 for _, d in questions if d == level))
    test.save(update_fields=['total_questions', 'total_marks', 'easy_questions', 'medium_questions', 'hard_questions'])


def _refresh_series(series, Test):
    tests = Test.objects.filter(test_series=series, is_active=True)
    series.total_tests = tests.count()
    series.total_questions = sum(t.total_questions for t in tests)
    series.total_marks = sum(t.total_marks for t in tests)
    series.save(update_fields=['total_tests', 'total_questions', 'total_marks'])


def seed(TestSeries, Test, Question, Subject, Category, log=print):
    """Create or top up the NIOS series. Returns the number of tests added."""
    subjects = {
        code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
        for code, (name, color, icon) in nios.SUBJECTS.items()
    }
    board = next(b for b in STATE_BOARDS if b.code == 'nios')
    Category.objects.get_or_create(name=board.category, defaults={
        'slug': slugify(board.category), 'icon': 'school', 'icon_color': '#4f46e5', 'description': board.note,
    })

    added = 0
    for grade, slug, title, description, banks, mocks, price in nios.SERIES:
        series = TestSeries.objects.filter(slug=slug).first()
        if series is None:
            series = TestSeries.objects.create(
                title=title, slug=slug, board='nios', grade=grade, stream='', description=description,
                difficulty='medium' if grade == 10 else 'hard',
                estimated_duration='15 minutes per subject test, 30 minutes per mock',
                is_free=False, price=Decimal(price),
                has_negative_marking=False, negative_marks=0, pass_percentage=33,
            )
            log(f"  + series {title}")

        existing = set(Test.objects.filter(test_series=series).values_list('title', flat=True))
        by_code = {bank[0]: bank for bank in banks}

        plan = []  # (title, description, minutes, paper_type, [(subject code, question)])
        for test_title, test_desc, codes, per_subject in mocks:
            rng = random.Random(f'{slug}-{test_title}')
            items = [(code, q) for code in codes for q in rng.sample(by_code[code][3], per_subject)]
            plan.append((test_title, test_desc, 30, 'mock', items))
        for code, test_title, test_desc, questions in banks:
            plan.append((test_title, test_desc, 15, 'subject', [(code, q) for q in questions]))
        scheme_code, scheme_title, scheme_desc, scheme_questions = nios.SCHEME
        plan.append((scheme_title, scheme_desc, 10, 'topic', [(scheme_code, q) for q in scheme_questions]))

        for test_title, test_desc, minutes, paper_type, items in plan:
            if test_title in existing:
                continue
            test = Test.objects.create(
                test_series=series, title=test_title, slug=slugify(test_title)[:50] or f'test-{len(existing) + 1}',
                description=test_desc, duration_minutes=minutes, max_attempts=3,
                shuffle_questions=False, paper_type=paper_type,
            )
            Question.objects.bulk_create([
                Question(
                    test=test, subject=subjects[code], question_type='mcq_single', difficulty=difficulty,
                    question_text=text, marks=1, negative_marks=0, options=options,
                    correct_answer={'answer': answer}, explanation=explanation, order=order,
                )
                for order, (code, (text, opts, ans, difficulty, explanation)) in enumerate(items, start=1)
                for options, answer in [_shuffled(text, opts, ans)]
            ])
            _refresh_test(test, Question)
            existing.add(test_title)
            added += 1

        _add_demo(series, Test, Question)
        _refresh_series(series, Test)
        log(f"  {series.title}: {series.total_tests} tests, {series.total_questions} questions")
    return added


def _add_demo(series, Test, Question):
    """A free 10-question demo sampled across subjects (same idea as make_series_paid)."""
    if Test.objects.filter(test_series=series, is_demo=True).exists():
        return
    questions = list(
        Question.objects.filter(test__test_series=series, test__paper_type='subject')
        .order_by('test__created_at', 'test_id', 'order')
    )
    by_subject = {}
    for q in questions:
        by_subject.setdefault(q.subject_id, []).append(q)
    picked = [q for row in zip_longest(*by_subject.values()) for q in row if q is not None][:DEMO_QUESTIONS]
    if not picked:
        return
    demo = Test.objects.create(
        test_series=series, title=DEMO_TITLE, slug='free-demo-test',
        description=f"Try {len(picked)} sample questions from this series in the real exam interface, free and without buying the series.",
        duration_minutes=max(5, math.ceil(15 * len(picked) / 10)), max_attempts=3,
        shuffle_questions=False, show_result_immediately=True, allow_review=True, is_demo=True,
    )
    Question.objects.bulk_create([
        Question(
            test=demo, order=n, subject_id=q.subject_id, question_type=q.question_type, difficulty=q.difficulty,
            question_text=q.question_text, marks=q.marks, negative_marks=q.negative_marks, options=q.options,
            correct_answer=q.correct_answer, explanation=q.explanation,
        )
        for n, q in enumerate(picked, start=1)
    ])
    _refresh_test(demo, Question)
