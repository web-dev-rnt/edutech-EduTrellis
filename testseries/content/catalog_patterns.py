"""Practice patterns for the exams added from the exam list (exam_catalog.csv).

Imported only by patterns.py (at its end), so the helpers it uses are already defined.
"""
import re

from .patterns import (
    BIOLOGY, CHEMISTRY, COMPUTER, CS, ENGG_MATHS, ENGLISH, ENGLISH_BANK, GA, GA_BANK, GEN_SCIENCE, MATHS_10, MATHS_ADV,
    MEDICAL, PHYSICS, QUANT, QUANT_BANK, QUANT_BASIC, REASON, REASON_BANK, TEACHING, Exam, S,
)

from .catalog import GROUP_BY_NAME, rows

# ------------------------------------------------------------------ subject papers
HINDI = ['hindi.paryayvachi', 'hindi.vilom', 'hindi.muhavare', 'hindi.sandhi', 'hindi.grammar']
LAW = ['law.legal_reasoning', 'law.maxims', 'law.cases', 'law.acts', 'law.legal_gk', 'ga.polity', 'ga.polity_articles']
NURSING = ['nursing.core', 'medicine.clinical', 'medicine.pharmacology', 'biology.human_physiology', 'medicine.microbiology',
           'medicine.obg_paeds', 'medicine.psm']
PHARMACY = ['pharmacy.core', 'pharmacy.pharmacognosy', 'pharmacy.jurisprudence', 'medicine.pharmacology', 'medicine.side_effects',
            'chemistry.organic']
AGRI = ['agriculture.core', 'agriculture.institutes', 'agriculture.revolutions', 'biology.plant_physiology', 'biology.genetics',
        'biology.ecology', 'environment.ecology']
ACCOUNTS = ['commerce.accounting', 'commerce.accounting_theory', 'commerce.gst', 'commerce.business_law', 'ga.banking_terms']
CIVIL = ['engineering.core', 'physics.force_energy', 'quant.mensuration', 'physics.units']
MECH = ['engineering.mechanical', 'engineering.core', 'physics.heat_matter', 'physics.force_energy']
ELEC = ['engineering.electrical', 'physics.electricity', 'digital.logic', 'engineering.core']
ECE = ['digital.logic', 'physics.electricity', 'engineering.electrical', 'physics.modern']
TRADE = ['engineering.core', 'physics.units', 'physics.electricity', 'physics.force_energy', 'ga.science']

# (pattern, subject code, paper name, topics). First match wins; None topics = no question pool yet.
SUBJECTS = [
    (r'nurs|staff nurse|\banm\b|\bgnm\b|sister grade|\bcho\b|nclex|health worker', 'NUR1', 'Nursing', NURSING),
    (r'pharma', 'PHA1', 'Pharmacy', PHARMACY),
    (r'dental|\bmds\b', 'DEN1', 'Dentistry', ['dentistry.core']),
    (r'lab(oratory)? (technician|technologist|assistant)|paramedical|malaria|\bmlt\b',
     'MED1', 'Medical Laboratory & Allied Health', ['medicine.microbiology', 'medicine.pathology', 'biology.human_physiology', 'biology.diseases']),
    (r'medical officer|surgeon|senior resident|usmle|gdmo|\bmbbs\b|neet pg|dnb', 'MED1', 'Medicine', MEDICAL),
    (r'veterinar|pashudhan|animal husbandry|livestock', 'ARD1', 'Animal Husbandry & Veterinary Science',
     ['agriculture.core', 'biology.human_physiology', 'biology.diseases', 'biology.genetics']),
    (r'agricultur|horticult|seed officer|\bafo\b|cane supervisor|fisheries|\bb\.?sc.*agri', 'ARD1', 'Agriculture', AGRI),
    (r'forest|wild ?life|range officer|\bacf\b|environment', 'ARD1', 'Forestry & Environment',
     ['environment.ecology', 'biology.ecology', 'ga.national_parks', 'agriculture.core', 'biology.plant_physiology']),
    (r'\blaw\b|legal|judicial|judge|prosecut|\bllb\b|\bjlo\b|\bclat\b|\bslat\b', 'LGL1', 'Law', LAW),
    (r'civil|\bce\b|surveyor|draughtsman|draftsman|town planner|estate officer', 'CIV1', 'Civil Engineering', CIVIL),
    (r'mechanic|\bme\b|fitter|welder|machinist|automobile|metallurg|mining|production|plant operator|nuclear', 'CIV1',
     'Mechanical Engineering', MECH),
    (r'electrical|\bee\b|\beee\b|electrician|lineman|power', 'PHY1', 'Electrical Engineering', ELEC),
    (r'electronic|\bec\b|\bece\b|telecom|instrument|s ?& ?t|signal|radio operator|\bin\b', 'PHY1', 'Electronics & Communication', ECE),
    (r'computer science|\bcs\b|\bcse\b|\bit\b|information tech|programmer|system analyst|software|computer instructor|computor|'
     r'\bmca\b|\bbca\b|c-dac|\bict\b|data entry|computer operator|java|php|javascript|c\+\+|operating system|networking|\bcsa\b|'
     r'\baws\b|scientist b|\bnic\b', 'CSE1', 'Computer Science', CS + COMPUTER),
    (r'physic', 'PHY1', 'Physics', PHYSICS),
    (r'chemi', 'CHE1', 'Chemistry', CHEMISTRY),
    (r'biolog|life science|botany|zoology|biotech|microbiolog|\bxl\b', 'BIO1', 'Biology', BIOLOGY),
    (r'math|statistic', 'MAT1', 'Mathematics', MATHS_ADV),
    (r'accountan|account|auditor|\bcost\b|tax\b|treasury|credit|chartered|\bjao\b|cashier|finance|commerce|business studies', 'ACC1',
     'Accountancy & Finance', ACCOUNTS),
    (r'econom', 'ECO1', 'Economics', ['commerce.economics', 'ga.economy', 'ga.banking_terms', 'ga.organisations']),
    (r'histor|archaeolog|gandhian', 'HIS1', 'History', ['ga.history', 'ga.freedom_events', 'ga.culture', 'ga.monuments', 'ga.founders', 'ga.titles']),
    (r'geograph|geolog', 'GEO1', 'Geography', ['ga.geography', 'ga.rivers', 'ga.lakes', 'ga.national_parks', 'ga.world', 'ga.states']),
    (r'politic|polity|public admin|civics|strategic', 'POL1', 'Political Science', ['ga.polity', 'ga.polity_articles', 'ga.amendments', 'ga.schedules', 'law.cases']),
    (r'sociolog|home science|philosophy|library|sanskrit|marathi|population|forensic|mass comm|journalism|tamil|telugu|'
     r'bengali|urdu|music|fine art|drawing', None, None, None),
    (r'social (science|studies)|\bsst\b|\barts\b|humanities', 'SST1', 'Social Science', ['ga.history', 'ga.geography', 'ga.polity', 'ga.economy']),
    (r'\bscience\b|\bscientific\b', 'SCI1', 'Science', GEN_SCIENCE + ['physics.concepts', 'chemistry.concepts', 'biology.concepts']),
    (r'hindi|rajbhasha|translator|pradhyapak', 'HIN1', 'Hindi', HINDI),
    (r'english', 'ENG1', 'English', ENGLISH),
    (r'management|\bhr\b|human resource|personnel|marketing|business|labour welfare|\bhrm\b|logistics', 'DM1', 'Management',
     ['management.decision', 'commerce.business', 'commerce.business_law', 'commerce.economics']),
    (r'design|fashion|nift|\bnid\b|pearl|interior|footwear|\bfddi\b|\baifd\b', 'DSG1', 'Design & Visual Aptitude', ['design.aptitude', 'design.architecture']),
    (r'architect|\bnata\b|b ?arch', 'DSG1', 'Architecture & Drawing Aptitude', ['design.architecture', 'design.aptitude']),
    (r'hotel|hospitality|catering|bhmct', 'HSP1', 'Hospitality & Service Aptitude', ['hospitality.aptitude']),
    (r'physical education|yoga|sports', 'BIO1', 'Physical Education & Health', ['biology.human_physiology', 'biology.diseases']),
    (r'psycholog|education\b|counsel', 'TCH1', 'Education & Psychology', TEACHING + ['teaching.research']),
]
# Hindi-medium states: their state-level papers have a Hindi section instead of English.
HINDI_STATES = (r'\bup\b|uttar pradesh|upsssc|uppsc|uppcl|\bbihar\b|bssc|bpsc|\bmp\b|madhya pradesh|mppeb|vyapam|mppsc|rajasthan|rsmssb|'
                r'rssb|rpsc|haryana|hssc|hpsc|himachal|\bhp\b|hpssc|uttarakhand|ukssc|uksssc|ukpsc|jharkhand|jssc|jpsc|chhattisgarh|'
                r'\bcg\b|cgpsc|delhi|dsssb|\bdda\b|allahabad|patna')


def subject_for(text):
    """(code, paper name, topics) for the subject an exam name points to; topics None when no pool exists yet."""
    for pattern, code, name, topics in SUBJECTS:
        if re.search(pattern, text):
            return (code, name, topics) if code else (None, None, None)
    return None


def _language(text):
    return S('HIN1', 'Hindi Language', 0, 1, 0, HINDI) if re.search(HINDI_STATES, text) else S('ENG1', 'English Language', 0, 1, 0, ENGLISH)


def _secs(spec, marks, neg):
    """[(code, name, count, topics)] -> sections with the same marking."""
    return [S(code, name, n, marks, neg, topics) for code, name, n, topics in spec if n]


def general(text, n=25, marks=1, neg=0.25, maths=QUANT, gk=GA):
    lang = _language(text)
    return _secs([('RSN1', 'General Intelligence & Reasoning', n, REASON), ('GA1', 'General Knowledge & Current Affairs', n, gk),
                  ('QNT1', 'Numerical Ability', n, maths), (lang.code, lang.name, n, lang.topics)], marks, neg)


def with_subject(text, subject, subject_n, rest_n, marks=1, neg=0.25, extra=None):
    """Subject paper plus the general sections most recruitment papers add."""
    code, name, topics = subject
    secs = _secs([(code, f"{name} (Subject Knowledge)", subject_n, topics)], marks, neg) if topics else []
    secs += _secs(extra or [('RSN1', 'Reasoning', rest_n, REASON), ('GA1', 'General Awareness', rest_n, GA),
                            ('QNT1', 'Quantitative Aptitude', rest_n, QUANT_BASIC)], marks, neg)
    return secs


def _cat_like():
    return _secs([('ENG1', 'Verbal Ability & Reading Comprehension', 24, ENGLISH_BANK),
                  ('DI1', 'Data Interpretation & Logical Reasoning', 20, ['quant.di', 'reasoning.ranking', 'reasoning.blood_relation', 'reasoning.direction', 'reasoning.inequality']),
                  ('QNT1', 'Quantitative Ability', 22, QUANT)], 3, 1)


def _bank_po():
    return _secs([('ENG1', 'English Language', 30, ENGLISH_BANK), ('QNT1', 'Quantitative Aptitude', 35, QUANT_BANK),
                  ('RSN1', 'Reasoning Ability', 35, REASON_BANK)], 1, 0.25)


def _pcm(pcb=False, n=30):
    third = ('BIO1', 'Biology', n, BIOLOGY) if pcb else ('MAT1', 'Mathematics', n, MATHS_ADV)
    return _secs([('PHY1', 'Physics', n, PHYSICS), ('CHE1', 'Chemistry', n, CHEMISTRY), third], 4, 1)


def _school(text):
    senior = re.search(r'class (ix|x|xi|xii|9|10|11|12)\b|standard (viii|ix)|kvpy|ntse|talent search|mtse|hbbvs', text)
    maths = MATHS_10 if senior else QUANT_BASIC
    return _secs([('MAT1', 'Mathematics', 20, maths), ('SCI1', 'Science', 20, GEN_SCIENCE),
                  ('RSN1', 'Mental Ability', 15, REASON), ('GA1', 'General Knowledge', 10, GA[:12]),
                  ('ENG1', 'English', 10, ENGLISH[:7])], 1, 0)


def _teaching(text, subject):
    """TET / teacher recruitment papers."""
    lang = _language(text)
    if re.search(r'ugc net|\bset\b|kset|state eligibility|csir', text) and not re.search(r'tet\b', text):
        paper1 = _secs([('TCH1', 'Paper 1 – Teaching & Research Aptitude', 25, TEACHING + ['teaching.research']),
                        ('RSN1', 'Paper 1 – Reasoning, Data & ICT', 25, REASON[:6] + ['quant.di'] + COMPUTER)], 2, 0)
        sub = _secs([(subject[0], f"Paper 2 – {subject[1]}", 50, subject[2])], 2, 0) if subject and subject[2] else []
        return paper1 + sub, 180 if sub else 60, 'hard'
    if re.search(r'paper\s*-?\s*(i|1)\b|primary|\bprt\b|jbt|\bett\b|junior teacher|\bntt\b|nursery|d\.?el\.?ed|assistant teacher|'
                 r'level 1|varg 3', text) and not re.search(r'paper\s*-?\s*(ii|2)\b', text):
        return _secs([('CDP1', 'Child Development & Pedagogy', 30, TEACHING), (lang.code, 'Language I', 30, lang.topics),
                      ('ENG1' if lang.code != 'ENG1' else 'HIN1', 'Language II', 30, ENGLISH if lang.code != 'ENG1' else HINDI),
                      ('MAT1', 'Mathematics', 30, QUANT_BASIC), ('EVS1', 'Environmental Studies', 30, ['evs.general', 'evs.animals'] + GEN_SCIENCE[:4])],
                     1, 0), 150, 'medium'
    if re.search(r'\bstet\b', text) and subject and subject[2]:
        # Bihar STET: a subject test for secondary / senior secondary teachers.
        return _secs([(subject[0], subject[1], 100, subject[2]), ('CDP1', 'Teaching Aptitude & Pedagogy', 50, TEACHING)], 1, 0), 150, 'hard'
    if re.search(r'\btet\b|paper\s*-?\s*(ii|2)\b', text) and not re.search(r'\bpgt\b|\btgt\b|lecturer', text):
        # TET Paper II (Classes 6-8): pedagogy, two languages and the subject area.
        other = ('ENG1', 'Language II', 30, ENGLISH) if lang.code != 'ENG1' else ('HIN1', 'Language II', 30, HINDI)
        if subject and subject[2]:
            area = [(subject[0], subject[1], 60, subject[2])]
        else:
            area = [('MAT1', 'Mathematics & Science', 30, QUANT_BASIC + GEN_SCIENCE[:4]),
                    ('SST1', 'Social Studies', 30, ['ga.history', 'ga.geography', 'ga.polity', 'ga.economy'])]
        return _secs([('CDP1', 'Child Development & Pedagogy', 30, TEACHING), (lang.code, 'Language I', 30, lang.topics), other]
                     + area, 1, 0), 150, 'medium'
    if re.search(r'b\.?ed|m\.?ed|b\.?p\.? ?ed', text):
        return _secs([('TCH1', 'Teaching Aptitude', 25, TEACHING), ('GA1', 'General Awareness', 25, GA),
                      ('RSN1', 'Reasoning', 25, REASON), ('ENG1', 'English', 25, ENGLISH)], 1, 0), 120, 'medium'
    pgt = re.search(r'\bpgt\b|lecturer|professor|principal|headmaster|head teacher|school lecturer', text)
    secs = _secs([(subject[0], f"{subject[1]} (Subject)", 60 if pgt else 50, subject[2])], 1, 0.25) if subject and subject[2] else []
    secs += _secs([('CDP1', 'Teaching Aptitude & Pedagogy', 20, TEACHING), ('GA1', 'General Awareness', 15, GA),
                   ('RSN1', 'Reasoning', 15, REASON)], 1, 0.25)
    if not secs[0].code.startswith(('CDP', 'GA')):
        pass
    return secs, 150 if pgt else 120, 'hard' if pgt else 'medium'


def _engineering_job(text, subject):
    if subject and subject[2]:
        return with_subject(text, subject, 60, 0, 1, 0.25, extra=[('RSN1', 'Reasoning', 20, REASON), ('GA1', 'General Awareness', 20, GA)])
    return _secs([('CIV1', 'Engineering Fundamentals', 40, TRADE), ('RSN1', 'Reasoning', 20, REASON),
                  ('QNT1', 'Quantitative Aptitude', 20, QUANT_BASIC), ('GA1', 'General Awareness', 20, GA)], 1, 0.25)


def _trade(text):
    lang = _language(text)
    return _secs([('CIV1', 'Trade / Technical Basics', 30, TRADE), ('QNT1', 'Mathematics', 20, QUANT_BASIC),
                  ('RSN1', 'Reasoning', 20, REASON), ('GA1', 'General Awareness', 20, GA), (lang.code, lang.name, 10, lang.topics)], 1, 0.25)


def pattern_for(group, sub, name):
    """(sections, minutes, difficulty, note) for a new exam."""
    text = f"{name} | {sub}".lower()
    sub_l = sub.lower()
    subject = subject_for(name.lower()) or subject_for(sub_l)
    missing = subject is not None and subject[2] is None
    officer = re.search(r'officer|manager|\bpo\b|executive|grade[ -]?(a|b)\b|\bago\b|probationary|management trainee|\bmt\b|'
                        r'scientist|assistant commandant|\bagm\b|deputy|director', text)
    constable = re.search(r'constable|sepoy|home ?guard|fireman|warder|rifleman|agniveer|soldier|tradesman|driver|\bmts\b|'
                          r'multi[- ]?tasking|attendant|group[ -]?d\b|peon|helper|security guard|chowkidar|guard\b|forest guard|'
                          r'jail|bandi|navik|commando', text)

    if name.lower().startswith('gate '):
        core = subject[2] if subject and subject[2] else ['engineering.core']
        code = subject[0] if subject and subject[2] else 'CIV1'
        return _secs([('RSN1', 'General Aptitude', 10, ['quant.percentage', 'quant.ratio', 'reasoning.number_series', 'english.grammar', 'quant.di']),
                      (code, 'Engineering Maths & Core Subject', 55, core + ENGG_MATHS[:3])], 1.5, 0.5), 180, 'hard', (
            '' if subject and subject[2] else
            f"Core-subject questions for {name} are not in the question bank yet; the paper uses engineering fundamentals and maths.")

    if group == 'Professional Courses':
        if re.search(r'english|vocab|verbal|reading|cloze|para', text):
            return _secs([('ENG1', name, 50, ENGLISH_BANK if re.search('reading|cloze|para', text) else ENGLISH)], 1, 0), 45, 'medium', ''
        if re.search(r'hindi', text):
            return _secs([('HIN1', name, 50, HINDI)], 1, 0), 45, 'medium', ''
        if re.search(r'banking', text):
            return _secs([('GA1', name, 50, GA_BANK)], 1, 0), 40, 'medium', ''
        if re.search(r'geograph|polity|econom|histor|general studies|static gk|current', text):
            topics = (subject[2] if subject and subject[2] else GA)
            return _secs([('GA1', name, 50, topics)], 1, 0), 40, 'hard' if 'advance' in text else 'medium', ''
        if re.search(r'data interpretation|\bdi\b', text):
            return _secs([('DI1', name, 30, ['quant.di', 'quant.percentage', 'quant.ratio', 'quant.average'])], 1, 0), 40, 'hard', ''
        if re.search(r'vedic|stem', text):
            return _secs([('QNT1', name, 40, QUANT_BASIC)], 1, 0), 40, 'medium', ''
        return _secs([('RSN1', 'Logical Reasoning', 25, REASON), ('QNT1', 'Numerical Ability', 25, QUANT_BASIC)], 1, 0), 45, \
            'hard' if 'advance' in text else 'medium', ''

    if group == 'School Level - All India' or 'olympiad' in text or 'smart test' in text:
        return _school(text), 60, 'medium', ''

    if group == 'CUET':
        if 'general test' in text:
            return _secs([('GA1', 'General Knowledge & Current Affairs', 15, GA), ('QNT1', 'Quantitative Reasoning', 15, QUANT_BASIC),
                          ('RSN1', 'Logical & Analytical Reasoning', 20, REASON)], 5, 1), 60, 'medium', ''
        if 'mba' in text:
            return _cat_like(), 120, 'hard', ''
        if 'law' in text:
            subject = ('LGL1', 'Legal Studies', LAW)
        if 'computer' in text:
            subject = ('CSE1', 'Computer Science / IP', CS + COMPUTER)
        if subject and subject[2]:
            return _secs([(subject[0], name.replace('CUET UG ', ''), 50, subject[2])], 5, 1), 60, 'medium', ''
        return general(text, 15, 5, 1, QUANT_BASIC), 60, 'medium', \
            "Subject-specific questions for this CUET paper are not in the question bank yet, so these tests cover the General Test sections."

    if group == 'Foreign Education':
        if re.search(r'ielts|toefl|toeic|test of english', text):
            return _secs([('ENG1', 'Reading', 20, ['english.comprehension']), ('ENG1', 'Grammar & Usage', 20,
                          ['english.grammar', 'english.error_spotting', 'english.sentence_improvement']),
                          ('ENG1', 'Vocabulary', 20, ['english.synonym', 'english.antonym', 'english.idioms', 'english.one_word'])], 1, 0), 60, 'medium', \
                "Objective practice for the reading and language parts; speaking, listening and writing are not tested here."
        if re.search(r'\bgre\b|\bgmat\b|\bsat\b|\bact\b|ukcat', text):
            secs = _secs([('ENG1', 'Verbal Reasoning', 25, ENGLISH_BANK), ('QNT1', 'Quantitative Reasoning', 25, QUANT)], 1, 0)
            if re.search(r'\bact\b', text):
                secs += _secs([('SCI1', 'Science Reasoning', 20, GEN_SCIENCE)], 1, 0)
            if re.search(r'gmat|ukcat', text):
                secs += _secs([('RSN1', 'Data Insights / Decision Making', 20, ['quant.di', 'reasoning.inequality', 'reasoning.ranking'])], 1, 0)
            return secs, 120, 'hard', ''
        return _secs([('MAT1', 'Mathematics', 25, MATHS_ADV), ('PHY1', 'Physics', 20, PHYSICS), ('CHE1', 'Chemistry', 15, CHEMISTRY),
                      ('BIO1', 'Biology', 15, BIOLOGY)], 1, 0), 120, 'hard', ''

    if group == 'Finance':
        topics = ACCOUNTS + ['ga.economy', 'ga.organisations']
        if subject and subject[2] and subject[0] in ('CSE1', 'DM1'):
            topics = subject[2] + ['ga.banking_terms']
        return _secs([('ACC1', 'Banking & Finance', 100, topics)], 1, 0), 120, 'hard', \
            "IIBF papers are case-study heavy; these questions cover the core banking, accounting and law concepts."

    if group == 'IT Placement Papers':
        if subject and subject[0] == 'CSE1':
            return _secs([('CSE1', name, 40, CS + COMPUTER)], 1, 0), 45, 'medium', \
                ("Questions come from programming, data structures and computer fundamentals; language-specific questions "
                 f"for {name} are being added.") if re.search(r'java|php|javascript|c\+\+|aws|operating|network|csa', name.lower()) else ''
        return _secs([('QNT1', 'Quantitative Aptitude', 20, QUANT_BASIC), ('RSN1', 'Logical Reasoning', 20, REASON),
                      ('ENG1', 'Verbal Ability', 20, ENGLISH_BANK), ('CSE1', 'Computer & Programming Fundamentals', 15, CS[:6] + COMPUTER)],
                     1, 0), 90, 'medium', ''

    if group == 'Computer & Information Technology':
        return _secs([('MAT1', 'Mathematics', 40, MATHS_ADV), ('RSN1', 'Analytical Ability & Logical Reasoning', 30, REASON),
                      ('CMP1', 'Computer Awareness', 20, COMPUTER + CS[:4]), ('ENG1', 'General English', 10, ENGLISH)], 1, 0.25), 120, 'hard', ''

    if group == 'Designing':
        return _secs([('DSG1', 'Design & Visual Aptitude', 40, ['design.aptitude', 'design.architecture']), ('ENG1', 'English', 20, ENGLISH),
                      ('GA1', 'General Awareness', 20, GA), ('RSN1', 'Analytical Ability', 20, REASON)], 1, 0.25), 120, 'medium', \
            "Drawing and studio tests are not part of these online mocks."

    if group == 'Management':
        if re.search(r'bba|\bipm\b|ugat|npat|\bset\b|du-jat|jipmat|under ?graduate|bhmct|hotel|ncat|iuet|upes', text):
            secs = _secs([('ENG1', 'English', 25, ENGLISH), ('QNT1', 'Quantitative Aptitude', 25, QUANT_BASIC),
                          ('RSN1', 'Logical Reasoning', 25, REASON), ('GA1', 'General Awareness', 25, GA)], 1, 0.25)
            if re.search(r'hotel|bhmct', text):
                secs += _secs([('HSP1', 'Service Sector Aptitude', 25, ['hospitality.aptitude'])], 1, 0.25)
            return secs, 120, 'medium', ''
        return _cat_like(), 120, 'hard', ''

    if group == 'Law, Arts, Commerce':
        if re.search(r'foundation|cma|ipcc|\bca\b', text):
            return _secs([('ACC1', 'Principles of Accounting', 30, ACCOUNTS), ('LAW1', 'Business Laws', 20, ['commerce.business_law', 'law.acts']),
                          ('ECO1', 'Business Economics', 25, ['commerce.economics', 'ga.economy']), ('QNT1', 'Quantitative Aptitude', 25, QUANT)],
                         1, 0.25), 180, 'hard', ''
        if re.search(r'law|llb|clat|slat|klee', text):
            pg = re.search(r'llb \(3|3 years|du llb|klee|calcutta|rajasthan university|pg', text)
            return _secs([('ENG1', 'English Language', 25, ENGLISH_BANK), ('GA1', 'Current Affairs & GK', 25, GA),
                          ('LGL1', 'Legal Reasoning', 35 if pg else 30, LAW), ('RSN1', 'Logical Reasoning', 25, REASON),
                          ('QNT1', 'Quantitative Techniques', 0 if pg else 10, QUANT_BASIC)], 1, 0.25), 120, 'hard' if pg else 'medium', ''
        if subject and subject[2]:
            return _secs([(subject[0], subject[1], 50, subject[2]), ('GA1', 'General Awareness', 25, GA), ('ENG1', 'English', 25, ENGLISH)],
                         1, 0), 90, 'medium', ''
        return general(text, 25, 1, 0), 90, 'medium', ''

    if group == 'Engineering Entrance':
        if re.search(r'polytechnic|polycet|\biti\b|leet|ppt|jexpo|dseu|diploma', text):
            return _secs([('MAT1', 'Mathematics', 40, MATHS_10), ('PHY1', 'Physics', 30, PHYSICS[:5]), ('CHE1', 'Chemistry', 30, CHEMISTRY[:4])],
                         1, 0), 150, 'medium', ''
        if re.search(r'agri|mppat|aieea|icar', text):
            return _pcm(pcb=True), 180, 'hard', ''
        return _pcm(), 180, 'hard', ''

    if group == 'Medical':
        if re.search(r'pre medical|pmt|cpmt|imat|mcat|neet|rpvt|pre veterinary|bhu pmt', text) and 'pg' not in text:
            return _pcm(pcb=True, n=45), 180, 'hard', ''
        if re.search(r'b\.?sc\.? ?nursing|gnm|cpnet|nursing entrance|nursing cet|b ?pharm|pharmacy entrance', text) and 'officer' not in text:
            return _secs([('PHY1', 'Physics', 20, PHYSICS[:5]), ('CHE1', 'Chemistry', 20, CHEMISTRY[:4]), ('BIO1', 'Biology', 30, BIOLOGY),
                          ('ENG1', 'English', 15, ENGLISH), ('GA1', 'General Knowledge', 15, GA)], 1, 0.25), 120, 'medium', ''
        if subject and subject[2]:
            hard = re.search(r'medical officer|surgeon|resident|usmle|pg|dnb|jrf', text)
            return with_subject(text, subject, 70, 10), 120, 'hard' if hard else 'medium', ''
        if re.search(r'cashier|clerk|personal assistant|\bpa\b|assistant', text):
            return general(text), 120, 'medium', ''
        return with_subject(text, ('NUR1', 'Nursing', NURSING), 70, 10), 120, 'medium', ''

    if group == 'Teaching':
        if re.search(r'tet|teach|pgt|tgt|prt|lecturer|professor|net\b|set\b|kset|b\.?ed|d\.?el|instructor|head|principal|ntt|jbt|ett|'
                     r'counsel|master cadre|assistant teacher|varg|level', text) and not re.search(r'secretariat|accountant|\bldc\b|clerk', text):
            secs, minutes, diff = _teaching(text, subject)
            note = ''
            # Say so when the paper's subject part has no question pool (TET papers are fully covered).
            expects_subject = re.search(r'ugc net|csir|\bset\b|kset|\bpgt\b|\btgt\b|lecturer|professor|senior teacher', name.lower())
            if subject and subject[2] is None or (not subject and expects_subject and not re.search(r'\btet\b', name.lower())):
                note = (f"Subject questions for {name} are not in the question bank yet, so these tests cover the "
                        "general paper (teaching aptitude, reasoning and awareness).")
            return secs, minutes, diff, note
        if subject and subject[2]:
            return with_subject(text, subject, 60, 15), 120, 'medium', ''
        return general(text), 120, 'medium', ''

    if group == 'Civil Services' and re.search(r'teacher|lecturer|professor|headmaster', text):
        secs, minutes, diff = _teaching(text, subject)
        return secs, minutes, diff, '' if subject and subject[2] else (
            f"Subject questions for {name} are not in the question bank yet, so these tests cover teaching aptitude, reasoning and awareness.")

    if re.search(r'\batc\b|air traffic', text):
        return _secs([('PHY1', 'Physics', 40, PHYSICS), ('MAT1', 'Mathematics', 40, MATHS_ADV), ('ENG1', 'English', 20, ENGLISH_BANK)],
                     1, 0.25), 120, 'hard', ''

    if group == 'Civil Services' and not (subject and subject[2]) and not re.search(r'clerk|assistant|ldc|secretariat|steno', text):
        return _secs([('GA1', 'GS – History, Art & Culture', 30, ['ga.history', 'ga.freedom_events', 'ga.culture', 'ga.monuments', 'ga.founders']),
                      ('GA1', 'GS – Geography & Environment', 25, ['ga.geography', 'ga.rivers', 'ga.national_parks', 'environment.ecology', 'ga.states']),
                      ('GA1', 'GS – Polity & Governance', 25, ['ga.polity', 'ga.polity_articles', 'ga.amendments', 'ga.schedules']),
                      ('GA1', 'GS – Economy, Science & Current Affairs', 20, ['ga.economy', 'ga.science', 'ga.organisations', 'ga.important_days']),
                      ('RSN1', 'Aptitude (CSAT)', 20, REASON[:6] + ['quant.percentage', 'quant.ratio', 'english.comprehension'])],
                     2, 0.66), 150, 'hard', \
            "General Studies questions come from all-India pools; add your state's own GK and current affairs separately."

    if constable and not re.search(r'sub inspector|\bsi\b|\basi\b|inspector|head constable|commandant', text):
        if subject and subject[2] and subject[0] in ('CIV1', 'PHY1', 'NUR1', 'PHA1') and re.search(r'trades|technical|tradesman|pharma|nurs', text):
            return with_subject(text, subject, 40, 20), 120, 'medium', ''
        return general(text, 25, 1, 0.25, QUANT_BASIC), 90, 'easy', ''

    if re.search(r'sub inspector|\bsi\b|\basi\b|inspector|head constable', text) and group == 'Defence & Police':
        return general(text, 25, 1, 0.25), 120, 'medium', ''

    if re.search(r'judicial|civil judge|district judge|judge', text):
        return _secs([('LGL1', 'Law', 70, LAW), ('GA1', 'General Knowledge', 20, GA), ('ENG1', 'English', 10, ENGLISH)], 1, 0.25), 120, 'hard', ''

    if group == 'Banking':
        if re.search(r'specialist|\bso\b|it officer|law officer|agriculture|marketing|hr officer|rajbhasha|credit|treasury|'
                     r'programmer|economics|\bafo\b|generalist', text) and subject and subject[2]:
            return _secs([('RSN1', 'Reasoning', 30, REASON_BANK), ('ENG1', 'English Language', 30, ENGLISH_BANK),
                          ('GA1', 'General / Banking Awareness', 25, GA_BANK),
                          (subject[0], f"Professional Knowledge – {subject[1]}", 40, subject[2])], 1, 0.25), 120, 'hard', ''
        return _bank_po(), 60, 'hard' if officer else 'medium', ''

    if group == 'Insurance':
        if re.search(r'nism|irda|agent|junior officer', text):
            return _secs([('GA1', 'Insurance & Financial Markets', 50, ['ga.banking_terms', 'commerce.business_law', 'commerce.accounting_theory', 'ga.economy'])],
                         1, 0.25), 60, 'medium', ''
        if subject and subject[2] and officer and subject[0] not in ('ACC1',):
            return _secs([('RSN1', 'Reasoning', 30, REASON_BANK), ('ENG1', 'English Language', 30, ENGLISH_BANK),
                          (subject[0], f"Professional Knowledge – {subject[1]}", 40, subject[2])], 1, 0.25), 120, 'hard', ''
        return _bank_po(), 60, 'hard' if officer else 'medium', ''

    if group == 'SSC':
        if re.search(r'translator|pradhyapak|hindi', text):
            return _secs([('HIN1', 'General Hindi', 100, HINDI), ('ENG1', 'General English', 100, ENGLISH)], 1, 0.25), 120, 'medium', ''
        if re.search(r'matric', text):
            return general(text, 25, 1, 0.25, QUANT_BASIC), 60, 'easy', ''
        if re.search(r'scientific', text):
            return with_subject(text, ('PHY1', 'Physics & Computer Science', PHYSICS + COMPUTER), 50, 0,
                                extra=[('RSN1', 'Reasoning', 25, REASON), ('GA1', 'General Awareness', 25, GA)]), 120, 'hard', ''
        return general(text), 60, 'medium', ''

    if group == 'Railway':
        if re.search(r'apprentice|scra', text):
            return _secs([('MAT1', 'Mathematics', 30, MATHS_10), ('PHY1', 'Physics', 20, PHYSICS[:5]), ('CHE1', 'Chemistry', 20, CHEMISTRY[:4]),
                          ('RSN1', 'Reasoning', 15, REASON), ('GA1', 'General Awareness', 15, GA)], 1, 0.33), 120, 'medium', ''
        if 'psychometric' in text:
            return _secs([('RSN1', 'Psychometric & Aptitude', 50, REASON)], 1, 0), 60, 'medium', ''
        return _secs([('GA1', 'General Awareness', 40, GA), ('QNT1', 'Mathematics', 30, QUANT), ('RSN1', 'General Intelligence & Reasoning', 30, REASON)],
                     1, 0.33), 90, 'hard' if officer else 'medium', ''

    if subject and subject[2]:
        if subject[0] in ('CIV1', 'PHY1', 'CSE1') or group in ('Graduate Engineering', 'PSUs & Research'):
            if re.search(r'technician|apprentice|trainee \(|helper|operator|maintainer|welder|fitter|electrician|lineman|iti|diploma|'
                         r'tradesman|plant|\bmechanic\b|assistant technician|technical attendant', text) and not officer:
                return _trade(text), 120, 'medium', ''
            if subject[0] in ('CIV1', 'PHY1', 'CSE1'):
                return _engineering_job(text, subject), 120, 'hard' if officer or re.search(r'\bae\b|assistant engineer|scientist', text) else 'medium', ''
        diff = 'hard' if officer or re.search(r'lecturer|professor|scientist|research', text) else 'medium'
        return with_subject(text, subject, 60, 15), 120, diff, ''

    if group in ('Graduate Engineering', 'PSUs & Research') and not re.search(r'clerk|assistant|steno|ldc|udc|secretar|accountant', text):
        if re.search(r'technician|apprentice|helper|operator|maintainer|tradesman|attendant|plant', text):
            return _trade(text), 120, 'medium', ''
        return _engineering_job(text, None), 120, 'hard' if officer else 'medium', \
            "Branch-specific questions are not in the question bank yet; the technical section covers common engineering fundamentals."

    if group == 'Others' and re.search(r'iit jam|jnu|m\.?sc|b\.?sc', text):
        return general(text), 120, 'hard', \
            f"Subject questions for {name} are not in the question bank yet, so these tests cover general aptitude and awareness."

    if re.search(r'steno|typist|data entry|computer operator|\bdeo\b', text):
        return general(text, 25, 1, 0.25) + _secs([('CMP1', 'Computer Awareness', 20, COMPUTER)], 1, 0.25), 120, 'medium', \
            "Skill (typing / shorthand) tests are separate and not part of these mocks."
    note = ''
    if missing:
        note = f"Subject questions for {name} are not in the question bank yet, so these tests cover the general sections."
    return general(text), 120, 'hard' if officer else 'medium', note


def _summary(secs, minutes):
    total = sum(s.count for s in secs)
    marks = sum(s.count * s.marks for s in secs)
    negs = sorted({s.negative for s in secs if s.negative})
    parts = ', '.join(f"{s.name} {s.count}" for s in secs)
    marking = (f"−{negs[0]:g} per wrong answer" if len(negs) == 1 else "negative marking varies by section") if negs else "no negative marking"
    return f"{total} questions, {marks:g} marks, {minutes} minutes ({parts}); {marking}."


def build_exams(existing_names):
    """Exam patterns for every catalog exam the site does not already have."""
    out = []
    for row in rows():
        if row['kind'] != 'exam' or row['site_exam'] or row['exam'] in existing_names:
            continue
        group, sub, name = row['group'], row['sub_category'], row['exam']
        secs, minutes, difficulty, note = pattern_for(group, sub, name)
        secs = [s for s in secs if s.count]
        _, key, _label, icon, color = GROUP_BY_NAME.get(group, GROUP_BY_NAME['Others'])
        pattern = (f"Practice pattern: {_summary(secs, minutes)} Based on the format commonly published for {name}; "
                   "always confirm the current pattern in the official notification.")
        out.append(Exam(name, minutes, secs, pattern, difficulty, mocks=1, pyp=0, group=key, icon=icon, color=color,
                        note=note, light=True))
    return out


