"""Turn the exam list CSV (Category / Sub-Category / Exam, columns 'L0 Name', 'L1 Name', 'L2 Name') into
testseries/content/exam_catalog.csv, the catalog the site builds its exam list and test series from.

    python manage.py import_exam_catalog "C:/path/All_Exam_Details.csv"

Rows for exams the site already has are linked to that exam (see ALIASES) so nothing is duplicated; placeholder rows
(recruitment rounds, sample tests, links, books), hobby and skills courses, driving-licence and language courses are
left out; school rows become board classes to build. Re-run it whenever the list changes, then build_test_content.
"""
import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from testseries.content.patterns import EXAMS

OUT = Path(__file__).resolve().parents[2] / 'content' / 'exam_catalog.csv'
FIELDS = ['kind', 'group', 'sub_category', 'exam', 'site_exam', 'board', 'grade', 'stream']

SKIP_GROUPS = {'New Level 0', 'Driving License', 'Professional Certification Courses'}
SKIP_SUBS = {
    ('Professional Courses', s) for s in (
        'Drama', 'Daily Activities', 'Design And Creativity', 'Personality Development', 'Kids Learning', 'Health and Fitness',
        'NSDC', 'TV Shows', 'Blogging', 'Social Media', 'Trading', 'Entrepreneurship', 'Sales & Marketing', 'Operations',
        'Internet', 'Computer Systems', 'Computer Basics', 'Research & Analytics', 'Ecommerce', 'IT & Software', 'Spoken English',
        'Artificial Intelligence', 'Microsoft Office')
} | {('Law, Arts, Commerce', 'French'), ('Foreign Education', 'Foreign Languages'), ('Others', 'Gibbon'),
     ('Defence & Police', 'Sashastra Seema Bal (SSB)')}
SKIP_EXAMS = {'Books', 'Offline Books', 'Foreign Trainer in English', 'Android', 'SSB - Mock Interview Test'}
MOVE = {'National Council Licensure Examination (NCLEX)': ('Medical', 'Other Medical Exams')}

# CSV exam name -> exam the site already has.
ALIASES = {
    'JEE Main Advanced': 'JEE Main', 'COMEDK': 'COMEDK UGET', 'VIT Engineering Entrance Exam': 'VITEEE',
    'Maharashtra Common Entrance Test - Engineering (MHT CET)': 'MHT CET', 'Karnataka Common Entrance Test KCET': 'KCET',
    'AP EAMCET Engineering': 'AP EAPCET', 'TS EAMCET Engineering': 'TS EAPCET', 'Gujarat Common Entrance Test GUJCET': 'GUJCET',
    'Kalinga Institute of Industrial Technology Entrance Exam ( KIITEE)': 'KIITEE', 'JEE B Arch': 'JEE Main Paper 2 (B.Arch)',
    'Architecture NATA': 'NATA', 'National Aptitude Test in Architecture': 'NATA',
    'GATE Computer Science and Information Technology CS And IT': 'GATE', 'GATE Electrical Engineering EE': 'GATE EE',
    'GATE Mechanical Engineering ME': 'GATE ME', 'GATE Civil Engineering CE': 'GATE CE',
    'GATE Electronics and Communication Engineering EC': 'GATE EC', 'IES - ESE (CE)': 'UPSC ESE', 'IES - ESE (EE)': 'UPSC ESE',
    'IES - ESE (EC)': 'UPSC ESE', 'IES - ESE (ME)': 'UPSC ESE', 'JIPMER': 'NEET UG', 'UPSC CMSE': 'UPSC CMS',
    'AIIMS Nursing Officer': 'AIIMS NORCET', 'Graduate Pharmacy Aptitude Test': 'GPAT',
    'SSC CHSL (Combined Higher Secondary Level)': 'SSC CHSL', 'SSC Constable (GD)': 'SSC GD', 'SSC Sub Inspector (CPO)': 'SSC CPO',
    'SSC Stenographer Grade C & D': 'SSC Stenographer', 'SSC Junior Engineer Civil': 'SSC JE', 'SSC Junior Engineer Mechanical': 'SSC JE',
    'SSC Junior Engineer Electrical': 'SSC JE', 'SSC Selection Post Phase VIII': 'SSC Selection Post',
    'RRB (NTPC)': 'RRB NTPC', 'RRB/RRC Group D': 'RRB Group D', 'RRB / RRC Group D (Telugu)': 'RRB Group D',
    'RRB JE ME': 'RRB JE', 'RRB JE IT': 'RRB JE', 'RRB JE EC': 'RRB JE', 'RRB Junior Engineering Civil': 'RRB JE',
    'RRB Junior Engineering Electrical': 'RRB JE', 'RPF SI (Sub Inspector)': 'RPF SI', 'RPF Constable Ancillary': 'RPF Constable',
    'IBPS RRB Scale I': 'IBPS RRB PO', 'IBPS RRB Office Assistant': 'IBPS RRB Clerk', 'IBPS SO Prelims': 'IBPS SO',
    'NABARD (Assistant Manager Grade A & B)': 'NABARD Grade A', 'SEBI Grade A (Assistant Manager)': 'SEBI Grade A',
    'LIC AAO (Generalist)': 'LIC AAO', 'NIACL (AO)': 'NIACL AO', 'NIACL (Assistant)': 'NIACL Assistant',
    'IDBI Bank Assistant Manager': 'IDBI Junior Assistant Manager', 'UPSC Central Armed Police Forces AC': 'CAPF Assistant Commandant',
    'Air Force X & Y Group': 'Indian Air Force', 'IAF Agniveervayu': 'Indian Air Force', 'Indian Navy Agniveer SSR': 'Indian Navy Agniveer',
    'Indian Navy Agniveer MR': 'Indian Navy Agniveer', 'Artificer Apprentice (AA) & Senior Secondary Recruits (SSR)': 'Indian Navy Agniveer',
    'INET - Indian Navy Entrance Test (Officer Entry)': 'INET (Indian Navy)', 'Soldier GD': 'Indian Army GD',
    'Indian Army Soldier Clerk': 'Indian Army Agniveer Clerk', 'Coast Guard (Navik) GD': 'Indian Coast Guard',
    'Coast Guard (Navik) DB': 'Indian Coast Guard', 'Coast Guard (Yantrik)': 'Indian Coast Guard', 'UPSC NDA': 'NDA',
    'Indian Military Academy (IMA)': 'CDS', 'Officers Training Academy (OTA)': 'CDS', 'Territorial Army Officer': 'Territorial Army',
    'UP Police Sub Inspector': 'UP Police SI', 'Bihar Police Constable (CSBC)': 'Bihar Police Constable',
    'MP Police (Constable)': 'MP Police Constable', 'CISF Head Constable': 'CAPF Head Constable',
    'CRPF Head Constable Ministerial': 'CAPF Head Constable', 'IB ACIO Grade - II': 'IB ACIO',
    'Intelligence Bureau Security Assistant': 'IB Security Assistant', 'EPFO Social Security Assistant': 'EPFO SSA',
    'ESIC Upper Division Clerk (UDC)': 'ESIC UDC', 'UPSC EPFO - Enforcement Officer / Account Officer': 'UPSC EPFO',
    'FCI Phase I': 'FCI Assistant Grade 3', 'FCI Assistant Phase III (AG)-III': 'FCI Assistant Grade 3',
    'UPSSSC Preliminary Eligibility Test': 'UPSSSC PET', 'UPSSSC Rajasva Lekhpal': 'UP Lekhpal',
    'UPSSSC Village Development Officer': 'VDO / Gram Sevak', 'BSSC Inter Level': 'Bihar SSC Inter Level',
    'UPSC Prelims': 'UPSC Civil Services', 'Uttar Pradesh PSC': 'UPPSC PCS', 'Bihar PSC': 'BPSC CCE',
    'Madhya Pradesh Public Service Commission (MPPSC)': 'MPPSC State Service', 'Rajasthan Public Service Commission (RPSC)': 'RPSC RAS',
    'Rajasthan State and Subordinate Services': 'RPSC RAS', 'Maharashtra Public Service Commission': 'MPSC Rajyaseva',
    'TNPSC (Group-I Services)': 'TNPSC Group 1', 'TNPSC (Group-IV Services)': 'TNPSC Group 4',
    'Karnataka Public Service Commission (KPSC)': 'KPSC KAS', 'Andhra Pradesh PSC': 'APPSC Group 1',
    'Telangana State Public Service Commission Group 1': 'TGPSC Group 1', 'West Bengal Public Service Commission': 'WBCS',
    'Odisha Public Service Commission (OPSC)': 'OPSC OCS', 'Odisha Administrative Services': 'OPSC OCS', 'Haryana PSC': 'HPSC HCS',
    'Chhattisgarh PSC (CGPSC)': 'CGPSC State Service', 'Jharkhand PSC (JPSC)': 'JPSC CCE',
    'Uttarakhand Public Service Commission (UKPSC)': 'UKPSC PCS', 'Himachal Pradesh Public Service Commission (HPPSC)': 'HPPSC HPAS',
    'Punjab Public Service Commission (PPSC)': 'PPSC Civil Services', 'CTET Paper - I': 'CTET',
    'CTET Paper-II (Science & Mathematics)': 'CTET', 'CTET Paper-II (Social Science)': 'CTET', 'UPTET Paper - I': 'UPTET',
    'Super TET Paper - I': 'Super TET', 'Super TET Paper - II (Social Science)': 'Super TET',
    'Super TET Paper - II (Science & Mathematics)': 'Super TET', 'Rajasthan Teachers Eligibility Test - Level 1 Primary Level (RTET)': 'REET',
    'RTET - Level 2 (Mathematics & Science)': 'REET', 'RTET - Level 2 (Social Studies)': 'REET', 'Haryana Primary Teacher (PRT)': 'HTET',
    'Maharashtra Teacher Eligibility Test': 'MAHA TET', 'KTET Category III': 'KTET', 'OTET Paper I': 'OTET',
    'OTET Paper II (Social Science)': 'OTET', 'MPTET Paper I - Varg 3': 'MP TET (Varg 3)', 'CGTET Paper - I': 'CG TET',
    'CGTET Paper - II (Science & Mathematics)': 'CG TET', 'CGTET Paper - II (Social Studies)': 'CG TET', 'KVS PRT': 'NVS / KVS PRT',
    'DSSSB PRT': 'DSSSB', 'UGC NET Paper I': 'UGC NET', 'Integrated Programme in Management IPM (IIM-Indore)': 'IPMAT',
    'IPM (IIM-Indore)': 'IPMAT', 'Common Management Admission Test (CMAT)': 'CMAT', 'MAH - CET (MBA)': 'MAH MBA CET',
    'Management Aptitude Test (MAT)': 'MAT', 'AIMS Test for Management Admissions (ATMA)': 'ATMA', 'NPAT (BBA)': 'NPAT',
    'CLAT UG': 'CLAT', 'CLAT (PG)': 'CLAT PG', 'AILET (UG)': 'AILET', 'AIBE (Bar Council)': 'AIBE', 'MH CET LLB 5 Years': 'MH CET Law',
    'ICSI CSEET': 'CSEET', 'Integrated Professional Competence Course (IPCC)': 'CA Intermediate',
    'NCHM JEE (Hotel Mgmt & Catering)': 'NCHM JEE', 'Undergraduate Common Entrance Exam for Design (UCEED)': 'UCEED',
    'NID Bachelor of Design': 'NID DAT Prelims', 'NIFT B.Des': 'NIFT Entrance', 'NIMCET (NIT)': 'NIMCET', 'IISER SCB': 'IISER IAT',
    'NEST National Entrance Screening Test': 'NEST', 'AIEEA UG Exam ICAR': 'CUET ICAR UG (Agriculture)',
    'Course on Computer Concepts (CCC)': 'NIELIT CCC', 'TCS National Qualifier Test (NQT)': 'TCS NQT', 'Wipro': 'Wipro NLTH',
    'Infosys': 'Infosys Online Test', 'Cognizant': 'Cognizant GenC', 'Placements (Common)': 'Campus Placement Aptitude',
    'Common IT Placement Paper': 'Campus Placement Aptitude', 'C Language': 'C Programming', 'Python': 'Python Programming',
    'DBMS': 'DBMS & SQL', 'SQL': 'DBMS & SQL', 'Sainik School Entrance Class VI': 'Sainik School (AISSEE)',
    'Sainik School Entrance Class IX': 'Sainik School Class 9 (AISSEE)', 'Jawahar Navodaya Entrance Class VI': 'JNVST (Navodaya)',
    'Jawahar Navodaya Entrance Class IX': 'JNVST Class 9', 'Rashtriya Military School Entrance Class VI': 'RMS CET',
    'NCO (National Cyber Olympiad)': 'NCO Cyber Olympiad', 'SOF - NSO Class I - IV': 'NSO Science Olympiad',
    'SOF - NSO Class V - X': 'NSO Science Olympiad', 'SOF - NSO Class XI - XII': 'NSO Science Olympiad',
    'IMO Class V - X': 'IMO Maths Olympiad', 'IMO Class I - IV': 'IMO Maths Olympiad', 'IEO Class III': 'IEO English Olympiad',
    'IEO Class IV': 'IEO English Olympiad', 'IEO Class V': 'IEO English Olympiad', 'IEO Class IX': 'IEO English Olympiad',
    'IEO Class X': 'IEO English Olympiad', 'IEO Class XI': 'IEO English Olympiad', 'IEO Class XII': 'IEO English Olympiad',
    'RRB NTPC (Bengali)': 'RRB NTPC', 'RRB NTPC (Telugu)': 'RRB NTPC', 'RRB NTPC (Marathi)': 'RRB NTPC', 'RRB NTPC (Gujarati)': 'RRB NTPC',
    'RRB NTPC (Kannada)': 'RRB NTPC', 'RRB NTPC (Odia)': 'RRB NTPC', 'RRB NTPC (Tamil)': 'RRB NTPC', 'RRB NTPC (Malayalam)': 'RRB NTPC',
    'Kerala PSC Degree Level': 'Kerala PSC', 'AIIMS Delhi Staff Nurse': 'Staff Nurse (Govt) Exam',
}
# Generic names made specific (CSV name -> name on the site).
RENAMES = {
    ('IT Placement Papers', 'English'): 'Placement Paper – English (Verbal Ability)',
    ('IT Placement Papers', 'Computer'): 'Placement Paper – Computer Fundamentals',
    ('Foreign Education', 'AP'): 'AP (Advanced Placement) Exams', ('Foreign Education', 'SAT'): 'SAT',
    ('Foreign Education', 'ACT'): 'ACT', ('Law, Arts, Commerce', 'Commerce'): 'Commerce (General)',
    ('Management', 'BBA'): 'BBA Entrance', ('Computer & Information Technology', 'BCA'): 'BCA Entrance',
    ('Computer & Information Technology', 'JNU'): 'JNU MCA Entrance', ('Management', 'Hotel Management'): 'Hotel Management Entrance',
    ('Government Exams', 'Junior Assistant'): 'NBE Junior Assistant', ('Others', 'Current Affairs'): 'Current Affairs',
    ('Professional Courses', 'Psychometric'): 'Psychometric Test', ('Management', 'SET'): 'SET (Symbiosis Entrance Test)',
    ('Management', 'IGNOU'): 'IGNOU OPENMAT', ('Others', 'JEXPO'): 'JEXPO (WB Polytechnic)', ('Others', 'HSEE'): 'HSEE (IIT Madras)',
    ('Government Exams', 'Bank Note Press'): 'SPMCIL Bank Note Press', ('Civil Services', 'NCERT'): 'UPSC NCERT Foundation (GS)',
}

ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12}
BOARD_CODES = {
    'Bihar Board': 'bseb', 'Rajasthan Board': 'rj', 'Jharkhand Board': 'jh', 'Punjab Board': 'pb', 'Uttar Pradesh (UP Board)': 'up',
    'Haryana Board': 'hr', 'Himachal Pradesh Board': 'hp', 'Uttarakhand Board': 'uk', 'Madhya Pradesh Board': 'mp',
    'Maharashtra Board': 'mh', 'Gujarat Board': 'gj', 'West Bengal Board': 'wb', 'Kerala Board': 'kl', 'Andhra Pradesh Board': 'ap',
    'Tamil Nadu Board': 'tn', 'Jammu and Kashmir Board': 'jk', 'Odisha Board': 'od', 'Assam State Board (SEBA)': 'as',
    'Karnataka Board': 'ka', 'Telangana Board': 'ts', 'Arunachal Pradesh Board': 'ar', 'Chhattisgarh Board': 'cg',
    'Manipur Board': 'mn', 'Goa Board': 'ga', 'Meghalaya Board': 'ml', 'Mizoram Board': 'mz', 'CBSE': 'cbse', 'ICSE': 'icse',
    'NIOS Board': 'nios',
}


def clean(text):
    text = (text or '').replace('\ufffd\ufffd\ufffd', "'").replace('\ufffd', "'")
    return ' '.join(text.split())


def norm(text):
    text = text.lower().replace('&', ' and ')
    return ' '.join(re.sub(r'[^a-z0-9 ]+', ' ', text).split())


def school_class(name):
    """'Goa Board Class XI (Commerce)' -> (11, ['commerce']); KG/Nursery/Montessori -> None."""
    m = re.search(r'class\s*-?\s*([ivx]+|\d+)\b', name, re.I)
    if not m:
        return None
    raw = m.group(1).upper()
    grade = ROMAN.get(raw) or (int(raw) if raw.isdigit() else None)
    if not grade:
        return None
    lower = name.lower()
    streams = [s for s, words in (('science', ('science',)), ('commerce', ('commerce',)), ('arts', ('arts', 'humanities')))
               if any(w in lower for w in words)]
    if grade >= 11 and not streams:
        streams = ['science', 'commerce', 'arts']
    return grade, streams or ['']


class Command(BaseCommand):
    help = __doc__.splitlines()[0]

    def add_arguments(self, parser):
        parser.add_argument('csv_path')

    def handle(self, csv_path, **opts):
        path = Path(csv_path)
        if not path.exists():
            raise CommandError(f"{path} not found")
        with path.open(encoding='utf-8', errors='replace', newline='') as fh:
            rows = [(clean(r.get('L0 Name')), clean(r.get('L1 Name')), clean(r.get('L2 Name'))) for r in csv.DictReader(fh)]

        site = {norm(e.name): e.name for e in EXAMS if not e.light}  # exams with a researched pattern
        aliases = {norm(k): v for k, v in ALIASES.items()}
        out, seen, skipped = [], set(), 0
        for group, sub, name in rows:
            if not name or group in SKIP_GROUPS and name not in MOVE or (group, sub) in SKIP_SUBS or name in SKIP_EXAMS \
                    or name.startswith('http'):
                skipped += 1
                continue
            group, sub = MOVE.get(name, (group, sub))
            if group.startswith('School Level') and sub in BOARD_CODES:
                parsed = school_class(name)
                if not parsed:
                    skipped += 1   # Nursery / LKG / UKG / Montessori: no pre-school content yet
                    continue
                grade, streams = parsed
                for stream in streams:
                    key = ('school', BOARD_CODES[sub], grade, stream)
                    if key not in seen:
                        seen.add(key)
                        out.append({'kind': 'school', 'group': group, 'sub_category': sub, 'exam': name,
                                    'board': BOARD_CODES[sub], 'grade': grade, 'stream': stream})
                continue
            name = RENAMES.get((group, name), name)
            if sub == 'IPM Olympiads':
                name = 'IPM Olympiad ' + name.replace('Standard - ', 'Standard ')
            name = name[:100]
            site_exam = site.get(norm(name)) or aliases.get(norm(name), '')
            key = ('exam', site_exam or norm(name))
            if key in seen:
                continue
            seen.add(key)
            out.append({'kind': 'exam', 'group': group, 'sub_category': sub, 'exam': site_exam or name, 'site_exam': site_exam})

        with OUT.open('w', encoding='utf-8', newline='') as fh:
            writer = csv.DictWriter(fh, FIELDS)
            writer.writeheader()
            writer.writerows(out)
        exams = [r for r in out if r['kind'] == 'exam']
        self.stdout.write(self.style.SUCCESS(
            f"{len(rows)} rows: {sum(1 for r in exams if not r['site_exam'])} new exams, "
            f"{sum(1 for r in exams if r['site_exam'])} linked to existing exams, "
            f"{sum(1 for r in out if r['kind'] == 'school')} school classes, {skipped} skipped. Wrote {OUT}."
        ))
