"""Reasoning generators. Every answer is worked out by the code that writes the question."""
import datetime
import math
import string

from .core import generator, mcq, near, register

S = 'RSN1'
AZ = string.ascii_uppercase
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def _series(rng):
    kind = rng.randrange(8)
    if kind == 0:
        a, d = rng.randint(2, 40), rng.randint(3, 17)
        return [a + d * i for i in range(6)], f"Add {d} each time."
    if kind == 1:
        a, r = rng.randint(1, 6), rng.choice([2, 3])
        return [a * r ** i for i in range(6)], f"Multiply by {r} each time."
    if kind == 2:
        s, c = rng.randint(1, 8), rng.choice([0, 1, -1, 2])
        return [(s + i) ** 2 + c for i in range(6)], f"n² {'+' if c >= 0 else '−'} {abs(c)} for consecutive n." if c else "Consecutive squares."
    if kind == 3:
        a, d, dd = rng.randint(1, 20), rng.randint(1, 5), rng.randint(1, 4)
        out, step = [a], d
        for _ in range(5):
            out.append(out[-1] + step)
            step += dd
        return out, f"Differences increase by {dd}."
    if kind == 4:
        a = rng.randint(1, 5)
        out = [a]
        for i in range(5):
            out.append(out[-1] * (i + 2))
        return out, "Multiply by 2, 3, 4, 5, … in turn."
    if kind == 5:
        s = rng.randint(1, 6)
        return [(s + i) ** 3 for i in range(6)], "Consecutive cubes."
    if kind == 6:
        a, m, c = rng.randint(1, 5), 2, rng.choice([1, 2, 3, -1])
        out = [a]
        for _ in range(5):
            out.append(out[-1] * m + c)
        return out, f"×2 then {'+' if c > 0 else '−'}{abs(c)}."
    a, b = rng.randint(1, 10), rng.randint(20, 40)
    d1, d2 = rng.randint(2, 6), rng.randint(2, 6)
    out = []
    for i in range(6):
        out.append(a + d1 * (i // 2) if i % 2 == 0 else b - d2 * (i // 2))
    return out, f"Two alternating series: +{d1} and −{d2}."


@generator('reasoning.number_series', S, 'Number Series')
def number_series(rng):
    seq, rule = _series(rng)
    shown, ans = seq[:5], seq[5]
    return mcq(rng, f"Find the next number in the series: {', '.join(map(str, shown))}, ?", str(ans), near(rng, ans), 'medium', rule)


@generator('reasoning.missing_number', S, 'Missing Number')
def missing_number(rng):
    seq, rule = _series(rng)
    i = rng.randrange(1, 5)
    shown = [str(v) if j != i else '?' for j, v in enumerate(seq)]
    return mcq(rng, f"Find the missing number: {', '.join(shown)}", str(seq[i]), near(rng, seq[i]), 'medium', rule)


@generator('reasoning.wrong_number', S, 'Wrong Number Series')
def wrong_number(rng):
    seq, rule = _series(rng)
    i = rng.randrange(1, 6)
    wrong = seq[:]
    wrong[i] = seq[i] + rng.choice([-3, -2, -1, 1, 2, 3, 5])
    others = [str(v) for j, v in enumerate(wrong) if j != i]
    return mcq(rng, f"Find the wrong number in the series: {', '.join(map(str, wrong))}", str(wrong[i]), others, 'hard',
               f"{rule} The term should be {seq[i]}.")


@generator('reasoning.letter_series', S, 'Alphabet & Letter Series')
def letter_series(rng):
    kind = rng.randrange(3)
    if kind == 0:
        start, step = rng.randrange(0, 8), rng.randint(2, 4)
        seq = [AZ[(start + step * i) % 26] for i in range(6)]
        return mcq(rng, f"Find the next letter: {', '.join(seq[:5])}, ?", seq[5], [AZ[(AZ.index(seq[5]) + d) % 26] for d in (1, -1, 2, 3)],
                   'easy', f"Skip {step - 1} letter(s) each time.")
    if kind == 1:
        s, g = rng.randrange(0, 10), rng.randint(1, 3)
        terms = [''.join(AZ[(s + i * g + j) % 26] for j in range(3)) for i in range(5)]
        wrong = [''.join(AZ[(s + 4 * g + j + d) % 26] for j in range(3)) for d in (1, -1, 2)]
        return mcq(rng, f"Find the next term: {', '.join(terms[:4])}, ?", terms[4], wrong, 'medium', f"Each letter moves {g} place(s) forward.")
    n, k = rng.randint(5, 20), rng.randint(3, 9)
    direction = rng.choice(['right', 'left'])
    pos = n + k if direction == 'right' else n - k
    if not 1 <= pos <= 26:
        direction, pos = 'right', n + 3
        k = 3
    ans = AZ[pos - 1]
    return mcq(rng, f"In the English alphabet, which letter is {k}th to the {direction} of the {n}th letter from the left?", ans,
               [AZ[(pos - 1 + d) % 26] for d in (1, -1, 2, -2)], 'easy', f"{n} {'+' if direction == 'right' else '−'} {k} = {pos} → {ans}.")


WORDS = ['MOTHER', 'FATHER', 'SISTER', 'TEACHER', 'PENCIL', 'GARDEN', 'WINTER', 'MARKET', 'PLANET', 'BRIDGE', 'CANDLE',
         'FOREST', 'SILVER', 'MOBILE', 'DOCTOR', 'NATION', 'STREAM', 'BUTTER', 'ORANGE', 'POCKET', 'SCHOOL', 'FLOWER',
         'BOTTLE', 'MIRROR', 'CAMERA', 'PRAYER', 'KNIGHT', 'JUNGLE', 'TICKET', 'WALLET']


@generator('reasoning.coding', S, 'Coding-Decoding')
def coding(rng):
    w1, w2 = rng.sample(WORDS, 2)
    kind = rng.randrange(4)
    if kind == 0:
        k = rng.choice([1, 2, 3, -1, -2])
        enc = lambda w: ''.join(AZ[(AZ.index(c) + k) % 26] for c in w)
        rule = f"Each letter is shifted {abs(k)} place(s) {'forward' if k > 0 else 'backward'}."
    elif kind == 1:
        enc = lambda w: ''.join(AZ[25 - AZ.index(c)] for c in w)
        rule = "Each letter is replaced by its opposite (A↔Z, B↔Y, …)."
    elif kind == 2:
        enc = lambda w: w[::-1]
        rule = "The word is written in reverse."
    else:
        enc = lambda w: ''.join(AZ[(AZ.index(c) + (1 if i % 2 == 0 else -1)) % 26] for i, c in enumerate(w))
        rule = "Letters are shifted +1, −1, +1, −1, … alternately."
    ans = enc(w2)
    wrong = {''.join(AZ[(AZ.index(c) + d) % 26] for c in ans) for d in (1, -1)} | {ans[::-1], ans[1:] + ans[0]}
    return mcq(rng, f"If {w1} is coded as {enc(w1)}, how is {w2} coded in the same language?", ans, list(wrong), 'medium', rule)


@generator('reasoning.letter_value', S, 'Letter Values & Word Sums')
def letter_value(rng):
    w1, w2 = rng.sample([w for w in WORDS if len(w) <= 6], 2)
    val = lambda w: sum(AZ.index(c) + 1 for c in w)
    return mcq(rng, f"If A = 1, B = 2, …, Z = 26 and {w1} = {val(w1)}, then {w2} = ?", str(val(w2)), near(rng, val(w2)), 'medium',
               f"Add the positions of the letters of {w2}.")


@generator('reasoning.analogy', S, 'Analogy & Classification')
def analogy(rng):
    kind = rng.randrange(3)
    if kind == 0:
        rel, desc = rng.choice([(lambda n: n * n, 'n : n²'), (lambda n: n ** 3, 'n : n³'), (lambda n: n * n + 1, 'n : n² + 1'),
                                (lambda n: n * (n + 1), 'n : n(n + 1)'), (lambda n: 2 * n + 3, 'n : 2n + 3')])
        a, b = rng.sample(range(3, 15), 2)
        return mcq(rng, f"{a} : {rel(a)} :: {b} : ?", str(rel(b)), near(rng, rel(b)), 'easy', f"Rule {desc}.")
    if kind == 1:
        primes = [p for p in range(11, 98) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
        comps = [c for c in range(12, 99) if c not in primes and c % 2]
        group = rng.sample(primes, 3)
        odd = rng.choice(comps)
        return mcq(rng, f"Find the odd one out: {', '.join(map(str, rng.sample(group + [odd], 4)))}", str(odd), list(map(str, group)), 'medium',
                   f"All others are prime; {odd} = {next(d for d in range(3, odd) if odd % d == 0)} × {odd // next(d for d in range(3, odd) if odd % d == 0)}.")
    sq = [n * n for n in range(4, 16)]
    group = rng.sample(sq, 3)
    odd = rng.choice([v for v in range(20, 200) if v not in sq and int(v ** 0.5) ** 2 != v])
    return mcq(rng, f"Find the odd one out: {', '.join(map(str, rng.sample(group + [odd], 4)))}", str(odd), list(map(str, group)), 'easy',
               "All others are perfect squares.")


@generator('reasoning.direction', S, 'Direction Sense')
def direction(rng):
    a, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
    # walk a east/west and b north/south, with a detour that cancels out
    ew, ns = rng.choice(['east', 'west']), rng.choice(['north', 'south'])
    extra = rng.randint(2, 9)
    opp = {'east': 'west', 'west': 'east', 'north': 'south', 'south': 'north'}
    text = (f"Ravi walks {b + extra} km {ns}, turns and walks {a} km {ew}, then walks {extra} km {opp[ns]}. "
            f"How far is he from the starting point?")
    return mcq(rng, text, f"{c} km", [f"{v} km" for v in (a + b, a + b + extra, c + extra, b)], 'medium',
               f"Net displacement: {b} km {ns} and {a} km {ew}; √({a}² + {b}²) = {c} km.")


@generator('reasoning.ranking', S, 'Ranking & Order')
def ranking(rng):
    left, right = rng.randint(5, 25), rng.randint(5, 25)
    total = left + right - 1
    kind = rng.randrange(2)
    if kind == 0:
        return mcq(rng, f"In a row of students, Aman is {left}th from the left and {right}th from the right. How many students are in the row?",
                   str(total), [str(total + 1), str(total - 1), str(total + 2), str(left + right)], 'easy', f"{left} + {right} − 1 = {total}.")
    return mcq(rng, f"In a class of {total} students, Neha ranks {left}th from the top. What is her rank from the bottom?",
               str(right), [str(right + 1), str(right - 1), str(total - left), str(left)], 'easy', f"{total} − {left} + 1 = {right}.")


@generator('reasoning.calendar', S, 'Calendar')
def calendar(rng):
    year = rng.randint(2000, 2030)
    d1 = datetime.date(year, rng.randint(1, 6), rng.randint(1, 28))
    d2 = d1 + datetime.timedelta(days=rng.randint(20, 250))
    ans = DAYS[d2.weekday()]
    return mcq(rng, f"If {d1:%d %B %Y} was a {DAYS[d1.weekday()]}, what day of the week was {d2:%d %B %Y}?", ans,
               [d for d in DAYS if d != ans], 'medium',
               f"{(d2 - d1).days} days later; {(d2 - d1).days} mod 7 = {(d2 - d1).days % 7} odd day(s).")


@generator('reasoning.clock', S, 'Clock')
def clock(rng):
    kind = rng.randrange(2)
    h, m = rng.randint(1, 12), rng.choice([0, 10, 15, 20, 30, 40, 45, 50])
    if kind == 0:
        ang = abs(30 * h - 5.5 * m)
        ang = min(ang, 360 - ang)
        a = f"{ang:g}°"
        return mcq(rng, f"What is the angle between the hour and minute hands of a clock at {h}:{m:02d}?", a,
                   [f"{v:g}°" for v in (ang + 5, abs(ang - 7.5), ang + 15, 360 - ang if ang != 180 else 90)], 'medium',
                   f"|30×{h} − 5.5×{m}| = {abs(30 * h - 5.5 * m):g}°; take the smaller angle.")
    total = (11 * 60 + 60) - (h % 12 * 60 + m)
    mh, mm = divmod(total, 60)
    mh = mh or 12
    ans = f"{mh}:{mm:02d}"
    return mcq(rng, f"A clock shows {h}:{m:02d}. What time does its mirror image show?", ans,
               [f"{(mh % 12) + 1}:{mm:02d}", f"{mh}:{(mm + 15) % 60:02d}", f"{h}:{(60 - m) % 60:02d}", f"{12 - h or 12}:{m:02d}"], 'medium',
               f"Mirror time = 11:60 − {h}:{m:02d}.")


@generator('reasoning.inequality', S, 'Coded Inequalities')
def inequality(rng):
    names = rng.sample('ABCDEFGHJKLMPQRSTUVW', 5)
    ops = [rng.choice(['>', '≥', '=']) for _ in range(4)]
    statement = names[0] + ''.join(f" {o} {n}" for o, n in zip(ops, names[1:]))

    def relation(i, j):
        """Definite relation between names[i] and names[j] for i < j along the chain."""
        seg = ops[i:j]
        if all(o == '=' for o in seg):
            return '='
        if '>' in seg:
            return '>'
        return '≥'

    def holds(i, j, op):
        if i > j:
            flip = {'>': '<', '<': '>', '≥': '≤', '≤': '≥', '=': '='}
            return holds(j, i, flip[op])
        r = relation(i, j)
        return {'>': r == '>', '≥': r in ('>', '≥', '='), '=': r == '=', '<': False, '≤': r == '='}[op]

    # Two different pairs, so the 'either-or' (complementary pair) case never arises.
    pairs = rng.sample([(i, j) for i in range(5) for j in range(5) if i < j], 2)
    conclusions = []
    for i, j in pairs:
        if rng.random() < 0.5:
            i, j = j, i
        op = rng.choice(['>', '≥', '<', '='])
        conclusions.append((f"{names[i]} {op} {names[j]}", holds(i, j, op)))
    (c1, t1), (c2, t2) = conclusions
    if t1 and t2:
        ans = 'Both I and II follow'
    elif t1:
        ans = 'Only I follows'
    elif t2:
        ans = 'Only II follows'
    else:
        ans = 'Neither I nor II follows'
    opts = ['Only I follows', 'Only II follows', 'Both I and II follow', 'Neither I nor II follows', 'Either I or II follows']
    return mcq(rng, f"Statement: {statement}\nConclusions:\nI. {c1}\nII. {c2}", ans, [o for o in opts if o != ans], 'hard',
               "Read each pair along the chain: any '>' makes it strictly greater; only '=' all the way makes it equal.")


@generator('reasoning.dictionary_order', S, 'Word Arrangement')
def dictionary_order(rng):
    group = rng.sample(WORDS, 5)
    order = sorted(group)
    k = rng.randrange(5)
    pos = ['first', 'second', 'third', 'fourth', 'last'][k]
    return mcq(rng, f"If these words are arranged in dictionary order, which comes {pos}?\n{', '.join(w.title() for w in group)}",
               order[k].title(), [w.title() for w in group if w != order[k]], 'easy', f"Order: {', '.join(w.title() for w in order)}.")


@generator('reasoning.cubes', S, 'Cubes & Dice')
def cubes(rng):
    n = rng.randint(3, 7)
    kind = rng.randrange(4)
    what, val = [("exactly three faces", 8), ("exactly two faces", 12 * (n - 2)),
                 ("exactly one face", 6 * (n - 2) ** 2), ("no face", (n - 2) ** 3)][kind]
    return mcq(rng, f"A cube painted red on all faces is cut into {n ** 3} equal smaller cubes. How many small cubes have {what} painted?",
               str(val), near(rng, val) + [str(6 * n)], 'medium',
               "Corners: 8; edges: 12(n−2); faces: 6(n−2)²; inside: (n−2)³" + f" with n = {n}.")


@generator('reasoning.math_operations', S, 'Mathematical Operations')
def math_operations(rng):
    sym = {'+': '×', '−': '÷', '×': '−', '÷': '+'}
    a, b, c, d = rng.randint(2, 9) * 6, rng.choice([2, 3, 6]), rng.randint(2, 9), rng.randint(2, 20)
    expr = f"{a} − {b} + {c} × {d}"   # means a ÷ b × c − d
    val = a // b * c - d
    return mcq(rng, f"If '+' means '×', '−' means '÷', '×' means '−' and '÷' means '+', then {expr} = ?", str(val),
               near(rng, val) + [str(a - b + c * d)], 'medium', f"Becomes {a} ÷ {b} × {c} − {d} = {val}.")


@generator('reasoning.counting', S, 'Symbol & Digit Counting')
def counting(rng):
    digits = ''.join(rng.choice('3579') for _ in range(24))
    a, b = rng.sample('3579', 2)
    count = sum(1 for i in range(1, len(digits)) if digits[i] == a and digits[i - 1] == b)
    return mcq(rng, f"How many {a}s are immediately preceded by {b} in:\n{' '.join(digits)}", str(count),
               [str(v) for v in {count + 1, count + 2, max(0, count - 1), count + 3} if v != count], 'easy', f"Count the pairs '{b} {a}'.")


@generator('reasoning.blood_relation', S, 'Blood Relations')
def blood_relation(rng):
    cases = [
        ("Pointing to a man, Sita says, 'He is the son of my grandfather's only son.' How is the man related to Sita?", 'Brother',
         ['Cousin', 'Uncle', 'Father', 'Nephew'], "Her grandfather's only son is her father; his son is her brother."),
        ("A is the brother of B. B is the daughter of C. D is the father of C. How is A related to D?", 'Grandson',
         ['Son', 'Granddaughter', 'Nephew', 'Brother'], "C is D's child; A is C's son, so D's grandson."),
        ("P is the mother of Q. Q is the sister of R. R is the father of S. How is P related to S?", 'Grandmother',
         ['Mother', 'Aunt', 'Sister', 'Cousin'], "P is R's mother; R is S's father."),
        ("Introducing a woman, Raj says, 'Her mother is the only daughter of my mother.' How is the woman related to Raj?", 'Niece',
         ['Sister', 'Daughter', 'Cousin', 'Mother'], "The only daughter of his mother is his sister; her daughter is his niece."),
        ("X is the husband of Y. Y is the sister of Z. Z is the son of W. How is X related to W?", 'Son-in-law',
         ['Son', 'Brother', 'Father', 'Nephew'], "Y is W's daughter; Y's husband X is W's son-in-law."),
        ("M is the father of N. N is the brother of O. O is the mother of P. How is N related to P?", 'Maternal uncle',
         ['Father', 'Brother', 'Grandfather', 'Cousin'], "N is the brother of P's mother."),
        ("A's father is B's only son. B has no daughter. How is B related to A?", 'Grandfather',
         ['Father', 'Uncle', 'Brother', 'Grandson'], "B's son is A's father."),
        ("Pointing to a photograph, Mohan says, 'She is the daughter of my father's only son.' How is she related to Mohan?", 'Daughter',
         ['Sister', 'Niece', 'Mother', 'Cousin'], "His father's only son is Mohan himself."),
        ("K is the sister of L. L is the husband of M. How is K related to M?", 'Sister-in-law',
         ['Sister', 'Mother', 'Aunt', 'Cousin'], "K is the sister of M's husband."),
        ("D is the son of E. F is the brother of E. G is the daughter of F. How is G related to D?", 'Cousin',
         ['Sister', 'Niece', 'Aunt', 'Daughter'], "D and G are children of brothers E and F."),
    ]
    text, ans, wrong, expl = rng.choice(cases)
    return mcq(rng, text, ans, wrong, 'medium', expl)


def _reasoning_numeric(rng):
    from .core import numerical
    seq, rule = _series(rng)
    return numerical(f"Find the next number in the series: {', '.join(map(str, seq[:5]))}, ?\n(Type the answer – numbers only.)", seq[5], 'medium', rule)


register('reasoning.number_series', S, 'Number Series', numeric=_reasoning_numeric)
