"""School mathematics, chapter by chapter for Classes 1–12 (NCERT order; state boards follow the same topics).
Every answer is computed from the generated numbers."""
import math
from fractions import Fraction as F

from .core import fmt, frac_str, mcq, near, numerical, register

S = 'MAT1'
NUM_WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
             'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

CHAPTERS = {}   # grade -> [(topic key, chapter title)]


def chapter(grade, key, title):
    def wrap(fn):
        register(key, S, title, gen=fn)
        CHAPTERS.setdefault(grade, []).append((key, title))
        return fn
    return wrap


def scale(grade):
    return {1: 20, 2: 100, 3: 1000, 4: 10000, 5: 100000}.get(grade, 1000)


# ------------------------------------------------------------------ Classes 1–5
for g in range(1, 6):
    top = scale(g)

    def add(rng, top=top, g=g):
        a, b = rng.randint(1, top // 2), rng.randint(1, top // 2)
        return mcq(rng, f"{a:,} + {b:,} = ?", f"{a + b:,}", [f"{x:,}" for x in (a + b + 1, a + b - 1, a + b + 10, abs(a - b))], 'easy', f"{a:,} + {b:,} = {a + b:,}.")

    def sub(rng, top=top, g=g):
        a = rng.randint(top // 4, top)
        b = rng.randint(1, a)
        return mcq(rng, f"{a:,} − {b:,} = ?", f"{a - b:,}", [f"{x:,}" for x in (a - b + 1, a - b - 1 if a - b else 2, a + b, a - b + 10)], 'easy', f"{a:,} − {b:,} = {a - b:,}.")

    def story(rng, top=top, g=g):
        item = rng.choice(['mangoes', 'pencils', 'marbles', 'stickers', 'books', 'balloons'])
        a, b = rng.randint(2, max(5, top // 4)), rng.randint(1, max(3, top // 5))
        if rng.random() < 0.5:
            return mcq(rng, f"Riya has {a} {item}. Her friend gives her {b} more. How many {item} does she have now?", str(a + b),
                       [str(x) for x in (a + b + 1, a + b - 1, abs(a - b), a + b + 2)], 'easy', f"{a} + {b} = {a + b}.")
        a, b = max(a, b), min(a, b)
        return mcq(rng, f"Aman had {a} {item}. He gave away {b}. How many are left?", str(a - b),
                   [str(x) for x in (a - b + 1, a + b, a - b + 2, max(0, a - b - 1) if a - b > 1 else a)], 'easy', f"{a} − {b} = {a - b}.")

    def compare(rng, top=top, g=g):
        a, b = rng.sample(range(1, top), 2)
        kind = rng.randrange(3)
        if kind == 0:
            return mcq(rng, f"Which number is greater: {a:,} or {b:,}?", f"{max(a, b):,}", [f"{min(a, b):,}", "Both are equal", "Cannot say"], 'easy', "Compare digit by digit from the left.")
        if kind == 1:
            return mcq(rng, f"What comes just after {a:,}?", f"{a + 1:,}", [f"{a - 1:,}", f"{a + 10:,}", f"{a:,}"], 'easy', "Add one.")
        return mcq(rng, f"What comes just before {a:,}?", f"{a - 1:,}", [f"{a + 1:,}", f"{a - 10:,}" if a > 10 else f"{a + 2:,}", f"{a:,}"], 'easy', "Subtract one.")

    register(f'math.c{g}.addition', S, 'Addition', gen=add)
    register(f'math.c{g}.subtraction', S, 'Subtraction', gen=sub)
    register(f'math.c{g}.word_problems', S, 'Word Problems', gen=story)
    register(f'math.c{g}.numbers', S, 'Numbers & Comparison', gen=compare)
    CHAPTERS.setdefault(g, []).extend([(f'math.c{g}.numbers', 'Numbers & Comparison'), (f'math.c{g}.addition', 'Addition'),
                                       (f'math.c{g}.subtraction', 'Subtraction'), (f'math.c{g}.word_problems', 'Word Problems')])


@chapter(1, 'math.c1.shapes_patterns', 'Shapes & Patterns')
def shapes_patterns_1(rng):
    kind = rng.randrange(3)
    if kind == 0:
        shape, sides = rng.choice([('triangle', 3), ('square', 4), ('rectangle', 4), ('pentagon', 5), ('hexagon', 6)])
        return mcq(rng, f"How many sides does a {shape} have?", str(sides), [str(x) for x in range(2, 8) if x != sides], 'easy', f"A {shape} has {sides} sides.")
    if kind == 1:
        start, step = rng.randint(1, 10), rng.choice([1, 2, 5, 10])
        seq = [start + step * i for i in range(5)]
        return mcq(rng, f"Complete the pattern: {', '.join(map(str, seq[:4]))}, ___", str(seq[4]), [str(seq[4] + step), str(seq[4] - 1), str(seq[3])], 'easy', f"Add {step} each time.")
    n = rng.randint(1, 20)
    return mcq(rng, f"How is the number {n} written in words?", NUM_WORDS[n], [NUM_WORDS[x] for x in {n + 1, max(0, n - 1), (n + 10) % 21, (n + 3) % 21} if x != n], 'easy', f"{n} = {NUM_WORDS[n]}.")


@chapter(2, 'math.c2.tables', 'Multiplication Tables')
def tables_2(rng):
    a, b = rng.randint(2, 10), rng.randint(1, 10)
    return mcq(rng, f"{a} × {b} = ?", str(a * b), [str(x) for x in (a * b + a, a * b - a if a * b > a else a * b + 2, a + b, a * b + 1)], 'easy', f"{a} times {b} is {a * b}.")


@chapter(2, 'math.c2.money_time', 'Money & Time')
def money_time_2(rng):
    kind = rng.randrange(3)
    if kind == 0:
        a, b = rng.choice([5, 10, 20, 50]), rng.choice([2, 5, 10, 20])
        return mcq(rng, f"Meena has a ₹{a} note and a ₹{b} note. How much money does she have?", f"₹{a + b}", [f"₹{x}" for x in (a + b + 5, abs(a - b), a * b)], 'easy', f"₹{a} + ₹{b} = ₹{a + b}.")
    if kind == 1:
        h = rng.randint(1, 12)
        return mcq(rng, f"The short hand of a clock is on {h} and the long hand is on 12. What time is it?", f"{h} o'clock",
                   [f"{x} o'clock" for x in {h % 12 + 1, (h + 10) % 12 + 1, 12} if x != h] + ["Half past 12"], 'easy', "Long hand on 12 means 'o'clock'.")
    d = rng.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    nxt = days[(days.index(d) + 1) % 7]
    return mcq(rng, f"Which day comes after {d}?", nxt, [x for x in days if x not in (nxt, d)], 'easy', f"{d} → {nxt}.")


for g in (3, 4, 5):
    def mult(rng, g=g):
        a, b = (rng.randint(11, 99), rng.randint(2, 9)) if g == 3 else (rng.randint(100, 999), rng.randint(11, 99))
        return mcq(rng, f"{a:,} × {b} = ?", f"{a * b:,}", [f"{x:,}" for x in (a * b + a, a * b - b, a * (b + 1), a * b + 10)], 'medium', f"{a:,} × {b} = {a * b:,}.")

    def div(rng, g=g):
        b = rng.randint(2, 9) if g == 3 else rng.randint(3, 25)
        q = rng.randint(5, 99 if g == 3 else 999)
        r = rng.randint(0, b - 1) if g >= 4 else 0
        a = b * q + r
        text = f"{a:,} ÷ {b} = ?" if not r else f"What are the quotient and remainder when {a:,} is divided by {b}?"
        ans = f"{q:,}" if not r else f"Quotient {q}, remainder {r}"
        wrong = [f"{x:,}" for x in (q + 1, q - 1, q + 10)] if not r else [f"Quotient {q + 1}, remainder {r}", f"Quotient {q}, remainder {r + 1}", f"Quotient {q - 1}, remainder {r + b}"]
        return mcq(rng, text, ans, wrong, 'medium', f"{b} × {q} + {r} = {a}.")

    def measure(rng, g=g):
        kind = rng.randrange(4)
        if kind == 0:
            m = rng.randint(2, 50)
            return mcq(rng, f"{m} m = ___ cm", f"{m * 100:,}", [f"{x:,}" for x in (m * 10, m * 1000, m + 100)], 'easy', "1 m = 100 cm.")
        if kind == 1:
            kg, g_ = rng.randint(1, 20), rng.choice([0, 250, 500, 750])
            return mcq(rng, f"{kg} kg {g_} g = ___ g", f"{kg * 1000 + g_:,}", [f"{x:,}" for x in (kg * 100 + g_, kg + g_, kg * 1000 + g_ + 100)], 'easy', "1 kg = 1000 g.")
        if kind == 2:
            h = rng.randint(2, 12)
            return mcq(rng, f"{h} hours = ___ minutes", str(h * 60), [str(x) for x in (h * 100, h * 30, h * 60 + 60)], 'easy', "1 hour = 60 minutes.")
        l = rng.randint(2, 30)
        return mcq(rng, f"{l} litres = ___ mL", f"{l * 1000:,}", [f"{x:,}" for x in (l * 100, l * 10, l * 10000)], 'easy', "1 L = 1000 mL.")

    def place(rng, g=g):
        n = rng.randint(1000 if g >= 4 else 100, scale(g) - 1)
        digits = str(n)
        i = rng.randrange(len(digits))
        while digits[i] == '0':
            i = rng.randrange(len(digits))
        names = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'lakhs']
        place_value = int(digits[i]) * 10 ** (len(digits) - 1 - i)
        return mcq(rng, f"What is the place value of {digits[i]} in {n:,}?", f"{place_value:,}",
                   [f"{x:,}" for x in {int(digits[i]), place_value * 10, max(1, place_value // 10)} if x != place_value] + [f"{place_value + 1:,}"],
                   'medium', f"{digits[i]} is in the {names[len(digits) - 1 - i]} place.")

    register(f'math.c{g}.multiplication', S, 'Multiplication', gen=mult)
    register(f'math.c{g}.division', S, 'Division', gen=div)
    register(f'math.c{g}.measurement', S, 'Measurement (Length, Weight, Capacity, Time)', gen=measure)
    register(f'math.c{g}.place_value', S, 'Place Value', gen=place)
    CHAPTERS[g] += [(f'math.c{g}.place_value', 'Place Value'), (f'math.c{g}.multiplication', 'Multiplication'),
                    (f'math.c{g}.division', 'Division'), (f'math.c{g}.measurement', 'Measurement (Length, Weight, Capacity, Time)')]


def fractions_basic(rng):
    kind = rng.randrange(3)
    d = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
    a, b = rng.randint(1, d - 1), rng.randint(1, d - 1)
    if kind == 0:
        s = F(a, d) + F(b, d)
        return mcq(rng, f"{a}/{d} + {b}/{d} = ?", frac_str(s), [f"{a + b}/{2 * d}", frac_str(s + F(1, d)), frac_str(F(a * b, d))], 'easy', "Same denominator: add numerators.")
    if kind == 1:
        k = rng.randint(2, 5)
        return mcq(rng, f"Which fraction is equivalent to {a}/{d}?", f"{a * k}/{d * k}", [f"{a + k}/{d + k}", f"{a * k}/{d}", f"{a}/{d * k}"], 'easy', f"Multiply top and bottom by {k}.")
    x, y = F(a, d), F(b, rng.choice([3, 4, 5, 7, 9]))
    if x == y:
        y += F(1, 9)
    return mcq(rng, f"Which is greater: {frac_str(x)} or {frac_str(y)}?", frac_str(max(x, y)), [frac_str(min(x, y)), 'Both are equal', 'Cannot compare'], 'medium', "Compare using a common denominator.")


def area_perimeter_basic(rng):
    l, b = rng.randint(2, 30), rng.randint(2, 20)
    if rng.random() < 0.5:
        return mcq(rng, f"The perimeter of a rectangle of length {l} cm and breadth {b} cm is ___.", f"{2 * (l + b)} cm",
                   [f"{x} cm" for x in (l * b, l + b, 2 * l + b)], 'easy', "Perimeter = 2(l + b).")
    return mcq(rng, f"The area of a rectangle of length {l} cm and breadth {b} cm is ___.", f"{l * b} sq cm",
               [f"{x} sq cm" for x in (2 * (l + b), l + b, l * b + l)], 'easy', "Area = l × b.")


def lcm_hcf_basic(rng):
    a, b = rng.choice([(4, 6), (6, 8), (8, 12), (9, 12), (10, 15), (12, 18), (14, 21), (15, 20), (16, 24), (18, 27)])
    if rng.random() < 0.5:
        return mcq(rng, f"The LCM of {a} and {b} is ___.", str(math.lcm(a, b)), [str(x) for x in (a * b, math.gcd(a, b), math.lcm(a, b) * 2)], 'easy', "Smallest common multiple.")
    return mcq(rng, f"The HCF of {a} and {b} is ___.", str(math.gcd(a, b)), [str(x) for x in (math.lcm(a, b), 1, math.gcd(a, b) * 2)], 'easy', "Largest common factor.")


def decimals_basic(rng):
    a, b = rng.randint(11, 999) / 10, rng.randint(11, 999) / 100
    s = round(a + b, 2)
    return mcq(rng, f"{a} + {b} = ?", fmt(s), [fmt(round(s + 0.1, 2)), fmt(round(s - 1, 2)), fmt(round(a * 10 + b, 2))], 'medium', "Line up the decimal points.")


for g, key, title, fn in [(3, 'math.c3.fractions', 'Fractions', fractions_basic), (4, 'math.c4.fractions', 'Fractions', fractions_basic),
                          (5, 'math.c5.fractions', 'Fractions', fractions_basic), (4, 'math.c4.area_perimeter', 'Perimeter & Area', area_perimeter_basic),
                          (5, 'math.c5.area_perimeter', 'Perimeter & Area', area_perimeter_basic), (5, 'math.c5.lcm_hcf', 'Factors, Multiples, LCM & HCF', lcm_hcf_basic),
                          (5, 'math.c5.decimals', 'Decimals', decimals_basic), (4, 'math.c4.money', 'Money', lambda rng: money_bill(rng))]:
    register(key, S, title, gen=fn)
    CHAPTERS[g].append((key, title))


def money_bill(rng):
    items = rng.sample([('pen', 15), ('notebook', 40), ('eraser', 5), ('box of crayons', 65), ('ruler', 12), ('bag', 350), ('bottle', 120)], 3)
    qty = [rng.randint(1, 4) for _ in items]
    total = sum(p * q for (_, p), q in zip(items, qty))
    lines = ', '.join(f"{q} {n}{'s' if q > 1 else ''} at ₹{p} each" for (n, p), q in zip(items, qty))
    return mcq(rng, f"Find the total cost: {lines}.", f"₹{total}", [f"₹{x}" for x in (total + 10, total - 5, sum(p for _, p in items))], 'medium', f"Total = ₹{total}.")


# ------------------------------------------------------------------ Classes 6–8

@chapter(6, 'math.c6.integers', 'Integers')
def integers(rng):
    a, b = rng.randint(-50, 50), rng.randint(-50, 50)
    op = rng.choice(['+', '−', '×'])
    v = a + b if op == '+' else a - b if op == '−' else a * b
    return mcq(rng, f"({a}) {op} ({b}) = ?", str(v), [str(x) for x in (-v if v else 5, v + 2, v - 10, a + b if op != '+' else a - b)], 'easy', f"= {v}.")


@chapter(6, 'math.c6.fractions_decimals', 'Fractions & Decimals')
def fractions_decimals(rng):
    a, b = F(rng.randint(1, 9), rng.choice([2, 3, 4, 5, 6])), F(rng.randint(1, 9), rng.choice([2, 3, 4, 5, 6]))
    op = rng.choice(['+', '−', '×', '÷'])
    v = {'+': a + b, '−': a - b, '×': a * b, '÷': a / b}[op]
    return mcq(rng, f"{frac_str(a)} {op} {frac_str(b)} = ?", frac_str(v), [frac_str(x) for x in (v + 1, v * 2, -v if v else F(1, 2), a + b if op != '+' else a * b)], 'medium',
               f"= {frac_str(v)}.")


@chapter(6, 'math.c6.ratio', 'Ratio & Proportion')
def ratio_school(rng):
    a, b, k = rng.randint(1, 9), rng.randint(1, 9), rng.randint(2, 12)
    if a == b:
        b += 1
    g = math.gcd(a, b)
    return mcq(rng, f"The ratio {a * k} : {b * k} in its simplest form is ___.", f"{a // g} : {b // g}",
               [f"{b // g} : {a // g}", f"{a * k // 2} : {b * k // 2}" if k % 2 == 0 else f"{a + 1} : {b}", f"{a // g + 1} : {b // g + 1}"], 'easy', f"Divide both by {g * k}.")


@chapter(6, 'math.c6.algebra_intro', 'Introduction to Algebra')
def algebra_intro(rng):
    x, a, b = rng.randint(1, 12), rng.randint(2, 9), rng.randint(1, 20)
    return mcq(rng, f"If x = {x}, what is the value of {a}x + {b}?", str(a * x + b), [str(v) for v in (a + x + b, a * x, a * (x + b), a * x - b)], 'easy', f"{a}×{x} + {b} = {a * x + b}.")


@chapter(7, 'math.c7.simple_equations', 'Simple Equations')
def simple_equations(rng):
    x, a, b = rng.randint(-10, 20), rng.randint(2, 9), rng.randint(-15, 15)
    c = a * x + b
    sign = '+' if b >= 0 else '−'
    return mcq(rng, f"Solve: {a}x {sign} {abs(b)} = {c}", f"x = {x}", [f"x = {v}" for v in (x + 1, -x if x else 2, x - 2, c - b)], 'easy', f"{a}x = {c - b} → x = {x}.")


@chapter(7, 'math.c7.lines_angles', 'Lines & Angles')
def lines_angles(rng):
    a = rng.randint(10, 80)
    kind = rng.randrange(3)
    if kind == 0:
        return mcq(rng, f"The complement of {a}° is ___.", f"{90 - a}°", [f"{180 - a}°", f"{a}°", f"{abs(90 - 2 * a)}°" if 90 - 2 * a else "45°"], 'easy', "Complementary angles add to 90°.")
    if kind == 1:
        a = rng.randint(20, 160)
        return mcq(rng, f"The supplement of {a}° is ___.", f"{180 - a}°", [f"{90 - a}°" if a < 90 else f"{a - 90}°", f"{a}°", f"{360 - a}°"], 'easy', "Supplementary angles add to 180°.")
    b = rng.randint(20, 100)
    while a + b >= 170:
        b -= 30
    return mcq(rng, f"Two angles of a triangle are {a}° and {b}°. The third angle is ___.", f"{180 - a - b}°", [f"{90 - a}°" if a < 90 else "45°", f"{a + b}°", f"{180 - a}°"], 'easy', "Angle sum is 180°.")


@chapter(7, 'math.c7.percentage', 'Comparing Quantities (Percentage, Profit & Loss, SI)')
def percentage_school(rng):
    from .gen_quant import percentage, profit_loss, interest
    return rng.choice([percentage, profit_loss, interest])(rng)


@chapter(7, 'math.c7.data_handling', 'Data Handling (Mean, Median, Mode)')
def data_handling(rng):
    data = sorted(rng.randint(1, 30) for _ in range(rng.choice([5, 7])))
    kind = rng.randrange(3)
    if kind == 0:
        m = F(sum(data), len(data))
        return mcq(rng, f"Find the mean of: {', '.join(map(str, data))}", fmt(m), near(rng, m, spread=1), 'easy', f"{sum(data)}/{len(data)} = {fmt(m)}.")
    if kind == 1:
        shuffled = data[:]
        rng.shuffle(shuffled)
        med = data[len(data) // 2]
        return mcq(rng, f"Find the median of: {', '.join(map(str, shuffled))}", str(med), [str(x) for x in {data[0], data[-1], data[len(data) // 2 - 1], med + 1} if x != med], 'medium',
                   f"Sorted: {', '.join(map(str, data))}; the middle value is {med}.")
    v = rng.randint(1, 30)
    data = data[:-2] + [v, v, v]
    rng.shuffle(data)
    return mcq(rng, f"Find the mode of: {', '.join(map(str, data))}", str(v), [str(x) for x in set(data) if x != v][:3] + [str(v + 1)], 'easy', f"{v} occurs most often.")


@chapter(8, 'math.c8.squares_cubes', 'Squares, Square Roots, Cubes & Cube Roots')
def squares_cubes(rng):
    kind = rng.randrange(3)
    n = rng.randint(11, 99)
    if kind == 0:
        return mcq(rng, f"√{n * n:,} = ?", str(n), [str(x) for x in (n + 1, n - 1, n + 10)], 'easy', f"{n}² = {n * n:,}.")
    if kind == 1:
        return mcq(rng, f"{n}² = ?", f"{n * n:,}", [f"{x:,}" for x in (n * n + n, n * 2, (n + 1) ** 2)], 'easy', f"{n} × {n}.")
    m = rng.randint(2, 20)
    return mcq(rng, f"∛{m ** 3:,} = ?", str(m), [str(x) for x in (m + 1, m - 1, m * 3)], 'medium', f"{m}³ = {m ** 3:,}.")


@chapter(8, 'math.c8.exponents', 'Exponents & Powers')
def exponents(rng):
    a, m, n = rng.choice([2, 3, 5, 10]), rng.randint(2, 6), rng.randint(1, 5)
    kind = rng.randrange(3)
    if kind == 0:
        return mcq(rng, f"{a}^{m} × {a}^{n} = ?", f"{a}^{m + n}", [f"{a}^{m * n}", f"{a * a}^{m + n}", f"{a}^{abs(m - n)}"], 'easy', "aᵐ × aⁿ = aᵐ⁺ⁿ.")
    if kind == 1:
        return mcq(rng, f"({a}^{m})^{n} = ?", f"{a}^{m * n}", [f"{a}^{m + n}", f"{a}^{m ** n}", f"{a * n}^{m}"], 'easy', "(aᵐ)ⁿ = aᵐⁿ.")
    return mcq(rng, f"{a}^(−{n}) = ?", f"1/{a ** n}", [f"−{a ** n}", f"{a ** n}", f"−1/{a ** n}"], 'medium', "a⁻ⁿ = 1/aⁿ.")


@chapter(8, 'math.c8.linear_equations', 'Linear Equations in One Variable')
def linear_one(rng):
    x = rng.randint(-8, 12)
    a, b, c = rng.randint(2, 7), rng.randint(1, 9), rng.randint(1, 5)
    if a == c:
        a += 1
    d = a * x + b - c * x
    return mcq(rng, f"Solve: {a}x + {b} = {c}x + {d}", f"x = {x}", [f"x = {v}" for v in (x + 1, -x if x else 3, x - 2, d - b)], 'medium',
               f"({a} − {c})x = {d} − {b} → x = {x}.")


@chapter(8, 'math.c8.mensuration', 'Mensuration')
def mensuration_school(rng):
    from .gen_quant import mensuration
    return mensuration(rng)


@chapter(8, 'math.c8.algebraic_identities', 'Algebraic Expressions & Identities')
def identities(rng):
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    kind = rng.randrange(3)
    if kind == 0:
        return mcq(rng, f"Using (a + b)² = a² + 2ab + b², find ({a}x + {b})².", f"{a * a}x² + {2 * a * b}x + {b * b}",
                   [f"{a * a}x² + {b * b}", f"{a * a}x² + {a * b}x + {b * b}", f"{2 * a}x² + {2 * a * b}x + {2 * b}"], 'medium', "Expand with the identity.")
    if kind == 1:
        n = rng.choice([97, 98, 99, 101, 102, 103, 49, 51])
        return mcq(rng, f"Using an identity, {n}² = ?", f"{n * n:,}", [f"{x:,}" for x in (n * n + 100, n * n - 1, n * 100)], 'medium', f"Write {n} as {round(n, -1 if n < 60 else -2)} {'+' if n > round(n, -1 if n < 60 else -2) else '−'} {abs(n - round(n, -1 if n < 60 else -2))} and use (a ± b)² = a² ± 2ab + b²: {n * n:,}.")
    return mcq(rng, f"({a}x + {b})({a}x − {b}) = ?", f"{a * a}x² − {b * b}", [f"{a * a}x² + {b * b}", f"{a * a}x² − {2 * a * b}x − {b * b}", f"{2 * a}x² − {2 * b}"], 'easy', "(p + q)(p − q) = p² − q².")


# ------------------------------------------------------------------ Classes 9–10

@chapter(9, 'math.c9.number_systems', 'Number Systems')
def number_systems(rng):
    kind = rng.randrange(3)
    if kind == 0:
        cands = [('√2', 'irrational'), ('√9', 'rational'), ('π', 'irrational'), ('0.333…', 'rational'), ('√5', 'irrational'), ('22/7', 'rational'),
                 ('√16', 'rational'), ('0.101001000…', 'irrational'), ('√3', 'irrational'), ('1.25', 'rational')]
        target = rng.choice(['rational', 'irrational'])
        right = rng.choice([c for c, t in cands if t == target])
        wrong = [c for c, t in cands if t != target]
        return mcq(rng, f"Which of the following is {target}?", right, wrong, 'easy', f"{right} is {target}.")
    if kind == 1:
        a = rng.choice([2, 3, 5, 7])
        return mcq(rng, f"Rationalise the denominator of 1/√{a}.", f"√{a}/{a}", [f"{a}/√{a}", f"1/{a}", f"√{a}"], 'easy', f"Multiply by √{a}/√{a}.")
    n = rng.choice([2, 3, 4, 5])
    x = rng.choice([4, 8, 9, 16, 27, 32, 64, 81])
    # x^(1/n) only when exact
    root = round(x ** (1 / n))
    if root ** n != x:
        x, n, root = 64, 3, 4
    return mcq(rng, f"{x}^(1/{n}) = ?", str(root), [str(v) for v in (root + 1, x // n, root * 2)], 'medium', f"{root}^{n} = {x}.")


@chapter(9, 'math.c9.polynomials', 'Polynomials')
def polynomials(rng):
    a, b, c = rng.randint(1, 5), rng.randint(-9, 9), rng.randint(-9, 9)
    k = rng.randint(-4, 4)
    val = a * k * k + b * k + c
    poly = f"{a}x² {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)}"
    if rng.random() < 0.5:
        return mcq(rng, f"If p(x) = {poly}, then p({k}) = ?", str(val), [str(v) for v in (val + 2, -val if val else 4, a * k + b + c)], 'medium', f"Substitute x = {k}.")
    return mcq(rng, f"The remainder when p(x) = {poly} is divided by (x {'−' if k >= 0 else '+'} {abs(k)}) is ___.", str(val),
               [str(v) for v in (val + 1, a * k * k - b * k + c, c)], 'medium', f"Remainder theorem: p({k}) = {val}.")


@chapter(9, 'math.c9.coordinate', 'Coordinate Geometry')
def coordinate(rng):
    x, y = rng.choice([-1, 1]) * rng.randint(1, 9), rng.choice([-1, 1]) * rng.randint(1, 9)
    quad = {(1, 1): 'First', (-1, 1): 'Second', (-1, -1): 'Third', (1, -1): 'Fourth'}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    return mcq(rng, f"The point ({x}, {y}) lies in the ___ quadrant.", quad, [q for q in ('First', 'Second', 'Third', 'Fourth') if q != quad], 'easy',
               "Signs (+,+) I, (−,+) II, (−,−) III, (+,−) IV.")


@chapter(9, 'math.c9.herons_area', "Heron's Formula & Areas")
def herons(rng):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (13, 14, 15), (6, 8, 10), (7, 24, 25), (9, 10, 17), (10, 13, 13)])
    s = F(a + b + c, 2)
    area = math.isqrt(int(s * (s - a) * (s - b) * (s - c)))
    return mcq(rng, f"The area of a triangle with sides {a} cm, {b} cm and {c} cm is ___.", f"{area} cm²",
               [f"{x} cm²" for x in (area * 2, a * b // 2 if a * b // 2 != area else area + 6, area + 4)], 'medium', f"s = {fmt(s)}; √(s(s−a)(s−b)(s−c)) = {area}.")


@chapter(9, 'math.c9.surface_volume', 'Surface Areas & Volumes')
def surface_volume(rng):
    from .gen_quant import mensuration
    return mensuration(rng)


@chapter(9, 'math.c9.linear_two', 'Linear Equations in Two Variables')
def linear_two(rng):
    x, y = rng.randint(-5, 9), rng.randint(-5, 9)
    a, b = rng.randint(1, 5), rng.randint(1, 5)
    c = a * x + b * y
    return mcq(rng, f"Which point lies on the line {a}x + {b}y = {c}?", f"({x}, {y})", [f"({x + 1}, {y})", f"({y}, {x})" if x != y else f"({x}, {y + 2})", f"({x}, {y - 1})"],
               'easy', f"{a}×{x} + {b}×{y} = {c}.")


@chapter(10, 'math.c10.real_numbers', 'Real Numbers')
def real_numbers(rng):
    from .gen_quant import number_system
    return number_system(rng)


@chapter(10, 'math.c10.pair_linear', 'Pair of Linear Equations in Two Variables')
def pair_linear(rng):
    x, y = rng.randint(-5, 9), rng.randint(-5, 9)
    a1, b1, a2, b2 = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5), rng.randint(-5, -1)
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    return mcq(rng, f"Solve: {a1}x + {b1}y = {c1} and {a2}x − {abs(b2)}y = {c2}", f"x = {x}, y = {y}",
               [f"x = {y}, y = {x}" if x != y else f"x = {x + 1}, y = {y}", f"x = {x + 1}, y = {y - 1}", f"x = {-x}, y = {y}" if x else f"x = 2, y = {y}"], 'medium',
               "Eliminate one variable.")


@chapter(10, 'math.c10.quadratic', 'Quadratic Equations')
def quadratic_school(rng):
    r1, r2 = rng.randint(-9, 9), rng.randint(-9, 9)
    b, c = -(r1 + r2), r1 * r2
    eq = f"x² {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)} = 0"
    kind = rng.randrange(2)
    if kind == 0:
        ans = f"{min(r1, r2)}, {max(r1, r2)}"
        return mcq(rng, f"The roots of {eq} are ___.", ans, [f"{-max(r1, r2)}, {-min(r1, r2)}", f"{min(r1, r2) + 1}, {max(r1, r2)}", f"{r1 * r2}, {r1 + r2}"], 'medium', "Factorise.")
    a2, b2, c2 = rng.randint(1, 4), rng.randint(-8, 8), rng.randint(-6, 6)
    disc = b2 * b2 - 4 * a2 * c2
    nature = 'Two distinct real roots' if disc > 0 else 'Two equal real roots' if disc == 0 else 'No real roots'
    eq2 = f"{a2}x² {'+' if b2 >= 0 else '−'} {abs(b2)}x {'+' if c2 >= 0 else '−'} {abs(c2)} = 0"
    return mcq(rng, f"The nature of the roots of {eq2} is ___.", nature, [n for n in ('Two distinct real roots', 'Two equal real roots', 'No real roots', 'Infinitely many roots') if n != nature],
               'medium', f"D = b² − 4ac = {disc}.")


@chapter(10, 'math.c10.ap', 'Arithmetic Progressions')
def ap(rng):
    a, d, n = rng.randint(-10, 20), rng.choice([-4, -3, -2, 2, 3, 4, 5, 7]), rng.randint(8, 30)
    if rng.random() < 0.5:
        t = a + (n - 1) * d
        return mcq(rng, f"The {n}th term of the AP {a}, {a + d}, {a + 2 * d}, … is ___.", str(t), [str(x) for x in (a + n * d, t + d, a * n)], 'easy', f"aₙ = a + (n − 1)d = {t}.")
    s = n * (2 * a + (n - 1) * d) // 2 if (n * (2 * a + (n - 1) * d)) % 2 == 0 else None
    if s is None:
        n += 1
        s = n * (2 * a + (n - 1) * d) // 2
    return mcq(rng, f"The sum of the first {n} terms of the AP {a}, {a + d}, {a + 2 * d}, … is ___.", str(s),
               [str(x) for x in (s + d, n * a, s - n)], 'medium', f"Sₙ = n/2[2a + (n − 1)d] = {s}.")


@chapter(10, 'math.c10.coordinate', 'Coordinate Geometry (Distance & Section Formula)')
def coordinate_10(rng):
    x1, y1 = rng.randint(-6, 6), rng.randint(-6, 6)
    dx, dy, dist = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (0, 7, 7), (9, 12, 15)])
    x2, y2 = x1 + rng.choice([-1, 1]) * dx, y1 + rng.choice([-1, 1]) * dy
    if rng.random() < 0.5:
        return mcq(rng, f"The distance between ({x1}, {y1}) and ({x2}, {y2}) is ___ units.", str(dist), [str(x) for x in (dx + dy, dist + 1, abs(dx - dy) or 2)], 'easy',
                   f"√({dx}² + {dy}²) = {dist}.")
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    return mcq(rng, f"The midpoint of ({x1}, {y1}) and ({x2}, {y2}) is ___.", f"({fmt(mx)}, {fmt(my)})",
               [f"({fmt(my)}, {fmt(mx)})", f"({x1 + x2}, {y1 + y2})", f"({fmt(mx + 1)}, {fmt(my)})"], 'easy', "Average the coordinates.")


@chapter(10, 'math.c10.trigonometry', 'Introduction to Trigonometry & Applications')
def trig_school(rng):
    from .gen_quant import trigonometry
    return trigonometry(rng)


@chapter(10, 'math.c10.statistics', 'Statistics')
def stats_10(rng):
    return data_handling(rng)


@chapter(10, 'math.c10.probability', 'Probability')
def prob_10(rng):
    from .gen_quant import probability
    return probability(rng)


@chapter(10, 'math.c10.circles_areas', 'Circles & Areas Related to Circles')
def circles_10(rng):
    kind = rng.randrange(2)
    if kind == 0:
        r, d, t = rng.choice([(3, 5, 4), (5, 13, 12), (6, 10, 8), (8, 17, 15), (7, 25, 24), (9, 15, 12)])
        return mcq(rng, f"From a point {d} cm from the centre of a circle of radius {r} cm, the length of the tangent is ___.", f"{t} cm",
                   [f"{x} cm" for x in (d - r, d + r, t + 1)], 'medium', f"√({d}² − {r}²) = {t}.")
    r, ang = 7 * rng.randint(1, 3), rng.choice([30, 45, 60, 90, 120])
    area = F(ang, 360) * F(22, 7) * r * r
    return mcq(rng, f"The area of a sector of angle {ang}° in a circle of radius {r} cm is ___ cm². (π = 22/7)", fmt(area),
               [fmt(x) for x in (area * 2, F(22, 7) * r * r, area + 11)], 'medium', f"θ/360 × πr² = {fmt(area)}.")


# ------------------------------------------------------------------ Classes 11–12

@chapter(11, 'math.c11.sets_functions', 'Sets, Relations & Functions')
def sets_functions(rng):
    kind = rng.randrange(3)
    if kind == 0:
        n = rng.randint(2, 7)
        return mcq(rng, f"A set has {n} elements. How many subsets does it have?", str(2 ** n), [str(x) for x in (2 ** n - 1, n * n, 2 * n)], 'easy', f"2ⁿ = {2 ** n}.")
    if kind == 1:
        a, b, both = rng.randint(20, 60), rng.randint(20, 60), rng.randint(5, 19)
        return mcq(rng, f"n(A) = {a}, n(B) = {b} and n(A ∩ B) = {both}. Find n(A ∪ B).", str(a + b - both), [str(x) for x in (a + b, a + b + both, abs(a - b))], 'easy',
                   "n(A ∪ B) = n(A) + n(B) − n(A ∩ B).")
    m, n = rng.randint(2, 4), rng.randint(2, 4)
    return mcq(rng, f"If n(A) = {m} and n(B) = {n}, the number of relations from A to B is ___.", str(2 ** (m * n)), [str(x) for x in (m * n, 2 ** (m + n), n ** m)], 'medium',
               f"2^(mn) = 2^{m * n}.")


@chapter(11, 'math.c11.trigonometric_functions', 'Trigonometric Functions')
def trig_functions(rng):
    deg = rng.choice([30, 45, 60, 90, 120, 135, 150, 180, 270, 360])
    r = F(deg, 180)
    rad = ('π' if r == 1 else f"{r.numerator}π") if r.denominator == 1 else (f"π/{r.denominator}" if r.numerator == 1 else f"{r.numerator}π/{r.denominator}")
    wrong = [w for w in ('π/6', 'π/4', 'π/3', 'π/2', '2π/3', '3π/4', '5π/6', 'π', '3π/2', '2π') if w != rad]
    rng.shuffle(wrong)
    if rad == '2π':
        pass
    return mcq(rng, f"{deg}° in radians is ___.", rad, wrong, 'easy', "Multiply by π/180.")


@chapter(11, 'math.c11.complex', 'Complex Numbers')
def complex_numbers(rng):
    kind = rng.randrange(2)
    if kind == 0:
        n = rng.randint(5, 103)
        v = ['1', 'i', '−1', '−i'][n % 4]
        return mcq(rng, f"i^{n} = ?", v, [x for x in ('1', 'i', '−1', '−i') if x != v], 'easy', f"{n} mod 4 = {n % 4}.")
    a, b, m = rng.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (1, 1, None)])
    mod = str(m) if m else '√2'
    return mcq(rng, f"The modulus of {a} + {b}i is ___.", mod, [str(a + b), str(a * b), '√2' if m else '2', str((m or 2) + 1)], 'easy', f"√({a}² + {b}²).")


@chapter(11, 'math.c11.pnc_binomial', 'Permutations, Combinations & Binomial Theorem')
def pnc(rng):
    if rng.random() < 0.5:
        from .gen_quant import probability
        return probability(rng)
    n, r = rng.randint(4, 10), rng.randint(1, 3)
    coef = math.comb(n, r)
    return mcq(rng, f"The coefficient of x^{r} in (1 + x)^{n} is ___.", str(coef), [str(x) for x in (n * r, math.perm(n, r), coef + n)], 'medium', f"ⁿCᵣ = {coef}.")


@chapter(11, 'math.c11.sequences', 'Sequences & Series')
def sequences(rng):
    a, r, n = rng.randint(1, 5), rng.choice([2, 3]), rng.randint(4, 8)
    if rng.random() < 0.5:
        return mcq(rng, f"The {n}th term of the GP {a}, {a * r}, {a * r * r}, … is ___.", str(a * r ** (n - 1)), [str(x) for x in (a * r ** n, a * r * n, a + r ** n)], 'easy', "arⁿ⁻¹.")
    s = a * (r ** n - 1) // (r - 1)
    return mcq(rng, f"The sum of the first {n} terms of the GP {a}, {a * r}, {a * r * r}, … is ___.", str(s), [str(x) for x in (a * r ** n, s + a, s - a * r ** (n - 1))], 'medium',
               "a(rⁿ − 1)/(r − 1).")


@chapter(11, 'math.c11.straight_lines', 'Straight Lines & Conic Sections')
def lines_conics(rng):
    kind = rng.randrange(3)
    if kind == 0:
        x1, y1, x2, y2 = rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-5, 5)
        if x1 == x2:
            x2 += 2
        m = F(y2 - y1, x2 - x1)
        return mcq(rng, f"The slope of the line through ({x1}, {y1}) and ({x2}, {y2}) is ___.", frac_str(m), [frac_str(x) for x in (-m if m else F(1), 1 / m if m else F(2), m + 1)], 'easy',
                   "(y₂ − y₁)/(x₂ − x₁).")
    if kind == 1:
        h, k, r = rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(1, 9)
        c = h * h + k * k - r * r
        eq = f"x² + y² {'−' if h > 0 else '+'} {abs(2 * h)}x {'−' if k > 0 else '+'} {abs(2 * k)}y {'+' if c >= 0 else '−'} {abs(c)} = 0"
        return mcq(rng, f"The radius of the circle {eq} is ___.", str(r), [str(x) for x in (r * r, r + 1, abs(c) or 3)], 'medium', f"Centre ({h}, {k}); r = √(h² + k² − c) = {r}.")
    a = rng.randint(1, 6)
    return mcq(rng, f"The focus of the parabola y² = {4 * a}x is ___.", f"({a}, 0)", [f"(0, {a})", f"({4 * a}, 0)", f"(−{a}, 0)"], 'medium', "y² = 4ax has focus (a, 0).")


@chapter(11, 'math.c11.limits_derivatives', 'Limits & Derivatives')
def limits_derivatives(rng):
    kind = rng.randrange(2)
    if kind == 0:
        a = rng.randint(1, 6)
        n = rng.randint(2, 5)
        v = n * a ** (n - 1)
        return mcq(rng, f"lim (x→{a}) (x^{n} − {a ** n})/(x − {a}) = ?", str(v), [str(x) for x in (a ** n, n * a ** n, v + n)], 'medium', "Standard limit n·aⁿ⁻¹.")
    c, n, x0 = rng.randint(1, 6), rng.randint(2, 4), rng.randint(1, 4)
    d = c * n * x0 ** (n - 1)
    return mcq(rng, f"If f(x) = {c}x^{n}, then f′({x0}) = ?", str(d), [str(x) for x in (c * x0 ** n, c * n * x0 ** n, d + c)], 'easy', f"f′(x) = {c * n}x^{n - 1}.")


@chapter(11, 'math.c11.statistics_probability', 'Statistics & Probability')
def stats_11(rng):
    data = [rng.randint(1, 10) * 2 for _ in range(4)]
    mean = F(sum(data), 4)
    var = sum((F(x) - mean) ** 2 for x in data) / 4
    if rng.random() < 0.5:
        return mcq(rng, f"The variance of {', '.join(map(str, data))} is ___.", fmt(var), [fmt(x) for x in (var * 2, mean, var + 1)] + [fmt(math.sqrt(var))], 'hard',
                   f"Mean {fmt(mean)}; average squared deviation = {fmt(var)}.")
    from .gen_quant import probability
    return probability(rng)


@chapter(12, 'math.c12.matrices', 'Matrices & Determinants')
def matrices(rng):
    a, b, c, d = (rng.randint(-5, 9) for _ in range(4))
    kind = rng.randrange(3)
    if kind == 0:
        det = a * d - b * c
        return mcq(rng, f"The determinant of [[{a}, {b}], [{c}, {d}]] is ___.", str(det), [str(x) for x in (a * d + b * c, a + d, -det if det else 1)], 'easy', "ad − bc.")
    if kind == 1:
        m, n, p = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4)
        return mcq(rng, f"If A is {m} × {n} and B is {n} × {p}, the order of AB is ___.", f"{m} × {p}", [f"{n} × {n}", f"{p} × {m}", f"{m} × {n}"] if (m, p) != (n, n) else [f"{p} × {n}", f"{m} × {m + 1}", "Not defined"],
                   'easy', "Rows of A × columns of B.")
    e, f_, g, h = (rng.randint(-3, 5) for _ in range(4))
    prod = [[a * e + b * g, a * f_ + b * h], [c * e + d * g, c * f_ + d * h]]
    ans = f"[[{prod[0][0]}, {prod[0][1]}], [{prod[1][0]}, {prod[1][1]}]]"
    return mcq(rng, f"If A = [[{a}, {b}], [{c}, {d}]] and B = [[{e}, {f_}], [{g}, {h}]], then AB = ?", ans,
               [f"[[{a * e}, {b * f_}], [{c * g}, {d * h}]]", f"[[{a + e}, {b + f_}], [{c + g}, {d + h}]]", f"[[{prod[0][0]}, {prod[1][0]}], [{prod[0][1]}, {prod[1][1]}]]"],
               'medium', "Row × column.")


@chapter(12, 'math.c12.determinant3', '3 × 3 Determinants & Inverse')
def det3(rng):
    m = [[rng.randint(-3, 4) for _ in range(3)] for _ in range(3)]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    shown = ', '.join('[' + ', '.join(map(str, r)) + ']' for r in m)
    return mcq(rng, f"Find the determinant of [{shown}].", str(det), [str(x) for x in (det + 2, -det if det else 3, det - 5)], 'hard', "Expand along the first row.")


@chapter(12, 'math.c12.calculus', 'Continuity, Differentiation & Applications')
def calculus(rng):
    kind = rng.randrange(2)
    if kind == 0:
        a, b, c = rng.randint(1, 5), rng.randint(-10, 10), rng.randint(-5, 5)
        x0 = F(-b, 2 * a)
        mn = a * x0 * x0 + b * x0 + c
        return mcq(rng, f"The minimum value of f(x) = {a}x² {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)} is ___.", fmt(mn),
                   [fmt(x) for x in (c, mn - 1, -mn if mn else 2)], 'hard', f"At x = −b/2a = {fmt(x0)}.")
    n, k = rng.randint(2, 5), rng.randint(2, 6)
    return mcq(rng, f"d/dx [sin({k}x)] = ?", f"{k} cos({k}x)", [f"cos({k}x)", f"−{k} cos({k}x)", f"{k} sin({k}x)"], 'easy', "Chain rule.")


@chapter(12, 'math.c12.integrals', 'Integrals & Applications')
def integrals(rng):
    a, b = rng.randint(0, 2), rng.randint(3, 5)
    c, n = rng.randint(1, 4), rng.randint(1, 3)
    val = F(c, n + 1) * (b ** (n + 1) - a ** (n + 1))
    coef = '' if c == 1 else str(c)
    power = '' if n == 1 else f"^{n}"
    return mcq(rng, f"∫ from {a} to {b} of {coef}x{power} dx = ?", fmt(val), [fmt(x) for x in (val * 2, F(c) * (b ** n - a ** n), val + c)], 'medium',
               f"[{coef}x^{n + 1}/{n + 1}] from {a} to {b} = {fmt(val)}.")


@chapter(12, 'math.c12.vectors_3d', 'Vectors & Three-Dimensional Geometry')
def vectors(rng):
    a = [rng.randint(-4, 5) for _ in range(3)]
    b = [rng.randint(-4, 5) for _ in range(3)]
    fmtv = lambda v: f"{v[0]}î {'+' if v[1] >= 0 else '−'} {abs(v[1])}ĵ {'+' if v[2] >= 0 else '−'} {abs(v[2])}k̂"
    if rng.random() < 0.6:
        dot = sum(x * y for x, y in zip(a, b))
        return mcq(rng, f"If a = {fmtv(a)} and b = {fmtv(b)}, then a · b = ?", str(dot), [str(x) for x in (dot + 2, -dot if dot else 1, sum(a) + sum(b))], 'easy', "Multiply components and add.")
    p, q, r = rng.choice([(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7)])
    return mcq(rng, f"The magnitude of the vector {p}î + {q}ĵ + {r}k̂ is ___.", str(int(math.sqrt(p * p + q * q + r * r))),
               [str(x) for x in (p + q + r, p * q * r, int(math.sqrt(p * p + q * q + r * r)) + 1)], 'easy', "√(x² + y² + z²).")


@chapter(12, 'math.c12.lpp_probability', 'Linear Programming & Probability')
def lpp(rng):
    corners = [(0, 0)] + [(rng.randint(0, 10), rng.randint(0, 10)) for _ in range(3)]
    p, q = rng.randint(1, 6), rng.randint(1, 6)
    values = [p * x + q * y for x, y in corners]
    best = max(values)
    pts = ', '.join(f"({x}, {y})" for x, y in corners)
    return mcq(rng, f"The corner points of a feasible region are {pts}. The maximum of Z = {p}x + {q}y is ___.", str(best),
               [str(v) for v in sorted(set(values) - {best})][:3] + [str(best + p)], 'medium', "Evaluate Z at every corner.")


def _school_numeric(rng):
    a, d, n = rng.randint(1, 20), rng.randint(2, 7), rng.randint(5, 25)
    return numerical(f"Find the {n}th term of the AP {a}, {a + d}, {a + 2 * d}, …", a + (n - 1) * d, 'easy', "aₙ = a + (n − 1)d.")


register('math.c10.ap', S, '', numeric=_school_numeric)
