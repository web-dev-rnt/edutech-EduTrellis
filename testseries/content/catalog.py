"""The exam catalog: every exam's category and sub-category (the three levels of the exam list), read from
exam_catalog.csv (see the import_exam_catalog command). Practice patterns for the new exams are in catalog_patterns.py.

Exams that already had a researched pattern keep it; they only take their category and sub-category from the list.
New exams get a "light" series (2 full mocks, a few topic tests and a free demo) built from the question pools that fit
the paper. Patterns follow the format commonly published for each exam; where the subject paper has no question pool
yet, the series covers the general sections and says so.
"""
import csv
from functools import lru_cache
from pathlib import Path

CATALOG_CSV = Path(__file__).with_name('exam_catalog.csv')

# Category (first level of the list): (CSV name, key, label shown on the site, icon, colour)
GROUPS = [
    ('School Level - All India', 'school-exams', 'School Exams & Olympiads', 'school', '#0f766e'),
    ('Engineering Entrance', 'engineering', 'Engineering Entrance', 'gears', '#2563eb'),
    ('Medical', 'medical', 'Medical & Nursing', 'stethoscope', '#dc2626'),
    ('SSC', 'ssc', 'SSC', 'user-tie', '#1d4ed8'),
    ('Railway', 'railway', 'Railways', 'train', '#b45309'),
    ('Banking', 'banking', 'Banking', 'building-columns', '#0369a1'),
    ('Insurance', 'insurance', 'Insurance', 'shield-heart', '#0e7490'),
    ('Defence & Police', 'defence-police', 'Defence & Police', 'shield-halved', '#1e3a8a'),
    ('Civil Services', 'civil-services', 'Civil Services & State PSC', 'landmark', '#9a3412'),
    ('Government Exams', 'government', 'Government Exams', 'building-flag', '#4338ca'),
    ('Teaching', 'teaching', 'Teaching', 'chalkboard-user', '#16a34a'),
    ('Graduate Engineering', 'graduate-engineering', 'Engineering Jobs & GATE', 'helmet-safety', '#ca8a04'),
    ('PSUs & Research', 'psu', 'PSUs & Research', 'industry', '#475569'),
    ('Management', 'management', 'MBA & Management', 'briefcase', '#7c3aed'),
    ('Law, Arts, Commerce', 'law-commerce', 'Law, CA, CS & Commerce', 'scale-balanced', '#b45309'),
    ('CUET', 'cuet', 'CUET', 'graduation-cap', '#0891b2'),
    ('Designing', 'design', 'Design & Fashion', 'pen-ruler', '#db2777'),
    ('Computer & Information Technology', 'computer-it', 'Computer & IT Entrance', 'computer', '#4f46e5'),
    ('IT Placement Papers', 'placement', 'IT Placements & Programming', 'laptop-code', '#2563eb'),
    ('Finance', 'finance', 'Banking Certifications (JAIIB, CAIIB)', 'coins', '#a16207'),
    ('Foreign Education', 'foreign', 'Study Abroad Exams', 'earth-asia', '#0d9488'),
    ('Professional Courses', 'skills', 'Aptitude, English & GK Practice', 'brain', '#9333ea'),
    ('Others', 'others', 'University & Other Entrance', 'layer-group', '#64748b'),
]
GROUP_BY_NAME = {g[0]: g for g in GROUPS}

# Exams that had a pattern before the list was imported and are not in it: (category, sub-category).
PLACEMENT_FALLBACK = {
    'JEE Advanced': ('Engineering Entrance', 'Engineering All India'),
    'Polytechnic Entrance': ('Engineering Entrance', 'Polytechnic'),
    'FMGE': ('Medical', 'PG Medical Entrance'), 'INI-CET': ('Medical', 'PG Medical Entrance'),
    'NIPER JEE': ('Medical', 'Pharmacy Entrance'), 'Pharmacist (Govt) Exam': ('Medical', 'Pharmacy Entrance'),
    'BSc Nursing Entrance': ('Medical', 'State Level Exams'), 'RRB Paramedical': ('Railway', 'Railway Recruitment Board (RRB)'),
    'NDA GAT': ('Defence & Police', 'UPSC NDA'), 'CDS GK': ('Defence & Police', 'UPSC CDS'), 'CDS Maths': ('Defence & Police', 'UPSC CDS'),
    'Sub Inspector (SI)': ('Defence & Police', 'State Police'), 'State Police Constable': ('Defence & Police', 'State Police'),
    'UPSC CSAT': ('Civil Services', 'UPSC'), 'State PSC': ('Civil Services', 'State PSC Prelims'),
    'GPSC Class 1-2': ('Civil Services', 'State PSC Prelims'), 'APSC CCE': ('Civil Services', 'State PSC Prelims'),
    'JKPSC CCE': ('Civil Services', 'State PSC Prelims'), 'Judicial Services': ('Government Exams', 'High Court'),
    'Supreme Court JCA': ('Government Exams', 'High Court'), 'High Court Clerk / Assistant': ('Government Exams', 'High Court'),
    'CUET UG': ('CUET', 'CUET UG'), 'IIT JAM': ('Others', 'IIT JAM'), 'ICAR AIEEA PG': ('Others', 'B.Sc. & M.Sc. Entrance Examination'),
    'CSIR NET': ('Teaching', 'CSIR NET'), 'State TET': ('Teaching', 'State Eligibility Test'),
    'KVS Teacher': ('Teaching', 'Kendriya Vidyalaya Sangathan KVS'), 'Bihar STET': ('Teaching', 'Bihar Special Teacher Eligibility Test (STET)'),
    'PSTET': ('Teaching', 'State Eligibility Test'), 'TNTET': ('Teaching', 'State Eligibility Test'), 'APTET': ('Teaching', 'State Eligibility Test'),
    'TS TET': ('Teaching', 'State Eligibility Test'), 'State SET (Paper 1)': ('Teaching', 'State Eligibility Test'),
    'B.Ed Entrance': ('Teaching', 'B.Ed/M.Ed Entrance'), 'CA Foundation Economics': ('Law, Arts, Commerce', 'Institute of Chartered Accountants of India (ICAI)'),
    'IRDAI Assistant Manager': ('Insurance', 'Junior Officer (IRDA)'), 'GATE DA': ('Graduate Engineering', 'GATE'),
    'Data Structures & Algorithms': ('IT Placement Papers', 'Programming Languages'),
    'Accenture Assessment': ('IT Placement Papers', 'Placement Papers'), 'NIELIT O Level': ('Computer & Information Technology', 'Computer Exams'),
    'IOQM': ('School Level - All India', 'Olympiads'), 'Olympiad': ('School Level - All India', 'Olympiads'),
    'NMMS': ('School Level - All India', 'Scholarship Exams'), 'IGKO GK Olympiad': ('School Level - All India', 'Olympiads'),
}
# Old homepage group key -> category, for any exam not placed above.
OLD_GROUP_FALLBACK = {
    'engineering': 'Engineering Entrance', 'medical': 'Medical', 'ssc-railway': 'SSC', 'banking': 'Banking',
    'defence-police': 'Defence & Police', 'civil-services': 'Civil Services', 'state-govt': 'Government Exams',
    'mba-law': 'Management', 'university': 'Others', 'teaching': 'Teaching', 'commerce': 'Law, Arts, Commerce',
    'programming': 'IT Placement Papers', 'scholarship': 'School Level - All India',
}

@lru_cache(maxsize=1)
def rows():
    if not CATALOG_CSV.exists():
        return []
    with CATALOG_CSV.open(encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


@lru_cache(maxsize=1)
def placements():
    """Exam name -> (category, sub-category) for every exam on the site."""
    from .patterns import EXAMS

    placed = {}
    for row in rows():
        if row['kind'] == 'exam':
            placed.setdefault(row['exam'], (row['group'], row['sub_category']))
    for exam in EXAMS:
        if exam.name not in placed:
            group, sub = PLACEMENT_FALLBACK.get(exam.name) or (OLD_GROUP_FALLBACK.get(exam.group, 'Others'), 'Popular Exams')
            placed[exam.name] = (group, sub)
    return placed


def placement(name):
    return placements().get(name, ('Others', 'Other Exams'))


def school_classes():
    """{board code: {(grade, stream)}} the catalog asks for."""
    out = {}
    for row in rows():
        if row['kind'] == 'school':
            out.setdefault(row['board'], set()).add((int(row['grade']), row['stream']))
    return out


def exam_groups(preferred_order=()):
    """[(key, label, icon, [exam names])] in list order: exams that already existed first, then the rest."""
    from .patterns import EXAMS

    rank = {name: i for i, name in enumerate(preferred_order)}
    names = [e.name for e in EXAMS]
    grouped = []
    for csv_name, key, label, icon, _color in GROUPS:
        members = [n for n in names if placement(n)[0] == csv_name]
        members.sort(key=lambda n: (rank.get(n, len(rank)), names.index(n)))
        if members:
            grouped.append((key, label, icon, members))
    return grouped
