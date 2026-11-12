"""On-screen tools that real exams provide, applied to their pattern mocks."""

# Exam name (TestSeries.exam) -> Test.calculator
EXAM_CALCULATORS = {
    'GATE': 'scientific',        # virtual scientific calculator in the CBT
    'IIT JAM': 'scientific',     # virtual scientific calculator in the CBT
    'CAT': 'basic',              # on-screen basic calculator
    'CA Foundation': 'basic',    # ICAI allows a simple non-programmable calculator
    'CA Intermediate': 'basic',
    'CMA Foundation': 'basic',   # ICMAI allows a simple calculator
    'CA Foundation Economics': 'basic',
    'GATE EE': 'scientific',
    'GATE ME': 'scientific',
    'GATE CE': 'scientific',
    'GATE EC': 'scientific',
    'GATE DA': 'scientific',
    'TCS NQT': 'basic',          # TCS iON on-screen calculator in the Numerical Ability section
    'GPAT': 'none',
}

# Home page "Browse all test series" tabs: (key, label, icon, exam names in display order).
# Series whose exam is not listed here fall into the last tab.
EXAM_GROUPS = [
    ('engineering', 'Engineering', 'gears', [
        'JEE Main', 'JEE Advanced', 'BITSAT', 'VITEEE', 'MHT CET', 'WBJEE', 'KCET', 'AP EAPCET',
        'TS EAPCET', 'GATE', 'GATE EE', 'GATE ME', 'GATE CE', 'GATE EC', 'GATE DA', 'UPSC ESE', 'NATA', 'Polytechnic Entrance',
        'COMEDK UGET', 'SRMJEEE', 'KIITEE', 'KEAM', 'GUJCET', 'JEE Main Paper 2 (B.Arch)',
    ]),
    ('medical', 'Medical', 'stethoscope', [
        'NEET UG', 'AIIMS', 'NEET PG', 'INI-CET', 'NEET MDS', 'FMGE', 'AIIMS NORCET', 'UPSC CMS',
        'GPAT', 'NIPER JEE', 'Pharmacist (Govt) Exam', 'Staff Nurse (Govt) Exam', 'BSc Nursing Entrance',
    ]),
    ('ssc-railway', 'SSC & Railways', 'train', [
        'SSC CGL', 'SSC CHSL', 'SSC MTS', 'SSC GD', 'SSC JE', 'SSC Stenographer',
        'SSC CPO', 'SSC Selection Post', 'RRB NTPC', 'RRB Group D', 'RRB ALP', 'RRB JE',
        'RRB Technician', 'RRB Paramedical',
    ]),
    ('banking', 'Banking & Insurance', 'building-columns', [
        'IBPS PO', 'IBPS Clerk', 'SBI PO', 'SBI Clerk', 'IBPS RRB PO', 'IBPS RRB Clerk',
        'RBI Grade B', 'RBI Assistant', 'NABARD Grade A', 'SEBI Grade A', 'LIC AAO',
        'IBPS SO', 'IDBI Junior Assistant Manager', 'NABARD Development Assistant', 'LIC Assistant', 'LIC ADO',
        'NIACL AO', 'NIACL Assistant', 'NICL AO', 'IRDAI Assistant Manager', 'RBI Office Attendant', 'SBI Apprentice',
    ]),
    ('defence-police', 'Defence & Police', 'shield-halved', [
        'NDA', 'NDA GAT', 'CDS', 'CDS GK', 'CDS Maths', 'AFCAT', 'CAPF Assistant Commandant', 'Indian Air Force', 'Indian Army GD',
        'Indian Navy Agniveer', 'Indian Coast Guard', 'Sub Inspector (SI)', 'State Police Constable',
        'Delhi Police Constable', 'RPF Constable',
        'INET (Indian Navy)', 'Territorial Army', 'Indian Army Agniveer Clerk', 'CAPF Head Constable', 'RPF SI',
        'UP Police Constable', 'UP Police SI', 'Bihar Police Constable', 'Bihar Police SI', 'MP Police Constable',
        'Rajasthan Police Constable', 'Haryana Police Constable', 'Delhi Police Head Constable',
    ]),
    ('civil-services', 'Civil Services', 'landmark', [
        'UPSC Civil Services', 'UPSC CSAT', 'State PSC', 'UPSC EPFO', 'Judicial Services',
        'UPPSC PCS', 'BPSC CCE', 'MPPSC State Service', 'RPSC RAS', 'MPSC Rajyaseva', 'TNPSC Group 1', 'TNPSC Group 4',
        'KPSC KAS', 'APPSC Group 1', 'TGPSC Group 1', 'WBCS', 'OPSC OCS', 'HPSC HCS', 'CGPSC State Service', 'JPSC CCE',
        'UKPSC PCS', 'HPPSC HPAS', 'Kerala PSC', 'GPSC Class 1-2', 'PPSC Civil Services', 'APSC CCE', 'JKPSC CCE',
    ]),
    ('state-govt', 'State & Central Govt Jobs', 'building-flag', [
        'UPSSSC PET', 'UP Lekhpal', 'VDO / Gram Sevak', 'RSMSSB Patwari', 'MP Patwari', 'Bihar SSC Inter Level',
        'IB ACIO', 'IB Security Assistant', 'FCI Assistant Grade 3', 'EPFO SSA', 'ESIC UDC', 'Supreme Court JCA',
        'High Court Clerk / Assistant',
    ]),
    ('mba-law', 'MBA & Law', 'briefcase', [
        'CAT', 'XAT', 'MAT', 'CMAT', 'NMAT', 'IPMAT', 'SNAP', 'MAH MBA CET', 'NPAT', 'ATMA',
        'CLAT', 'AILET', 'CLAT PG', 'AIBE', 'MH CET Law',
    ]),
    ('university', 'University & Research', 'graduation-cap', [
        'CUET UG', 'CUET PG', 'IIT JAM', 'NIMCET', 'CSIR NET', 'UGC NET', 'NIFT Entrance',
        'IISER IAT', 'NEST', 'ICAR AIEEA PG', 'CUET ICAR UG (Agriculture)', 'NCHM JEE', 'UCEED', 'CEED', 'NID DAT Prelims',
    ]),
    ('teaching', 'Teaching', 'chalkboard-user', [
        'CTET', 'State TET', 'KVS Teacher', 'DSSSB', 'NVS / KVS PRT', 'Super TET', 'UPTET', 'REET', 'HTET',
        'MAHA TET', 'Bihar STET', 'PSTET', 'KTET', 'TNTET', 'APTET', 'TS TET', 'OTET', 'MP TET (Varg 3)', 'CG TET',
        'State SET (Paper 1)', 'B.Ed Entrance',
    ]),
    ('commerce', 'CA, CS & CMA', 'calculator', [
        'CA Foundation', 'CA Foundation Economics', 'CA Intermediate', 'CSEET', 'CMA Foundation',
    ]),
    ('programming', 'Programming & IT', 'laptop-code', [
        'Python Programming', 'C Programming', 'Data Structures & Algorithms', 'DBMS & SQL', 'TCS NQT',
        'Campus Placement Aptitude', 'Infosys Online Test', 'Wipro NLTH', 'Accenture Assessment', 'Cognizant GenC',
        'NIELIT CCC', 'NIELIT O Level',
    ]),
    ('scholarship', 'Olympiads & Scholarships', 'trophy', [
        'NSO Science Olympiad', 'IMO Maths Olympiad', 'IEO English Olympiad', 'NCO Cyber Olympiad', 'IOQM',
        'Olympiad', 'IGKO GK Olympiad', 'JNVST (Navodaya)', 'JNVST Class 9', 'Sainik School (AISSEE)',
        'Sainik School Class 9 (AISSEE)', 'RMS CET', 'NMMS',
    ]),
]
