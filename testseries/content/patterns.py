"""2026 exam patterns: sections, question counts, marking scheme and duration of every competitive exam.

Patterns follow the latest official notifications available (2025–26 cycle). Where a paper has several stages,
the mocks follow the first computer-based stage (prelims / Tier 1 / CBT-1), which is what candidates practise most.
Each section draws from topic pools; questions written earlier for that exam are always used first.
"""
from dataclasses import dataclass, field

QUANT = ['quant.percentage', 'quant.profit_loss', 'quant.interest', 'quant.ratio', 'quant.average', 'quant.time_work', 'quant.speed',
         'quant.number_system', 'quant.simplification', 'quant.mensuration', 'quant.algebra', 'quant.trigonometry', 'quant.mixture',
         'quant.probability', 'quant.di']
QUANT_BANK = ['quant.simplification', 'quant.quadratic', 'reasoning.wrong_number', 'quant.di', 'quant.percentage', 'quant.profit_loss',
              'quant.interest', 'quant.ratio', 'quant.average', 'quant.time_work', 'quant.speed', 'quant.mixture', 'quant.probability']
QUANT_BASIC = ['quant.simplification', 'quant.number_system', 'quant.percentage', 'quant.profit_loss', 'quant.interest', 'quant.ratio',
               'quant.average', 'quant.time_work', 'quant.speed', 'quant.mensuration']
REASON = ['reasoning.number_series', 'reasoning.missing_number', 'reasoning.letter_series', 'reasoning.coding', 'reasoning.letter_value',
          'reasoning.analogy', 'reasoning.direction', 'reasoning.ranking', 'reasoning.calendar', 'reasoning.clock',
          'reasoning.dictionary_order', 'reasoning.cubes', 'reasoning.math_operations', 'reasoning.counting', 'reasoning.blood_relation']
REASON_BANK = ['reasoning.inequality', 'reasoning.coding', 'reasoning.blood_relation', 'reasoning.direction', 'reasoning.ranking',
               'reasoning.dictionary_order', 'reasoning.letter_series', 'reasoning.calendar', 'reasoning.counting', 'reasoning.math_operations']
ENGLISH = ['english.synonym', 'english.antonym', 'english.idioms', 'english.one_word', 'english.spelling', 'english.grammar',
           'english.error_spotting', 'english.voice_narration', 'english.sentence_improvement', 'english.comprehension']
ENGLISH_BANK = ['english.comprehension', 'english.error_spotting', 'english.grammar', 'english.sentence_improvement', 'english.synonym',
                'english.antonym', 'english.idioms']
GA = ['ga.polity', 'ga.polity_articles', 'ga.history', 'ga.geography', 'ga.states', 'ga.rivers', 'ga.national_parks', 'ga.culture',
      'ga.economy', 'ga.science', 'ga.books', 'ga.inventions', 'ga.sports', 'ga.organisations', 'ga.instruments', 'ga.important_days',
      'ga.world', 'ga.currencies',
      # India GK added Nov 2026 (bank_india); appended so existing GA[:n] slices are unchanged
      'ga.monuments', 'ga.festivals', 'ga.lakes', 'ga.state_languages', 'ga.freedom_events', 'ga.titles', 'ga.founders',
      'ga.firsts', 'ga.schedules', 'ga.amendments']
GA_BANK = ['ga.economy', 'ga.banking_terms', 'ga.polity', 'ga.organisations', 'ga.geography', 'ga.important_days', 'ga.books', 'ga.currencies',
           'ga.schedules', 'ga.firsts', 'ga.freedom_events', 'cs.abbreviations']
UPSC_GS = ['ga.polity', 'ga.polity_articles', 'ga.history', 'ga.geography', 'ga.rivers', 'ga.national_parks', 'ga.culture', 'ga.economy',
           'ga.science', 'biology.diseases', 'ga.organisations', 'environment.ecology',
           'ga.schedules', 'ga.amendments', 'ga.freedom_events', 'ga.founders', 'ga.monuments', 'ga.lakes']
GEN_SCIENCE = ['ga.science', 'physics.units', 'physics.concepts', 'chemistry.compounds', 'chemistry.concepts', 'biology.concepts',
               'biology.diseases', 'biology.cell', 'biology.hormones', 'physics.kinematics', 'physics.electricity']
PHYSICS = ['physics.kinematics', 'physics.force_energy', 'physics.electricity', 'physics.optics_waves', 'physics.heat_matter',
           'physics.units', 'physics.concepts', 'physics.modern']
CHEMISTRY = ['chemistry.mole', 'chemistry.solutions', 'chemistry.periodic', 'chemistry.compounds', 'chemistry.concepts', 'chemistry.organic']
BIOLOGY = ['biology.cell', 'biology.hormones', 'biology.diseases', 'biology.plant_physiology', 'biology.concepts', 'biology.genetics',
           'biology.human_physiology', 'biology.ecology', 'biology.taxonomy']
MATHS_ADV = ['math.c11.sets_functions', 'math.c11.trigonometric_functions', 'math.c11.complex', 'math.c11.pnc_binomial',
             'math.c11.sequences', 'math.c11.straight_lines', 'math.c11.limits_derivatives', 'math.c11.statistics_probability',
             'math.c12.matrices', 'math.c12.determinant3', 'math.c12.calculus', 'math.c12.integrals', 'math.c12.vectors_3d',
             'math.c12.lpp_probability', 'math.c10.quadratic']
MATHS_10 = ['math.c10.real_numbers', 'math.c10.pair_linear', 'math.c10.quadratic', 'math.c10.ap', 'math.c10.coordinate',
            'math.c10.trigonometry', 'math.c10.statistics', 'math.c10.probability', 'math.c10.circles_areas', 'math.c9.polynomials',
            'math.c9.surface_volume', 'math.c9.herons_area']
ENGG_MATHS = ['math.c12.matrices', 'math.c12.determinant3', 'math.c12.calculus', 'math.c12.integrals', 'quant.probability',
              'math.c11.statistics_probability', 'math.c11.sets_functions', 'math.c12.vectors_3d']
CS = ['programming.python', 'programming.c', 'dsa.structures', 'dsa.complexity', 'dbms.sql', 'digital.logic',
      'programming.number_systems', 'cs.theory']
MEDICAL = ['medicine.pharmacology', 'medicine.antidotes', 'medicine.clinical_signs', 'medicine.anatomy', 'medicine.clinical',
           'medicine.microbiology', 'medicine.pathology', 'medicine.psm', 'medicine.side_effects', 'medicine.obg_paeds']
COMPUTER = ['cs.awareness', 'programming.number_systems', 'cs.abbreviations', 'cs.shortcuts']
TEACHING = ['teaching.theorists', 'teaching.pedagogy']


@dataclass
class Sec:
    code: str              # Subject code
    name: str              # section name shown on the paper
    count: int
    marks: float
    negative: float
    topics: list
    numeric: int = 0       # how many of `count` are numerical-answer (typed) questions


@dataclass
class Exam:
    name: str
    minutes: int
    sections: list
    pattern: str
    difficulty: str = 'medium'
    mocks: int = 3
    pyp: int = 2
    group: str = ''        # EXAM_GROUPS key, for exams added in 2026
    icon: str = 'graduation-cap'
    color: str = '#667eea'
    note: str = ''
    light: bool = False    # catalog exams: 2 full mocks, a few topic tests and a demo

    @property
    def total(self):
        return sum(s.count for s in self.sections)

    @property
    def total_marks(self):
        return sum(s.count * s.marks for s in self.sections)


def S(code, name, count, marks, negative, topics, numeric=0):
    return Sec(code, name, count, marks, negative, list(topics), numeric)


def ssc4(name, minutes, n, marks, neg, pattern, english=True, **kw):
    """SSC-style four-section paper."""
    secs = [S('RSN1', 'General Intelligence & Reasoning', n, marks, neg, REASON),
            S('GA1', 'General Awareness', n, marks, neg, GA),
            S('QNT1', 'Quantitative Aptitude', n, marks, neg, QUANT)]
    if english:
        secs.append(S('ENG1', 'English Comprehension', n, marks, neg, ENGLISH))
    return Exam(name, minutes, secs, pattern, **kw)


def bank3(name, minutes, eng, quant, rsn, neg, pattern, quant_name='Quantitative Aptitude', **kw):
    secs = []
    if eng:
        secs.append(S('ENG1', 'English Language', eng, 1, neg, ENGLISH_BANK))
    secs.append(S('QNT1', quant_name, quant, 1, neg, QUANT_BANK))
    secs.append(S('RSN1', 'Reasoning Ability', rsn, 1, neg, REASON_BANK))
    return Exam(name, minutes, secs, pattern, **kw)


def gate(name, code, label, mcq_topics, nat_topics, paper, **kw):
    """GATE paper: GA 10 questions (15 marks) + 55 core questions (85 marks), 1- and 2-mark MCQs and NATs."""
    return Exam(name, 180, [
        S('RSN1', 'General Aptitude (1 mark)', 5, 1, 0.33, ['quant.percentage', 'quant.ratio', 'reasoning.number_series', 'english.grammar', 'english.synonym']),
        S('RSN1', 'General Aptitude (2 marks)', 5, 2, 0.67, ['quant.probability', 'quant.di', 'reasoning.direction', 'reasoning.inequality', 'english.comprehension']),
        S(code, f'{label} – MCQ (1 mark)', 17, 1, 0.33, mcq_topics),
        S(code, f'{label} – NAT (1 mark)', 8, 1, 0, nat_topics, numeric=8),
        S(code, f'{label} – MCQ (2 marks)', 20, 2, 0.67, mcq_topics),
        S(code, f'{label} – NAT (2 marks)', 10, 2, 0, nat_topics, numeric=10),
    ], f"{paper} paper: 65 questions, 100 marks, 3 hours (General Aptitude 15 marks, Engineering Maths + core subject 85 marks). "
       "MCQ: −1/3 (1-mark) and −2/3 (2-mark); numerical-answer questions have no negative marking. Virtual scientific calculator.",
       'hard', mocks=2, pyp=1, group='engineering', **kw)


EXAMS = [
    # ---------------------------------------------------------------- Engineering
    Exam('JEE Main', 180, [
        S('PHY1', 'Physics', 25, 4, 1, PHYSICS, numeric=5),
        S('CHE1', 'Chemistry', 25, 4, 1, CHEMISTRY, numeric=5),
        S('MAT1', 'Mathematics', 25, 4, 1, MATHS_ADV, numeric=5),
    ], "75 questions (25 each in Physics, Chemistry and Mathematics: 20 MCQs + 5 numerical-value questions, all compulsory), "
       "300 marks, 3 hours. +4 for a correct answer, −1 for a wrong one (MCQ and numerical).", 'hard'),
    Exam('JEE Advanced', 180, [
        S('PHY1', 'Physics – MCQ', 12, 3, 1, PHYSICS), S('PHY1', 'Physics – Numerical', 6, 4, 0, PHYSICS, numeric=6),
        S('CHE1', 'Chemistry – MCQ', 12, 3, 1, CHEMISTRY), S('CHE1', 'Chemistry – Numerical', 6, 4, 0, CHEMISTRY, numeric=6),
        S('MAT1', 'Mathematics – MCQ', 12, 3, 1, MATHS_ADV), S('MAT1', 'Mathematics – Numerical', 6, 4, 0, MATHS_ADV, numeric=6),
    ], "Two compulsory 3-hour papers. The structure changes every year; each mock follows one paper: per subject 12 objective "
       "questions (+3 / −1) and 6 numerical-answer questions (+4, no negative).", 'expert', mocks=3, pyp=2),
    Exam('BITSAT', 180, [
        S('PHY1', 'Physics', 30, 3, 1, PHYSICS), S('CHE1', 'Chemistry', 30, 3, 1, CHEMISTRY),
        S('ENG1', 'English Proficiency', 10, 3, 1, ENGLISH), S('RSN1', 'Logical Reasoning', 20, 3, 1, REASON),
        S('MAT1', 'Mathematics', 40, 3, 1, MATHS_ADV),
    ], "130 questions (Physics 30, Chemistry 30, English 10, Logical Reasoning 20, Mathematics 40), 390 marks, 3 hours. +3 / −1.", 'hard'),
    Exam('VITEEE', 150, [
        S('MAT1', 'Mathematics', 40, 1, 0, MATHS_ADV), S('PHY1', 'Physics', 35, 1, 0, PHYSICS),
        S('CHE1', 'Chemistry', 35, 1, 0, CHEMISTRY), S('RSN1', 'Aptitude', 10, 1, 0, REASON), S('ENG1', 'English', 5, 1, 0, ENGLISH),
    ], "125 questions (Maths 40, Physics 35, Chemistry 35, Aptitude 10, English 5), 125 marks, 150 minutes. No negative marking."),
    Exam('MHT CET', 180, [
        S('PHY1', 'Physics', 50, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 50, 1, 0, CHEMISTRY), S('MAT1', 'Mathematics', 50, 2, 0, MATHS_ADV),
    ], "PCM group: 150 questions (Physics 50, Chemistry 50 at 1 mark; Mathematics 50 at 2 marks), 200 marks, 3 hours. No negative marking."),
    Exam('WBJEE', 240, [
        S('MAT1', 'Mathematics', 75, 1, 0.25, MATHS_ADV), S('PHY1', 'Physics', 40, 1, 0.25, PHYSICS), S('CHE1', 'Chemistry', 40, 1, 0.25, CHEMISTRY),
    ], "155 questions in two papers (Paper 1 Maths 75; Paper 2 Physics 40 + Chemistry 40), 2 hours each. Category-1 questions +1 / −¼.", mocks=2, pyp=1),
    Exam('KCET', 240, [
        S('PHY1', 'Physics', 60, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 60, 1, 0, CHEMISTRY), S('MAT1', 'Mathematics', 60, 1, 0, MATHS_ADV),
    ], "180 questions (60 each in Physics, Chemistry, Mathematics), 1 mark each, 80 minutes per subject. No negative marking.", mocks=2, pyp=1),
    Exam('AP EAPCET', 180, [
        S('MAT1', 'Mathematics', 80, 1, 0, MATHS_ADV), S('PHY1', 'Physics', 40, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 40, 1, 0, CHEMISTRY),
    ], "Engineering stream: 160 questions (Maths 80, Physics 40, Chemistry 40), 160 marks, 3 hours. No negative marking.", mocks=2, pyp=1),
    Exam('TS EAPCET', 180, [
        S('MAT1', 'Mathematics', 80, 1, 0, MATHS_ADV), S('PHY1', 'Physics', 40, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 40, 1, 0, CHEMISTRY),
    ], "Engineering stream: 160 questions (Maths 80, Physics 40, Chemistry 40), 160 marks, 3 hours. No negative marking.", mocks=2, pyp=1),
    Exam('GATE', 180, [
        S('RSN1', 'General Aptitude (1 mark)', 5, 1, 0.33, ['quant.percentage', 'quant.ratio', 'reasoning.number_series', 'english.grammar', 'english.synonym']),
        S('RSN1', 'General Aptitude (2 marks)', 5, 2, 0.67, ['quant.probability', 'quant.di', 'reasoning.direction', 'reasoning.inequality', 'english.comprehension']),
        S('CSE1', 'CS & IT – MCQ (1 mark)', 17, 1, 0.33, CS + ENGG_MATHS),
        S('CSE1', 'CS & IT – NAT (1 mark)', 8, 1, 0, CS + ENGG_MATHS, numeric=8),
        S('CSE1', 'CS & IT – MCQ (2 marks)', 20, 2, 0.67, CS + ENGG_MATHS),
        S('CSE1', 'CS & IT – NAT (2 marks)', 10, 2, 0, CS + ENGG_MATHS, numeric=10),
    ], "Computer Science & IT paper: 65 questions, 100 marks, 3 hours (General Aptitude 15 marks, Engineering Maths + CS 85 marks). "
       "MCQ: −1/3 (1-mark) and −2/3 (2-mark); numerical-answer questions have no negative marking. Virtual scientific calculator.", 'hard'),
    gate('GATE EE', 'PHY1', 'Electrical Engineering', ['engineering.electrical', 'physics.electricity', 'digital.logic', 'engineering.core'] + ENGG_MATHS, ['engineering.electrical', 'physics.electricity'] + ENGG_MATHS, 'Electrical Engineering', icon='bolt', color='#ca8a04'),
    gate('GATE ME', 'CIV1', 'Mechanical Engineering', ['engineering.mechanical', 'physics.heat_matter', 'physics.force_energy', 'engineering.core'] + ENGG_MATHS, ['engineering.mechanical', 'physics.force_energy', 'physics.kinematics'] + ENGG_MATHS, 'Mechanical Engineering', icon='gear', color='#475569'),
    gate('GATE CE', 'CIV1', 'Civil Engineering', ['engineering.core', 'engineering.mechanical', 'quant.mensuration', 'physics.force_energy'] + ENGG_MATHS, ['engineering.mechanical', 'quant.mensuration'] + ENGG_MATHS, 'Civil Engineering', icon='helmet-safety', color='#78716c'),
    Exam('UPSC ESE', 120, [
        S('GA1', 'Current Issues & General Studies', 30, 2, 0.66, UPSC_GS),
        S('RSN1', 'Engineering Aptitude & Reasoning', 30, 2, 0.66, REASON + QUANT_BASIC),
        S('CIV1', 'Engineering Mathematics & Basics', 25, 2, 0.66, ['engineering.core', 'engineering.electrical', 'engineering.mechanical'] + ENGG_MATHS),
        S('CMP1', 'ICT, Ethics & Environment', 15, 2, 0.66, ['cs.awareness', 'environment.ecology', 'ga.science']),
    ], "Prelims Paper I (General Studies & Engineering Aptitude): 100 questions, 200 marks, 2 hours. −⅓ of the marks for a wrong answer.", 'hard', mocks=2, pyp=1),
    Exam('NATA', 90, [
        S('DSG1', 'Visual & Design Aptitude', 25, 2, 0, ['design.aptitude', 'reasoning.cubes', 'reasoning.analogy']),
        S('MAT1', 'Mathematics & Logical Reasoning', 15, 2, 0, ['quant.mensuration', 'math.c10.coordinate', 'reasoning.number_series', 'math.c10.trigonometry']),
        S('GA1', 'General Awareness & Architecture', 10, 2, 0, ['design.architecture', 'ga.culture', 'ga.inventions']),
    ], "Part B (online aptitude): 50 questions, 90 minutes, no negative marking. Part A (drawing & composition) is a pen-and-paper test and is not included.",
       mocks=2, pyp=1),
    Exam('Polytechnic Entrance', 150, [
        S('MAT1', 'Mathematics', 50, 1, 0.25, MATHS_10), S('PHY1', 'Physics', 35, 1, 0.25, PHYSICS[:5] + ['physics.units']),
        S('CHE1', 'Chemistry', 35, 1, 0.25, CHEMISTRY[:5]),
    ], "Class 10-level PCM paper as used by most state polytechnic entrances (JEECUP, DCECE, Delhi CET, etc.): 120 questions, 150 minutes. "
       "Exact counts and negative marking vary by state.", mocks=2, pyp=1),

    # ---------------------------------------------------------------- Medical
    Exam('NEET UG', 180, [
        S('PHY1', 'Physics', 45, 4, 1, PHYSICS), S('CHE1', 'Chemistry', 45, 4, 1, CHEMISTRY),
        S('BIO1', 'Biology (Botany & Zoology)', 90, 4, 1, BIOLOGY),
    ], "180 compulsory questions (Physics 45, Chemistry 45, Botany 45, Zoology 45), 720 marks, 3 hours (pen-and-paper). +4 / −1. "
       "The optional Section B was removed from 2025.", 'hard'),
    Exam('AIIMS', 180, [
        S('PHY1', 'Physics', 45, 4, 1, PHYSICS), S('CHE1', 'Chemistry', 45, 4, 1, CHEMISTRY),
        S('BIO1', 'Biology (Botany & Zoology)', 90, 4, 1, BIOLOGY),
    ], "AIIMS MBBS seats are filled through NEET UG since 2020. These are AIIMS-level (harder) mocks in the NEET pattern: 180 questions, "
       "720 marks, 3 hours, +4 / −1.", 'expert', mocks=2, pyp=1),
    Exam('NEET PG', 210, [S('MED1', 'Clinical, Para-clinical & Pre-clinical Subjects', 200, 4, 1, MEDICAL)],
         "200 MCQs, 800 marks, 3.5 hours (computer-based). +4 / −1.", 'expert', mocks=2, pyp=1),
    Exam('NEET MDS', 180, [S('DEN1', 'Dental Subjects', 160, 4, 1, ['dentistry.core'] + MEDICAL), S('MED1', 'Medical Subjects', 80, 4, 1, MEDICAL)],
         "240 MCQs, 960 marks, 3 hours. +4 / −1.", 'expert', mocks=1, pyp=1),
    Exam('FMGE', 150, [S('MED1', 'Part A – Pre-clinical, Para-clinical & Clinical', 150, 1, 0, MEDICAL)],
         "300 MCQs in two parts of 150 (150 minutes each), 1 mark each, no negative marking. Pass mark 150/300. Each mock is one part.",
         'hard', mocks=2, pyp=1),
    Exam('AIIMS NORCET', 90, [
        S('NUR1', 'Nursing', 90, 1, 0.33, ['nursing.core', 'medicine.clinical', 'medicine.pharmacology', 'biology.human_physiology', 'medicine.microbiology']),
        S('GA1', 'General Knowledge & Aptitude', 10, 1, 0.33, ['ga.science', 'ga.polity', 'reasoning.number_series', 'quant.percentage']),
    ], "Stage 1 (prelims): 100 MCQs (Nursing 90, General Knowledge & Aptitude 10), 90 minutes. −⅓ for a wrong answer.", mocks=2, pyp=1),
    Exam('UPSC CMS', 120, [S('MED1', 'General Medicine & Paediatrics', 120, 2.08, 0.69, MEDICAL)],
         "Paper I: 120 questions (General Medicine 96, Paediatrics 24), 250 marks, 2 hours. −⅓ of the marks for a wrong answer.", 'hard', mocks=2, pyp=1),

    # ---------------------------------------------------------------- SSC & Railways
    ssc4('SSC CGL', 60, 25, 2, 0.5, "Tier 1: 100 questions (Reasoning, General Awareness, Quantitative Aptitude, English – 25 each), 200 marks, "
         "60 minutes. +2 / −0.5."),
    ssc4('SSC CHSL', 60, 25, 2, 0.5, "Tier 1: 100 questions (English, Reasoning, Quantitative Aptitude, General Awareness – 25 each), 200 marks, "
         "60 minutes. +2 / −0.5."),
    Exam('SSC MTS', 90, [
        S('QNT1', 'Session I – Numerical & Mathematical Ability', 20, 3, 0, QUANT_BASIC),
        S('RSN1', 'Session I – Reasoning Ability & Problem Solving', 20, 3, 0, REASON),
        S('GA1', 'Session II – General Awareness', 25, 3, 1, GA),
        S('ENG1', 'Session II – English Language & Comprehension', 25, 3, 1, ENGLISH),
    ], "90 questions, 270 marks, two sessions of 45 minutes. Session I has no negative marking; Session II has −1 per wrong answer."),
    Exam('SSC GD', 60, [
        S('RSN1', 'General Intelligence & Reasoning', 20, 2, 0.25, REASON), S('GA1', 'General Knowledge & Awareness', 20, 2, 0.25, GA),
        S('QNT1', 'Elementary Mathematics', 20, 2, 0.25, QUANT_BASIC), S('ENG1', 'English / Hindi', 20, 2, 0.25, ENGLISH),
    ], "80 questions (20 each), 160 marks, 60 minutes. +2 / −0.25."),
    Exam('SSC JE', 120, [
        S('RSN1', 'General Intelligence & Reasoning', 50, 1, 0.25, REASON), S('GA1', 'General Awareness', 50, 1, 0.25, GA),
        S('CIV1', 'General Engineering (Civil / Electrical / Mechanical)', 100, 1, 0.25, ['engineering.core', 'engineering.electrical', 'engineering.mechanical', 'physics.electricity', 'physics.heat_matter']),
    ], "Paper I: 200 questions (Reasoning 50, General Awareness 50, Engineering 100), 200 marks, 2 hours. −0.25 per wrong answer.", mocks=2, pyp=1),
    Exam('SSC Stenographer', 120, [
        S('RSN1', 'General Intelligence & Reasoning', 50, 1, 0.25, REASON), S('GA1', 'General Awareness', 50, 1, 0.25, GA),
        S('ENG1', 'English Language & Comprehension', 100, 1, 0.25, ENGLISH),
    ], "200 questions (Reasoning 50, General Awareness 50, English 100), 200 marks, 2 hours. −0.25 per wrong answer.", mocks=2, pyp=1),
    ssc4('SSC CPO', 120, 50, 1, 0.25, "Paper I: 200 questions (Reasoning, General Knowledge, Quantitative Aptitude, English – 50 each), 200 marks, "
         "2 hours. −0.25 per wrong answer.", mocks=2, pyp=1, group='ssc-railway', icon='user-shield', color='#1d4ed8'),
    ssc4('SSC Selection Post', 60, 25, 2, 0.5, "Phase-wise posts (Matric, Higher Secondary, Graduate level): 100 questions (25 each), 200 marks, "
         "60 minutes. +2 / −0.5.", mocks=2, pyp=1, group='ssc-railway', icon='id-card', color='#0f766e'),
    Exam('RRB NTPC', 90, [
        S('QNT1', 'Mathematics', 30, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 30, 1, 0.33, REASON),
        S('GA1', 'General Awareness', 40, 1, 0.33, GA + GEN_SCIENCE[:3]),
    ], "CBT-1: 100 questions (Mathematics 30, Reasoning 30, General Awareness 40), 90 minutes. −⅓ per wrong answer."),
    Exam('RRB Group D', 90, [
        S('QNT1', 'Mathematics', 25, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 30, 1, 0.33, REASON),
        S('SCI1', 'General Science', 25, 1, 0.33, GEN_SCIENCE), S('GA1', 'General Awareness & Current Affairs', 20, 1, 0.33, GA),
    ], "Level-1 CBT: 100 questions (Maths 25, Reasoning 30, General Science 25, General Awareness 20), 90 minutes. −⅓ per wrong answer."),
    Exam('RRB ALP', 60, [
        S('QNT1', 'Mathematics', 20, 1, 0.33, QUANT_BASIC), S('RSN1', 'Mental Ability', 25, 1, 0.33, REASON),
        S('SCI1', 'General Science', 20, 1, 0.33, GEN_SCIENCE), S('GA1', 'General Awareness', 10, 1, 0.33, GA),
    ], "CBT-1: 75 questions, 60 minutes. −⅓ per wrong answer."),
    Exam('RRB JE', 90, [
        S('QNT1', 'Mathematics', 30, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 25, 1, 0.33, REASON),
        S('GA1', 'General Awareness', 15, 1, 0.33, GA), S('SCI1', 'General Science', 30, 1, 0.33, GEN_SCIENCE),
    ], "CBT-1: 100 questions (Maths 30, Reasoning 25, General Awareness 15, General Science 30), 90 minutes. −⅓ per wrong answer."),

    # ---------------------------------------------------------------- Banking & Insurance
    bank3('IBPS PO', 60, 30, 35, 35, 0.25, "Prelims: 100 questions (English 30, Quantitative Aptitude 35, Reasoning 35), 100 marks, 60 minutes "
          "(20 minutes per section). −0.25 per wrong answer."),
    bank3('IBPS Clerk', 60, 30, 35, 35, 0.25, "Prelims: 100 questions (English 30, Numerical Ability 35, Reasoning 35), 60 minutes. −0.25.", quant_name='Numerical Ability'),
    bank3('SBI PO', 60, 40, 30, 30, 0.25, "Prelims: 100 questions (English 40, Quantitative Aptitude 30, Reasoning 30), 100 marks, 60 minutes. −0.25."),
    bank3('SBI Clerk', 60, 40, 30, 30, 0.25, "Prelims: 100 questions (English 40, Numerical Ability 30, Reasoning 30), 60 minutes. −0.25.", quant_name='Numerical Ability'),
    bank3('IBPS RRB PO', 45, 0, 40, 40, 0.25, "Officer Scale-I prelims: 80 questions (Reasoning 40, Quantitative Aptitude 40), 45 minutes. −0.25."),
    bank3('IBPS RRB Clerk', 45, 0, 40, 40, 0.25, "Office Assistant prelims: 80 questions (Reasoning 40, Numerical Ability 40), 45 minutes. −0.25.", quant_name='Numerical Ability'),
    bank3('RBI Assistant', 60, 30, 35, 35, 0.25, "Prelims: 100 questions (English 30, Numerical Ability 35, Reasoning 35), 60 minutes. −0.25.",
          quant_name='Numerical Ability', group='banking', icon='building-columns', color='#0369a1', mocks=2, pyp=1),
    Exam('RBI Grade B', 120, [
        S('GA1', 'General Awareness', 80, 1, 0.25, GA_BANK + GA[:6]), S('RSN1', 'Reasoning', 60, 1, 0.25, REASON_BANK),
        S('QNT1', 'Quantitative Aptitude', 30, 1, 0.25, QUANT_BANK), S('ENG1', 'English Language', 30, 1, 0.25, ENGLISH_BANK),
    ], "Phase I: 200 questions (General Awareness 80, Reasoning 60, Quant 30, English 30), 200 marks, 120 minutes. −0.25.", 'hard', mocks=2, pyp=1),
    Exam('NABARD Grade A', 120, [
        S('RSN1', 'Reasoning', 20, 1, 0.25, REASON_BANK), S('ENG1', 'English Language', 30, 1, 0.25, ENGLISH_BANK),
        S('CMP1', 'Computer Knowledge', 20, 1, 0.25, COMPUTER), S('QNT1', 'Quantitative Aptitude', 20, 1, 0.25, QUANT_BANK),
        S('DM1', 'Decision Making', 10, 1, 0.25, ['management.decision']), S('GA1', 'General Awareness', 20, 1, 0.25, GA_BANK),
        S('ECO1', 'Economic & Social Issues', 40, 1, 0.25, ['commerce.economics', 'ga.economy', 'environment.ecology']),
        S('ARD1', 'Agriculture & Rural Development', 40, 1, 0.25, ['agriculture.core', 'biology.plant_physiology', 'environment.ecology']),
    ], "Phase I: 200 questions, 200 marks, 120 minutes. −0.25 per wrong answer.", 'hard', mocks=2, pyp=1),
    Exam('SEBI Grade A', 60, [
        S('GA1', 'General Awareness (incl. Financial Sector)', 25, 1, 0.25, GA_BANK), S('ENG1', 'English Language', 25, 1, 0.25, ENGLISH_BANK),
        S('QNT1', 'Quantitative Aptitude', 25, 1, 0.25, QUANT_BANK), S('RSN1', 'Test of Reasoning', 25, 1, 0.25, REASON_BANK),
    ], "Phase I Paper 1: 100 questions, 100 marks, 60 minutes. −0.25 per wrong answer.", 'hard', mocks=2, pyp=1),
    bank3('LIC AAO', 60, 30, 35, 35, 0.25, "Prelims: 100 questions (Reasoning 35, Quantitative Aptitude 35, English 30), 60 minutes. −0.25. English is qualifying "
          "in the real exam.", mocks=2, pyp=1),

    # ---------------------------------------------------------------- Defence & Police
    Exam('NDA', 150, [S('MAT1', 'Mathematics', 120, 2.5, 0.83, MATHS_ADV + MATHS_10[:4])],
         "Paper I Mathematics: 120 questions, 300 marks, 2½ hours (+2.5 / −0.83). Paper II GAT (150 questions, 600 marks) is in the GAT mocks.", 'hard'),
    Exam('NDA GAT', 150, [
        S('ENG1', 'English', 50, 4, 1.33, ENGLISH), S('PHY1', 'General Knowledge – Physics', 25, 4, 1.33, PHYSICS[:6]),
        S('CHE1', 'General Knowledge – Chemistry', 15, 4, 1.33, CHEMISTRY[:5]), S('BIO1', 'General Science', 10, 4, 1.33, BIOLOGY[:5]),
        S('GA1', 'History, Geography, Polity & Current Events', 50, 4, 1.33, GA),
    ], "Paper II General Ability Test: 150 questions (English 50, General Knowledge 100), 600 marks, 2½ hours. +4 / −1.33.",
       'hard', mocks=2, pyp=1, group='defence-police', icon='jet-fighter', color='#1e3a8a'),
    Exam('CDS', 120, [S('ENG1', 'English', 120, 0.83, 0.28, ENGLISH)],
         "Each CDS paper is 2 hours: English (120 questions, 100 marks), General Knowledge (120 questions, 100 marks) and Elementary Mathematics "
         "(100 questions, 100 marks). −⅓ of the marks for a wrong answer. These mocks are the English paper; GK and Maths mocks are listed separately.", 'medium', mocks=2, pyp=1),
    Exam('CDS GK', 120, [S('GA1', 'General Knowledge', 120, 0.83, 0.28, GA + GEN_SCIENCE[:5])],
         "General Knowledge paper: 120 questions, 100 marks, 2 hours. −⅓ of the marks for a wrong answer.", mocks=2, pyp=1,
         group='defence-police', icon='earth-asia', color='#166534'),
    Exam('CDS Maths', 120, [S('MAT1', 'Elementary Mathematics', 100, 1, 0.33, MATHS_10 + QUANT_BASIC)],
         "Elementary Mathematics paper (IMA, INA, AFA): 100 questions, 100 marks, 2 hours. −⅓ per wrong answer.", mocks=2, pyp=1,
         group='defence-police', icon='square-root-variable', color='#7c2d12'),
    Exam('AFCAT', 120, [
        S('GA1', 'General Awareness', 25, 3, 1, GA), S('ENG1', 'Verbal Ability in English', 30, 3, 1, ENGLISH),
        S('QNT1', 'Numerical Ability', 20, 3, 1, QUANT_BASIC), S('RSN1', 'Reasoning & Military Aptitude', 25, 3, 1, REASON),
    ], "100 questions, 300 marks, 2 hours. +3 / −1."),
    Exam('CAPF Assistant Commandant', 120, [
        S('GA1', 'General Studies & Current Events', 70, 2, 0.66, UPSC_GS), S('QNT1', 'General Mental Ability', 25, 2, 0.66, REASON + QUANT_BASIC),
        S('SCI1', 'General Science', 30, 2, 0.66, GEN_SCIENCE),
    ], "Paper I (General Ability & Intelligence): 125 questions, 250 marks, 2 hours. −⅓ of the marks for a wrong answer.", mocks=2, pyp=1),
    Exam('Indian Air Force', 60, [
        S('ENG1', 'English', 20, 1, 0.25, ENGLISH), S('PHY1', 'Physics', 25, 1, 0.25, PHYSICS[:6]), S('MAT1', 'Mathematics', 25, 1, 0.25, MATHS_10),
    ], "Agniveervayu (Science subjects): 70 questions (English 20, Physics 25, Maths 25), 60 minutes. +1 / −0.25."),
    Exam('Indian Army GD', 60, [
        S('GA1', 'General Knowledge', 15, 2, 0.5, GA), S('SCI1', 'General Science', 15, 2, 0.5, GEN_SCIENCE),
        S('QNT1', 'Mathematics', 15, 2, 0.5, QUANT_BASIC), S('RSN1', 'Logical Reasoning', 5, 2, 0.5, REASON),
    ], "Agniveer GD online CEE: 50 questions, 100 marks, 60 minutes. +2 / −0.5."),
    Exam('Indian Navy Agniveer', 60, [
        S('ENG1', 'English', 25, 1, 0.25, ENGLISH), S('SCI1', 'Science', 25, 1, 0.25, GEN_SCIENCE),
        S('MAT1', 'Mathematics', 25, 1, 0.25, MATHS_10), S('GA1', 'General Awareness', 25, 1, 0.25, GA),
    ], "Agniveer (SSR) INET: 100 questions (English, Science, Maths, General Awareness – 25 each), 60 minutes. +1 / −0.25."),
    Exam('Indian Coast Guard', 60, [
        S('MAT1', 'Mathematics', 20, 1, 0, MATHS_10), S('PHY1', 'Physics', 15, 1, 0, PHYSICS[:6]), S('ENG1', 'English', 15, 1, 0, ENGLISH),
        S('GA1', 'General Awareness & Reasoning', 10, 1, 0, GA + REASON[:4]),
    ], "Navik (GD) Section I + II: 60-question computer-based test, 60 minutes. No negative marking."),
    Exam('Sub Inspector (SI)', 120, [
        S('RSN1', 'Reasoning', 50, 1, 0.25, REASON), S('GA1', 'General Knowledge', 50, 1, 0.25, GA),
        S('QNT1', 'Quantitative Aptitude', 50, 1, 0.25, QUANT_BASIC), S('ENG1', 'English / Hindi', 50, 1, 0.25, ENGLISH),
    ], "State and central SI written tests follow a similar 200-question, 2-hour format (e.g. SSC CPO). −0.25 per wrong answer.", mocks=2, pyp=1),
    Exam('State Police Constable', 120, [
        S('GA1', 'General Knowledge', 38, 2, 0.5, GA), S('RSN1', 'Mental Aptitude, IQ & Reasoning', 38, 2, 0.5, REASON),
        S('QNT1', 'Numerical Ability', 37, 2, 0.5, QUANT_BASIC), S('HIN1', 'General Hindi / Language', 37, 2, 0.5, ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.grammar', 'hindi.sandhi']),
    ], "UP Police Constable style: 150 questions, 300 marks, 2 hours. +2 / −0.5. Other states use similar formats.", mocks=2, pyp=1),
    Exam('Delhi Police Constable', 90, [
        S('GA1', 'General Knowledge & Current Affairs', 50, 1, 0.25, GA), S('RSN1', 'Reasoning', 25, 1, 0.25, REASON),
        S('QNT1', 'Numerical Ability', 15, 1, 0.25, QUANT_BASIC), S('CMP1', 'Computer Fundamentals', 10, 1, 0.25, COMPUTER),
    ], "100 questions (GK 50, Reasoning 25, Numerical 15, Computer 10), 100 marks, 90 minutes. −0.25."),
    Exam('RPF Constable', 90, [
        S('GA1', 'General Awareness', 50, 1, 0.33, GA), S('QNT1', 'Arithmetic', 35, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 35, 1, 0.33, REASON),
    ], "CBT: 120 questions (General Awareness 50, Arithmetic 35, Reasoning 35), 90 minutes. −⅓ per wrong answer."),

    # ---------------------------------------------------------------- Civil services & state PSC
    Exam('UPSC Civil Services', 120, [S('GA1', 'General Studies Paper I', 100, 2, 0.66, UPSC_GS)],
         "Prelims GS Paper I: 100 questions, 200 marks, 2 hours. −⅓ of the marks (0.66) for a wrong answer. CSAT (Paper II, qualifying 33%) mocks are listed separately.", 'expert'),
    Exam('UPSC CSAT', 120, [
        S('ENG1', 'Comprehension', 30, 2.5, 0.83, ['english.comprehension', 'english.sentence_improvement']),
        S('RSN1', 'Logical Reasoning & Analytical Ability', 25, 2.5, 0.83, REASON_BANK + ['reasoning.number_series']),
        S('QNT1', 'Basic Numeracy & Data Interpretation', 25, 2.5, 0.83, QUANT + ['quant.di']),
    ], "Prelims Paper II (qualifying, 33%): 80 questions, 200 marks, 2 hours. −⅓ of the marks for a wrong answer.", 'hard', mocks=2, pyp=1,
       group='civil-services', icon='scale-balanced', color='#9a3412'),
    Exam('State PSC', 120, [S('GA1', 'General Studies', 150, 2, 0.66, UPSC_GS + ['ga.states', 'ga.culture'])],
         "Typical state PSC prelims GS paper (UPPSC, BPSC, MPPSC, RPSC RAS…): 150 questions, 2 hours. Marks and negative marking vary by state.", 'hard', mocks=2, pyp=1),
    Exam('UPSC EPFO', 120, [
        S('GA1', 'General Studies & Indian Polity', 50, 2.5, 0.83, UPSC_GS), S('ECO1', 'Economy, Labour Laws & Social Security', 30, 2.5, 0.83, ['commerce.economics', 'ga.economy', 'commerce.business_law']),
        S('RSN1', 'General Mental Ability & Quantitative Aptitude', 20, 2.5, 0.83, REASON + QUANT_BASIC), S('CMP1', 'Computers & Accounting', 20, 2.5, 0.83, COMPUTER + ['commerce.accounting_theory']),
    ], "Recruitment test (EO/AO, APFC): 120 questions, 300 marks, 2 hours. −⅓ of the marks for a wrong answer.", mocks=2, pyp=1),
    Exam('Judicial Services', 120, [
        S('LGL1', 'Law (Constitution, Contract, Torts, Criminal Law)', 100, 1, 0.25, ['law.maxims', 'law.cases', 'law.legal_reasoning', 'ga.polity_articles', 'ga.polity', 'commerce.business_law']),
        S('GA1', 'General Knowledge', 25, 1, 0.25, GA), S('ENG1', 'English', 25, 1, 0.25, ENGLISH),
    ], "Typical PCS-J / Civil Judge prelims: 150 objective questions, 2 hours (patterns differ by state).", 'hard', mocks=2, pyp=1),

    # ---------------------------------------------------------------- MBA & Law
    Exam('CAT', 120, [
        S('ENG1', 'Verbal Ability & Reading Comprehension', 24, 3, 1, ['english.comprehension', 'english.sentence_improvement', 'english.grammar']),
        S('DI1', 'Data Interpretation & Logical Reasoning', 22, 3, 1, ['quant.di', 'reasoning.inequality', 'reasoning.ranking', 'reasoning.blood_relation']),
        S('QNT1', 'Quantitative Ability', 16, 3, 1, QUANT), S('QNT1', 'Quantitative Ability – TITA', 6, 3, 0, QUANT, numeric=6),
    ], "68 questions (VARC 24, DILR 22, QA 22), 204 marks, 120 minutes (40 per section). +3 / −1 on MCQs; no negative on type-in answers.", 'hard'),
    Exam('XAT', 165, [
        S('ENG1', 'Verbal & Logical Ability', 26, 1, 0.25, ENGLISH_BANK), S('DM1', 'Decision Making', 22, 1, 0.25, ['management.decision']),
        S('QNT1', 'Quantitative Ability & Data Interpretation', 28, 1, 0.25, QUANT),
    ], "Part 1: 76 questions (VALR 26, Decision Making 22, QADI 28), 165 minutes. −0.25; −0.10 after 8 unanswered questions. GK (Part 2) is not scored for the percentile.", 'hard'),
    Exam('MAT', 120, [
        S('ENG1', 'Language Comprehension', 30, 1, 0.25, ENGLISH), S('RSN1', 'Intelligence & Critical Reasoning', 30, 1, 0.25, REASON),
        S('DI1', 'Data Analysis & Sufficiency', 30, 1, 0.25, ['quant.di', 'quant.percentage', 'quant.ratio']), S('QNT1', 'Mathematical Skills', 30, 1, 0.25, QUANT),
        S('GA1', 'Indian & Global Environment', 30, 1, 0.25, GA_BANK),
    ], "150 questions (5 sections of 30), 150 marks, 120 minutes. −0.25 per wrong answer.", mocks=2, pyp=1),
    Exam('CMAT', 180, [
        S('QNT1', 'Quantitative Techniques & Data Interpretation', 20, 4, 1, QUANT), S('RSN1', 'Logical Reasoning', 20, 4, 1, REASON),
        S('ENG1', 'Language Comprehension', 20, 4, 1, ENGLISH), S('GA1', 'General Awareness', 20, 4, 1, GA),
        S('BST1', 'Innovation & Entrepreneurship', 20, 4, 1, ['commerce.business', 'commerce.economics']),
    ], "100 questions (5 sections of 20), 400 marks, 3 hours. +4 / −1.", mocks=2, pyp=1),
    Exam('NMAT', 120, [
        S('ENG1', 'Language Skills', 36, 3, 0, ENGLISH), S('QNT1', 'Quantitative Skills', 36, 3, 0, QUANT),
        S('RSN1', 'Logical Reasoning', 36, 3, 0, REASON + ['reasoning.inequality']),
    ], "108 questions (36 per section), 324 marks, 120 minutes. No negative marking.", mocks=2, pyp=1),
    Exam('IPMAT', 120, [
        S('QNT1', 'Quantitative Ability – Short Answer', 15, 4, 0, QUANT, numeric=15),
        S('QNT1', 'Quantitative Ability – MCQ', 30, 4, 1, QUANT), S('ENG1', 'Verbal Ability', 45, 4, 1, ENGLISH),
    ], "IIM Indore: 90 questions (QA short answer 15, QA MCQ 30, Verbal 45), 360 marks, 120 minutes. +4 / −1 (no negative on short answers).", mocks=2, pyp=1),
    Exam('CLAT', 120, [
        S('ENG1', 'English Language', 24, 1, 0.25, ['english.comprehension', 'english.grammar', 'english.idioms']),
        S('GA1', 'Current Affairs & General Knowledge', 28, 1, 0.25, GA + ['law.cases']),
        S('LGL1', 'Legal Reasoning', 32, 1, 0.25, ['law.legal_reasoning', 'law.maxims', 'law.cases', 'ga.polity_articles']),
        S('RSN1', 'Logical Reasoning', 24, 1, 0.25, ['reasoning.inequality', 'reasoning.blood_relation', 'reasoning.direction', 'reasoning.ranking']),
        S('QNT1', 'Quantitative Techniques', 12, 1, 0.25, ['quant.percentage', 'quant.ratio', 'quant.average', 'quant.di']),
    ], "UG: 120 questions (English 22–26, GK 28–32, Legal 28–32, Logical 22–26, Quant 10–14), 120 marks, 2 hours. −0.25.", 'hard'),
    Exam('AILET', 120, [
        S('ENG1', 'English Language', 50, 1, 0.25, ENGLISH), S('GA1', 'Current Affairs & GK', 30, 1, 0.25, GA),
        S('LGL1', 'Logical & Legal Reasoning', 70, 1, 0.25, ['law.legal_reasoning', 'law.maxims', 'law.cases'] + REASON_BANK[:4]),
    ], "NLU Delhi BA LLB: 150 questions (English 50, GK 30, Logical Reasoning 70), 150 marks, 2 hours. −0.25.", 'hard', mocks=2, pyp=1),

    # ---------------------------------------------------------------- University & research
    Exam('CUET UG', 60, [S('GA1', 'General Aptitude Test', 50, 5, 1, GA[:8] + QUANT_BASIC[:4] + REASON[:4])],
         "Each subject test: 50 compulsory questions, 250 marks, 60 minutes. +5 / −1. These mocks cover the General Aptitude Test; "
         "use the Class 12 series for domain subjects.", mocks=3, pyp=2),
    Exam('CUET PG', 90, [S('GA1', 'General & Domain Aptitude', 75, 4, 1, GA[:6] + REASON[:5] + QUANT_BASIC[:5] + ENGLISH[:4])],
         "75 questions, 300 marks, 90 minutes. +4 / −1.", mocks=2, pyp=1),
    Exam('IIT JAM', 180, [
        S('MAT1', 'Section A – MCQ (1 mark)', 10, 1, 0.33, MATHS_ADV), S('MAT1', 'Section A – MCQ (2 marks)', 20, 2, 0.67, MATHS_ADV),
        S('MAT1', 'Section B – MSQ-style (2 marks)', 10, 2, 0, MATHS_ADV),
        S('MAT1', 'Section C – NAT (1 mark)', 10, 1, 0, MATHS_ADV, numeric=10), S('MAT1', 'Section C – NAT (2 marks)', 10, 2, 0, MATHS_ADV, numeric=10),
    ], "60 questions, 100 marks, 3 hours (Section A 30 MCQs, Section B 10 MSQs, Section C 20 NATs). Mocks are in Mathematics; "
       "MSQ items are given as single-answer here. Virtual scientific calculator.", 'hard', mocks=2, pyp=1),
    Exam('CSIR NET', 180, [
        S('RSN1', 'Part A – General Aptitude', 15, 2, 0.5, REASON + QUANT_BASIC),
        S('BIO1', 'Part B – Life Sciences', 35, 2, 0.5, BIOLOGY), S('BIO1', 'Part C – Life Sciences (analytical)', 25, 4, 1.32, BIOLOGY),
    ], "Life Sciences paper: officially Part A 20 (attempt 15), Part B 50 (attempt 35), Part C 75 (attempt 25); 200 marks, 3 hours. "
       "Each mock gives exactly the number you must attempt.", 'expert', mocks=2, pyp=1),
    Exam('UGC NET', 180, [
        S('TCH1', 'Paper 1 – Teaching & Research Aptitude', 50, 2, 0, ['teaching.research', 'teaching.pedagogy', 'teaching.theorists', 'cs.awareness', 'quant.di', 'reasoning.inequality', 'environment.ecology']),
        S('TCH1', 'Paper 2 – Subject (Education / General)', 100, 2, 0, ['teaching.pedagogy', 'teaching.theorists', 'teaching.research', 'ga.polity', 'commerce.economics']),
    ], "150 questions (Paper 1: 50, Paper 2: 100), 300 marks, 3 hours, no negative marking. Paper 2 here follows the Education subject.", mocks=2, pyp=1),
    Exam('NIFT Entrance', 120, [
        S('DSG1', 'Communication & Design Aptitude', 30, 1, 0.25, ['design.aptitude', 'design.architecture']),
        S('ENG1', 'English Comprehension', 25, 1, 0.25, ENGLISH), S('QNT1', 'Quantitative Ability', 20, 1, 0.25, QUANT_BASIC),
        S('RSN1', 'Analytical & Logical Ability', 25, 1, 0.25, REASON), S('GA1', 'General Knowledge & Current Affairs', 20, 1, 0.25, GA),
    ], "General Ability Test (B.Des): 120 questions, 2 hours. −0.25. The Creative Ability Test is a drawing test and is not included.", mocks=2, pyp=1),
    Exam('NIMCET', 120, [
        S('MAT1', 'Mathematics', 50, 12, 3, MATHS_ADV), S('RSN1', 'Analytical Ability & Logical Reasoning', 40, 6, 1.5, REASON),
        S('CMP1', 'Computer Awareness', 20, 6, 1.5, COMPUTER + ['cs.theory', 'digital.logic']), S('ENG1', 'General English', 10, 4, 1, ENGLISH),
    ], "MCA entrance (NITs): 120 questions, 1000 marks, 2 hours. Maths +12/−3, Reasoning & Computer +6/−1.5, English +4/−1.",
       'hard', mocks=2, pyp=1, group='university', icon='laptop-code', color='#4338ca'),

    # ---------------------------------------------------------------- Teaching
    Exam('CTET', 150, [
        S('CDP1', 'Child Development & Pedagogy', 30, 1, 0, TEACHING), S('MAT1', 'Mathematics & Pedagogy', 30, 1, 0, ['math.c5.fractions', 'math.c5.lcm_hcf', 'math.c6.integers', 'math.c7.lines_angles', 'math.c8.squares_cubes', 'quant.percentage']),
        S('EVS1', 'Environmental Studies / Science', 30, 1, 0, ['evs.general', 'evs.animals', 'ga.science', 'biology.concepts']),
        S('ENG1', 'Language I – English', 30, 1, 0, ENGLISH[:7]), S('HIN1', 'Language II – Hindi', 30, 1, 0, ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.sandhi', 'hindi.grammar']),
    ], "Each paper: 150 questions, 150 marks, 2½ hours, no negative marking. Paper I (Classes 1–5) shown; Paper II has Maths & Science or Social Studies.", mocks=3, pyp=2),
    Exam('State TET', 150, [
        S('CDP1', 'Child Development & Pedagogy', 30, 1, 0, TEACHING), S('MAT1', 'Mathematics', 30, 1, 0, ['math.c5.fractions', 'math.c6.integers', 'math.c7.percentage', 'math.c8.exponents']),
        S('EVS1', 'Environmental Studies', 30, 1, 0, ['evs.general', 'ga.science', 'ga.geography']), S('ENG1', 'English', 30, 1, 0, ENGLISH[:7]),
        S('HIN1', 'Hindi / Regional Language', 30, 1, 0, ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.grammar']),
    ], "UPTET / REET / MPTET / HTET style Paper I: 150 questions, 150 marks, 2½ hours, no negative marking.", mocks=2, pyp=1),
    Exam('KVS Teacher', 180, [
        S('ENG1', 'General English & Hindi', 20, 1, 0, ENGLISH[:6]), S('GA1', 'General Awareness & Current Affairs', 10, 1, 0, GA),
        S('RSN1', 'Reasoning Ability', 10, 1, 0, REASON), S('CMP1', 'Computer Literacy', 10, 1, 0, COMPUTER),
        S('CDP1', 'Perspectives on Education & Pedagogy', 30, 1, 0, TEACHING + ['teaching.research']), S('MAT1', 'Subject Knowledge (Maths)', 100, 1, 0, MATHS_10 + MATHS_ADV[:6]),
    ], "PGT/TGT style written test: 180 questions, 180 marks, 3 hours. Subject section shown for Mathematics.", mocks=2, pyp=1),
    Exam('DSSSB', 120, [
        S('GA1', 'General Awareness', 40, 1, 0.25, GA), S('RSN1', 'General Intelligence & Reasoning', 40, 1, 0.25, REASON),
        S('QNT1', 'Arithmetical & Numerical Ability', 40, 1, 0.25, QUANT_BASIC), S('HIN1', 'Hindi Language', 40, 1, 0.25, ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.grammar', 'hindi.sandhi']),
        S('ENG1', 'English Language', 40, 1, 0.25, ENGLISH),
    ], "One-tier exam (Section A): 200 questions, 200 marks, 2 hours. −0.25 per wrong answer.", mocks=2, pyp=1),

    # ---------------------------------------------------------------- CA, CS, CMA
    Exam('CA Foundation', 120, [
        S('MAT1', 'Paper 3 – Quantitative Aptitude', 100, 1, 0.25, ['commerce.accounting'] + QUANT + ['math.c11.statistics_probability', 'math.c11.pnc_binomial', 'math.c11.sequences']),
    ], "Paper 3 Quantitative Aptitude: 100 marks, 2 hours, objective with −0.25 negative marking (Paper 4 Business Economics is listed separately).", mocks=3, pyp=2),
    Exam('CA Foundation Economics', 120, [S('ECO1', 'Paper 4 – Business Economics', 100, 1, 0.25, ['commerce.economics', 'ga.economy'])],
         "Paper 4 Business Economics: 100 marks, 2 hours, objective with −0.25 negative marking.", mocks=2, pyp=1, group='commerce', icon='chart-line', color='#b45309'),
    Exam('CA Intermediate', 180, [
        S('ACC1', 'Advanced Accounting & Cost Management', 40, 2, 0, ['commerce.accounting', 'commerce.accounting_theory']),
        S('LAW1', 'Corporate & Other Laws', 30, 2, 0, ['commerce.business_law', 'law.maxims']), S('TAX1', 'Taxation', 30, 2, 0, ['commerce.gst']),
    ], "Each paper is 100 marks (30 marks of case-based MCQs + 70 descriptive), 3 hours. These mocks practise the MCQ portion across papers.", 'hard', mocks=2, pyp=1),
    Exam('CSEET', 120, [
        S('BST1', 'Business Communication', 35, 1, 0, ENGLISH[:7]), S('LAW1', 'Legal Aptitude & Logical Reasoning', 35, 1, 0, ['commerce.business_law', 'law.maxims', 'law.legal_reasoning', 'reasoning.inequality']),
        S('ECO1', 'Economic & Business Environment', 35, 1, 0, ['commerce.economics', 'commerce.business', 'ga.economy']), S('GA1', 'Current Affairs', 15, 1, 0, GA_BANK),
    ], "120 questions, 120 marks, 2 hours, no negative marking.", mocks=2, pyp=1),
    Exam('CMA Foundation', 120, [
        S('ACC1', 'Fundamentals of Accounting & Cost', 50, 1, 0, ['commerce.accounting', 'commerce.accounting_theory']),
        S('LAW1', 'Laws & Ethics', 25, 1, 0, ['commerce.business_law']), S('QNT1', 'Business Mathematics & Statistics', 25, 1, 0, QUANT_BASIC + ['math.c11.statistics_probability']),
    ], "Objective papers, 2 hours each, 100 marks, no negative marking. Mocks mix all four papers.", mocks=2, pyp=1),

    # ---------------------------------------------------------------- Olympiads & scholarships
    Exam('NSO Science Olympiad', 60, [
        S('RSN1', 'Logical Reasoning', 10, 1, 0, REASON[:8]), S('SCI1', 'Science', 35, 1, 0, GEN_SCIENCE + ['evs.general']),
        S('SCI1', "Achievers' Section", 5, 3, 0, PHYSICS[:5] + CHEMISTRY[:3]),
    ], "Classes 3–10 (level shown: Class 8–10): 50 questions, 60 marks, 60 minutes. No negative marking.", mocks=3, pyp=2),
    Exam('IMO Maths Olympiad', 60, [
        S('RSN1', 'Logical Reasoning', 10, 1, 0, REASON[:8]), S('MAT1', 'Mathematical Reasoning', 25, 1, 0, MATHS_10[:8] + ['math.c8.exponents', 'math.c8.squares_cubes']),
        S('MAT1', 'Everyday Mathematics', 10, 1, 0, QUANT_BASIC), S('MAT1', "Achievers' Section", 5, 3, 0, MATHS_10),
    ], "50 questions, 60 marks, 60 minutes. No negative marking.", mocks=3, pyp=2),
    Exam('IEO English Olympiad', 60, [
        S('ENG1', 'Word & Structure Knowledge', 35, 1, 0, ENGLISH), S('ENG1', 'Reading', 10, 1, 0, ['english.comprehension', 'english.idioms']),
        S('ENG1', 'Spoken & Written Expression', 5, 1, 0, ['english.sentence_improvement', 'english.voice_narration']),
    ], "50 questions, 60 minutes. No negative marking.", mocks=2, pyp=1),
    Exam('NCO Cyber Olympiad', 60, [
        S('RSN1', 'Logical Reasoning', 15, 1, 0, REASON[:8]), S('CMP1', 'Computers & IT', 30, 1, 0, COMPUTER + ['digital.logic']),
        S('CMP1', "Achievers' Section", 5, 3, 0, ['programming.python', 'cs.awareness']),
    ], "50 questions, 60 marks, 60 minutes. No negative marking.", mocks=2, pyp=1),
    Exam('IOQM', 180, [S('MAT1', 'Problems (integer answers 00–99)', 30, 3, 0, ['math.c10.ap', 'quant.number_system', 'math.c11.pnc_binomial', 'math.c10.quadratic', 'math.c11.sequences'], numeric=30)],
         "Indian Olympiad Qualifier in Mathematics: 30 integer-answer questions (10 × 2, 10 × 3, 10 × 5 marks officially; 3 marks each here), 3 hours, no negative marking.", 'expert', mocks=2, pyp=1),
    Exam('Olympiad', 60, [
        S('RSN1', 'Mental Ability', 15, 1, 0, REASON[:10]), S('MAT1', 'Mathematics', 15, 1, 0, QUANT_BASIC), S('SCI1', 'Science', 15, 1, 0, GEN_SCIENCE),
        S('GA1', 'General Knowledge', 5, 1, 0, GA[:8]),
    ], "Multi-subject olympiad practice (SOF/Silverzone style): 50 questions, 60 minutes, no negative marking.", mocks=2, pyp=1),
    Exam('JNVST (Navodaya)', 120, [
        S('RSN1', 'Mental Ability Test', 40, 1.25, 0, REASON[:10]), S('MAT1', 'Arithmetic Test', 20, 1.25, 0, ['math.c5.fractions', 'math.c5.decimals', 'math.c5.lcm_hcf', 'math.c5.area_perimeter', 'math.c4.measurement', 'math.c5.multiplication']),
        S('ENG1', 'Language Test', 20, 1.25, 0, ['english.comprehension', 'english.grammar', 'english.spelling']),
    ], "Class 6 entry: 80 questions, 100 marks, 2 hours (Mental Ability 40, Arithmetic 20, Language 20). No negative marking."),
    Exam('JNVST Class 9', 150, [
        S('ENG1', 'English', 15, 1, 0, ENGLISH[:7]), S('HIN1', 'Hindi', 15, 1, 0, ['hindi.paryayvachi', 'hindi.vilom', 'hindi.grammar']),
        S('MAT1', 'Mathematics', 35, 1, 0, ['math.c8.squares_cubes', 'math.c8.exponents', 'math.c8.linear_equations', 'math.c8.mensuration', 'math.c8.algebraic_identities', 'math.c7.percentage']),
        S('SCI1', 'General Science', 35, 1, 0, GEN_SCIENCE),
    ], "Lateral entry to Class 9: 100 questions, 100 marks, 2½ hours. No negative marking.", mocks=2, pyp=1),
    Exam('Sainik School (AISSEE)', 150, [
        S('MAT1', 'Mathematics', 50, 3, 0, ['math.c5.fractions', 'math.c5.decimals', 'math.c5.lcm_hcf', 'math.c5.area_perimeter', 'math.c4.measurement', 'math.c4.money', 'math.c5.multiplication', 'math.c5.division']),
        S('GA1', 'General Knowledge', 25, 2, 0, ['evs.general', 'ga.states', 'ga.important_days', 'ga.science']), S('ENG1', 'Language', 25, 2, 0, ENGLISH[:7]),
        S('RSN1', 'Intelligence', 25, 2, 0, REASON[:10]),
    ], "Class 6 entry: 125 questions, 300 marks, 150 minutes. Maths 3 marks each; others 2 marks. No negative marking."),
    Exam('NMMS', 180, [
        S('RSN1', 'Mental Ability Test (MAT)', 90, 1, 0, REASON),
        S('SCI1', 'Scholastic Aptitude Test (SAT)', 90, 1, 0, GEN_SCIENCE + ['math.c8.linear_equations', 'math.c8.squares_cubes', 'ga.history', 'ga.geography', 'ga.polity']),
    ], "Class 8 scholarship: MAT 90 + SAT 90 questions, 90 minutes each. No negative marking.", mocks=2, pyp=1),

    # ---------------------------------------------------------------- Programming, IT & placements (new in 2026)
    Exam('TCS NQT', 75, [
        S('QNT1', 'Numerical Ability', 20, 1, 0, QUANT), S('ENG1', 'Verbal Ability', 25, 1, 0, ENGLISH_BANK),
        S('RSN1', 'Reasoning Ability', 20, 1, 0, REASON), S('CSE1', 'Programming Logic', 10, 1, 0, ['programming.python', 'programming.c', 'dsa.structures']),
    ], "Foundation section style: 75 questions, about 75 minutes, no negative marking (Advanced coding round not included).",
       group='programming', icon='laptop-code', color='#2563eb', mocks=3, pyp=2),
    Exam('Campus Placement Aptitude', 60, [
        S('QNT1', 'Quantitative Aptitude', 20, 1, 0, QUANT), S('RSN1', 'Logical Reasoning', 15, 1, 0, REASON),
        S('ENG1', 'Verbal Ability', 15, 1, 0, ENGLISH_BANK), S('CSE1', 'Technical MCQ', 10, 1, 0, CS),
    ], "Infosys / Wipro / Accenture / Capgemini style online assessment: 60 questions, 60 minutes, no negative marking.",
       group='programming', icon='briefcase', color='#0891b2', mocks=3, pyp=2),
    Exam('Python Programming', 60, [S('CSE1', 'Python', 40, 1, 0, ['programming.python', 'cs.theory', 'dsa.structures'], numeric=5)],
         "Skill test: 40 questions on output prediction, data types, loops, functions and data structures. 60 minutes, no negative marking.",
         group='programming', icon='code', color='#3776ab', mocks=3, pyp=0),
    Exam('C Programming', 60, [S('CSE1', 'C Language', 40, 1, 0, ['programming.c', 'programming.number_systems', 'cs.theory', 'dsa.structures'])],
         "Skill test: 40 questions on operators, loops, pointers, arrays and output prediction. 60 minutes, no negative marking.",
         group='programming', icon='terminal', color='#475569', mocks=3, pyp=0),
    Exam('Data Structures & Algorithms', 60, [S('CSE1', 'DSA', 40, 1, 0, ['dsa.structures', 'dsa.complexity', 'programming.python', 'cs.theory'])],
         "40 questions on stacks, queues, trees, sorting, searching and complexity. 60 minutes, no negative marking.",
         group='programming', icon='diagram-project', color='#7c3aed', mocks=3, pyp=0),
    Exam('DBMS & SQL', 45, [S('CSE1', 'DBMS & SQL', 30, 1, 0, ['dbms.sql', 'cs.theory'])],
         "30 questions on SQL queries (answered by running them), normalisation, keys and transactions. 45 minutes.",
         group='programming', icon='database', color='#0f766e', mocks=3, pyp=0),
    Exam('NIELIT CCC', 90, [S('CMP1', 'Course on Computer Concepts', 100, 1, 0, COMPUTER + ['digital.logic'])],
         "100 MCQs, 90 minutes, no negative marking; 50% to pass. Covers computer basics, OS, MS Office/LibreOffice, internet and digital finance.",
         group='programming', icon='desktop', color='#16a34a', mocks=3, pyp=2),
]

# The Nov 2026 expansion lives in its own module; it imports the helpers above, so it must be imported here at the end.
from .patterns_india import EXAMS_2026_EXPANSION  # noqa: E402

EXAMS += EXAMS_2026_EXPANSION

# Every other exam in the exam list (testseries/content/exam_catalog.csv), with a practice pattern each.
from .catalog_patterns import build_exams  # noqa: E402

EXAMS += build_exams({e.name for e in EXAMS})

EXAM_INDEX = {e.name: e for e in EXAMS}
assert len(EXAM_INDEX) == len(EXAMS), "duplicate exam names in patterns"
