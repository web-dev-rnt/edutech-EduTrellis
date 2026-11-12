"""School syllabus map: which chapters (topic pools) each board, class and subject is tested on.

Boards that prescribe NCERT books (CBSE and most state boards) share the NCERT chapter order; ICSE splits Science
and Social Science into separate subjects. Legacy questions written for the board/class are always included.
"""
from .core import TOPICS, mcq, register
from .gen_math_school import CHAPTERS

# ------------------------------------------------------------------ simple English for Classes 1–5
OPPOSITES = [('big', 'small'), ('hot', 'cold'), ('up', 'down'), ('day', 'night'), ('happy', 'sad'), ('fast', 'slow'), ('tall', 'short'),
             ('open', 'close'), ('old', 'new'), ('wet', 'dry'), ('full', 'empty'), ('light', 'heavy'), ('inside', 'outside'), ('early', 'late'),
             ('clean', 'dirty'), ('soft', 'hard'), ('rich', 'poor'), ('push', 'pull'), ('come', 'go'), ('near', 'far')]
PLURALS = [('cat', 'cats'), ('box', 'boxes'), ('baby', 'babies'), ('child', 'children'), ('man', 'men'), ('mouse', 'mice'), ('tooth', 'teeth'),
           ('bus', 'buses'), ('leaf', 'leaves'), ('foot', 'feet'), ('city', 'cities'), ('knife', 'knives'), ('tomato', 'tomatoes'),
           ('sheep', 'sheep'), ('woman', 'women'), ('glass', 'glasses')]
PAST = [('play', 'played'), ('go', 'went'), ('eat', 'ate'), ('run', 'ran'), ('write', 'wrote'), ('sing', 'sang'), ('jump', 'jumped'),
        ('see', 'saw'), ('drink', 'drank'), ('sleep', 'slept'), ('take', 'took'), ('come', 'came')]
ARTICLE_WORDS = ['apple', 'umbrella', 'egg', 'ink-pot', 'owl', 'elephant', 'orange', 'ant', 'hour', 'honest man',
                 'ball', 'cat', 'dog', 'kite', 'pen', 'tree', 'university', 'uniform', 'one-rupee coin', 'house']


def kids_english(rng):
    kind = rng.randrange(4)
    if kind == 0:
        a, b = rng.choice(OPPOSITES)
        others = [x for p in OPPOSITES for x in p if x not in (a, b)]
        rng.shuffle(others)
        return mcq(rng, f"What is the opposite of '{a}'?", b, others, 'easy', f"'{a}' and '{b}' are opposites.")
    if kind == 1:
        s, p = rng.choice(PLURALS)
        wrong = {s + 's', s + 'es', s[:-1] + 'ies' if s.endswith('y') else s + 'ys', s + 'en'} - {p}
        return mcq(rng, f"What is the plural of '{s}'?", p, list(wrong), 'easy' if p.endswith('s') else 'medium', f"One {s}, many {p}.")
    if kind == 2:
        v, p = rng.choice(PAST)
        wrong = {v + 'ed', v + 'ing', v + 's', p + 'ed'} - {p}
        return mcq(rng, f"What is the past tense of '{v}'?", p, list(wrong), 'medium', f"Today I {v}; yesterday I {p}.")
    w = rng.choice(ARTICLE_WORDS)
    vowel_sound = w in ('apple', 'umbrella', 'egg', 'ink-pot', 'owl', 'elephant', 'orange', 'ant', 'hour', 'honest man')
    ans = 'an' if vowel_sound else 'a'
    return mcq(rng, f"Fill in with 'a' or 'an': ___ {w}", ans, ['the', 'a' if ans == 'an' else 'an', 'no article'], 'easy',
               "'an' before a vowel sound, 'a' before a consonant sound.")


register('english.kids', 'ENG1', 'Words & Grammar', gen=kids_english)

PRIMARY_ENG = [('Words & Grammar', ['english.kids'])]
MIDDLE_ENG = [('Grammar', ['english.grammar']), ('Vocabulary: Synonyms & Antonyms', ['english.synonym', 'english.antonym']),
              ('Idioms & One-word Substitution', ['english.idioms', 'english.one_word']), ('Spelling', ['english.spelling'])]
SENIOR_ENG = MIDDLE_ENG + [('Error Spotting & Sentence Improvement', ['english.error_spotting', 'english.sentence_improvement']),
                           ('Voice & Narration', ['english.voice_narration']), ('Reading Comprehension', ['english.comprehension'])]
HINDI_PRIMARY = [('पर्यायवाची एवं विलोम', ['hindi.paryayvachi', 'hindi.vilom'])]
HINDI_MIDDLE = HINDI_PRIMARY + [('मुहावरे', ['hindi.muhavare']), ('व्याकरण', ['hindi.grammar'])]
HINDI_SENIOR = HINDI_MIDDLE + [('संधि-विच्छेद', ['hindi.sandhi'])]
EVS = [('Animals & Their Homes', ['evs.animals', 'evs.young_ones']), ('Our Environment', ['evs.general'])]
GK = [('General Knowledge', ['evs.general', 'ga.important_days']), ('India: States & Symbols', ['ga.states'])]
SCI_MIDDLE = [('Living World & Health', ['biology.cell', 'biology.diseases']), ('Materials & Chemicals', ['chemistry.compounds', 'chemistry.periodic']),
              ('Measurement, Heat & Pressure', ['physics.units', 'physics.heat_matter']), ('Motion, Light & Electricity', ['physics.kinematics', 'physics.concepts'])]
SCI_SECONDARY = [('Chemical Reactions, Acids, Bases & Salts', ['chemistry.concepts', 'chemistry.compounds', 'chemistry.solutions']),
                 ('Atoms, Molecules & Periodic Classification', ['chemistry.mole', 'chemistry.periodic']),
                 ('Motion, Force, Work & Energy', ['physics.kinematics', 'physics.force_energy']),
                 ('Electricity & Magnetic Effects', ['physics.electricity']), ('Light & Sound', ['physics.optics_waves']),
                 ('Life Processes & the Cell', ['biology.cell', 'biology.human_physiology']),
                 ('Control, Coordination & Heredity', ['biology.hormones', 'biology.genetics']),
                 ('Health, Environment & Natural Resources', ['biology.diseases', 'biology.ecology'])]
SST_MIDDLE = [('History', ['ga.history']), ('Geography', ['ga.geography', 'ga.states', 'ga.rivers']), ('Civics', ['ga.polity'])]
SST_SECONDARY = [('History', ['ga.history']), ('Geography', ['ga.geography', 'ga.rivers', 'ga.national_parks']),
                 ('Political Science', ['ga.polity', 'ga.polity_articles']), ('Economics', ['ga.economy', 'commerce.economics'])]
PHY_11 = [('Units & Measurement', ['physics.units']), ('Motion & Laws of Motion', ['physics.kinematics', 'physics.concepts']),
          ('Work, Energy & Power', ['physics.force_energy']), ('Thermal Properties & Thermodynamics', ['physics.heat_matter']),
          ('Oscillations & Waves', ['physics.optics_waves'])]
PHY_12 = [('Current Electricity', ['physics.electricity']), ('Optics', ['physics.optics_waves']),
          ('Dual Nature, Atoms & Nuclei', ['physics.modern']), ('Electronic Devices', ['physics.modern', 'digital.logic'])]
CHE_11 = [('Some Basic Concepts of Chemistry', ['chemistry.mole']), ('Structure of Atom & Periodicity', ['chemistry.periodic']),
          ('Bonding, Equilibrium & Thermodynamics', ['chemistry.concepts']), ('Organic Chemistry Basics & Hydrocarbons', ['chemistry.organic'])]
CHE_12 = [('Solutions & Electrochemistry', ['chemistry.solutions']), ('Organic Compounds (Haloalkanes to Amines)', ['chemistry.organic']),
          ('Biomolecules & Everyday Chemistry', ['chemistry.organic', 'chemistry.compounds']), ('Coordination & d-block (concepts)', ['chemistry.concepts'])]
BIO_11 = [('Diversity of Living Organisms', ['biology.taxonomy']), ('Cell: Structure & Function', ['biology.cell']),
          ('Plant Physiology', ['biology.plant_physiology']), ('Human Physiology', ['biology.human_physiology', 'biology.hormones'])]
BIO_12 = [('Reproduction', ['biology.concepts']), ('Genetics & Evolution', ['biology.genetics']), ('Biology in Human Welfare', ['biology.diseases']),
          ('Biotechnology', ['biology.genetics', 'biology.concepts']), ('Ecology & Environment', ['biology.ecology'])]
ACC = [('Accounting Principles', ['commerce.accounting_theory']), ('Depreciation, Ratios & Calculations', ['commerce.accounting']),
       ('GST', ['commerce.gst'])]
BST = [('Management & Business Studies', ['commerce.business']), ('Business Law Basics', ['commerce.business_law'])]
ECO = [('Microeconomics', ['commerce.economics']), ('Indian Economy & Money', ['ga.economy'])]
HIS = [('Indian History', ['ga.history']), ('Art, Culture & Heritage', ['ga.culture', 'design.architecture'])]
POL = [('Constitution & Polity', ['ga.polity']), ('Articles of the Constitution', ['ga.polity_articles']), ('Landmark Judgments', ['law.cases'])]
GEO = [('Physical & Indian Geography', ['ga.geography', 'ga.rivers']), ('States, Parks & World', ['ga.states', 'ga.national_parks', 'ga.world']),
       ('Environment & Resources', ['biology.ecology'])]


def math_chapters(grade):
    return [(title, [key]) for key, title in CHAPTERS.get(grade, [])]


def subjects_for(board, grade, stream, hindi=True):
    """[(subject code, subject title, [(chapter title, [topic keys])])] for one class."""
    if grade <= 2:
        subs = [('ENG1', 'English', PRIMARY_ENG), ('HIN1', 'Hindi', HINDI_PRIMARY), ('MAT1', 'Mathematics', math_chapters(grade)),
                ('EVS1', 'EVS', EVS), ('GK1', 'General Knowledge', GK)]
    elif grade <= 5:
        subs = [('ENG1', 'English', PRIMARY_ENG), ('HIN1', 'Hindi', HINDI_PRIMARY), ('MAT1', 'Mathematics', math_chapters(grade)),
                ('EVS1', 'EVS', EVS), ('GK1', 'General Knowledge', GK)]
    elif grade <= 8:
        subs = [('ENG1', 'English', MIDDLE_ENG), ('HIN1', 'Hindi', HINDI_MIDDLE), ('MAT1', 'Mathematics', math_chapters(grade)),
                ('SCI1', 'Science', SCI_MIDDLE), ('SST1', 'Social Science', SST_MIDDLE)]
    elif grade <= 10:
        maths = math_chapters(grade) if grade == 10 else math_chapters(9)
        if board == 'icse':
            subs = [('ENG1', 'English', SENIOR_ENG), ('HIN1', 'Hindi', HINDI_SENIOR), ('MAT1', 'Mathematics', maths),
                    ('PHY1', 'Physics', SCI_SECONDARY[2:5]), ('CHE1', 'Chemistry', SCI_SECONDARY[:2]),
                    ('BIO1', 'Biology', SCI_SECONDARY[5:]), ('HCV1', 'History & Civics', SST_SECONDARY[0:1] + SST_SECONDARY[2:3]),
                    ('GEO1', 'Geography', SST_SECONDARY[1:2])]
        else:
            subs = [('ENG1', 'English', SENIOR_ENG), ('HIN1', 'Hindi', HINDI_SENIOR), ('MAT1', 'Mathematics', maths),
                    ('SCI1', 'Science', SCI_SECONDARY), ('SST1', 'Social Science', SST_SECONDARY)]
    else:
        maths = math_chapters(grade)
        streams = {
            'science': [('PHY1', 'Physics', PHY_11 if grade == 11 else PHY_12), ('CHE1', 'Chemistry', CHE_11 if grade == 11 else CHE_12),
                        ('MAT1', 'Mathematics', maths), ('BIO1', 'Biology', BIO_11 if grade == 11 else BIO_12), ('ENG1', 'English', SENIOR_ENG)],
            'commerce': [('ACC1', 'Accountancy', ACC), ('BST1', 'Business Studies', BST), ('ECO1', 'Economics', ECO),
                         ('MAT1', 'Mathematics', maths), ('ENG1', 'English', SENIOR_ENG)],
            'arts': [('HIS1', 'History', HIS), ('POL1', 'Political Science', POL), ('GEO1', 'Geography', GEO),
                     ('ECO1', 'Economics', ECO), ('ENG1', 'English', SENIOR_ENG)],
        }
        subs = streams[stream or 'science']
    if not hindi:
        subs = [s for s in subs if s[0] != 'HIN1']
    return subs


def legacy_keys(board, grade, code):
    """Legacy pools for a board/class/subject, most specific first."""
    keys = [f"school.{board}.{grade}.{code}", f"school.any.{grade}.{code}"]
    # ICSE splits subjects; state boards draw on the merged pools. Science/SST legacy may sit under split codes.
    alias = {'SCI1': ['PHY1', 'CHE1', 'BIO1'], 'SST1': ['HCV1', 'GEO1'], 'HCV1': ['SST1'], 'GEO1': ['SST1']}
    for other in alias.get(code, []):
        keys.append(f"school.any.{grade}.{other}")
    seen, out = set(), []
    for k in keys:
        if k in TOPICS and k not in seen and TOPICS[k].rows:
            seen.add(k)
            out.append(k)
    return out
