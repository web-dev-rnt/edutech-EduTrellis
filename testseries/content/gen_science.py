"""Physics and chemistry numericals (computed) plus physics, chemistry and biology fact tables (NEET, JEE, boards)."""
import math
from fractions import Fraction as F

from .core import fmt, generator, mcq, near, numerical, register, table_topics

PHY, CHE, BIO = 'PHY1', 'CHE1', 'BIO1'


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


# ------------------------------------------------------------------ physics numericals

@generator('physics.kinematics', PHY, 'Motion & Kinematics')
def kinematics(rng):
    kind = rng.randrange(4)
    u, a, t = rng.randint(0, 20), rng.randint(1, 6), rng.randint(2, 10)
    if kind == 0:
        v = u + a * t
        return mcq(rng, f"A body starts with velocity {u} m/s and accelerates uniformly at {a} m/s² for {t} s. Its final velocity is ___.",
                   f"{v} m/s", [f"{x} m/s" for x in (u * t + a, a * t, v + a, u + a * t * t)], 'easy', f"v = u + at = {u} + {a}×{t} = {v} m/s.")
    if kind == 1:
        s = F(u * t) + F(a * t * t, 2)
        return mcq(rng, f"A car moving at {u} m/s accelerates at {a} m/s² for {t} s. The distance covered is ___.",
                   f"{fmt(s)} m", [f"{fmt(x)} m" for x in (u * t + a * t * t, u * t, s + a, F(a * t * t, 2))], 'medium',
                   f"s = ut + ½at² = {u}×{t} + ½×{a}×{t}² = {fmt(s)} m.")
    if kind == 2:
        h = rng.choice([5, 20, 45, 80, 125, 180])
        tt = int(math.sqrt(2 * h / 10))
        return mcq(rng, f"A stone is dropped from a height of {h} m. Taking g = 10 m/s², the time taken to reach the ground is ___.",
                   f"{tt} s", [f"{x} s" for x in (tt + 1, tt * 2, max(1, tt - 1) if tt > 1 else 3, h // 10)], 'medium',
                   f"h = ½gt² → t = √(2h/g) = {tt} s.")
    v = rng.choice([10, 20, 30, 40])
    hmax = F(v * v, 20)
    return mcq(rng, f"A ball is thrown vertically upward at {v} m/s. Taking g = 10 m/s², the maximum height reached is ___.",
               f"{fmt(hmax)} m", [f"{fmt(x)} m" for x in (hmax * 2, F(v, 10), hmax / 2, v * v)], 'medium', f"H = u²/2g = {fmt(hmax)} m.")


@generator('physics.force_energy', PHY, 'Force, Work, Energy & Power')
def force_energy(rng):
    kind = rng.randrange(5)
    m = rng.randint(2, 20)
    if kind == 0:
        a = rng.randint(2, 10)
        return mcq(rng, f"A force acts on a {m} kg mass and produces an acceleration of {a} m/s². The force is ___.", f"{m * a} N",
                   [f"{x} N" for x in (m + a, F(m, a), m * a * 2, m * a + 10)], 'easy', f"F = ma = {m * a} N.")
    if kind == 1:
        v = rng.randint(2, 20)
        ke = F(m * v * v, 2)
        return mcq(rng, f"The kinetic energy of a {m} kg body moving at {v} m/s is ___.", f"{fmt(ke)} J",
                   [f"{fmt(x)} J" for x in (m * v * v, m * v, ke / 2, ke + m)], 'easy', f"KE = ½mv² = {fmt(ke)} J.")
    if kind == 2:
        h = rng.randint(2, 30)
        return mcq(rng, f"The potential energy of a {m} kg body at a height of {h} m (g = 10 m/s²) is ___.", f"{m * 10 * h} J",
                   [f"{x} J" for x in (m * h, m * 10 * h // 2, m * 9 * h, m * 10 * h + 100)], 'easy', f"PE = mgh = {m * 10 * h} J.")
    if kind == 3:
        w, t = rng.randrange(200, 5000, 100), rng.choice([2, 4, 5, 10, 20, 25])
        p = F(w, t)
        return mcq(rng, f"A machine does {w} J of work in {t} s. Its power is ___.", f"{fmt(p)} W",
                   [f"{fmt(x)} W" for x in (w * t, p * 2, p + 10, p / 2)], 'easy', f"P = W/t = {fmt(p)} W.")
    v = rng.randint(2, 15)
    return mcq(rng, f"The momentum of a {m} kg body moving at {v} m/s is ___.", f"{m * v} kg·m/s",
               [f"{x} kg·m/s" for x in (m + v, F(m * v * v, 2), m * v * 2, m * v + 5)], 'easy', f"p = mv = {m * v} kg·m/s.")


@generator('physics.electricity', PHY, 'Current Electricity')
def electricity(rng):
    kind = rng.randrange(5)
    if kind == 0:
        i, r = rng.choice([0.5, 1, 2, 3, 4, 5]), rng.choice([2, 4, 5, 10, 12, 20, 25])
        v = F(i).limit_denominator() * r
        return mcq(rng, f"A current of {fmt(i)} A flows through a {r} Ω resistor. The potential difference across it is ___.",
                   f"{fmt(v)} V", [f"{fmt(x)} V" for x in (F(r) / F(i).limit_denominator(), v * 2, v + 2, F(i).limit_denominator() + r)],
                   'easy', f"V = IR = {fmt(v)} V.")
    if kind == 1:
        rs = [rng.choice([2, 3, 4, 6, 8, 10, 12]) for _ in range(rng.randint(2, 3))]
        return mcq(rng, f"Resistors of {', '.join(map(str, rs))} Ω are connected in series. The equivalent resistance is ___.",
                   f"{sum(rs)} Ω", [f"{fmt(x)} Ω" for x in (1 / sum(F(1, r) for r in rs), sum(rs) + 2, max(rs), sum(rs) * 2)], 'easy',
                   f"Series: R = {' + '.join(map(str, rs))} = {sum(rs)} Ω.")
    if kind == 2:
        a, b = rng.choice([(2, 2), (3, 6), (4, 4), (6, 12), (10, 15), (4, 12), (12, 24), (20, 30)])
        r = F(a * b, a + b)
        return mcq(rng, f"Resistors of {a} Ω and {b} Ω are connected in parallel. The equivalent resistance is ___.",
                   f"{fmt(r)} Ω", [f"{fmt(x)} Ω" for x in (a + b, r * 2, F(a + b, 2), r + 1)], 'medium', f"R = ab/(a + b) = {fmt(r)} Ω.")
    if kind == 3:
        p, hours, days = rng.choice([100, 200, 500, 1000, 1500, 2000]), rng.randint(2, 10), rng.choice([1, 10, 30])
        units = F(p * hours * days, 1000)
        return mcq(rng, f"An appliance of {p} W is used {hours} hours a day for {days} day(s). Energy consumed is ___.",
                   f"{fmt(units)} kWh", [f"{fmt(x)} kWh" for x in (units * 10, units / 2, F(p * hours, 1000), units + 1)], 'medium',
                   f"E = {p} × {hours} × {days} / 1000 = {fmt(units)} kWh (units).")
    v, r = rng.choice([6, 12, 24, 220, 230]), rng.choice([2, 4, 6, 10, 20, 50, 100])
    p = F(v * v, r)
    return mcq(rng, f"A {r} Ω heater is connected to a {v} V supply. The power consumed is ___.", f"{fmt(p)} W",
               [f"{fmt(x)} W" for x in (F(v, r), v * r, p / 2, p * 2)], 'medium', f"P = V²/R = {fmt(p)} W.")


@generator('physics.optics_waves', PHY, 'Light, Sound & Waves')
def optics_waves(rng):
    kind = rng.randrange(4)
    if kind == 0:
        f = rng.choice([10, 15, 20, 25, 30, 40])
        u = -rng.choice([2, 3, 4]) * f
        v = F(1) / (F(1, f) + F(1, u))   # lens: 1/v − 1/u = 1/f
        return mcq(rng, f"An object is placed {abs(u)} cm in front of a convex lens of focal length {f} cm. The image distance is ___.",
                   f"{fmt(v)} cm", [f"{fmt(x)} cm" for x in (-v, v * 2, F(abs(u)), v + 5)], 'hard', f"1/v = 1/f + 1/u = 1/{f} − 1/{abs(u)} → v = {fmt(v)} cm.")
    if kind == 1:
        f = rng.choice([0.25, 0.5, 1, 2, 0.2, 0.4])
        power = F(1) / F(f).limit_denominator()
        return mcq(rng, f"The power of a convex lens of focal length {fmt(f * 100)} cm is ___.", f"+{fmt(power)} D",
                   [f"{s}{fmt(x)} D" for s, x in (('−', power), ('+', power * 2), ('+', F(f).limit_denominator() * 100), ('+', power / 2))],
                   'medium', f"P = 1/f(m) = 1/{fmt(f)} = +{fmt(power)} D.")
    if kind == 2:
        fr, lam = rng.choice([100, 200, 256, 340, 500, 680, 1000]), None
        v = 340
        lam = F(v, fr)
        return mcq(rng, f"A sound wave of frequency {fr} Hz travels at {v} m/s. Its wavelength is ___.", f"{fmt(lam)} m",
                   [f"{fmt(x)} m" for x in (F(fr, v), lam * 2, lam / 2, v * fr)], 'medium', f"λ = v/f = {fmt(lam)} m.")
    d = rng.choice([170, 340, 510, 680, 850])
    t = F(2 * d, 340)
    return mcq(rng, f"A person hears the echo of a shout from a cliff {d} m away. If sound travels at 340 m/s, the echo is heard after ___.",
               f"{fmt(t)} s", [f"{fmt(x)} s" for x in (t / 2, t * 2, t + 1, F(d, 100))], 'medium', f"t = 2d/v = {fmt(t)} s.")


@generator('physics.heat_matter', PHY, 'Heat, Pressure & Properties of Matter')
def heat_matter(rng):
    kind = rng.randrange(4)
    if kind == 0:
        m, dt = rng.choice([0.5, 1, 2, 5]), rng.choice([10, 20, 25, 40, 50])
        q = int(m * 4200 * dt)
        return mcq(rng, f"Heat needed to raise the temperature of {fmt(m)} kg of water by {dt} °C (c = 4200 J/kg°C) is ___.",
                   f"{q:,} J", [f"{x:,} J" for x in (q * 2, q // 2, int(m * 4200), q + 4200)], 'medium', f"Q = mcΔT = {q:,} J.")
    if kind == 1:
        m, v = rng.randint(2, 50), rng.choice([2, 4, 5, 10])
        return mcq(rng, f"A body of mass {m * v} g has a volume of {v} cm³. Its density is ___.", f"{m} g/cm³",
                   [f"{fmt(x)} g/cm³" for x in (m * v * v, F(v, m * v), m + 1, m * 2)], 'easy', f"ρ = m/V = {m} g/cm³.")
    if kind == 2:
        f_, a = rng.choice([100, 200, 500, 1000, 2000]), rng.choice([0.5, 2, 4, 5, 10])
        p = F(f_) / F(a).limit_denominator()
        return mcq(rng, f"A force of {f_} N acts on an area of {fmt(a)} m². The pressure is ___.", f"{fmt(p)} Pa",
                   [f"{fmt(x)} Pa" for x in (f_ * F(a).limit_denominator(), p * 2, p / 2, p + 50)], 'easy', f"P = F/A = {fmt(p)} Pa.")
    c = rng.choice([-40, 0, 25, 37, 100, 50, 20])
    fah = F(9, 5) * c + 32
    return mcq(rng, f"{c} °C on the Fahrenheit scale is ___.", f"{fmt(fah)} °F", [f"{fmt(x)} °F" for x in (fah + 10, c + 32, fah - 18, c * 2)],
               'easy', f"F = 9C/5 + 32 = {fmt(fah)} °F.")


PHYSICS_FACTS = rows("""
Force|Newton
Work|Joule
Power|Watt
Pressure|Pascal
Frequency|Hertz
Electric charge|Coulomb
Electric potential|Volt
Resistance|Ohm
Capacitance|Farad
Inductance|Henry
Magnetic flux|Weber
Magnetic flux density|Tesla
Luminous intensity|Candela
Amount of substance|Mole
Thermodynamic temperature|Kelvin
Radioactivity (activity)|Becquerel
Power of a lens|Dioptre
""")
table_topics('physics.units', PHY, 'Units & Measurements', PHYSICS_FACTS, [
    ("The SI unit of {a} is the ___.", 'b', "{a} is measured in {b}s."),
    ("The {b} is the SI unit of ___.", 'a', "{b}: unit of {a}."),
], difficulty='easy')

PHYSICS_CONCEPTS = [
    ("The slope of a displacement–time graph gives ___.", ['Velocity', 'Acceleration', 'Distance', 'Force'], 'easy', "v = ds/dt."),
    ("The area under a velocity–time graph gives ___.", ['Displacement', 'Acceleration', 'Speed', 'Momentum'], 'easy', "∫v dt."),
    ("Newton's third law states that ___.", ['Every action has an equal and opposite reaction', 'F = ma', 'A body stays at rest unless acted on', 'Momentum is always zero'], 'easy', "Action–reaction pairs."),
    ("The value of g at the centre of the Earth is ___.", ['Zero', '9.8 m/s²', 'Maximum', 'Infinite'], 'medium', "g decreases linearly with depth."),
    ("The escape velocity from Earth's surface is about ___.", ['11.2 km/s', '7.9 km/s', '3 km/s', '25 km/s'], 'easy', "√(2gR)."),
    ("Which quantity is conserved in an elastic collision but not in an inelastic one?", ['Kinetic energy', 'Momentum', 'Mass', 'Charge'], 'medium', "Momentum is conserved in both."),
    ("The time period of a simple pendulum depends on ___.", ['Its length and g', 'The mass of the bob', 'The amplitude (for small swings)', 'The material of the bob'], 'medium', "T = 2π√(l/g)."),
    ("Bernoulli's principle is based on the conservation of ___.", ['Energy', 'Mass', 'Momentum', 'Charge'], 'medium', "P + ½ρv² + ρgh = constant."),
    ("Total internal reflection is the principle behind ___.", ['Optical fibres', 'Microscopes', 'Plane mirrors', 'Prisms only'], 'easy', "Light trapped inside the fibre."),
    ("The splitting of white light into colours is called ___.", ['Dispersion', 'Reflection', 'Diffraction', 'Polarisation'], 'easy', "By a prism."),
    ("The blue colour of the sky is due to ___ of light.", ['Scattering', 'Reflection', 'Refraction', 'Dispersion'], 'easy', "Rayleigh scattering ∝ 1/λ⁴."),
    ("A person with myopia uses a ___ lens.", ['Concave', 'Convex', 'Cylindrical', 'Bifocal'], 'easy', "Diverging lens."),
    ("Ultrasound has frequencies above ___.", ['20 kHz', '20 Hz', '2 kHz', '200 Hz'], 'easy', "Human hearing: 20 Hz – 20 kHz."),
    ("The device that converts mechanical energy into electrical energy is the ___.", ['Generator', 'Motor', 'Transformer', 'Battery'], 'easy', "Electromagnetic induction."),
    ("A transformer works on ___.", ['AC only', 'DC only', 'Both AC and DC', 'Neither'], 'easy', "It needs a changing flux."),
    ("Fleming's left-hand rule gives the direction of ___.", ['Force on a current-carrying conductor', 'Induced current', 'Magnetic field', 'Electric field'], 'medium', "Used for motors."),
    ("The charge on an electron is ___.", ['−1.6 × 10⁻¹⁹ C', '+1.6 × 10⁻¹⁹ C', '9.1 × 10⁻³¹ C', '−1 C'], 'easy', "Elementary charge."),
    ("In a semiconductor, the majority carriers in an n-type material are ___.", ['Electrons', 'Holes', 'Protons', 'Ions'], 'medium', "Doped with pentavalent atoms."),
    ("The photoelectric effect was explained by ___.", ['Albert Einstein', 'Max Planck', 'Niels Bohr', 'J. J. Thomson'], 'easy', "Nobel Prize 1921."),
    ("Nuclear power plants produce energy by ___.", ['Nuclear fission', 'Nuclear fusion', 'Combustion', 'Radioactive decay only'], 'easy', "Splitting heavy nuclei."),
    ("The energy of the Sun is produced by ___.", ['Nuclear fusion', 'Nuclear fission', 'Combustion', 'Chemical reactions'], 'easy', "Hydrogen to helium."),
    ("Which logic gate gives output 1 only when all inputs are 1?", ['AND', 'OR', 'NOR', 'XOR'], 'easy', "AND gate."),
    ("The dimensional formula of work is ___.", ['[ML²T⁻²]', '[MLT⁻²]', '[ML²T⁻³]', '[MLT⁻¹]'], 'medium', "Work = force × distance."),
    ("Kepler's second law is a consequence of conservation of ___.", ['Angular momentum', 'Linear momentum', 'Energy', 'Mass'], 'hard', "Equal areas in equal times."),
    ("The efficiency of a Carnot engine depends on ___.", ['Temperatures of the source and sink', 'The working substance', 'The size of the engine', 'The fuel used'], 'medium', "η = 1 − T₂/T₁."),
]
register('physics.concepts', PHY, 'Physics Concepts', rows=PHYSICS_CONCEPTS)


def _physics_numeric(rng):
    kind = rng.randrange(3)
    if kind == 0:
        u, a, t = rng.randint(0, 20), rng.randint(1, 6), rng.randint(2, 10)
        return numerical(f"A body starts at {u} m/s with uniform acceleration {a} m/s². Find its velocity (in m/s) after {t} s.", u + a * t, 'easy', "v = u + at.")
    if kind == 1:
        a, b = rng.choice([(3, 6), (6, 12), (4, 12), (12, 24), (10, 15), (20, 30)])
        return numerical(f"Find the equivalent resistance (in Ω) of {a} Ω and {b} Ω in parallel.", F(a * b, a + b), 'medium', "ab/(a + b).")
    m, v = rng.randint(2, 10), rng.choice([2, 4, 6, 10])
    return numerical(f"Find the kinetic energy (in J) of a {m} kg body moving at {v} m/s.", F(m * v * v, 2), 'easy', "½mv².")


for key in ('physics.kinematics', 'physics.electricity', 'physics.force_energy'):
    register(key, PHY, '', numeric=_physics_numeric)

# ------------------------------------------------------------------ chemistry

MASS = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'Al': 27, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40, 'Fe': 56, 'Cu': 63.5}
COMPOUNDS = [
    ('H₂O', {'H': 2, 'O': 1}), ('CO₂', {'C': 1, 'O': 2}), ('NaCl', {'Na': 1, 'Cl': 1}), ('NH₃', {'N': 1, 'H': 3}),
    ('CH₄', {'C': 1, 'H': 4}), ('H₂SO₄', {'H': 2, 'S': 1, 'O': 4}), ('CaCO₃', {'Ca': 1, 'C': 1, 'O': 3}),
    ('NaOH', {'Na': 1, 'O': 1, 'H': 1}), ('HCl', {'H': 1, 'Cl': 1}), ('C₆H₁₂O₆', {'C': 6, 'H': 12, 'O': 6}),
    ('HNO₃', {'H': 1, 'N': 1, 'O': 3}), ('MgO', {'Mg': 1, 'O': 1}), ('Al₂O₃', {'Al': 2, 'O': 3}), ('KCl', {'K': 1, 'Cl': 1}),
    ('C₂H₅OH', {'C': 2, 'H': 6, 'O': 1}), ('Na₂CO₃', {'Na': 2, 'C': 1, 'O': 3}), ('CaO', {'Ca': 1, 'O': 1}),
]


def molar_mass(comp):
    return sum(F(MASS[e]).limit_denominator() * n for e, n in comp.items())


@generator('chemistry.mole', CHE, 'Mole Concept & Stoichiometry')
def mole(rng):
    name, comp = rng.choice(COMPOUNDS)
    mm = molar_mass(comp)
    kind = rng.randrange(3)
    if kind == 0:
        return mcq(rng, f"The molar mass of {name} is ___ g/mol.", fmt(mm), near(rng, mm, spread=2), 'easy',
                   " + ".join(f"{n}×{fmt(MASS[e])}" for e, n in comp.items()) + f" = {fmt(mm)} g/mol.")
    if kind == 1:
        n = rng.choice([F(1, 2), F(1), F(2), F(3), F(1, 4), F(5)])
        mass = mm * n
        return mcq(rng, f"How many moles are present in {fmt(mass)} g of {name}?", fmt(n), [fmt(x) for x in (n * 2, n / 2, n + 1, mm)],
                   'easy', f"n = mass/M = {fmt(mass)}/{fmt(mm)} = {fmt(n)} mol.")
    n = rng.choice([F(1, 2), F(1), F(2), F(1, 10)])
    count = n * F(6022, 1000)
    return mcq(rng, f"The number of molecules in {fmt(n)} mol of {name} is ___.", f"{fmt(count)} × 10²³",
               [f"{fmt(x)} × 10²³" for x in (count * 2, count / 2, F(6022, 1000))] + ["6.022 × 10²⁰"], 'easy', f"N = n × Nₐ = {fmt(count)} × 10²³.")


@generator('chemistry.solutions', CHE, 'Solutions, pH & Concentration')
def solutions(rng):
    kind = rng.randrange(3)
    if kind == 0:
        n = rng.randint(1, 5)
        acid = rng.random() < 0.6
        ph = n if acid else 14 - n
        what = f"HCl" if acid else "NaOH"
        return mcq(rng, f"The pH of a 10⁻{n} M {what} solution (at 25 °C) is ___.", str(ph), [str(x) for x in {14 - ph, ph + 1, abs(ph - 1), 7} if x != ph],
                   'medium', f"{'[H⁺]' if acid else '[OH⁻]'} = 10⁻{n} → pH = {ph}.")
    if kind == 1:
        name, comp = rng.choice([c for c in COMPOUNDS if c[0] in ('NaOH', 'NaCl', 'HCl', 'KCl', 'C₆H₁₂O₆', 'H₂SO₄')])
        mm = molar_mass(comp)
        moles, vol = rng.choice([F(1, 10), F(1, 4), F(1, 2), F(1), F(2)]), rng.choice([F(1, 4), F(1, 2), F(1), F(2)])
        mass = mm * moles
        m = moles / vol
        return mcq(rng, f"{float(mass):g} g of {name} is dissolved to make {fmt(vol * 1000)} mL of solution. Its molarity is ___.", f"{fmt(m)} M",
                   [f"{fmt(x)} M" for x in (m * 2, m / 2, moles, m + 1)], 'medium', f"M = moles/litres = {fmt(moles)}/{fmt(vol)} = {fmt(m)} M.")
    m1, v1, v2 = rng.choice([1, 2, 5]), rng.choice([100, 200, 250]), rng.choice([500, 1000])
    m2 = F(m1 * v1, v2)
    return mcq(rng, f"{v1} mL of {m1} M HCl is diluted to {v2} mL. The new molarity is ___.", f"{fmt(m2)} M",
               [f"{fmt(x)} M" for x in (m2 * 2, F(m1 * v2, v1), m2 / 2, m1)], 'medium', f"M₁V₁ = M₂V₂ → {fmt(m2)} M.")


ELEMENTS = [('Hydrogen', 'H', 1), ('Helium', 'He', 2), ('Lithium', 'Li', 3), ('Beryllium', 'Be', 4), ('Boron', 'B', 5),
            ('Carbon', 'C', 6), ('Nitrogen', 'N', 7), ('Oxygen', 'O', 8), ('Fluorine', 'F', 9), ('Neon', 'Ne', 10),
            ('Sodium', 'Na', 11), ('Magnesium', 'Mg', 12), ('Aluminium', 'Al', 13), ('Silicon', 'Si', 14), ('Phosphorus', 'P', 15),
            ('Sulphur', 'S', 16), ('Chlorine', 'Cl', 17), ('Argon', 'Ar', 18), ('Potassium', 'K', 19), ('Calcium', 'Ca', 20),
            ('Iron', 'Fe', 26), ('Copper', 'Cu', 29), ('Zinc', 'Zn', 30), ('Silver', 'Ag', 47), ('Tin', 'Sn', 50),
            ('Gold', 'Au', 79), ('Mercury', 'Hg', 80), ('Lead', 'Pb', 82), ('Tungsten', 'W', 74), ('Antimony', 'Sb', 51)]


def config(z):
    shells, left = [], z
    for cap in (2, 8, 8, 2):
        take = min(cap, left)
        shells.append(take)
        left -= take
        if not left:
            break
    return shells


@generator('chemistry.periodic', CHE, 'Atomic Structure & Periodic Table')
def periodic(rng):
    kind = rng.randrange(4)
    name, sym, z = rng.choice(ELEMENTS)
    if kind == 0:
        others = [s for n, s, _ in ELEMENTS if s != sym]
        rng.shuffle(others)
        return mcq(rng, f"The chemical symbol of {name} is ___.", sym, others, 'easy', f"{name}: {sym}.")
    if kind == 1:
        return mcq(rng, f"The atomic number of {name} ({sym}) is ___.", str(z), [str(x) for x in (z + 1, z - 1 if z > 1 else z + 3, z + 2, z * 2)],
                   'easy', f"{name} has {z} protons.")
    name, sym, z = rng.choice(ELEMENTS[2:20])
    shells = config(z)
    if kind == 2:
        c = ', '.join(map(str, shells))
        wrong = {', '.join(map(str, s)) for s in ([z], shells[::-1] if len(shells) > 1 else [z - 1, 1], shells[:-1] + [shells[-1] + 1], [2] + [z - 2])} - {c}
        return mcq(rng, f"The electronic configuration (K, L, M, N) of {name} (Z = {z}) is ___.", c, list(wrong) + ['2, 8, 8, 8'], 'medium',
                   f"Fill shells 2, 8, 8…: {c}.")
    val = shells[-1]
    valency = val if val <= 4 else 8 - val
    return mcq(rng, f"The valency of {name} (Z = {z}) is ___.", str(valency), [str(x) for x in range(0, 5) if x != valency], 'medium',
               f"Configuration {', '.join(map(str, shells))}; {val} valence electron(s) → valency {valency}.")


CHEM_NAMES = rows("""
Baking soda|Sodium hydrogen carbonate (NaHCO₃)
Washing soda|Sodium carbonate decahydrate (Na₂CO₃·10H₂O)
Bleaching powder|Calcium oxychloride (CaOCl₂)
Plaster of Paris|Calcium sulphate hemihydrate (CaSO₄·½H₂O)
Quicklime|Calcium oxide (CaO)
Slaked lime|Calcium hydroxide (Ca(OH)₂)
Limestone|Calcium carbonate (CaCO₃)
Gypsum|Calcium sulphate dihydrate (CaSO₄·2H₂O)
Caustic soda|Sodium hydroxide (NaOH)
Blue vitriol|Copper sulphate pentahydrate (CuSO₄·5H₂O)
Green vitriol|Ferrous sulphate heptahydrate (FeSO₄·7H₂O)
Dry ice|Solid carbon dioxide
Laughing gas|Nitrous oxide (N₂O)
Marsh gas|Methane (CH₄)
Common salt|Sodium chloride (NaCl)
Muriatic acid|Hydrochloric acid (HCl)
Oil of vitriol|Sulphuric acid (H₂SO₄)
""")
table_topics('chemistry.compounds', CHE, 'Common Compounds', CHEM_NAMES, [
    ("The chemical name of '{a}' is ___.", 'b', "{a} is {b}."),
    ("{b} is commonly known as ___.", 'a', "{b}: {a}."),
], difficulty='easy')

CHEM_CONCEPTS = [
    ("An aqueous solution with pH 3 is ___.", ['Acidic', 'Basic', 'Neutral', 'Amphoteric'], 'easy', "pH < 7."),
    ("The reaction between an acid and a base is called ___.", ['Neutralisation', 'Oxidation', 'Decomposition', 'Displacement'], 'easy', "Salt + water."),
    ("Rusting of iron is an example of ___.", ['Oxidation', 'Reduction', 'Neutralisation', 'Sublimation'], 'easy', "Iron reacts with oxygen and moisture."),
    ("CaCO₃ → CaO + CO₂ is a ___ reaction.", ['Decomposition', 'Combination', 'Displacement', 'Double displacement'], 'easy', "One reactant breaks into two products."),
    ("Fe + CuSO₄ → FeSO₄ + Cu is a ___ reaction.", ['Displacement', 'Combination', 'Decomposition', 'Neutralisation'], 'easy', "More reactive iron displaces copper."),
    ("Which gas turns lime water milky?", ['Carbon dioxide', 'Oxygen', 'Hydrogen', 'Nitrogen'], 'easy', "Forms CaCO₃."),
    ("The hybridisation of carbon in methane is ___.", ['sp³', 'sp²', 'sp', 'dsp²'], 'medium', "Tetrahedral, 109.5°."),
    ("The shape of a water molecule is ___.", ['Bent (V-shaped)', 'Linear', 'Trigonal planar', 'Tetrahedral'], 'medium', "Two lone pairs on oxygen; ~104.5°."),
    ("The most electronegative element is ___.", ['Fluorine', 'Oxygen', 'Chlorine', 'Nitrogen'], 'easy', "Pauling value 4.0."),
    ("The element with the largest atomic radius in period 3 is ___.", ['Sodium', 'Chlorine', 'Argon', 'Magnesium'], 'medium', "Radius decreases across a period."),
    ("The general formula of alkanes is ___.", ['CₙH₂ₙ₊₂', 'CₙH₂ₙ', 'CₙH₂ₙ₋₂', 'CₙHₙ'], 'easy', "Saturated hydrocarbons."),
    ("The functional group –COOH is called ___.", ['Carboxylic acid', 'Aldehyde', 'Ketone', 'Alcohol'], 'easy', "Carboxyl group."),
    ("The IUPAC name of CH₃COCH₃ is ___.", ['Propanone', 'Propanal', 'Ethanone', 'Propanol'], 'medium', "Acetone."),
    ("Isomers have the same ___.", ['Molecular formula', 'Structural formula', 'Physical properties', 'Boiling point'], 'easy', "Different structures."),
    ("Which quantum number describes the shape of an orbital?", ['Azimuthal (l)', 'Principal (n)', 'Magnetic (m)', 'Spin (s)'], 'medium', "l = 0, 1, 2… → s, p, d…"),
    ("The maximum number of electrons in a d-subshell is ___.", ['10', '6', '14', '2'], 'easy', "2(2l + 1) with l = 2."),
    ("According to Le Chatelier's principle, increasing pressure favours the side with ___.", ['Fewer moles of gas', 'More moles of gas', 'Higher temperature', 'More solids'], 'medium', "The system reduces the pressure."),
    ("A catalyst changes the ___.", ['Rate of reaction', 'Equilibrium constant', 'Enthalpy of reaction', 'Products formed'], 'medium', "It lowers activation energy."),
    ("The oxidation number of Mn in KMnO₄ is ___.", ['+7', '+6', '+4', '+2'], 'medium', "+1 + x − 8 = 0."),
    ("The oxidation number of Cr in K₂Cr₂O₇ is ___.", ['+6', '+7', '+3', '+5'], 'medium', "2 + 2x − 14 = 0."),
    ("The process of coating iron with zinc is called ___.", ['Galvanisation', 'Electroplating with tin', 'Anodising', 'Vulcanisation'], 'easy', "Zinc protects iron."),
    ("Vulcanisation of rubber uses ___.", ['Sulphur', 'Carbon', 'Zinc', 'Chlorine'], 'medium', "Cross-links polymer chains."),
    ("Which of these is a noble gas?", ['Argon', 'Nitrogen', 'Chlorine', 'Oxygen'], 'easy', "Group 18."),
    ("Ozone is an allotrope of ___.", ['Oxygen', 'Nitrogen', 'Carbon', 'Hydrogen'], 'easy', "O₃."),
    ("Graphite conducts electricity because ___.", ['It has delocalised electrons', 'It is a metal', 'It has ions', 'It is very hard'], 'medium', "Each carbon uses 3 electrons in bonds; the 4th is free."),
    ("The first law of thermodynamics is a statement of conservation of ___.", ['Energy', 'Mass', 'Momentum', 'Entropy'], 'easy', "ΔU = q + w."),
    ("A reaction with ΔH < 0 is ___.", ['Exothermic', 'Endothermic', 'Non-spontaneous always', 'At equilibrium'], 'easy', "It releases heat."),
    ("Which acid is present in lemons?", ['Citric acid', 'Acetic acid', 'Lactic acid', 'Tartaric acid'], 'easy', "Citrus fruits."),
    ("The chief ore of aluminium is ___.", ['Bauxite', 'Haematite', 'Galena', 'Cinnabar'], 'easy', "Al₂O₃·2H₂O."),
    ("Haematite is an ore of ___.", ['Iron', 'Copper', 'Zinc', 'Lead'], 'easy', "Fe₂O₃."),
]
register('chemistry.concepts', CHE, 'Chemistry Concepts', rows=CHEM_CONCEPTS)


def _chem_numeric(rng):
    name, comp = rng.choice(COMPOUNDS)
    mm = molar_mass(comp)
    if mm.denominator != 1:
        name, comp = 'H₂O', {'H': 2, 'O': 1}
        mm = F(18)
    return numerical(f"Find the molar mass (in g/mol) of {name}. (H = 1, C = 12, N = 14, O = 16, Na = 23, Mg = 24, Al = 27, S = 32, K = 39, Ca = 40)",
                     mm, 'easy', " + ".join(f"{n}×{fmt(MASS[e])}" for e, n in comp.items()) + f" = {fmt(mm)}.")


register('chemistry.mole', CHE, '', numeric=_chem_numeric)

# ------------------------------------------------------------------ biology

HORMONES = rows("""
Insulin|Pancreas (beta cells)
Glucagon|Pancreas (alpha cells)
Thyroxine|Thyroid gland
Adrenaline|Adrenal medulla
Cortisol|Adrenal cortex
Growth hormone|Anterior pituitary
Oxytocin|Posterior pituitary (made in the hypothalamus)
Melatonin|Pineal gland
Parathormone|Parathyroid glands
Testosterone|Testes
Oestrogen|Ovaries
Thymosin|Thymus
""")
table_topics('biology.hormones', BIO, 'Human Physiology – Hormones', HORMONES, [
    ("{a} is secreted by the ___.", 'b', "{a}: {b}."),
    ("Which hormone is secreted by the {b}?", 'a', "{b}: {a}."),
])

DISEASES = rows("""
Tuberculosis|Mycobacterium tuberculosis (bacterium)
Typhoid|Salmonella typhi (bacterium)
Cholera|Vibrio cholerae (bacterium)
Malaria|Plasmodium (protozoan)
Amoebiasis|Entamoeba histolytica (protozoan)
AIDS|HIV (virus)
Polio|Poliovirus
Ringworm|Fungi (Microsporum, Trichophyton)
Dengue|Dengue virus (spread by Aedes)
Filariasis|Wuchereria bancrofti (nematode)
Tetanus|Clostridium tetani (bacterium)
Diphtheria|Corynebacterium diphtheriae (bacterium)
Leprosy|Mycobacterium leprae (bacterium)
Kala-azar|Leishmania donovani (protozoan)
Pneumonia (commonly)|Streptococcus pneumoniae (bacterium)
""")
table_topics('biology.diseases', BIO, 'Human Health & Disease', DISEASES, [
    ("{a} is caused by ___.", 'b', "{a}: {b}."),
    ("Which disease is caused by {b}?", 'a', "{b} causes {a}."),
])

ORGANELLES = rows("""
Mitochondria|Site of aerobic respiration (ATP production)
Ribosomes|Protein synthesis
Chloroplast|Photosynthesis
Golgi apparatus|Packaging and secretion of materials
Lysosomes|Intracellular digestion ('suicide bags')
Rough endoplasmic reticulum|Synthesis and transport of proteins
Smooth endoplasmic reticulum|Lipid synthesis and detoxification
Nucleus|Controls cell activities and holds DNA
Centrioles|Form spindle fibres in animal cell division
Vacuole|Storage and maintaining turgor in plant cells
Cell wall|Rigidity and protection in plant cells
""")
table_topics('biology.cell', BIO, 'Cell: Structure & Function', ORGANELLES, [
    ("The main function of the {a} is ___.", 'b', "{a}: {b}."),
    ("Which cell organelle is responsible for: {b}?", 'a', "{a}: {b}."),
], difficulty='easy')

PLANT_HORMONES = rows("""
Auxin|Cell elongation and apical dominance
Gibberellin|Stem elongation and breaking seed dormancy
Cytokinin|Cell division and delaying leaf senescence
Abscisic acid|Stomatal closure and dormancy (stress hormone)
Ethylene|Fruit ripening
""")
table_topics('biology.plant_physiology', BIO, 'Plant Physiology', PLANT_HORMONES, [
    ("The plant hormone mainly responsible for {b} is ___.", 'a', "{a}: {b}."),
    ("{a} is mainly responsible for ___.", 'b', "{a}: {b}."),
])

BIOLOGY = [
    ("DNA replication is ___.", ['Semi-conservative', 'Conservative', 'Dispersive', 'Random'], 'medium', "Meselson–Stahl experiment."),
    ("The genetic code is read in groups of ___ nucleotides.", ['Three', 'Two', 'Four', 'One'], 'easy', "Codons are triplets."),
    ("The start codon in protein synthesis is ___.", ['AUG', 'UAA', 'UGA', 'UAG'], 'medium', "Codes for methionine."),
    ("Which base is found in RNA but not in DNA?", ['Uracil', 'Thymine', 'Adenine', 'Guanine'], 'easy', "U replaces T."),
    ("A cross between F₁ hybrid and its recessive parent is called a ___.", ['Test cross', 'Back cross with dominant', 'Dihybrid cross', 'Reciprocal cross'], 'medium', "Reveals the genotype."),
    ("The phenotypic ratio of a Mendelian dihybrid cross in F₂ is ___.", ['9 : 3 : 3 : 1', '3 : 1', '1 : 2 : 1', '1 : 1 : 1 : 1'], 'easy', "Independent assortment."),
    ("The phenotypic ratio of a monohybrid cross in F₂ is ___.", ['3 : 1', '9 : 3 : 3 : 1', '1 : 2 : 1', '1 : 1'], 'easy', "The genotypic ratio is 1 : 2 : 1."),
    ("Haemophilia is a ___ disorder.", ['Sex-linked recessive', 'Autosomal dominant', 'Autosomal recessive', 'Y-linked'], 'medium', "Gene on the X chromosome."),
    ("Down syndrome is caused by trisomy of chromosome ___.", ['21', '18', '13', 'X'], 'easy', "47 chromosomes."),
    ("The functional unit of the kidney is the ___.", ['Nephron', 'Neuron', 'Alveolus', 'Villus'], 'easy', "About a million per kidney."),
    ("Gaseous exchange in the lungs takes place in the ___.", ['Alveoli', 'Bronchi', 'Trachea', 'Pleura'], 'easy', "Thin, moist walls."),
    ("The pacemaker of the heart is the ___.", ['SA node', 'AV node', 'Bundle of His', 'Purkinje fibres'], 'medium', "Sino-atrial node."),
    ("The normal blood pressure of an adult is about ___.", ['120/80 mm Hg', '140/100 mm Hg', '90/60 mm Hg', '160/90 mm Hg'], 'easy', "Systolic/diastolic."),
    ("Which part of the brain controls balance and coordination?", ['Cerebellum', 'Cerebrum', 'Medulla oblongata', 'Hypothalamus'], 'easy', "Hindbrain."),
    ("Bile is produced by the ___.", ['Liver', 'Gall bladder', 'Pancreas', 'Stomach'], 'easy', "Stored in the gall bladder."),
    ("Pepsin acts on ___.", ['Proteins', 'Fats', 'Starch', 'Nucleic acids'], 'easy', "In the stomach."),
    ("The 'Kranz anatomy' is a feature of ___ plants.", ['C₄', 'C₃', 'CAM', 'Aquatic'], 'hard', "Bundle-sheath cells around veins."),
    ("The first stable product of the Calvin cycle in C₃ plants is ___.", ['3-phosphoglyceric acid', 'Oxaloacetic acid', 'Glucose', 'RuBP'], 'medium', "A 3-carbon compound."),
    ("In glycolysis, one glucose molecule gives ___ molecules of pyruvate.", ['Two', 'One', 'Three', 'Four'], 'easy', "In the cytoplasm."),
    ("Double fertilisation is characteristic of ___.", ['Angiosperms', 'Gymnosperms', 'Bryophytes', 'Pteridophytes'], 'easy', "Gives zygote and endosperm."),
    ("The endosperm of angiosperms is usually ___.", ['Triploid', 'Diploid', 'Haploid', 'Tetraploid'], 'medium', "Polar nuclei + male gamete."),
    ("Nitrogen fixation in root nodules of legumes is done by ___.", ['Rhizobium', 'Azotobacter', 'Nitrosomonas', 'Pseudomonas'], 'easy', "Symbiotic bacteria."),
    ("The 'father of taxonomy' is ___.", ['Carolus Linnaeus', 'Charles Darwin', 'Gregor Mendel', 'Robert Hooke'], 'easy', "Binomial nomenclature."),
    ("Who proposed the theory of natural selection?", ['Charles Darwin', 'Lamarck', 'Mendel', 'Hugo de Vries'], 'easy', "On the Origin of Species, 1859."),
    ("The cell was first observed by ___.", ['Robert Hooke', 'Leeuwenhoek', 'Schleiden', 'Robert Brown'], 'easy', "In cork, 1665."),
    ("Restriction enzymes are used in genetic engineering to ___.", ['Cut DNA at specific sequences', 'Join DNA fragments', 'Copy DNA', 'Translate RNA'], 'medium', "Molecular scissors; ligase joins."),
    ("PCR is used to ___.", ['Amplify DNA', 'Cut DNA', 'Sequence proteins', 'Translate mRNA'], 'easy', "Polymerase chain reaction."),
    ("Bt cotton contains a gene from ___.", ['Bacillus thuringiensis', 'Agrobacterium', 'E. coli', 'Rhizobium'], 'easy', "Produces an insecticidal Cry protein."),
    ("Which blood group has no antibodies in the plasma?", ['AB', 'O', 'A', 'B'], 'medium', "AB is the universal recipient."),
    ("The largest phylum in the animal kingdom is ___.", ['Arthropoda', 'Chordata', 'Mollusca', 'Annelida'], 'easy', "Insects alone are over a million species."),
    ("Which of these is a mammal that lays eggs?", ['Platypus', 'Bat', 'Whale', 'Kangaroo'], 'medium', "A monotreme."),
    ("The energy pyramid in an ecosystem is always ___.", ['Upright', 'Inverted', 'Spindle-shaped', 'Irregular'], 'medium', "About 10% passes to the next level."),
    ("The '10% law' of energy transfer was given by ___.", ['Lindeman', 'Odum', 'Tansley', 'Haeckel'], 'hard', "Raymond Lindeman, 1942."),
    ("The term 'ecosystem' was coined by ___.", ['A. G. Tansley', 'E. P. Odum', 'Charles Elton', 'Ernst Haeckel'], 'medium', "1935."),
    ("Which of these is a greenhouse gas?", ['Methane', 'Nitrogen', 'Oxygen', 'Argon'], 'easy', "CO₂, CH₄, N₂O, water vapour…"),
    ("Spermatogenesis takes place in the ___.", ['Seminiferous tubules', 'Epididymis', 'Vas deferens', 'Prostate'], 'medium', "In the testes."),
    ("Fertilisation in humans normally occurs in the ___.", ['Fallopian tube (ampulla)', 'Uterus', 'Ovary', 'Cervix'], 'medium', "Ampullary region of the oviduct."),
    ("Antibodies are produced by ___.", ['B lymphocytes (plasma cells)', 'T lymphocytes', 'RBCs', 'Platelets'], 'medium', "Humoral immunity."),
    ("The BCG vaccine protects against ___.", ['Tuberculosis', 'Polio', 'Measles', 'Tetanus'], 'easy', "Bacillus Calmette–Guérin."),
    ("Which vitamin is needed for blood clotting?", ['Vitamin K', 'Vitamin A', 'Vitamin C', 'Vitamin D'], 'easy', "Prothrombin synthesis."),
]
register('biology.concepts', BIO, 'Biology Concepts', rows=BIOLOGY)

SCIENCE_TOPICS = ['physics.kinematics', 'physics.force_energy', 'physics.electricity', 'physics.optics_waves', 'physics.heat_matter',
                  'physics.units', 'physics.concepts', 'chemistry.mole', 'chemistry.solutions', 'chemistry.periodic',
                  'chemistry.compounds', 'chemistry.concepts', 'biology.hormones', 'biology.diseases', 'biology.cell',
                  'biology.plant_physiology', 'biology.concepts']
