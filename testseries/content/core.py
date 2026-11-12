"""Question building blocks shared by every generator and bank.

A topic is either a generator (a function rng -> Q that computes its own answer, so every variant is correct by
construction) or a bank (fixed rows written by hand). Both are registered in TOPICS under a dotted key such as
'quant.percentage' and drawn from with `draw`.
"""
import random
from dataclasses import dataclass
from fractions import Fraction

LETTERS = 'abcd'


@dataclass
class Q:
    text: str
    options: list            # option texts; empty for numerical questions
    answer: int = 0          # index of the correct option
    difficulty: str = 'medium'
    explanation: str = ''
    kind: str = 'mcq_single'  # or 'numerical'
    value: str = ''           # correct value of a numerical question


@dataclass
class Topic:
    key: str
    subject: str              # Subject.code
    label: str
    gen: object = None        # callable(rng) -> Q
    rows: list = None         # bank rows
    numeric: object = None    # optional callable(rng) -> Q of kind 'numerical'

    @property
    def size(self):
        return len(self.rows) if self.rows is not None else None


TOPICS = {}


def register(key, subject, label, *, gen=None, rows=None, numeric=None):
    if key in TOPICS:
        topic = TOPICS[key]
        if rows:
            topic.rows = (topic.rows or []) + list(rows)
        if gen:
            topic.gen = gen
        if numeric:
            topic.numeric = numeric
        return topic
    TOPICS[key] = Topic(key, subject, label, gen=gen, rows=list(rows) if rows is not None else None, numeric=numeric)
    return TOPICS[key]


def generator(key, subject, label):
    """Decorator: register a generator topic."""
    def wrap(fn):
        register(key, subject, label, gen=fn)
        return fn
    return wrap


# ---------------------------------------------------------------- formatting


def fmt(x):
    """Plain number: 12, 12.5, 0.33 (at most two decimals, no trailing zeros)."""
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    if isinstance(x, int):
        return str(x)
    return f"{x:.2f}".rstrip('0').rstrip('.')


def inr(x):
    """Rupees with Indian digit grouping: ₹1,23,456."""
    x = Fraction(x) if not isinstance(x, (int, Fraction)) else x
    whole = int(x)
    frac = x - whole
    s = str(abs(whole))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ','.join(groups + [tail])
    out = f"₹{'-' if whole < 0 else ''}{s}"
    if frac:
        out += f"{float(frac):.2f}"[1:]
    return out


def frac_str(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


# ---------------------------------------------------------------- building questions


def mcq(rng, text, correct, wrong, difficulty='medium', explanation=''):
    """Four-option MCQ with the correct option at a random position. `wrong` may contain extras or duplicates."""
    correct = str(correct)

    def pick(norm):
        seen, out = {norm(correct)}, []
        for w in wrong:
            w = str(w)
            if norm(w) not in seen:
                seen.add(norm(w))
                out.append(w)
            if len(out) == 3:
                break
        return out

    # Case-insensitive first (so 'Paris' and 'paris' never both appear); questions that are *about* case,
    # punctuation or formulas such as λD/d vs λd/D fall back to an exact comparison.
    distractors = pick(lambda s: s.strip().lower())
    if len(distractors) < 3:
        distractors = pick(lambda s: s.strip())
    if len(distractors) < 3:
        raise ValueError(f"not enough distinct options for: {text[:60]}")
    options = distractors[:]
    pos = rng.randrange(4)
    options.insert(pos, correct)
    if sorted(options) == ['A', 'B', 'C', 'D']:  # error-spotting parts keep their order
        options.sort()
        pos = options.index(correct)
    return Q(text, options, pos, difficulty, explanation)


def numerical(text, value, difficulty='medium', explanation=''):
    return Q(text, [], 0, difficulty, explanation, kind='numerical', value=fmt(value))


def near(rng, value, count=6, as_text=fmt, spread=None, positive=True):
    """Plausible wrong numbers near `value` (common slips: ±small, ×10, swapped steps)."""
    value = Fraction(value) if not isinstance(value, Fraction) else value
    step = spread or max(1, abs(int(value)) // 10 or 1)
    cands = set()
    tries = 0
    while len(cands) < count and tries < 200:
        tries += 1
        kind = rng.random()
        if kind < 0.6:
            delta = rng.choice([-1, 1]) * rng.randint(1, 4) * step
            c = value + delta
        elif kind < 0.8:
            c = value * rng.choice([Fraction(1, 2), Fraction(3, 2), 2, Fraction(5, 4), Fraction(4, 5)])
        else:
            c = value + rng.choice([-1, 1]) * Fraction(rng.randint(1, 9), 10) * step
        if value.denominator == 1 and isinstance(step, int):
            c = Fraction(round(c))
        if c != value and (not positive or c > 0):
            cands.add(c)
    return [as_text(c) for c in cands]


def from_row(rng, row):
    """Bank row -> Q. Rows are (text, [correct, wrong1, wrong2, wrong3], difficulty, explanation) or the legacy
    (text, [a, b, c, d], answer_letter, difficulty, explanation) used by the older seed files."""
    if len(row) == 5:
        text, opts, letter, difficulty, explanation = row
        correct = opts[LETTERS.index(letter)]
        wrong = [o for i, o in enumerate(opts) if i != LETTERS.index(letter)]
    else:
        text, opts, difficulty, explanation = row
        correct, wrong = opts[0], opts[1:]
    return mcq(rng, text, correct, wrong, difficulty, explanation)


def table_topics(key, subject, label, rows, templates, difficulty='medium'):
    """Register a generator over a fact table.

    rows: [(a, b), ...]; templates: [(question_format_using_{a}_or_{b}, 'a' | 'b' answer column, explanation_fmt)].
    Distractors come from the same column of other rows, so every option is plausible.
    """
    rows = [tuple(r) for r in rows]

    def gen(rng):
        a, b, *rest = rng.choice(rows)
        q_fmt, col, expl = rng.choice(templates)
        idx = 0 if col == 'a' else 1
        correct = (a, b)[idx]
        pool = [r[idx] for r in rows if r[idx] != correct and r[1 - idx] != (a, b)[1 - idx]]
        rng.shuffle(pool)
        d = rest[0] if rest else difficulty
        return mcq(rng, q_fmt.format(a=a, b=b), correct, pool, d, expl.format(a=a, b=b))

    register(key, subject, label, gen=gen)
    TOPICS[key].table_size = len(rows) * len(templates)
    return gen


# ---------------------------------------------------------------- drawing


def topic_capacity(topic):
    if topic.rows is not None and not topic.gen:
        return len(topic.rows)
    return getattr(topic, 'table_size', None) or 10 ** 6


def draw(key, n, rng, used, numeric_share=0.0):
    """n questions from a topic, preferring texts not in `used` (shared across a whole series).

    numeric_share: fraction of questions to take from the topic's numerical-answer generator, if it has one.
    """
    topic = TOPICS[key]
    out = []
    local = set()

    def take(q):
        k = q.text.strip().lower()
        if k in local:
            return False
        local.add(k)
        out.append(q)
        used.add(k)
        return True

    want_numeric = round(n * numeric_share)
    tries = 0
    while want_numeric and tries < want_numeric * 60:
        tries += 1
        if topic.numeric and rng.random() < 0.5:
            q = _safe(topic.numeric, rng)
        elif topic.gen:
            q = as_numeric(_safe(topic.gen, rng))
        elif topic.rows:
            q = as_numeric(_safe(from_row, rng, rng.choice(topic.rows)))
        else:
            q = None
        if q is None:
            continue
        if q.text.strip().lower() not in used and take(q):
            want_numeric -= 1

    sources = []
    if topic.rows:
        rows = topic.rows[:]
        rng.shuffle(rows)
        sources.append(('rows', rows))
    if topic.gen:
        sources.append(('gen', None))

    # Fresh questions first: bank rows not used yet, then generated ones.
    for kind, rows in sources:
        if len(out) >= n:
            break
        if kind == 'rows':
            for row in rows:
                if len(out) >= n:
                    break
                q = _safe(from_row, rng, row)
                if q is not None and q.text.strip().lower() not in used:
                    take(q)
        else:
            tries = 0
            while len(out) < n and tries < n * 60:
                tries += 1
                q = _safe(topic.gen, rng)
                if q is not None and q.text.strip().lower() not in used:
                    take(q)

    # Pool exhausted for this series: reuse earlier questions (re-shuffled options) rather than leave gaps.
    tries = 0
    while len(out) < n and tries < n * 30:
        tries += 1
        if topic.rows:
            q = _safe(from_row, rng, rng.choice(topic.rows))
            if q is not None:
                take(q)
        elif topic.gen:
            q = _safe(topic.gen, rng)
            if q is not None:
                take(q)
    return out


def _safe(gen, rng, *args):
    """A generator occasionally lands on values that leave fewer than four distinct options; just try again."""
    try:
        return gen(rng, *args)
    except (ValueError, ZeroDivisionError, IndexError):
        return None


UNIT_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°%/²³·Ω ")


def as_numeric(q):
    """Turn an MCQ whose answer is a plain number (optionally with a unit) into a numerical-answer question, or None."""
    if q is None or q.kind == 'numerical':
        return q
    answer = q.options[q.answer].strip()
    rupee = answer.startswith('₹')
    head = answer.lstrip('₹').strip()
    number, _, unit = head.partition(' ')
    number = number.replace(',', '').replace('−', '-')
    if number.endswith('%'):
        number, unit = number[:-1], '%'
    try:
        value = float(number)
    except ValueError:
        return None
    if unit and not set(unit) <= UNIT_CHARS:
        return None  # e.g. "Quotient 3, remainder 1" or "3 : 1"
    if rupee:
        unit = '₹'
    text = q.text.rstrip()
    if '___' not in text and '?' not in text:
        text += ' = ?'
    hint = f"\n(Type the answer{' in ' + unit if unit else ''} – numbers only.)"
    return Q(text + hint, [], 0, q.difficulty, q.explanation, kind='numerical', value=fmt(value))


def seeded(*parts):
    return random.Random('|'.join(str(p) for p in parts))
