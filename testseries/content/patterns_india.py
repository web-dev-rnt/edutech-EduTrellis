"""Exams added in November 2026 so that every major Indian exam family has a test series: state PSCs, state police and
subordinate-service boards, state TETs, more banking/insurance, central government jobs, defence, railways,
pharmacy, nursing, agriculture, hotel management, design, law, MBA and campus-placement tests.

Patterns follow the latest notifications available to us. Where a board changes its format often, or publishes
it only in the notice, the description says so and gives the common format; students should always confirm the
pattern in the official notification. Mocks follow the first objective stage (prelims / CBT-1 / written test).
"""
from .patterns import (
    BIOLOGY, CHEMISTRY, COMPUTER, CS, ENGG_MATHS, ENGLISH, ENGLISH_BANK, GA, GA_BANK, GEN_SCIENCE, MATHS_10, MATHS_ADV,
    MEDICAL, PHYSICS, QUANT, QUANT_BANK, QUANT_BASIC, REASON, REASON_BANK, TEACHING, UPSC_GS, Exam, S, bank3, gate,
)

HINDI = ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.sandhi', 'hindi.grammar']
COMPUTER_PLUS = list(dict.fromkeys(COMPUTER + ['cs.abbreviations', 'cs.shortcuts', 'cs.theory']))
LAW_ALL = ['law.legal_reasoning', 'law.maxims', 'law.cases', 'law.acts', 'law.legal_gk', 'ga.polity', 'ga.polity_articles']
PHARMACY = ['pharmacy.core', 'pharmacy.pharmacognosy', 'pharmacy.jurisprudence', 'medicine.pharmacology', 'medicine.side_effects',
            'medicine.antidotes', 'chemistry.organic', 'medicine.microbiology']
AGRI = ['agriculture.core', 'agriculture.institutes', 'agriculture.revolutions', 'biology.plant_physiology', 'biology.genetics',
        'biology.ecology', 'environment.ecology']
NURSING = ['nursing.core', 'medicine.clinical', 'medicine.pharmacology', 'biology.human_physiology', 'medicine.microbiology',
           'medicine.obg_paeds', 'medicine.psm']

# General Studies split the way state PSC papers weight it (history and polity heavy).
GS_PARTS = [
    ('GS – History, Art & Culture', 0.25, ['ga.history', 'ga.freedom_events', 'ga.titles', 'ga.founders', 'ga.culture', 'ga.monuments', 'ga.festivals']),
    ('GS – Geography & Environment', 0.2, ['ga.geography', 'ga.rivers', 'ga.lakes', 'ga.national_parks', 'ga.states', 'ga.state_languages', 'environment.ecology']),
    ('GS – Polity & Governance', 0.2, ['ga.polity', 'ga.polity_articles', 'ga.schedules', 'ga.amendments', 'ga.firsts']),
    ('GS – Economy', 0.15, ['ga.economy', 'ga.banking_terms', 'ga.organisations', 'ga.important_days']),
    ('GS – Science & Technology', 0.2, ['ga.science', 'biology.diseases', 'ga.inventions', 'cs.awareness', 'physics.units']),
]


def split(total, weights):
    """Integer shares of `total` in proportion to `weights` that add up exactly."""
    raw = [total * w for w in weights]
    out = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - out[i], reverse=True)[:total - sum(out)]:
        out[i] += 1
    return out


def gs_sections(n, marks, neg):
    return [S('GA1', name, c, marks, neg, topics) for (name, _, topics), c in zip(GS_PARTS, split(n, [w for _, w, _ in GS_PARTS])) if c]


def psc(name, n, marks, neg, minutes, pattern, csat=0, csat_minutes=0, **kw):
    """State PSC prelims: GS paper (sectioned by subject) and, where it exists, a qualifying aptitude paper."""
    secs = gs_sections(n, marks, neg)
    if csat:
        a, b, c = split(csat, [0.4, 0.4, 0.2])
        secs += [S('QNT1', 'CSAT – Quantitative Aptitude', a, marks, neg, QUANT_BASIC),
                 S('RSN1', 'CSAT – Reasoning & Mental Ability', b, marks, neg, REASON),
                 S('ENG1', 'CSAT – Comprehension', c, marks, neg, ['english.comprehension', 'english.grammar'])]
    note = ("General Studies questions come from all-India pools (history, geography, polity, economy, science); "
            "add your state's own GK and current affairs separately.")
    return Exam(name, minutes + csat_minutes, secs, pattern, 'hard', group='civil-services', icon='landmark', color='#b45309',
                note=note, **kw)


def tet(name, pattern, lang2='Hindi', **kw):
    """CTET-style Paper I: 150 questions, 150 minutes, no negative marking."""
    lang2_sec = (S('HIN1', 'Language II – Hindi', 30, 1, 0, HINDI) if lang2 == 'Hindi'
                 else S('ENG1', f'Language II – {lang2}', 30, 1, 0, ENGLISH[:7]))
    return Exam(name, 150, [
        S('CDP1', 'Child Development & Pedagogy', 30, 1, 0, TEACHING + ['teaching.research']),
        S('ENG1', 'Language I – English', 30, 1, 0, ENGLISH[:7]),
        lang2_sec,
        S('MAT1', 'Mathematics', 30, 1, 0, ['math.c5.fractions', 'math.c5.lcm_hcf', 'math.c6.integers', 'math.c7.lines_angles',
                                             'math.c8.squares_cubes', 'quant.percentage', 'math.c5.area_perimeter']),
        S('EVS1', 'Environmental Studies', 30, 1, 0, ['evs.general', 'evs.animals', 'evs.young_ones', 'ga.science', 'biology.concepts']),
    ], pattern, group='teaching', icon='chalkboard-user', color='#4f46e5', **kw)


def police(name, minutes, sections, pattern, difficulty='medium', **kw):
    return Exam(name, minutes, sections, pattern, difficulty, group='defence-police', icon='shield-halved', color='#1e3a8a', **kw)


def state_job(name, minutes, sections, pattern, difficulty='medium', **kw):
    return Exam(name, minutes, sections, pattern, difficulty, group='state-govt', icon='building-flag', color='#0f766e', **kw)


def bank(name, minutes, eng, quant, rsn, neg, pattern, **kw):
    return bank3(name, minutes, eng, quant, rsn, neg, pattern, group='banking', icon='building-columns', color='#1d4ed8', **kw)


def ga(n, marks, neg, name='General Awareness', topics=None):
    return S('GA1', name, n, marks, neg, topics or GA)


EXAMS_2026_EXPANSION = [
    # ================================================================ State PSC prelims
    psc('UPPSC PCS', 150, 200 / 150, 0.44, 120,
        "Prelims Paper I (General Studies): 150 questions, 200 marks, 2 hours, −⅓ per wrong answer. Paper II (CSAT) is qualifying at 33%."),
    psc('BPSC CCE', 150, 1, 0.33, 120,
        "Prelims: one General Studies paper of 150 questions, 150 marks, 2 hours, with −⅓ negative marking."),
    psc('MPPSC State Service', 100, 2, 0, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, no negative marking. Paper II (General Aptitude) is qualifying."),
    psc('RPSC RAS', 150, 200 / 150, 0.44, 180,
        "Prelims: General Knowledge & General Science paper of 150 questions, 200 marks, 3 hours, −⅓ negative marking."),
    psc('MPSC Rajyaseva', 100, 2, 0.5, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −¼ negative marking. Paper II (CSAT) is qualifying."),
    psc('TNPSC Group 1', 175, 1.5, 0, 180,
        "Prelims: 200 questions, 300 marks, 3 hours (General Studies 175 + Aptitude & Mental Ability 25), no negative marking.",
        csat=25),
    psc('TNPSC Group 4', 75, 1.5, 0, 180,
        "200 questions, 300 marks, 3 hours: Tamil eligibility / General English 100, General Studies 75, Aptitude 25. No negative marking. "
        "The language part here is General English.", csat=25, mocks=3, pyp=2),
    psc('KPSC KAS', 100, 2, 0.5, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −¼ negative marking. Paper II is also 200 marks."),
    psc('APPSC Group 1', 120, 1, 0.33, 120,
        "Prelims Paper I (General Studies): 120 questions, 120 marks, 2 hours, −⅓ negative marking. Paper II is General Aptitude."),
    psc('TGPSC Group 1', 150, 1, 0, 150,
        "Telangana Group I prelims: General Studies & Mental Ability, 150 questions, 150 marks, 2½ hours, no negative marking."),
    psc('WBCS', 200, 1, 0.33, 150,
        "Prelims: 200 questions, 200 marks, 2½ hours (GS, history, geography, polity, economy, science, reasoning), −⅓ negative marking."),
    psc('OPSC OCS', 100, 2, 0.67, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −⅓ negative marking. Paper II (CSAT) is qualifying."),
    psc('HPSC HCS', 100, 1, 0.25, 120,
        "Prelims Paper I (General Studies): 100 questions, 2 hours, −¼ negative marking. Paper II (CSAT) is qualifying."),
    psc('CGPSC State Service', 100, 2, 0.67, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −⅓ negative marking. Paper II (Aptitude) is qualifying."),
    psc('JPSC CCE', 100, 2, 0, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, no negative marking."),
    psc('UKPSC PCS', 150, 1, 0.25, 120,
        "Prelims Paper I (General Studies): 150 questions, 2 hours, −¼ negative marking. Paper II (CSAT) is qualifying."),
    psc('HPPSC HPAS', 100, 2, 0.67, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −⅓ negative marking. Paper II (CSAT) is qualifying."),
    psc('Kerala PSC', 100, 1, 0.33, 75,
        "Degree / plus-two level common prelims: 100 questions, 75 minutes, −⅓ negative marking.", mocks=3, pyp=2),
    psc('GPSC Class 1-2', 200, 1, 0.3, 180,
        "Prelims General Studies Paper 1: 200 questions, 200 marks, 3 hours, −0.3 negative marking."),
    psc('PPSC Civil Services', 100, 2, 0.5, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −0.5 negative marking. Paper II (CSAT) is qualifying."),
    psc('APSC CCE', 100, 2, 0.67, 120,
        "Prelims General Studies: 100 questions, 200 marks, 2 hours, −⅓ negative marking."),
    psc('JKPSC CCE', 100, 2, 0.67, 120,
        "Prelims Paper I (General Studies): 100 questions, 200 marks, 2 hours, −⅓ negative marking. Paper II (CSAT) is qualifying."),

    # ================================================================ State subordinate services & state jobs
    state_job('UPSSSC PET', 120, [
        *gs_sections(40, 1, 0.25),
        S('QNT1', 'Elementary Arithmetic', 5, 1, 0.25, QUANT_BASIC), S('HIN1', 'General Hindi', 5, 1, 0.25, HINDI),
        S('ENG1', 'General English', 5, 1, 0.25, ENGLISH[:7]), S('RSN1', 'Logic & Reasoning', 5, 1, 0.25, REASON),
        S('DI1', 'Graph, Table & Factual Analysis', 20, 1, 0.25, ['quant.di', 'reasoning.missing_number']),
        S('GA1', 'Current Affairs & General Science', 20, 1, 0.25, GEN_SCIENCE + ['ga.important_days', 'ga.organisations']),
    ], "Preliminary Eligibility Test: 100 questions, 100 marks, 2 hours, −¼ negative marking.", mocks=4, pyp=2),
    state_job('RSMSSB Patwari', 180, [
        S('GA1', 'General Science, History, Polity & Geography', 38, 2, 0.67, UPSC_GS),
        S('GA1', 'Rajasthan & General GK', 37, 2, 0.67, ['ga.states', 'ga.culture', 'ga.monuments', 'ga.festivals', 'ga.lakes']),
        S('RSN1', 'Reasoning & Mental Ability', 38, 2, 0.67, REASON), S('CMP1', 'Basic Computer', 37, 2, 0.67, COMPUTER_PLUS),
    ], "150 questions, 300 marks, 3 hours, −⅓ negative marking. The Hindi, English and maths share varies by notification.", mocks=3, pyp=2),
    state_job('MP Patwari', 180, [
        ga(25, 2, 0, 'General Knowledge'), S('HIN1', 'General Hindi', 15, 2, 0, HINDI), S('ENG1', 'General English', 10, 2, 0, ENGLISH[:7]),
        S('QNT1', 'General Mathematics', 15, 2, 0, QUANT_BASIC), S('RSN1', 'General Aptitude & Reasoning', 15, 2, 0, REASON),
        S('CMP1', 'Computer Knowledge', 20, 2, 0, COMPUTER_PLUS),
    ], "100 questions, 200 marks, 3 hours (ESB / MPESB), no negative marking.", mocks=3, pyp=2),
    state_job('Bihar SSC Inter Level', 135, [
        ga(50, 1, 0.25, 'General Studies'), S('QNT1', 'General Mathematics', 50, 1, 0.25, QUANT_BASIC),
        S('RSN1', 'Mental Ability', 50, 1, 0.25, REASON),
    ], "150 questions, 2 hours 15 minutes, −¼ negative marking.", mocks=3, pyp=2),
    state_job('UP Lekhpal', 120, [
        S('HIN1', 'Hindi', 25, 1, 0.25, HINDI), S('QNT1', 'Mathematics', 25, 1, 0.25, QUANT_BASIC),
        ga(25, 1, 0.25, 'General Knowledge', UPSC_GS),
        S('ARD1', 'Rural Development & Rural Society', 25, 1, 0.25, AGRI),
    ], "100 questions, 100 marks, 2 hours, −¼ negative marking.", mocks=3, pyp=2),
    state_job('VDO / Gram Sevak', 120, [
        ga(30, 1, 0.25, 'General Knowledge', UPSC_GS), S('RSN1', 'Reasoning', 25, 1, 0.25, REASON),
        S('QNT1', 'Mathematics', 20, 1, 0.25, QUANT_BASIC), S('ARD1', 'Agriculture & Rural Development', 25, 1, 0.25, AGRI),
    ], "Village Development Officer / Gram Sevak written tests (UP, Rajasthan and others): about 100 questions, 2 hours.", mocks=3, pyp=1),
    state_job('IB ACIO', 60, [
        S('GA1', 'Current Affairs & General Studies', 40, 1, 0.25, GA), S('QNT1', 'Quantitative Aptitude', 20, 1, 0.25, QUANT),
        S('RSN1', 'Logical & Analytical Ability', 20, 1, 0.25, REASON), S('ENG1', 'English', 20, 1, 0.25, ENGLISH),
    ], "Tier 1: 100 questions, 100 marks, 1 hour, −¼ negative marking.", mocks=4, pyp=2),
    state_job('IB Security Assistant', 60, [
        S('GA1', 'General Awareness', 40, 1, 0.25, GA), S('QNT1', 'Quantitative Aptitude', 20, 1, 0.25, QUANT_BASIC),
        S('RSN1', 'Logical & Analytical Ability', 20, 1, 0.25, REASON), S('ENG1', 'English', 20, 1, 0.25, ENGLISH),
    ], "Tier 1: 100 questions, 100 marks, 1 hour, −¼ negative marking.", mocks=3, pyp=2),
    state_job('FCI Assistant Grade 3', 60, [
        S('ENG1', 'English Language', 25, 1, 0.25, ENGLISH_BANK), S('RSN1', 'Reasoning Ability', 25, 1, 0.25, REASON_BANK),
        S('QNT1', 'Numerical Aptitude', 25, 1, 0.25, QUANT_BANK), S('GA1', 'General Studies', 25, 1, 0.25, GA_BANK),
    ], "Phase I: 100 questions, 60 minutes (15 per section), −¼ negative marking.", mocks=3, pyp=2),
    state_job('EPFO SSA', 60, [
        S('ENG1', 'English Language', 30, 1, 0.25, ENGLISH_BANK), S('RSN1', 'General Intelligence', 35, 1, 0.25, REASON_BANK),
        S('QNT1', 'Quantitative Aptitude', 35, 1, 0.25, QUANT_BANK),
    ], "Social Security Assistant prelims: 100 questions, 60 minutes, −¼ negative marking.", mocks=3, pyp=2),
    state_job('ESIC UDC', 60, [
        S('RSN1', 'General Intelligence & Reasoning', 25, 2, 0.5, REASON), S('GA1', 'General Awareness', 25, 2, 0.5, GA),
        S('QNT1', 'Quantitative Aptitude', 25, 2, 0.5, QUANT), S('ENG1', 'English Comprehension', 25, 2, 0.5, ENGLISH),
    ], "Prelims: 100 questions, 200 marks, 60 minutes, −¼ of the marks per wrong answer.", mocks=3, pyp=2),
    state_job('Supreme Court JCA', 120, [
        S('ENG1', 'General English', 50, 1, 0.25, ENGLISH), ga(25, 1, 0.25, 'General Knowledge'),
        S('RSN1', 'Reasoning & Aptitude', 25, 1, 0.25, REASON), S('CMP1', 'Computer Knowledge', 25, 1, 0.25, COMPUTER_PLUS),
    ], "Junior Court Assistant objective test: 125 questions, 2 hours, −¼ negative marking.", mocks=3, pyp=2),
    state_job('High Court Clerk / Assistant', 120, [
        ga(30, 1, 0.25, 'General Knowledge', UPSC_GS), S('ENG1', 'English', 25, 1, 0.25, ENGLISH),
        S('RSN1', 'Reasoning', 20, 1, 0.25, REASON), S('CMP1', 'Computer Knowledge', 15, 1, 0.25, COMPUTER_PLUS),
        S('LGL1', 'Legal Awareness', 10, 1, 0.25, ['law.acts', 'law.legal_gk']),
    ], "Common format of High Court clerk / assistant written tests (Allahabad, Rajasthan, MP, Patna and others): about 100 questions, 2 hours.",
       mocks=3, pyp=1),

    # ================================================================ State police (named)
    police('UP Police Constable', 120, [
        S('GA1', 'General Knowledge', 38, 2, 0.5, GA), S('HIN1', 'General Hindi', 37, 2, 0.5, HINDI),
        S('QNT1', 'Numerical & Mental Ability', 38, 2, 0.5, QUANT_BASIC), S('RSN1', 'Mental Aptitude, IQ & Reasoning', 37, 2, 0.5, REASON),
    ], "150 questions, 300 marks, 2 hours. +2 / −0.5.", mocks=4, pyp=2),
    police('UP Police SI', 120, [
        S('HIN1', 'General Hindi', 40, 2.5, 0.5, HINDI), S('LGL1', 'Law, Constitution & General Knowledge', 40, 2.5, 0.5, GA[:10] + ['law.acts', 'law.legal_gk']),
        S('QNT1', 'Numerical & Mental Ability', 40, 2.5, 0.5, QUANT_BASIC), S('RSN1', 'Mental Aptitude, IQ & Reasoning', 40, 2.5, 0.5, REASON),
    ], "160 questions, 400 marks, 2 hours, −0.5 per wrong answer.", 'hard', mocks=3, pyp=2),
    police('Bihar Police Constable', 120, [
        S('HIN1', 'Hindi', 15, 1, 0, HINDI), S('ENG1', 'English', 15, 1, 0, ENGLISH[:7]), S('MAT1', 'Mathematics', 15, 1, 0, QUANT_BASIC),
        S('SCI1', 'Science', 15, 1, 0, GEN_SCIENCE), S('SST1', 'Social Science', 20, 1, 0, ['ga.history', 'ga.geography', 'ga.polity', 'ga.economy']),
        ga(20, 1, 0, 'General Knowledge & Current Affairs'),
    ], "CSBC written test: 100 questions, 100 marks, 2 hours, Class 12 level, no negative marking.", mocks=4, pyp=2),
    police('Bihar Police SI', 120, [*gs_sections(100, 2, 0.2)],
           "BPSSC prelims: 100 General Studies questions, 200 marks, 2 hours, −0.2 per wrong answer.",
           'hard', mocks=3, pyp=2),
    police('MP Police Constable', 120, [
        S('GA1', 'General Knowledge & Reasoning', 40, 1, 0, GA[:12] + REASON[:4]), S('RSN1', 'Intelligence Test', 30, 1, 0, REASON),
        S('SCI1', 'Science & Simple Arithmetic', 30, 1, 0, GEN_SCIENCE[:6] + QUANT_BASIC[:4]),
    ], "MPESB: 100 questions, 100 marks, 2 hours, no negative marking.", mocks=3, pyp=2),
    police('Rajasthan Police Constable', 120, [
        S('RSN1', 'Reasoning & Computer', 60, 1, 0.25, REASON + ['cs.abbreviations', 'cs.shortcuts']),
        ga(45, 1, 0.25, 'General Knowledge, Science & Social Studies', GA),
        S('LGL1', 'Women & Child Crime, Legal Provisions', 45, 1, 0.25, ['law.acts', 'law.legal_gk', 'ga.polity']),
    ], "150 questions, 2 hours, −¼ negative marking (Rajasthan GK is part of the GK section).", mocks=3, pyp=2),
    police('Haryana Police Constable', 105, [
        ga(40, 1, 0.25, 'General Studies (incl. Haryana GK)', UPSC_GS), S('RSN1', 'Reasoning', 20, 1, 0.25, REASON),
        S('QNT1', 'Mathematics', 20, 1, 0.25, QUANT_BASIC), S('CMP1', 'Computer & Agriculture', 20, 1, 0.25, COMPUTER_PLUS + ['agriculture.core']),
    ], "HSSC written test: about 100 questions, 1 hour 45 minutes. Check the notification for the current CET-based format.", mocks=3, pyp=1),
    police('Delhi Police Head Constable', 90, [
        S('ENG1', 'English Language', 20, 1, 0.25, ENGLISH), S('GA1', 'General Awareness', 20, 1, 0.25, GA),
        S('QNT1', 'Quantitative Aptitude', 20, 1, 0.25, QUANT_BASIC), S('RSN1', 'General Intelligence', 25, 1, 0.25, REASON),
        S('CMP1', 'Computer Fundamentals', 15, 1, 0.25, COMPUTER_PLUS),
    ], "Head Constable (Ministerial) CBT: 100 questions, 100 marks, 90 minutes, −¼ negative marking.", mocks=3, pyp=2),
    police('RPF SI', 90, [
        S('GA1', 'General Awareness', 50, 1, 0.33, GA), S('QNT1', 'Arithmetic', 35, 1, 0.33, QUANT_BASIC),
        S('RSN1', 'General Intelligence & Reasoning', 35, 1, 0.33, REASON),
    ], "120 questions, 120 marks, 90 minutes, −⅓ negative marking.", mocks=3, pyp=2),
    police('CAPF Head Constable', 90, [
        S('RSN1', 'General Intelligence', 25, 1, 0.25, REASON), S('GA1', 'General Awareness', 25, 1, 0.25, GA),
        S('QNT1', 'Quantitative Aptitude', 25, 1, 0.25, QUANT_BASIC), S('ENG1', 'English / Hindi', 25, 1, 0.25, ENGLISH),
    ], "CISF / BSF / CRPF / ITBP Head Constable (Ministerial) written tests: about 100 questions, 100 marks, 90 minutes.", mocks=3, pyp=1),

    # ================================================================ Defence
    Exam('INET (Indian Navy)', 120, [
        S('ENG1', 'English', 25, 1, 0.25, ENGLISH), S('RSN1', 'Reasoning & Numerical Ability', 25, 1, 0.25, REASON),
        S('MAT1', 'Mathematics', 25, 1, 0.25, MATHS_10 + ['quant.trigonometry']), S('GA1', 'General Knowledge & Science', 25, 1, 0.25, GA[:10] + GEN_SCIENCE[:5]),
    ], "Indian Navy Entrance Test (officers): 100 questions, 2 hours, −¼ negative marking.", 'medium', mocks=3, pyp=1,
       group='defence-police', icon='anchor', color='#1e40af'),
    Exam('Territorial Army', 240, [
        S('RSN1', 'Paper 1 – Reasoning', 50, 1, 0.25, REASON), S('MAT1', 'Paper 1 – Elementary Mathematics', 50, 1, 0.25, QUANT_BASIC + MATHS_10[:4]),
        S('ENG1', 'Paper 2 – English', 50, 1, 0.25, ENGLISH), S('GA1', 'Paper 2 – General Knowledge', 50, 1, 0.25, GA),
    ], "Two papers of 2 hours each (Reasoning + Elementary Maths; English + GK), 100 questions per paper. 40% in each part to qualify.",
       mocks=2, pyp=1, group='defence-police', icon='person-military-rifle', color='#3f6212'),
    Exam('Indian Army Agniveer Clerk', 60, [
        S('GA1', 'General Knowledge', 10, 2, 0.5, GA), S('SCI1', 'General Science', 5, 2, 0.5, GEN_SCIENCE),
        S('MAT1', 'Mathematics', 5, 2, 0.5, QUANT_BASIC), S('CMP1', 'Computer Science', 5, 2, 0.5, COMPUTER_PLUS),
        S('ENG1', 'General English', 25, 2, 0.5, ENGLISH),
    ], "Clerk / Store Keeper Technical CEE: 50 questions, 100 marks, 60 minutes, −0.5 per wrong answer.", mocks=3, pyp=1,
       group='defence-police', icon='person-military-rifle', color='#3f6212'),

    # ================================================================ Banking & insurance
    bank('IBPS SO', 120, 50, 50, 50, 0.25,
         "Specialist Officer prelims (IT, Agriculture, Marketing, HR): 150 questions (English 50, Reasoning 50, Quant 50), 2 hours, −¼. "
         "Law and Rajbhasha officers take General Awareness in place of Quant."),
    bank('NABARD Development Assistant', 60, 30, 35, 35, 0.25,
         "Prelims: 100 questions (English 30, Numerical Ability 35, Reasoning 35), 60 minutes, −¼ negative marking."),
    bank('LIC Assistant', 60, 30, 35, 35, 0.25,
         "Prelims: 100 questions (English 30, Reasoning 35, Numerical Ability 35), 60 minutes, −¼ negative marking."),
    bank('LIC ADO', 60, 30, 35, 35, 0.25,
         "Apprentice Development Officer prelims: 100 questions (Reasoning 35, Numerical Ability 35, English 30), 60 minutes, −¼."),
    bank('NIACL AO', 60, 30, 35, 35, 0.25,
         "New India Assurance AO prelims: 100 questions (English 30, Reasoning 35, Quant 35), 60 minutes, −¼ negative marking."),
    bank('NIACL Assistant', 60, 30, 35, 35, 0.25,
         "Prelims: 100 questions (English 30, Reasoning 35, Numerical Ability 35), 60 minutes, −¼ negative marking."),
    bank('NICL AO', 60, 30, 35, 35, 0.25,
         "National Insurance AO prelims: 100 questions (English 30, Reasoning 35, Quant 35), 60 minutes, −¼ negative marking."),
    Exam('IDBI Junior Assistant Manager', 120, [
        S('RSN1', 'Logical Reasoning, Data Analysis & Interpretation', 60, 1, 0.25, REASON_BANK + ['quant.di']),
        S('ENG1', 'English Language', 40, 1, 0.25, ENGLISH_BANK), S('QNT1', 'Quantitative Aptitude', 40, 1, 0.25, QUANT_BANK),
        S('GA1', 'General / Economy / Banking Awareness', 60, 1, 0.25, GA_BANK),
    ], "200 questions, 200 marks, 2 hours, −¼ negative marking.", mocks=3, pyp=2, group='banking', icon='building-columns', color='#1d4ed8'),
    Exam('IRDAI Assistant Manager', 90, [
        S('ENG1', 'English Language', 40, 1, 0.25, ENGLISH_BANK), S('RSN1', 'Reasoning', 40, 1, 0.25, REASON_BANK),
        S('GA1', 'General Awareness', 40, 1, 0.25, GA_BANK), S('QNT1', 'Quantitative Aptitude', 40, 1, 0.25, QUANT_BANK),
    ], "Phase I: 160 questions, 160 marks, 90 minutes, −¼ negative marking.", 'hard', mocks=2, pyp=1,
       group='banking', icon='building-columns', color='#1d4ed8'),
    Exam('RBI Office Attendant', 90, [
        S('RSN1', 'Reasoning', 30, 1, 0.25, REASON_BANK), S('ENG1', 'General English', 30, 1, 0.25, ENGLISH_BANK),
        S('GA1', 'General Awareness', 30, 1, 0.25, GA_BANK), S('QNT1', 'Numerical Ability', 30, 1, 0.25, QUANT_BASIC),
    ], "120 questions, 120 marks, 90 minutes, −¼ negative marking.", 'easy', mocks=3, pyp=2,
       group='banking', icon='building-columns', color='#1d4ed8'),
    Exam('SBI Apprentice', 60, [
        S('GA1', 'General / Financial Awareness', 25, 1, 0, GA_BANK), S('ENG1', 'General English', 25, 1, 0, ENGLISH_BANK),
        S('QNT1', 'Quantitative Aptitude', 25, 1, 0, QUANT_BANK), S('RSN1', 'Reasoning & Computer Aptitude', 25, 1, 0, REASON_BANK + ['cs.abbreviations']),
    ], "100 questions, 100 marks, 60 minutes (15 minutes per section).", 'easy', mocks=3, pyp=2,
       group='banking', icon='building-columns', color='#1d4ed8'),

    # ================================================================ Railways
    Exam('RRB Technician', 90, [
        S('MAT1', 'Mathematics', 25, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 25, 1, 0.33, REASON),
        S('SCI1', 'Basic Science & Engineering', 40, 1, 0.33, GEN_SCIENCE + ['engineering.electrical', 'engineering.mechanical']),
        S('GA1', 'General Awareness', 10, 1, 0.33, GA),
    ], "CBT: 100 questions, 90 minutes, −⅓ negative marking (Grade III; Grade I Signal has a different split).", mocks=4, pyp=2,
       group='ssc-railway', icon='train', color='#b91c1c'),
    Exam('RRB Paramedical', 90, [
        S('NUR1', 'Professional Ability', 70, 1, 0.33, NURSING + ['pharmacy.core']), S('GA1', 'General Awareness', 10, 1, 0.33, GA),
        S('QNT1', 'General Arithmetic', 5, 1, 0.33, QUANT_BASIC), S('RSN1', 'General Intelligence & Reasoning', 10, 1, 0.33, REASON),
        S('SCI1', 'General Science', 5, 1, 0.33, GEN_SCIENCE),
    ], "Staff Nurse, Pharmacist, Lab Assistant and other paramedical posts: 100 questions, 90 minutes, −⅓ negative marking.",
       mocks=3, pyp=2, group='ssc-railway', icon='train', color='#b91c1c'),

    # ================================================================ Medical, pharmacy, nursing
    Exam('INI-CET', 180, [S('MED1', 'Clinical & Pre/Para-clinical Subjects', 200, 1, 0.33, MEDICAL)],
         "AIIMS, JIPMER, PGIMER, NIMHANS PG entrance: 200 questions, 3 hours, −⅓ negative marking.", 'expert', mocks=2, pyp=1,
         group='medical', icon='stethoscope', color='#e11d48'),
    Exam('GPAT', 180, [
        S('PHA1', 'Pharmaceutics & Pharmacology', 65, 4, 1, PHARMACY),
        S('CHE1', 'Pharmaceutical & Medicinal Chemistry', 35, 4, 1, CHEMISTRY + ['chemistry.organic']),
        S('PHA1', 'Pharmacognosy & Other Subjects', 25, 4, 1, ['pharmacy.pharmacognosy', 'pharmacy.jurisprudence', 'biology.human_physiology']),
    ], "Graduate Pharmacy Aptitude Test: 125 questions, 500 marks, 3 hours. +4 / −1.", 'hard', mocks=3, pyp=2,
       group='medical', icon='prescription-bottle-medical', color='#7c3aed'),
    Exam('NIPER JEE', 120, [
        S('PHA1', 'Pharmaceutical Sciences', 160, 1, 0.25, PHARMACY), S('GA1', 'General Aptitude', 40, 1, 0.25, REASON[:6] + QUANT_BASIC[:4]),
    ], "Masters entrance: 200 questions, 2 hours, −¼ negative marking.", 'hard', mocks=2, pyp=1,
       group='medical', icon='prescription-bottle-medical', color='#7c3aed'),
    Exam('Pharmacist (Govt) Exam', 90, [
        S('PHA1', 'Pharmacy', 80, 1, 0.25, PHARMACY), S('GA1', 'General Knowledge & Aptitude', 20, 1, 0.25, GA[:8] + REASON[:4]),
    ], "Common format of state and central pharmacist recruitment tests (DSSSB, ESIC, state health services): about 100 questions, 90 minutes.",
       mocks=3, pyp=1, group='medical', icon='prescription-bottle-medical', color='#7c3aed'),
    Exam('Staff Nurse (Govt) Exam', 120, [
        S('NUR1', 'Nursing', 100, 1, 0.25, NURSING), S('GA1', 'General Knowledge & Aptitude', 20, 1, 0.25, GA[:8] + REASON[:4]),
    ], "Common format of ESIC, DSSSB, state PSC and health-department staff nurse tests: about 120 questions, 2 hours.",
       mocks=3, pyp=1, group='medical', icon='user-nurse', color='#ec4899'),
    Exam('BSc Nursing Entrance', 120, [
        S('PHY1', 'Physics', 30, 1, 0.33, PHYSICS), S('CHE1', 'Chemistry', 30, 1, 0.33, CHEMISTRY),
        S('BIO1', 'Biology', 30, 1, 0.33, BIOLOGY), S('GA1', 'General Knowledge', 10, 1, 0.33, GA[:10]),
    ], "AIIMS / state BSc (Hons) Nursing entrance format: about 100 questions on Physics, Chemistry, Biology and GK, 2 hours. "
       "Many states now admit through NEET UG.", mocks=3, pyp=1, group='medical', icon='user-nurse', color='#ec4899'),

    # ================================================================ Engineering & science entrances
    Exam('COMEDK UGET', 180, [
        S('PHY1', 'Physics', 60, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 60, 1, 0, CHEMISTRY), S('MAT1', 'Mathematics', 60, 1, 0, MATHS_ADV),
    ], "180 questions (60 each), 180 marks, 3 hours, no negative marking.", 'medium', mocks=3, pyp=2,
       group='engineering', icon='gears', color='#0369a1'),
    Exam('SRMJEEE', 150, [
        S('PHY1', 'Physics', 35, 1, 0, PHYSICS), S('CHE1', 'Chemistry', 35, 1, 0, CHEMISTRY), S('MAT1', 'Mathematics', 40, 1, 0, MATHS_ADV),
        S('ENG1', 'English', 5, 1, 0, ENGLISH[:6]), S('RSN1', 'Aptitude', 10, 1, 0, REASON[:8] + QUANT_BASIC[:4]),
    ], "125 questions, 2½ hours, no negative marking.", 'medium', mocks=3, pyp=1, group='engineering', icon='gears', color='#0369a1'),
    Exam('KIITEE', 180, [
        S('PHY1', 'Physics', 40, 4, 1, PHYSICS), S('CHE1', 'Chemistry', 40, 4, 1, CHEMISTRY), S('MAT1', 'Mathematics', 40, 4, 1, MATHS_ADV),
    ], "B.Tech: 120 questions, 480 marks, 3 hours. +4 / −1.", 'medium', mocks=3, pyp=1, group='engineering', icon='gears', color='#0369a1'),
    Exam('KEAM', 180, [
        S('MAT1', 'Mathematics', 75, 4, 1, MATHS_ADV), S('PHY1', 'Physics', 45, 4, 1, PHYSICS), S('CHE1', 'Chemistry', 30, 4, 1, CHEMISTRY),
    ], "Kerala engineering CBT: 150 questions (Maths 75, Physics 45, Chemistry 30), 600 marks, 3 hours. +4 / −1.", 'medium', mocks=3, pyp=2,
       group='engineering', icon='gears', color='#0369a1'),
    Exam('GUJCET', 180, [
        S('PHY1', 'Physics', 40, 1, 0.25, PHYSICS), S('CHE1', 'Chemistry', 40, 1, 0.25, CHEMISTRY), S('MAT1', 'Mathematics', 40, 1, 0.25, MATHS_ADV),
    ], "120 questions (40 each), 120 marks, 3 hours, −¼ negative marking.", 'medium', mocks=3, pyp=2,
       group='engineering', icon='gears', color='#0369a1'),
    Exam('JEE Main Paper 2 (B.Arch)', 180, [
        S('MAT1', 'Mathematics', 25, 4, 1, MATHS_ADV, numeric=5), S('DSG1', 'Aptitude Test', 50, 4, 1, ['design.aptitude', 'design.architecture', 'reasoning.cubes', 'reasoning.counting']),
    ], "Paper 2A: Mathematics 25 (20 MCQ + 5 numerical) and Aptitude 50 MCQs, +4 / −1; the drawing test (2 questions) is offline and not included.",
       'hard', mocks=3, pyp=1, group='engineering', icon='compass-drafting', color='#be185d'),
    gate('GATE EC', 'CSE1', 'Electronics & Communication', ['digital.logic', 'engineering.electrical', 'physics.electricity', 'physics.modern'] + ENGG_MATHS,
         ['engineering.electrical', 'digital.logic', 'quant.tita'], 'Electronics & Communication Engineering', icon='microchip', color='#0e7490'),
    gate('GATE DA', 'CSE1', 'Data Science & AI', ['quant.probability', 'math.c11.statistics_probability', 'math.c12.matrices', 'programming.python',
                                                    'dsa.structures', 'dsa.complexity', 'dbms.sql'] + ENGG_MATHS,
         ['quant.probability', 'math.c12.matrices', 'quant.tita'], 'Data Science & Artificial Intelligence', icon='brain', color='#6d28d9'),
    Exam('IISER IAT', 180, [
        S('BIO1', 'Biology', 15, 4, 1, BIOLOGY), S('CHE1', 'Chemistry', 15, 4, 1, CHEMISTRY),
        S('MAT1', 'Mathematics', 15, 4, 1, MATHS_ADV), S('PHY1', 'Physics', 15, 4, 1, PHYSICS),
    ], "IISER Aptitude Test: 60 questions (15 each), 240 marks, 3 hours. +4 / −1.", 'hard', mocks=3, pyp=1,
       group='university', icon='flask', color='#0d9488'),
    Exam('NEST', 210, [
        S('BIO1', 'Biology', 15, 3, 1, BIOLOGY), S('CHE1', 'Chemistry', 15, 3, 1, CHEMISTRY),
        S('MAT1', 'Mathematics', 15, 3, 1, MATHS_ADV), S('PHY1', 'Physics', 15, 3, 1, PHYSICS),
    ], "NISER / UM-DAE CEBS entrance: four subject sections, best three count, 3½ hours. Mixed single- and multiple-correct questions "
       "with partial negative marking (single-correct format here).", 'hard', mocks=2, pyp=1, group='university', icon='flask', color='#0d9488'),

    # ================================================================ Agriculture, hotel management, design
    Exam('ICAR AIEEA PG', 120, [S('ARD1', 'Agriculture & Allied Sciences', 120, 4, 1, AGRI)],
         "Masters entrance (AIEEA PG / AICE-JRF/SRF): 120 questions, 480 marks, 2 hours. +4 / −1.", 'hard', mocks=3, pyp=1,
         group='university', icon='seedling', color='#15803d'),
    Exam('CUET ICAR UG (Agriculture)', 60, [
        S('ARD1', 'Agriculture', 25, 5, 1, AGRI), S('BIO1', 'Biology', 25, 5, 1, BIOLOGY[:6]),
    ], "Domain papers taken for ICAR-AU UG seats through CUET UG: 50 questions per paper, 60 minutes, +5 / −1.", mocks=3, pyp=1,
       group='university', icon='seedling', color='#15803d'),
    Exam('NCHM JEE', 180, [
        S('QNT1', 'Numerical Ability & Analytical Aptitude', 30, 4, 1, QUANT_BASIC), S('RSN1', 'Reasoning & Logical Deduction', 30, 4, 1, REASON),
        S('GA1', 'General Knowledge & Current Affairs', 30, 4, 1, GA), S('ENG1', 'English Language', 60, 4, 1, ENGLISH),
        S('HSP1', 'Aptitude for Service Sector', 50, 4, 1, ['hospitality.aptitude']),
    ], "Hotel management entrance: 200 questions, 800 marks, 3 hours. +4 / −1.", mocks=3, pyp=1,
       group='university', icon='hotel', color='#b45309'),
    Exam('UCEED', 120, [
        S('DSG1', 'Part A – MCQ', 28, 3, 0.71, ['design.aptitude', 'design.architecture', 'reasoning.cubes', 'reasoning.counting', 'reasoning.analogy']),
        S('DSG1', 'Part A – Numerical', 14, 4, 0, ['reasoning.counting', 'reasoning.cubes', 'quant.mensuration'], numeric=14),
    ], "IIT B.Des entrance, Part A (computer-based): NAT, MSQ and MCQ questions; MSQs are shown here as single-correct. Part B (drawing) is not included.",
       'hard', mocks=3, pyp=1, group='university', icon='pen-ruler', color='#e11d48'),
    Exam('CEED', 60, [
        S('DSG1', 'Part A – MCQ', 26, 3, 0.5, ['design.aptitude', 'design.architecture', 'reasoning.cubes', 'reasoning.analogy']),
        S('DSG1', 'Part A – Numerical', 8, 4, 0, ['reasoning.counting', 'quant.mensuration'], numeric=8),
    ], "IIT M.Des entrance, Part A (1 hour, screening): NAT, MSQ and MCQ questions. Part B (sketching and design) is not included.",
       'hard', mocks=3, pyp=1, group='university', icon='pen-ruler', color='#e11d48'),
    Exam('NID DAT Prelims', 180, [
        S('DSG1', 'Design Aptitude (Objective)', 40, 1, 0, ['design.aptitude', 'design.architecture', 'reasoning.analogy', 'reasoning.cubes']),
        ga(10, 1, 0, 'General Awareness', GA[:8]),
    ], "Objective part of the NID Design Aptitude Test prelims (the drawing and subjective parts are not included).", mocks=2, pyp=1,
       group='university', icon='pen-ruler', color='#e11d48'),

    # ================================================================ Law & MBA
    Exam('AIBE', 210, [S('LGL1', 'Law Subjects', 100, 1, 0, LAW_ALL)],
         "All India Bar Examination: 100 questions, 3½ hours, no negative marking, open book (bare Acts allowed). 45% to pass (40% for SC/ST).",
         'medium', mocks=3, pyp=2, group='mba-law', icon='scale-balanced', color='#991b1b'),
    Exam('CLAT PG', 120, [S('LGL1', 'Law (Constitutional, Jurisprudence, Contract, Torts, Criminal and more)', 120, 1, 0.25, LAW_ALL)],
         "120 questions, 120 marks, 2 hours, −¼ negative marking. Questions are passage-based in the real paper.", 'hard', mocks=3, pyp=1,
         group='mba-law', icon='scale-balanced', color='#991b1b'),
    Exam('MH CET Law', 120, [
        S('LGL1', 'Legal Aptitude & Reasoning', 40, 1, 0, LAW_ALL), ga(30, 1, 0, 'General Knowledge & Current Affairs'),
        S('RSN1', 'Logical & Analytical Reasoning', 40, 1, 0, REASON), S('ENG1', 'English', 30, 1, 0, ENGLISH),
        S('QNT1', 'Basic Mathematics', 10, 1, 0, QUANT_BASIC),
    ], "5-year LLB: 150 questions, 150 marks, 2 hours, no negative marking.", mocks=3, pyp=1,
       group='mba-law', icon='scale-balanced', color='#991b1b'),
    Exam('SNAP', 60, [
        S('ENG1', 'General English', 15, 1, 0.25, ENGLISH_BANK), S('RSN1', 'Analytical & Logical Reasoning', 25, 1, 0.25, REASON_BANK),
        S('QNT1', 'Quantitative, Data Interpretation & Sufficiency', 20, 1, 0.25, QUANT_BANK),
    ], "Symbiosis MBA entrance: 60 questions, 60 marks, 1 hour, −¼ negative marking.", 'hard', mocks=4, pyp=2,
       group='mba-law', icon='briefcase', color='#4338ca'),
    Exam('MAH MBA CET', 150, [
        S('RSN1', 'Logical Reasoning', 75, 1, 0, REASON), S('RSN1', 'Abstract Reasoning', 25, 1, 0, ['reasoning.cubes', 'reasoning.analogy', 'reasoning.counting']),
        S('QNT1', 'Quantitative Aptitude', 50, 1, 0, QUANT), S('ENG1', 'Verbal Ability & Reading Comprehension', 50, 1, 0, ENGLISH_BANK),
    ], "200 questions, 200 marks, 150 minutes, no negative marking.", mocks=3, pyp=2, group='mba-law', icon='briefcase', color='#4338ca'),
    Exam('NPAT', 100, [
        S('QNT1', 'Quantitative & Numerical Ability', 40, 1, 0, QUANT), S('RSN1', 'Reasoning & General Intelligence', 40, 1, 0, REASON),
        S('ENG1', 'Verbal Ability', 40, 1, 0, ENGLISH_BANK),
    ], "NMIMS UG entrance: 120 questions, 100 minutes, no negative marking.", mocks=3, pyp=1,
       group='mba-law', icon='briefcase', color='#4338ca'),
    Exam('ATMA', 180, [
        S('RSN1', 'Analytical Reasoning', 60, 1, 0.25, REASON), S('QNT1', 'Quantitative Skills', 60, 1, 0.25, QUANT),
        S('ENG1', 'Verbal Skills', 60, 1, 0.25, ENGLISH_BANK),
    ], "AIMS Test for Management Admissions: 180 questions in six sections, 3 hours, with negative marking.", mocks=3, pyp=1,
       group='mba-law', icon='briefcase', color='#4338ca'),

    # ================================================================ Teaching
    tet('UPTET', "Uttar Pradesh TET Paper I (Classes 1–5): 150 questions, 150 marks, 2½ hours, no negative marking."),
    tet('Super TET', "UP Assistant Teacher recruitment exam: 150 questions, 150 marks, 2½ hours, no negative marking (format shown in TET style).",
        mocks=3, pyp=2),
    tet('REET', "Rajasthan REET Level 1: 150 questions, 150 marks, 2½ hours, no negative marking."),
    tet('HTET', "Haryana TET Level 1 (PRT): 150 questions, 150 marks, 2½ hours, no negative marking."),
    tet('MAHA TET', "Maharashtra TET Paper I: 150 questions, 150 marks, 2½ hours. Language II is Marathi in the real paper.", lang2='Marathi'),
    tet('Bihar STET', "Bihar teacher eligibility format (Paper I style): 150 questions, 150 marks, 2½ hours, no negative marking."),
    tet('PSTET', "Punjab TET Paper I: 150 questions, 150 marks, 2½ hours. Language I is Punjabi in the real paper.", lang2='Punjabi'),
    tet('KTET', "Kerala TET Category I: 150 questions, 150 marks, 2½ hours. Languages are Malayalam/English in the real paper.", lang2='Malayalam'),
    tet('TNTET', "Tamil Nadu TET Paper I: 150 questions, 150 marks, 3 hours. Language I is Tamil in the real paper.", lang2='Tamil'),
    tet('APTET', "Andhra Pradesh TET Paper I-A: 150 questions, 150 marks, 2½ hours. Language I is Telugu in the real paper.", lang2='Telugu'),
    tet('TS TET', "Telangana TET Paper I: 150 questions, 150 marks, 2½ hours. Language I is Telugu in the real paper.", lang2='Telugu'),
    tet('OTET', "Odisha TET Paper I: 150 questions, 150 marks, 2½ hours. Language I is Odia in the real paper.", lang2='Odia'),
    tet('MP TET (Varg 3)', "MP Primary Teacher Eligibility Test: 150 questions, 150 marks, 2½ hours, no negative marking."),
    tet('CG TET', "Chhattisgarh TET Paper I: 150 questions, 150 marks, 2½ hours, no negative marking."),
    Exam('State SET (Paper 1)', 60, [S('TCH1', 'Teaching & Research Aptitude', 50, 2, 0, ['teaching.research', 'teaching.pedagogy', 'reasoning.number_series', 'quant.di', 'cs.awareness', 'environment.ecology'])],
         "State Eligibility Test for Assistant Professor (MH-SET, WB-SET, KSET, TNSET and others) – Paper 1 is common: 50 questions, 100 marks, 1 hour.",
         mocks=4, pyp=2, group='teaching', icon='chalkboard-user', color='#4f46e5'),
    Exam('B.Ed Entrance', 120, [
        S('TCH1', 'Teaching Aptitude', 30, 1, 0, TEACHING + ['teaching.research']), ga(25, 1, 0, 'General Awareness'),
        S('RSN1', 'Logical & Analytical Reasoning', 25, 1, 0, REASON), S('ENG1', 'General English', 20, 1, 0, ENGLISH[:7]),
    ], "Common format of state B.Ed entrance tests (UP B.Ed JEE, Bihar B.Ed CET, others): about 100 questions, 2 hours. Check your state's pattern.",
       mocks=3, pyp=1, group='teaching', icon='chalkboard-user', color='#4f46e5'),
    Exam('NVS / KVS PRT', 180, [
        S('ENG1', 'General English', 10, 1, 0, ENGLISH), S('HIN1', 'General Hindi', 10, 1, 0, HINDI),
        ga(10, 1, 0, 'General Awareness & Current Affairs'), S('RSN1', 'Reasoning Ability', 10, 1, 0, REASON),
        S('CMP1', 'Computer Literacy', 10, 1, 0, COMPUTER_PLUS), S('CDP1', 'Perspectives on Education & Pedagogy', 100, 1, 0, TEACHING + ['teaching.research']),
    ], "Navodaya / Kendriya Vidyalaya primary teacher CBT: 150 questions, 180 minutes, no negative marking.", mocks=3, pyp=1,
       group='teaching', icon='chalkboard-user', color='#4f46e5'),

    # ================================================================ Placements & IT certifications
    Exam('Infosys Online Test', 100, [
        S('RSN1', 'Logical Reasoning', 15, 1, 0, REASON), S('QNT1', 'Mathematical Ability', 10, 1, 0, QUANT),
        S('ENG1', 'Verbal Ability', 20, 1, 0, ENGLISH_BANK), S('CSE1', 'Pseudocode & Puzzle Solving', 5, 1, 0, ['programming.python', 'programming.c']),
    ], "Infosys (System Engineer) online test style: reasoning, maths, verbal and pseudocode, about 100 minutes, no negative marking.",
       group='programming', icon='laptop-code', color='#0284c7', mocks=3, pyp=1),
    Exam('Wipro NLTH', 80, [
        S('QNT1', 'Quantitative Aptitude', 16, 1, 0, QUANT), S('RSN1', 'Logical Reasoning', 14, 1, 0, REASON),
        S('ENG1', 'Verbal Ability', 22, 1, 0, ENGLISH_BANK),
    ], "Wipro Elite NLTH aptitude round style: 52 questions, about 80 minutes (essay and coding rounds not included).",
       group='programming', icon='laptop-code', color='#7c3aed', mocks=3, pyp=1),
    Exam('Accenture Assessment', 90, [
        S('CSE1', 'Cognitive & Technical Assessment', 50, 1, 0, CS + COMPUTER_PLUS), S('RSN1', 'Critical Reasoning', 15, 1, 0, REASON),
        S('ENG1', 'English Ability', 25, 1, 0, ENGLISH_BANK),
    ], "Accenture cognitive and technical assessment style: about 90 questions, 90 minutes, no negative marking (coding round not included).",
       group='programming', icon='laptop-code', color='#a21caf', mocks=3, pyp=1),
    Exam('Cognizant GenC', 80, [
        S('QNT1', 'Quantitative Aptitude', 25, 1, 0, QUANT), S('RSN1', 'Logical Reasoning', 25, 1, 0, REASON),
        S('ENG1', 'English Comprehension', 30, 1, 0, ENGLISH_BANK),
    ], "Cognizant GenC aptitude round style: about 80 questions, 80 minutes, no negative marking.",
       group='programming', icon='laptop-code', color='#1d4ed8', mocks=3, pyp=1),
    Exam('NIELIT O Level', 180, [S('CMP1', 'IT Tools & Network Basics (M1-R5)', 100, 1, 0, COMPUTER_PLUS + ['digital.logic', 'cs.theory'])],
         "O Level module M1-R5 theory: 100 objective questions, 3 hours, no negative marking.", group='programming', icon='desktop',
         color='#16a34a', mocks=3, pyp=1),

    # ================================================================ School-level entrances & olympiads
    Exam('Sainik School Class 9 (AISSEE)', 180, [
        S('MAT1', 'Mathematics', 50, 4, 0, MATHS_10 + ['math.c8.squares_cubes', 'math.c8.linear_equations', 'math.c8.mensuration']),
        S('RSN1', 'Intelligence', 25, 2, 0, REASON), S('ENG1', 'English', 25, 2, 0, ENGLISH[:7]),
        S('SCI1', 'General Science', 25, 2, 0, GEN_SCIENCE), S('SST1', 'Social Science', 25, 2, 0, ['ga.history', 'ga.geography', 'ga.polity', 'ga.economy']),
    ], "Class 9 entry: 150 questions, 400 marks, 3 hours. Maths 4 marks each; others 2 marks. No negative marking.",
       group='scholarship', icon='trophy', color='#ca8a04', mocks=3, pyp=1),
    Exam('RMS CET', 150, [
        S('ENG1', 'English', 50, 1, 0, ENGLISH[:7]), S('RSN1', 'Intelligence', 50, 1, 0, REASON[:10]),
        S('MAT1', 'Mathematics', 50, 1, 0, ['math.c5.fractions', 'math.c5.decimals', 'math.c5.lcm_hcf', 'math.c5.area_perimeter', 'math.c4.measurement', 'math.c5.multiplication']),
        S('GA1', 'General Knowledge', 50, 1, 0, ['evs.general', 'ga.states', 'ga.important_days', 'ga.science']),
    ], "Rashtriya Military School Class 6 entry: English, Intelligence, Maths and GK, about 200 marks, 2½ hours (format shown as one paper).",
       group='scholarship', icon='trophy', color='#ca8a04', mocks=3, pyp=1),
    Exam('IGKO GK Olympiad', 60, [
        S('GA1', 'General Knowledge', 35, 1, 0, GA + ['ga.monuments', 'ga.festivals', 'ga.firsts', 'ga.titles']),
        S('GA1', 'Current Affairs & Life Skills', 10, 1, 0, ['ga.important_days', 'ga.organisations', 'ga.sports']),
        S('GA1', "Achievers' Section", 5, 3, 0, ['ga.inventions', 'ga.books', 'ga.world']),
    ], "International General Knowledge Olympiad (SOF): 50 questions, 60 marks, 60 minutes, no negative marking.",
       group='scholarship', icon='trophy', color='#ca8a04', mocks=3, pyp=1),
]
