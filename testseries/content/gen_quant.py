"""Quantitative aptitude generators (SSC, Banking, Railways, MBA, placements). Answers are computed, never typed."""
import math
from fractions import Fraction as F

from .core import fmt, frac_str, generator, inr, mcq, near, numerical, register

S = 'QNT1'


@generator('quant.percentage', S, 'Percentage')
def percentage(rng):
    kind = rng.randrange(4)
    if kind == 0:
        p, base = rng.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75, 80, 120, 125, 150]), rng.randrange(20, 900, 20)
        ans = F(p * base, 100)
        return mcq(rng, f"What is {p}% of {base}?", fmt(ans), near(rng, ans), 'easy', f"{p}/100 × {base} = {fmt(ans)}.")
    if kind == 1:
        b = rng.choice([40, 50, 80, 120, 160, 200, 250, 400, 500, 800])
        p = rng.choice([5, 10, 15, 20, 25, 30, 40, 60, 75])
        a = b * p // 100
        return mcq(rng, f"{a} is what percent of {b}?", f"{p}%", [f"{x}%" for x in near(rng, p)], 'easy', f"{a}/{b} × 100 = {p}%.")
    if kind == 2:
        x, y = rng.choice([10, 20, 25, 30, 40, 50]), rng.choice([10, 20, 25, 30, 40, 50])
        net = F(x - y) - F(x * y, 100)
        word = 'increase' if net > 0 else 'decrease'
        correct = f"{fmt(abs(net))}% {word}" if net else "No change"
        wrong = [f"{fmt(abs(x - y))}% {word if x != y else 'increase'}", f"{fmt(abs(net) + 1)}% {word}",
                 f"{fmt(abs(net))}% {'decrease' if net > 0 else 'increase'}", "No change", f"{fmt(x * y / 100)}% decrease"]
        return mcq(rng, f"The price of an article is first increased by {x}% and then decreased by {y}%. The net change is ___.",
                   correct, wrong, 'medium', f"Net % = {x} − {y} − ({x}×{y})/100 = {fmt(net)}%.")
    salary = rng.randrange(20000, 90000, 1000)
    spend = rng.choice([60, 65, 70, 75, 80, 85])
    saved = salary * (100 - spend) // 100
    return mcq(rng, f"A man spends {spend}% of his income and saves {inr(saved)}. His income is ___.", inr(salary),
               [inr(v) for v in (saved * 100 // spend, salary + 5000, salary - 4000, salary + 2000)], 'medium',
               f"He saves {100 - spend}%, so income = {saved} × 100/{100 - spend} = {inr(salary)}.")


@generator('quant.profit_loss', S, 'Profit, Loss & Discount')
def profit_loss(rng):
    kind = rng.randrange(4)
    if kind == 0:
        cp = rng.randrange(200, 2000, 20)
        p = rng.choice([5, 10, 12, 15, 20, 25, 30, 40])
        gain = rng.random() < 0.7
        sp = F(cp * (100 + (p if gain else -p)), 100)
        what = 'profit' if gain else 'loss'
        return mcq(rng, f"An article bought for {inr(cp)} is sold for {inr(sp)}. The {what} percent is ___.",
                   f"{p}%", [f"{x}%" for x in near(rng, p)], 'easy', f"{what.title()} = {inr(abs(sp - cp))}; {fmt(abs(sp - cp))}/{cp} × 100 = {p}%.")
    if kind == 1:
        mp = rng.randrange(500, 5000, 100)
        d1, d2 = rng.choice([10, 20, 25]), rng.choice([5, 10, 20])
        sp = F(mp) * (100 - d1) / 100 * (100 - d2) / 100
        return mcq(rng, f"The marked price of a watch is {inr(mp)}. Successive discounts of {d1}% and {d2}% are given. The selling price is ___.",
                   inr(sp), [inr(F(mp) * (100 - d1 - d2) / 100), inr(sp + 50), inr(sp - 40), inr(sp + 25)], 'medium',
                   f"{mp} × {(100 - d1) / 100:g} × {(100 - d2) / 100:g} = {inr(sp)}.")
    if kind == 2:
        a, b = rng.choice([(12, 10), (15, 12), (20, 16), (25, 20), (10, 8), (18, 15)])
        p = F(a - b, b) * 100
        return mcq(rng, f"If the cost price of {a} pens equals the selling price of {b} pens, the profit percent is ___.",
                   f"{fmt(p)}%", [f"{fmt(F(a - b, a) * 100)}%", f"{fmt(p + 5)}%", f"{fmt(p - 4)}%", f"{a - b}%"], 'medium',
                   f"Profit % = ({a} − {b})/{b} × 100 = {fmt(p)}%.")
    cp = rng.randrange(400, 3000, 50)
    m = rng.choice([20, 25, 30, 40, 50])
    d = rng.choice([10, 15, 20])
    sp = F(cp) * (100 + m) / 100 * (100 - d) / 100
    pp = (sp - cp) / cp * 100
    return mcq(rng, f"A shopkeeper marks his goods {m}% above cost price and allows a discount of {d}%. His profit percent is ___.",
               f"{fmt(pp)}%", [f"{m - d}%", f"{fmt(pp + 2)}%", f"{fmt(pp - 3)}%", f"{m}%"], 'medium',
               f"(1 + {m}/100)(1 − {d}/100) = {fmt(1 + pp / 100)} → profit {fmt(pp)}%.")


@generator('quant.interest', S, 'Simple & Compound Interest')
def interest(rng):
    kind = rng.randrange(4)
    if kind == 0:
        p, r, t = rng.randrange(1000, 20000, 500), rng.choice([4, 5, 6, 8, 10, 12, 15]), rng.randint(2, 6)
        si = F(p * r * t, 100)
        return mcq(rng, f"The simple interest on {inr(p)} at {r}% per annum for {t} years is ___.", inr(si),
                   [inr(x) for x in (si + p * r // 100, si - p * r // 100, F(p * r, 100), si * 2)], 'easy', f"SI = P×R×T/100 = {inr(si)}.")
    if kind == 1:
        p, r, t = rng.randrange(2000, 20000, 1000), rng.choice([5, 8, 10, 12, 15, 20]), rng.randint(2, 5)
        a = p + p * r * t // 100
        return mcq(rng, f"A sum of {inr(p)} amounts to {inr(a)} at simple interest in {t} years. The rate of interest is ___.",
                   f"{r}%", [f"{x}%" for x in near(rng, r)], 'medium', f"SI = {inr(a - p)}; R = SI×100/(P×T) = {r}%.")
    if kind == 2:
        p, r = rng.choice([1000, 2000, 5000, 8000, 10000, 16000]), rng.choice([5, 10, 20])
        a = F(p) * F(100 + r, 100) ** 2
        ci = a - p
        return mcq(rng, f"The compound interest on {inr(p)} at {r}% per annum for 2 years, compounded annually, is ___.",
                   inr(ci), [inr(F(p * r * 2, 100)), inr(ci + 10), inr(ci - 25), inr(a)], 'medium',
                   f"A = {p}(1 + {r}/100)² = {inr(a)}; CI = {inr(ci)}.")
    p, r = rng.choice([1000, 2000, 4000, 5000, 10000, 12500, 20000]), rng.choice([4, 5, 8, 10, 12, 15, 20])
    diff = F(p) * F(r, 100) ** 2
    return mcq(rng, f"The difference between compound and simple interest on {inr(p)} for 2 years at {r}% per annum is ___.",
               inr(diff), [inr(x) for x in (diff * 2, diff + 10, F(p * r, 100), diff * 3)], 'hard',
               f"For 2 years, CI − SI = P(R/100)² = {inr(diff)}.")


@generator('quant.ratio', S, 'Ratio, Proportion & Ages')
def ratio(rng):
    kind = rng.randrange(3)
    if kind == 0:
        a, b = rng.choice([(2, 3), (3, 5), (4, 5), (5, 7), (3, 4), (7, 9), (1, 2)])
        k = rng.randint(5, 60)
        total = (a + b) * k
        return mcq(rng, f"{inr(total)} is divided between A and B in the ratio {a} : {b}. B's share is ___.", inr(b * k),
                   [inr(a * k), inr(b * k + k), inr(total // 2), inr(b * k - k)], 'easy', f"B = {b}/{a + b} × {total} = {inr(b * k)}.")
    if kind == 1:
        a, b = rng.choice([(3, 4), (2, 5), (5, 6), (4, 7), (3, 7), (5, 8)])
        k, n = rng.randint(2, 8), rng.choice([4, 5, 6, 8, 10])
        x, y = a * k, b * k
        g = math.gcd(x + n, y + n)
        return mcq(rng, f"The ages of two friends are in the ratio {a} : {b}. After {n} years the ratio becomes "
                   f"{(x + n) // g} : {(y + n) // g}. The present age of the elder is ___ years.", str(y),
                   [str(v) for v in (x, y + n, y - a, y + b)], 'medium', f"Ages {a}k and {b}k with k = {k}: {x} and {y} years.")
    a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 12)
    d = F(b * c, a)
    return mcq(rng, f"Find the fourth proportional to {a}, {b} and {c}.", fmt(d), near(rng, d), 'easy', f"{a} : {b} = {c} : x → x = {b}×{c}/{a} = {fmt(d)}.")


@generator('quant.average', S, 'Average')
def average(rng):
    kind = rng.randrange(3)
    if kind == 0:
        nums = [rng.randint(10, 99) for _ in range(rng.randint(4, 7))]
        avg = F(sum(nums), len(nums))
        return mcq(rng, f"Find the average of {', '.join(map(str, nums))}.", fmt(avg), near(rng, avg, spread=2), 'easy',
                   f"Sum {sum(nums)} ÷ {len(nums)} = {fmt(avg)}.")
    if kind == 1:
        n, avg, new = rng.randint(10, 40), rng.randint(20, 60), rng.randint(1, 4)
        w = avg + new * (n + 1)
        return mcq(rng, f"The average age of {n} students is {avg} years. When the teacher's age is included the average rises by {new}. The teacher's age is ___ years.",
                   str(w), [str(v) for v in (avg + new * n, w + n, avg + new, w - new)], 'medium',
                   f"Teacher = {avg} + {new}×({n}+1) = {w}.")
    n = rng.randint(5, 50)
    return mcq(rng, f"The average of the first {n} natural numbers is ___.", fmt(F(n + 1, 2)),
               [fmt(F(n, 2)), fmt(F(n + 2, 2)), str(n), fmt(F(n * (n + 1), 2))], 'easy', f"(n + 1)/2 = {fmt(F(n + 1, 2))}.")


@generator('quant.time_work', S, 'Time & Work, Pipes & Cisterns')
def time_work(rng):
    pairs = [(10, 15), (12, 24), (20, 30), (6, 12), (15, 10), (18, 36), (8, 24), (12, 36), (30, 60), (20, 60), (10, 40), (24, 40)]
    a, b = rng.choice(pairs)
    kind = rng.randrange(3)
    if kind == 0:
        t = F(a * b, a + b)
        return mcq(rng, f"A can finish a work in {a} days and B in {b} days. Working together they finish it in ___ days.",
                   fmt(t), near(rng, t) + [fmt(F(a + b, 2))], 'easy', f"1/{a} + 1/{b} = 1/{fmt(t)}.")
    if kind == 1:
        a, b = max(a, b) // 2, max(a, b)
        if a == b:
            a = b // 3
        t = F(a * b, b - a)
        return mcq(rng, f"Pipe A fills a tank in {a} hours and pipe B empties it in {b} hours. With both open the tank fills in ___ hours.",
                   fmt(t), near(rng, t) + [fmt(F(a * b, a + b))], 'medium', f"1/{a} − 1/{b} = 1/{fmt(t)}.")
    m, d = rng.choice([(12, 18), (10, 24), (15, 20), (8, 30), (20, 12), (25, 16)])
    m2 = rng.choice([6, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60])
    t = F(m * d, m2)
    return mcq(rng, f"{m} men can complete a job in {d} days. In how many days can {m2} men complete it?", fmt(t),
               near(rng, t), 'easy', f"M₁D₁ = M₂D₂ → {m}×{d}/{m2} = {fmt(t)}.")


@generator('quant.speed', S, 'Speed, Time & Distance, Trains, Boats')
def speed(rng):
    kind = rng.randrange(5)
    if kind == 0:
        kmh = rng.choice([18, 36, 54, 72, 90, 108, 126, 144])
        return mcq(rng, f"{kmh} km/h is equal to ___ m/s.", str(kmh * 5 // 18), [str(v) for v in (kmh * 18 // 5, kmh // 2, kmh * 5 // 18 + 5, kmh * 5 // 18 - 5)],
                   'easy', "Multiply by 5/18.")
    if kind == 1:
        ms = rng.choice([10, 12, 15, 20, 25, 30])
        length = rng.randrange(100, 400, 20)
        t = F(length, ms)
        return mcq(rng, f"A train {length} m long runs at {ms * 18 // 5} km/h. Time taken to cross a pole is ___ seconds.", fmt(t),
                   near(rng, t), 'easy', f"{ms * 18 // 5} km/h = {ms} m/s; {length}/{ms} = {fmt(t)} s.")
    if kind == 2:
        ms = rng.choice([10, 15, 20, 25])
        tl, pl = rng.randrange(100, 300, 25), rng.randrange(100, 400, 25)
        t = F(tl + pl, ms)
        return mcq(rng, f"A train {tl} m long running at {ms * 18 // 5} km/h crosses a platform {pl} m long in ___ seconds.", fmt(t),
                   near(rng, t) + [fmt(F(tl, ms))], 'medium', f"Distance = {tl} + {pl} = {tl + pl} m at {ms} m/s.")
    if kind == 3:
        b, s = rng.choice([(10, 2), (12, 3), (15, 5), (8, 2), (20, 4), (9, 3), (14, 4)])
        d = rng.choice([24, 36, 48, 60, 72, 96])
        t = F(d, b - s) + F(d, b + s)
        return mcq(rng, f"A boat goes at {b} km/h in still water; the stream flows at {s} km/h. Time to go {d} km upstream and come back is ___ hours.",
                   fmt(t), near(rng, t, spread=1), 'hard', f"{d}/{b - s} + {d}/{b + s} = {fmt(t)} h.")
    v1, v2 = rng.choice([(40, 60), (30, 50), (45, 55), (60, 80), (36, 54)])
    avg = F(2 * v1 * v2, v1 + v2)
    return mcq(rng, f"A car goes from A to B at {v1} km/h and returns at {v2} km/h. Its average speed for the whole journey is ___ km/h.",
               fmt(avg), [fmt(F(v1 + v2, 2))] + near(rng, avg), 'medium', f"2×{v1}×{v2}/({v1}+{v2}) = {fmt(avg)}.")


@generator('quant.number_system', S, 'Number System, HCF & LCM')
def number_system(rng):
    kind = rng.randrange(5)
    if kind == 0:
        base, exp = rng.randint(2, 99), rng.randint(20, 300)
        u = pow(base, exp, 10)
        return mcq(rng, f"The unit digit of {base}^{exp} is ___.", str(u), [str(d) for d in rng.sample([d for d in range(10) if d != u], 5)],
                   'medium', f"Unit digits repeat in cycles of 4; {base % 10}^{exp} ends in {u}.")
    if kind == 1:
        nums = rng.sample([12, 15, 18, 20, 24, 30, 36, 40, 45, 48, 60, 72, 84, 90, 96], 3)
        l = math.lcm(*nums)
        return mcq(rng, f"The LCM of {', '.join(map(str, nums))} is ___.", str(l), [str(v) for v in (l * 2, l // 2 if l % 2 == 0 else l + 6, math.gcd(*nums), l + 12)],
                   'easy', f"LCM = {l}.")
    if kind == 2:
        g = rng.choice([6, 8, 9, 12, 14, 15, 16, 18, 21, 24])
        a, b = g * rng.choice([2, 3, 5, 7]), g * rng.choice([4, 9, 11, 13])
        h = math.gcd(a, b)
        return mcq(rng, f"The HCF of {a} and {b} is ___.", str(h), [str(v) for v in (h * 2, h // 2 if h % 2 == 0 else h + 3, h + 1, math.lcm(a, b))],
                   'easy', f"HCF({a}, {b}) = {h}.")
    if kind == 3:
        n = rng.choice([36, 48, 60, 72, 84, 90, 96, 100, 120, 144, 180, 210, 240, 360])
        count = sum(1 for d in range(1, n + 1) if n % d == 0)
        return mcq(rng, f"How many factors (divisors) does {n} have?", str(count), [str(v) for v in near(rng, count, spread=1)],
                   'medium', f"From the prime factorisation of {n}, (e₁+1)(e₂+1)… = {count}.")
    n, d = rng.randint(1000, 99999), rng.choice([7, 9, 11, 13, 6, 8, 12])
    r = n % d
    return mcq(rng, f"What is the remainder when {n} is divided by {d}?", str(r), [str(v) for v in rng.sample([x for x in range(d) if x != r], 3)],
               'easy', f"{n} = {d}×{n // d} + {r}.")


@generator('quant.simplification', S, 'Simplification & Approximation')
def simplification(rng):
    kind = rng.randrange(3)
    if kind == 0:
        a, b, c, d = rng.randint(10, 99), rng.randint(2, 12), rng.randint(2, 20), rng.randint(5, 60)
        v = a + b * c - d
        return mcq(rng, f"Simplify: {a} + {b} × {c} − {d}", str(v), [str((a + b) * c - d), str(v + 10), str(v - b), str(a + b * (c - d))],
                   'easy', f"BODMAS: {b}×{c} = {b * c}; {a} + {b * c} − {d} = {v}.")
    if kind == 1:
        a, b = rng.randint(11, 40), rng.randint(11, 40)
        v = a * a + b * b
        return mcq(rng, f"{a}² + {b}² = ?", str(v), [str(v + 10), str((a + b) ** 2), str(v - 20), str(v + 1)], 'easy', f"{a * a} + {b * b} = {v}.")
    p, base = rng.choice([12.5, 33.33, 16.66, 37.5, 62.5, 87.5]), rng.randrange(240, 2400, 24)
    exact = {12.5: F(1, 8), 33.33: F(1, 3), 16.66: F(1, 6), 37.5: F(3, 8), 62.5: F(5, 8), 87.5: F(7, 8)}[p]
    v = exact * base
    return mcq(rng, f"{p}% of {base} ≈ ?", fmt(round(v)), [fmt(round(v) + 10), fmt(round(v) - 12), fmt(round(v * F(6, 5))), fmt(round(v) + 25)],
               'medium', f"{p}% ≈ {frac_str(exact)}, so ≈ {fmt(round(v))}.")


@generator('quant.mensuration', S, 'Mensuration (2D & 3D)')
def mensuration(rng):
    kind = rng.randrange(6)
    if kind == 0:
        r = 7 * rng.randint(1, 6)
        area = F(22, 7) * r * r
        return mcq(rng, f"The area of a circle of radius {r} cm is ___ cm². (π = 22/7)", fmt(area),
                   [fmt(F(44, 7) * r), fmt(area * 2), fmt(area + 22), fmt(F(22, 7) * r)], 'easy', f"πr² = 22/7 × {r}² = {fmt(area)}.")
    if kind == 1:
        l, b = rng.randint(5, 40), rng.randint(3, 30)
        return mcq(rng, f"A rectangle is {l} m long and {b} m wide. Its perimeter is ___ m.", str(2 * (l + b)),
                   [str(l * b), str(l + b), str(2 * (l + b) + 4), str(4 * l)], 'easy', f"2({l} + {b}) = {2 * (l + b)} m.")
    if kind == 2:
        r, h = 7 * rng.randint(1, 3), rng.randint(5, 20)
        v = F(22, 7) * r * r * h
        return mcq(rng, f"The volume of a cylinder of radius {r} cm and height {h} cm is ___ cm³. (π = 22/7)", fmt(v),
                   [fmt(v / 3), fmt(2 * F(22, 7) * r * h), fmt(v * 2), fmt(v + 154)], 'medium', f"πr²h = {fmt(v)}.")
    if kind == 3:
        a = rng.randint(3, 15)
        return mcq(rng, f"The total surface area of a cube of edge {a} cm is ___ cm².", str(6 * a * a),
                   [str(a ** 3), str(4 * a * a), str(6 * a), str(12 * a)], 'easy', f"6a² = {6 * a * a}.")
    if kind == 4:
        a, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (7, 24, 25)])
        return mcq(rng, f"The area of a right triangle with legs {a} cm and {b} cm is ___ cm², and its hypotenuse is ___ cm.",
                   f"{fmt(F(a * b, 2))}, {c}", [f"{a * b}, {c}", f"{fmt(F(a * b, 2))}, {c + 1}", f"{a + b}, {c}", f"{fmt(F(a * b, 2))}, {a + b}"],
                   'medium', f"Area = ½ab = {fmt(F(a * b, 2))}; hypotenuse = √({a}² + {b}²) = {c}.")
    r = 3 * rng.randint(1, 5)
    v = F(4, 3) * F(22, 7) * r ** 3
    return mcq(rng, f"The volume of a sphere of radius {r} cm is ___ cm³. (π = 22/7)", fmt(v),
               [fmt(4 * F(22, 7) * r * r), fmt(v * 2), fmt(v / 2), fmt(F(22, 7) * r ** 3)], 'medium', f"4/3 πr³ = {fmt(v)}.")


@generator('quant.algebra', S, 'Algebra')
def algebra(rng):
    kind = rng.randrange(4)
    if kind == 0:
        k = rng.randint(3, 12)
        return mcq(rng, f"If x + 1/x = {k}, then x² + 1/x² = ?", str(k * k - 2), [str(k * k), str(k * k + 2), str(k * k - 1), str(2 * k)],
                   'medium', f"(x + 1/x)² − 2 = {k * k} − 2 = {k * k - 2}.")
    if kind == 1:
        a, b = rng.randint(2, 9), rng.randint(1, 9)
        return mcq(rng, f"If a + b = {a + b} and ab = {a * b}, then a² + b² = ?", str(a * a + b * b),
                   [str((a + b) ** 2), str(a * a + b * b + a * b), str((a + b) ** 2 + 2 * a * b), str(a * a + b * b - 2)],
                   'medium', f"(a + b)² − 2ab = {(a + b) ** 2} − {2 * a * b} = {a * a + b * b}.")
    if kind == 2:
        x = rng.randint(-9, 15)
        a, b = rng.randint(2, 9), rng.randint(-20, 20)
        c = a * x + b
        sign = '+' if b >= 0 else '−'
        return mcq(rng, f"Solve: {a}x {sign} {abs(b)} = {c}", f"x = {x}", [f"x = {v}" for v in (x + 1, x - 2, -x if x else 3, x + 3)],
                   'easy', f"{a}x = {c - b} → x = {x}.")
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    return mcq(rng, f"If a − b = {a - b if a >= b else b - a} and ab = {a * b}, find a³ − b³ (take a ≥ b).",
               str(abs(a ** 3 - b ** 3)), [str(abs(a - b) ** 3), str(abs(a ** 3 - b ** 3) + 9), str(a ** 3 + b ** 3), str(abs(a - b) * a * b)],
               'hard', "a³ − b³ = (a − b)³ + 3ab(a − b).")


TRIG = {0: ('0', '1', '0'), 30: ('1/2', '√3/2', '1/√3'), 45: ('1/√2', '1/√2', '1'), 60: ('√3/2', '1/2', '√3'), 90: ('1', '0', 'not defined')}


@generator('quant.trigonometry', S, 'Trigonometry, Heights & Distances')
def trigonometry(rng):
    kind = rng.randrange(3)
    if kind == 0:
        ang = rng.choice([0, 30, 45, 60, 90])
        fn = rng.randrange(3)
        name = ('sin', 'cos', 'tan')[fn]
        val = TRIG[ang][fn]
        wrong = list({v for t in TRIG.values() for v in t} - {val})
        rng.shuffle(wrong)
        return mcq(rng, f"The value of {name} {ang}° is ___.", val, wrong, 'easy', f"Standard value: {name} {ang}° = {val}.")
    if kind == 1:
        h = rng.choice([10, 15, 20, 25, 30, 50, 100])
        ang = rng.choice([30, 45, 60])
        dist = {30: f"{h}√3", 45: f"{h}", 60: f"{h}/√3"}[ang]
        return mcq(rng, f"The angle of elevation of the top of a {h} m tower from a point on the ground is {ang}°. The distance of the point from the foot of the tower is ___ m.",
                   dist, [f"{h}√3", f"{h}", f"{h}/√3", f"{2 * h}", f"{h}√2"], 'medium', f"tan {ang}° = {h}/d.")
    t = rng.choice(['sin²θ + cos²θ', 'sec²θ − tan²θ', 'cosec²θ − cot²θ'])
    return mcq(rng, f"{t} = ?", '1', ['0', '2', '−1', 'tan θ'], 'easy', "Pythagorean identity.")


@generator('quant.mixture', S, 'Mixture, Alligation & Partnership')
def mixture(rng):
    kind = rng.randrange(2)
    if kind == 0:
        c1, c2 = rng.choice([(20, 30), (40, 60), (15, 25), (50, 70), (10, 30)])
        m = rng.randint(c1 + 1, c2 - 1)
        r1, r2 = c2 - m, m - c1
        g = math.gcd(r1, r2)
        return mcq(rng, f"In what ratio must rice at ₹{c1}/kg be mixed with rice at ₹{c2}/kg to get a mixture worth ₹{m}/kg?",
                   f"{r1 // g} : {r2 // g}", [f"{r2 // g} : {r1 // g}" if r1 != r2 else "2 : 1", f"{c1} : {c2}", f"{r1 // g + 1} : {r2 // g}", "1 : 3"],
                   'medium', f"Alligation: ({c2} − {m}) : ({m} − {c1}) = {r1 // g} : {r2 // g}.")
    a, b = rng.randrange(10000, 60000, 5000), rng.randrange(10000, 60000, 5000)
    ta, tb = 12, rng.choice([6, 8, 9, 10])
    profit = rng.randrange(10000, 50000, 1000)
    sa, sb = a * ta, b * tb
    share_b = F(profit * sb, sa + sb)
    return mcq(rng, f"A invests {inr(a)} for 12 months and B invests {inr(b)} for {tb} months. Out of a profit of {inr(profit)}, B's share is ___.",
               inr(share_b), [inr(F(profit * b, a + b)), inr(share_b + 500), inr(profit - share_b), inr(share_b - 300)], 'hard',
               f"Ratio = {a}×12 : {b}×{tb}; B gets {inr(share_b)}.")


@generator('quant.probability', S, 'Probability, Permutation & Combination')
def probability(rng):
    kind = rng.randrange(5)
    if kind == 0:
        s = rng.choice([7, 8, 6, 9, 10, 5, 4, 11, 12])
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
        p = F(ways, 36)
        return mcq(rng, f"Two dice are thrown. The probability that the sum is {s} is ___.", frac_str(p),
                   [frac_str(F(ways + 1, 36)), frac_str(F(1, 6)) if p != F(1, 6) else '1/9', frac_str(F(ways, 12)), '1/2'],
                   'medium', f"{ways} favourable outcomes out of 36.")
    if kind == 1:
        what, count = rng.choice([('a king', 4), ('a heart', 13), ('a red card', 26), ('a face card', 12), ('an ace of spades', 1)])
        p = F(count, 52)
        return mcq(rng, f"A card is drawn from a well-shuffled pack of 52. The probability of getting {what} is ___.", frac_str(p),
                   [frac_str(F(count + 1, 52)), '1/4', '1/13', '1/2', '3/13'], 'easy', f"{count}/52 = {frac_str(p)}.")
    if kind == 2:
        n, r = rng.randint(5, 10), rng.randint(2, 4)
        v = math.comb(n, r)
        return mcq(rng, f"In how many ways can a committee of {r} be chosen from {n} people?", str(v),
                   [str(math.perm(n, r)), str(v + n), str(n * r), str(v * 2)], 'medium', f"ⁿCᵣ = {n}C{r} = {v}.")
    if kind == 3:
        word = rng.choice(['MANGO', 'TABLE', 'PLANT', 'CHAIR', 'WORLD', 'FRIEND', 'NUMBER', 'GARDEN'])
        v = math.factorial(len(word))
        return mcq(rng, f"In how many ways can the letters of the word '{word}' be arranged?", str(v),
                   [str(v // 2), str(len(word) ** 2), str(v * 2), str(math.factorial(len(word) - 1))], 'easy',
                   f"All {len(word)} letters are different: {len(word)}! = {v}.")
    c = rng.randint(2, 5)
    p = F(1, 2 ** c)
    return mcq(rng, f"{c} fair coins are tossed. The probability of getting all heads is ___.", frac_str(p),
               [frac_str(F(1, 2 ** c + 1)), '1/2', frac_str(F(c, 2 ** c)), frac_str(F(1, c))], 'easy', f"(1/2)^{c} = {frac_str(p)}.")


@generator('quant.di', 'DI1', 'Data Interpretation')
def data_interpretation(rng):
    years = list(range(2020, 2026))
    company = rng.choice(['Company X', 'a factory', 'a bank branch', 'a school', 'a state'])
    unit = rng.choice([('production', 'thousand units'), ('sales', 'lakh ₹'), ('admissions', 'students'), ('exports', 'crore ₹')])
    values = [rng.randrange(120, 600, 10) for _ in years]
    table = "\n".join(f"{y}: {v}" for y, v in zip(years, values))
    head = f"The table shows the {unit[0]} ({unit[1]}) of {company}:\n{table}\n\n"
    kind = rng.randrange(4)
    if kind == 0:
        avg = F(sum(values), len(values))
        return mcq(rng, head + "What is the average over the six years?", fmt(avg), near(rng, avg, spread=5), 'medium', f"Sum {sum(values)} ÷ 6 = {fmt(avg)}.")
    if kind == 1:
        i = rng.randrange(1, len(years))
        ch = F(values[i] - values[i - 1], values[i - 1]) * 100
        word = 'increase' if ch >= 0 else 'decrease'
        return mcq(rng, head + f"What is the percentage {word} from {years[i - 1]} to {years[i]}?", f"{float(abs(ch)):.1f}%",
                   [f"{float(abs(ch)) + d:.1f}%" for d in (2.5, -1.8, 4.2, 6.0) if float(abs(ch)) + d > 0], 'hard',
                   f"|{values[i]} − {values[i - 1]}| / {values[i - 1]} × 100 = {float(abs(ch)):.1f}%.")
    if kind == 2:
        hi = years[values.index(max(values))]
        return mcq(rng, head + "In which year was it the highest?", str(hi), [str(y) for y in years if y != hi], 'easy', f"Maximum {max(values)} in {hi}.")
    i, j = rng.sample(range(len(years)), 2)
    r = F(values[i], values[j])
    return mcq(rng, head + f"What is the ratio of {years[i]} to {years[j]}?", f"{r.numerator} : {r.denominator}",
               [f"{r.denominator} : {r.numerator}", f"{r.numerator + 1} : {r.denominator}", f"{r.numerator} : {r.denominator + 1}", "1 : 1"],
               'medium', f"{values[i]} : {values[j]} = {r.numerator} : {r.denominator}.")


@generator('quant.quadratic', S, 'Quadratic Equations (Banking)')
def quadratic(rng):
    def eq(roots, var):
        s, p = sum(roots), roots[0] * roots[1]
        b = f"− {s}{var}" if s > 0 else (f"+ {-s}{var}" if s < 0 else '')
        c = f"+ {p}" if p > 0 else (f"− {-p}" if p < 0 else '')
        return f"{var}² {b} {c} = 0".replace('  ', ' ')

    xr = rng.sample(range(-9, 10), 2)
    yr = rng.sample(range(-9, 10), 2)
    if min(xr) > max(yr):
        rel = 'x > y'
    elif min(xr) >= max(yr):
        rel = 'x ≥ y'
    elif max(xr) < min(yr):
        rel = 'x < y'
    elif max(xr) <= min(yr):
        rel = 'x ≤ y'
    else:
        rel = 'Relationship cannot be established'
    opts = ['x > y', 'x < y', 'x ≥ y', 'x ≤ y', 'x = y or relationship cannot be established', 'Relationship cannot be established']
    if rel == 'Relationship cannot be established':
        opts = [o for o in opts if o != 'x = y or relationship cannot be established']
    return mcq(rng, f"Solve and find the relation between x and y:\nI. {eq(xr, 'x')}\nII. {eq(yr, 'y')}", rel, [o for o in opts if o != rel],
               'hard', f"x = {xr[0]}, {xr[1]}; y = {yr[0]}, {yr[1]} → {rel}.")


def _quant_numeric(rng):
    """Integer-answer versions for numerical-answer sections (JEE / GATE / CAT TITA)."""
    q = rng.choice([percentage, interest, time_work, number_system, average])(rng)
    if not q.options:
        return q
    ans = q.options[q.answer].replace('₹', '').replace(',', '').replace('%', '').split()[0]
    try:
        float(ans)
    except ValueError:
        return numerical("Find the remainder when 2^100 is divided by 7.", 2, 'hard', "2³ ≡ 1 (mod 7); 2^100 = 2^99 × 2 ≡ 2.")
    return numerical(q.text + "\n(Type the answer – numbers only.)", float(ans), q.difficulty, q.explanation)


register('quant.tita', S, 'Quant – Type In The Answer', gen=_quant_numeric)
