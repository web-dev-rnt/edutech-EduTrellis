# UPSC/State PSC, management, law, teaching and commerce exams.
# Section: (subject code, section name, marks, negative marks, questions)

EXAMS = [
    {
        'exam': 'UPSC Civil Services', 'difficulty': 'expert', 'minutes': 24,
        'pattern': "Prelims GS Paper I: 100 questions, 200 marks, 2 hours. +2 / −0.66. (CSAT Paper II is qualifying.)",
        'sections': [
            ('GK1', 'History & Culture', 2, 0.66, [
                ("Which Harappan site has evidence of a ploughed field?", ['Lothal', 'Kalibangan', 'Dholavira', 'Rakhigarhi'], 'b', 'medium', "Kalibangan, Rajasthan."),
                ("The 'Doctrine of Lapse' was applied first to ___.", ['Jhansi', 'Satara', 'Nagpur', 'Awadh'], 'b', 'hard', "Satara, 1848."),
                ("Consider: The Montagu-Chelmsford Reforms introduced ___.", ['Provincial autonomy', 'Dyarchy in provinces', 'Federal court', 'Separate electorates for Muslims'], 'b', 'medium', "GoI Act 1919 – dyarchy."),
                ("Which Buddhist council was held during Kanishka's reign?", ['First', 'Second', 'Third', 'Fourth'], 'd', 'medium', "Fourth, in Kashmir."),
            ]),
            ('GK1', 'Polity & Governance', 2, 0.66, [
                ("Which of these is NOT a constitutional body?", ['Election Commission', 'Finance Commission', 'NITI Aayog', 'UPSC'], 'c', 'easy', "Created by executive resolution."),
                ("The 'basic structure' doctrine was laid down in ___.", ['Golaknath case', 'Kesavananda Bharati case', 'Minerva Mills case', 'Maneka Gandhi case'], 'b', 'easy', "1973."),
                ("Who decides whether a bill is a Money Bill?", ['President', 'Speaker of Lok Sabha', 'Chairman of Rajya Sabha', 'Finance Minister'], 'b', 'easy', "Article 110(3)."),
                ("The Anti-Defection Law is in the ___ Schedule.", ['Eighth', 'Ninth', 'Tenth', 'Eleventh'], 'c', 'medium', "52nd Amendment, 1985."),
            ]),
            ('GEO1', 'Geography & Environment', 2, 0.66, [
                ("Which national park is famous for the one-horned rhinoceros?", ['Gir', 'Kaziranga', 'Ranthambore', 'Periyar'], 'b', 'easy', "Assam."),
                ("The 'Ramsar Convention' is related to ___.", ['Ozone', 'Wetlands', 'Biodiversity', 'Desertification'], 'b', 'easy', "Wetlands, 1971."),
                ("Which of these rivers flows westward into the Arabian Sea?", ['Godavari', 'Krishna', 'Narmada', 'Mahanadi'], 'c', 'easy', "Rift valley river."),
                ("El Niño is associated with ___ of the eastern Pacific.", ['Cooling', 'Warming', 'Freezing', 'Desalination'], 'b', 'medium', "Abnormal warming."),
            ]),
            ('ECO1', 'Economy', 2, 0.66, [
                ("Which of these is a 'qualitative' tool of monetary policy?", ['CRR', 'Moral suasion', 'Repo rate', 'OMO'], 'b', 'medium', "Selective/qualitative."),
                ("The 'Twin balance sheet problem' refers to stress in ___.", ['Banks and corporates', 'Exports and imports', 'Centre and states', 'Households and firms'], 'a', 'hard', "Economic Survey 2016–17."),
                ("Fiscal deficit is best financed without inflation by ___.", ['Printing money', 'Market borrowing', 'RBI credit', 'Deficit financing'], 'b', 'medium', "Borrowing from the market."),
                ("GDP at factor cost + net indirect taxes = ___.", ['GNP', 'GDP at market prices', 'NNP', 'NDP'], 'b', 'medium', "Market prices include taxes less subsidies."),
            ]),
            ('SCI1', 'Science & Technology', 2, 0.66, [
                ("CRISPR-Cas9 is a technique for ___.", ['Gene editing', 'Space propulsion', 'Water purification', 'Data encryption'], 'a', 'easy', "Genome editing."),
                ("Which mission studied the Sun from the L1 point?", ['Chandrayaan-3', 'Aditya-L1', 'Mangalyaan', 'Astrosat'], 'b', 'easy', "Launched 2023."),
                ("Graphene is an allotrope of ___.", ['Silicon', 'Carbon', 'Boron', 'Sulphur'], 'b', 'easy', "Single layer of carbon."),
                ("Which disease is caused by a prion?", ['Malaria', 'Creutzfeldt-Jakob disease', 'Typhoid', 'Polio'], 'b', 'hard', "Misfolded protein."),
            ]),
        ],
    },
    {
        'exam': 'State PSC', 'difficulty': 'hard', 'minutes': 16,
        'pattern': "Typical State PSC prelims GS (e.g. UPPSC, BPSC, MPPSC): 150 questions, 2 hours, around +1.33 / −0.33. Here: +2 / −0.66 (UPSC ratio).",
        'sections': [
            ('GK1', 'History & Culture', 2, 0.66, [
                ("The 1857 revolt at Kanpur was led by ___.", ['Kunwar Singh', 'Nana Sahib', 'Begum Hazrat Mahal', 'Tantia Tope alone'], 'b', 'easy', "Nana Sahib."),
                ("Who founded the Vijayanagara empire?", ['Krishnadeva Raya', 'Harihara and Bukka', 'Pulakeshin II', 'Rajaraja'], 'b', 'easy', "1336."),
                ("The Champaran Satyagraha was related to ___ farmers.", ['Cotton', 'Indigo', 'Sugarcane', 'Jute'], 'b', 'easy', "Tinkathia system."),
                ("Khajuraho temples were built by the ___.", ['Cholas', 'Chandelas', 'Paramaras', 'Pratiharas'], 'b', 'medium', "Chandela dynasty."),
            ]),
            ('GK1', 'Polity', 2, 0.66, [
                ("The Governor of a state is appointed by the ___.", ['Chief Minister', 'President', 'Prime Minister', 'Chief Justice'], 'b', 'easy', "Article 155."),
                ("Legislative Councils exist in how many states (as of 2024)?", ['5', '6', '7', '8'], 'b', 'hard', "AP, Bihar, Karnataka, Maharashtra, Telangana, UP."),
                ("The State Election Commission conducts elections to ___.", ['Lok Sabha', 'Vidhan Sabha', 'Panchayats and municipalities', 'Rajya Sabha'], 'c', 'medium', "Articles 243K, 243ZA."),
                ("Article 356 deals with ___.", ['National emergency', "President's rule in states", 'Financial emergency', 'Amendment'], 'b', 'easy', "State emergency."),
            ]),
            ('GEO1', 'Geography', 2, 0.66, [
                ("The Ken-Betwa link project connects rivers in ___.", ['UP and MP', 'Bihar and Jharkhand', 'Gujarat and Rajasthan', 'Odisha and AP'], 'a', 'medium', "Bundelkhand region."),
                ("Which soil is most widespread in India?", ['Black', 'Alluvial', 'Red', 'Laterite'], 'b', 'easy', "Northern plains."),
                ("Which pass connects Sikkim with Tibet?", ['Shipki La', 'Nathu La', 'Zoji La', 'Bomdi La'], 'b', 'medium', "Nathu La."),
                ("The 'Terai' region lies at the foot of the ___.", ['Western Ghats', 'Himalayas (Shivaliks)', 'Aravallis', 'Vindhyas'], 'b', 'easy', "South of Bhabar."),
            ]),
            ('ECO1', 'Economy & Schemes', 2, 0.66, [
                ("PM-KISAN provides farmers ___ per year.", ['₹4,000', '₹6,000', '₹10,000', '₹12,000'], 'b', 'easy', "Three instalments of ₹2,000."),
                ("MGNREGA guarantees ___ days of work per household per year.", ['50', '100', '150', '200'], 'b', 'easy', "100 days."),
                ("The 'One District One Product' scheme was started by ___.", ['Gujarat', 'Uttar Pradesh', 'Punjab', 'Kerala'], 'b', 'medium', "UP, 2018."),
                ("NABARD mainly finances ___.", ['Industry', 'Agriculture and rural development', 'Exports', 'Housing'], 'b', 'easy', "Rural credit."),
            ]),
            ('SCI1', 'General Science', 2, 0.66, [
                ("Which vitamin helps blood clotting?", ['A', 'C', 'K', 'D'], 'c', 'easy', "Vitamin K."),
                ("Which gas is called 'laughing gas'?", ['N₂O', 'NO₂', 'CO', 'NH₃'], 'a', 'easy', "Nitrous oxide."),
                ("The pH of human blood is about ___.", ['6.4', '7.4', '8.4', '5.4'], 'b', 'medium', "Slightly alkaline."),
                ("Dengue is spread by the ___ mosquito.", ['Anopheles', 'Aedes', 'Culex', 'Mansonia'], 'b', 'easy', "Aedes aegypti."),
            ]),
        ],
    },
    {
        'exam': 'CAT', 'difficulty': 'expert', 'minutes': 36,
        'pattern': "CAT: 66–68 questions (VARC, DILR, QA) with 40 minutes per section, 2 hours. MCQ +3 / −1; TITA questions have no negative marking.",
        'sections': [
            ('ENG1', 'Verbal Ability & Reading Comprehension', 3, 1, [
                ("Passage: 'Markets reward not the most talented, but those who signal talent most convincingly.' The author's main claim is that ___.", ['Talent is irrelevant', 'Perceived ability can matter more than actual ability', 'Markets are always efficient', 'Signalling is unethical'], 'b', 'medium', "Signal vs substance."),
                ("Choose the word that best completes: The report was so ___ that even experts struggled to follow it.", ['lucid', 'abstruse', 'concise', 'trivial'], 'b', 'medium', "Abstruse = hard to understand."),
                ("Odd sentence out: (1) Cities generate most GDP. (2) Urban density spurs innovation. (3) Agglomeration lowers costs. (4) Monsoons decide crop output.", ['1', '2', '3', '4'], 'd', 'medium', "Off-topic: rural/agriculture."),
                ("Para summary: 'Habits form when cues trigger routines that deliver rewards; changing the routine while keeping cue and reward reshapes the habit.' Best summary:", ['Habits cannot change', 'Habits change by swapping the routine between the same cue and reward', 'Rewards create cues', 'Cues are unimportant'], 'b', 'medium', "Golden rule of habit change."),
                ("Which is closest in meaning to 'equivocal'?", ['Clear', 'Ambiguous', 'Equal', 'Loud'], 'b', 'easy', "Open to interpretation."),
                ("Para-jumble — first sentence of: (A) As a result, prices rose. (B) Demand surged after the festival. (C) Supply could not keep pace.", ['A', 'B', 'C', 'Cannot say'], 'b', 'medium', "B → C → A."),
                ("An author who writes 'it is not that the evidence is weak; it is that we refuse to look' is most likely ___.", ['Neutral', 'Critical of willful ignorance', 'Praising caution', 'Sceptical of evidence'], 'b', 'medium', "Tone: critical."),
            ]),
            ('DI1', 'Data Interpretation & Logical Reasoning', 3, 1, [
                ("Sales: Q1 = 120, Q2 = 150, Q3 = 180, Q4 = 150. Percentage increase from Q1 to Q3 = ___.", ['33.3%', '50%', '60%', '25%'], 'b', 'easy', "60/120."),
                ("Four friends A, B, C, D finish a race. A beats B, C beats A, D is last. Who finishes second?", ['A', 'B', 'C', 'D'], 'a', 'easy', "C, A, B, D."),
                ("In a group of 100, 60 like tea, 50 like coffee, 20 like both. How many like neither?", ['10', '20', '30', '0'], 'a', 'medium', "100 − (60 + 50 − 20)."),
                ("A pie chart shows rent at 90°. Rent as a share of the total = ___.", ['20%', '25%', '30%', '90%'], 'b', 'easy', "90/360."),
                ("Five people P–T sit in a row. P is at an end, Q is next to P, R is in the middle. S is not next to R. Where is T?", ['Next to R', 'At the other end', 'Next to P', 'Cannot say'], 'a', 'hard', "P Q R T S: S at the end, T beside R."),
                ("Revenue rose 20% and cost rose 10% from 100 and 80. New profit = ___.", ['20', '32', '28', '30'], 'b', 'medium', "120 − 88."),
            ]),
            ('QNT1', 'Quantitative Ability', 3, 1, [
                ("If log₂(x − 1) = 3, x = ___.", ['7', '8', '9', '10'], 'c', 'easy', "x − 1 = 8."),
                ("The sum of all two-digit numbers divisible by 7 is ___.", ['728', '735', '742', '700'], 'a', 'hard', "14 to 98: 13 terms, avg 56."),
                ("A mixture of milk and water is 3 : 1. How much water must be added to 20 L to make it 3 : 2?", ['5 L', '10 L', '4 L', '6 L'], 'a', 'medium', "15 milk, need 10 water."),
                ("How many integers n satisfy |n − 3| < 5?", ['8', '9', '10', '11'], 'b', 'medium', "−1 to 7."),
                ("A can do a job in 10 days and B in 15. They work alternately starting with A. Days to finish = ___.", ['12', '11', '13', '12.5'], 'a', 'hard', "Each 2-day cycle does 1/6."),
                ("If x + y = 10 and xy = 21, x² + y² = ___.", ['58', '79', '100', '42'], 'a', 'easy', "100 − 42."),
                ("The number of trailing zeros in 100! is ___.", ['20', '24', '25', '22'], 'b', 'medium', "20 + 4."),
            ]),
        ],
    },
    {
        'exam': 'MAT', 'difficulty': 'medium', 'minutes': 16,
        'pattern': "AIMA MAT: 150 questions (Language Comprehension, Mathematical Skills, Data Analysis & Sufficiency, Intelligence & Critical Reasoning – 30 each; Indian & Global Environment 30, not counted in composite), 120 minutes. +1 / −0.25.",
        'sections': [
            ('ENG1', 'Language Comprehension', 1, 0.25, [
                ("Choose the synonym of 'PRAGMATIC':", ['Idealistic', 'Practical', 'Romantic', 'Lazy'], 'b', 'easy', "Practical."),
                ("Choose the antonym of 'OPTIMISTIC':", ['Hopeful', 'Pessimistic', 'Cheerful', 'Positive'], 'b', 'easy', "Pessimistic."),
                ("Fill in: The manager ___ the proposal after careful review.", ['approve', 'approved', 'approving', 'approves of it'], 'b', 'easy', "Past."),
                ("Idiom 'to cut corners' means ___.", ['To save effort by doing badly', 'To take a shortcut road', 'To decorate', 'To be careful'], 'a', 'easy', "Doing something poorly to save time/money."),
            ]),
            ('QNT1', 'Mathematical Skills', 1, 0.25, [
                ("A trader marks 40% above CP and gives 20% discount. Profit % = ___.", ['10%', '12%', '20%', '8%'], 'b', 'medium', "1.4 × 0.8 = 1.12."),
                ("The LCM of 15, 25 and 35 is ___.", ['525', '1,050', '175', '375'], 'a', 'medium', "3 × 5² × 7."),
                ("If 3x − 2 = 2x + 5, x = ___.", ['3', '7', '5', '1'], 'b', 'easy', "x = 7."),
                ("Average of 5 numbers is 18. Adding a sixth makes it 20. The sixth number = ___.", ['28', '30', '22', '20'], 'b', 'medium', "120 − 90."),
            ]),
            ('DI1', 'Data Analysis & Sufficiency', 1, 0.25, [
                ("A company's profit was ₹40 lakh in 2023 and ₹50 lakh in 2024. Growth = ___.", ['20%', '25%', '10%', '30%'], 'b', 'easy', "10/40."),
                ("Data sufficiency: What is x? (I) x² = 16 (II) x > 0.", ['I alone suffices', 'II alone suffices', 'Both together suffice', 'Neither suffices'], 'c', 'medium', "I gives ±4; II picks 4."),
                ("A bar chart shows 200 Arts, 300 Science, 500 Commerce students. Science share = ___.", ['20%', '30%', '50%', '33%'], 'b', 'easy', "300/1000."),
                ("Data sufficiency: Is n even? (I) n² is even. (II) n is a multiple of 3.", ['I alone suffices', 'II alone suffices', 'Both needed', 'Neither'], 'a', 'medium', "n² even ⇒ n even."),
            ]),
            ('RSN1', 'Intelligence & Critical Reasoning', 1, 0.25, [
                ("Statement: 'All MBA graduates get high salaries.' Which weakens it most?", ['Some MBAs earn below average', 'MBA fees are high', 'MBAs work long hours', 'Many people want an MBA'], 'a', 'medium', "Counter-example."),
                ("Find the next term: 2, 5, 11, 23, ?", ['46', '47', '45', '48'], 'b', 'easy', "×2 + 1."),
                ("If MANAGER is coded NBOBHFS, then LEADER is coded ___.", ['MFBEFS', 'MFBDFS', 'KDZCDQ', 'MFCEFS'], 'a', 'easy', "+1."),
                ("A is B's sister. C is B's mother. D is C's father. A is D's ___.", ['Daughter', 'Granddaughter', 'Mother', 'Sister'], 'b', 'easy', "D is the maternal grandfather."),
            ]),
            ('GA1', 'Indian & Global Environment', 1, 0.25, [
                ("The headquarters of the World Bank is in ___.", ['Geneva', 'Washington, D.C.', 'New York', 'Paris'], 'b', 'easy', "Washington, D.C."),
                ("'Make in India' was launched in ___.", ['2012', '2014', '2016', '2018'], 'b', 'easy', "September 2014."),
                ("Which company owns Instagram?", ['Google', 'Meta', 'Microsoft', 'Amazon'], 'b', 'easy', "Meta Platforms."),
                ("BSE is located in ___.", ['Delhi', 'Mumbai', 'Kolkata', 'Chennai'], 'b', 'easy', "Dalal Street, Mumbai."),
            ]),
        ],
    },
    {
        'exam': 'CLAT', 'difficulty': 'hard', 'minutes': 20,
        'pattern': "CLAT UG: 120 questions (English, Current Affairs & GK, Legal Reasoning, Logical Reasoning, Quantitative Techniques), 2 hours. +1 / −0.25.",
        'sections': [
            ('ENG1', 'English Language', 1, 0.25, [
                ("Passage: 'Rights without remedies are mere declarations.' The author implies that ___.", ['Rights are unnecessary', 'Enforcement mechanisms give rights meaning', 'Declarations are illegal', 'Remedies are optional'], 'b', 'medium', "Rights need enforcement."),
                ("Choose the word closest to 'ARBITRARY':", ['Reasoned', 'Random/unreasoned', 'Lawful', 'Fair'], 'b', 'easy', "Not based on reason."),
                ("Choose the antonym of 'LENIENT':", ['Soft', 'Strict', 'Tolerant', 'Kind'], 'b', 'easy', "Strict."),
                ("Fill in: The court ___ the appeal on technical grounds.", ['dismissed', 'dismiss', 'dismissing', 'dismisses of'], 'a', 'easy', "Past."),
            ]),
            ('GK1', 'Current Affairs & General Knowledge', 1, 0.25, [
                ("The three new criminal laws came into force in India on ___.", ['1 January 2024', '1 July 2024', '15 August 2024', '26 January 2025'], 'b', 'medium', "BNS, BNSS, BSA."),
                ("The Bharatiya Sakshya Adhiniyam replaced the ___.", ['IPC', 'CrPC', 'Indian Evidence Act', 'Contract Act'], 'c', 'medium', "Evidence Act, 1872."),
                ("The International Court of Justice is located at ___.", ['Geneva', 'The Hague', 'New York', 'Vienna'], 'b', 'easy', "Netherlands."),
                ("Which article of the Constitution guarantees the right to life and personal liberty?", ['14', '19', '21', '32'], 'c', 'easy', "Article 21."),
                ("The Women's Reservation Act (2023) reserves ___ of seats in Lok Sabha for women.", ['25%', 'One-third', 'Half', '40%'], 'b', 'easy', "Nari Shakti Vandan Adhiniyam."),
            ]),
            ('LGL1', 'Legal Reasoning', 1, 0.25, [
                ("Principle: An offer must be accepted unconditionally to form a contract. A offers to sell a car for ₹5 lakh; B replies 'I accept at ₹4.5 lakh.' Is there a contract?", ['Yes', 'No, it is a counter-offer', 'Yes, at ₹4.5 lakh', 'Yes, at ₹4.75 lakh'], 'b', 'easy', "Conditional acceptance is a counter-offer."),
                ("Principle: A person is liable for negligence if they breach a duty of care causing harm. A doctor leaves a swab inside a patient, who suffers infection. The doctor is ___.", ['Not liable', 'Liable for negligence', 'Liable only if paid', 'Liable only criminally'], 'b', 'easy', "Breach of duty causing harm."),
                ("Principle: Consent of a minor is not valid consent for a contract. A 16-year-old signs a loan agreement. The contract is ___.", ['Valid', 'Void', 'Voidable at the lender\'s option', 'Valid if guardian is told later'], 'b', 'medium', "Mohori Bibee v. Dharmodas Ghose."),
                ("Principle: Self-defence permits reasonable force to repel imminent harm. X shoots an unarmed trespasser who is running away. X's act is ___.", ['Justified self-defence', 'Not justified', 'Justified if at night', 'Justified as property defence always'], 'b', 'medium', "No imminent threat; force excessive."),
                ("Principle: Ignorance of law is no excuse. Y did not know a new tax rule and failed to pay. Y ___.", ['Is excused', 'Is still liable', 'Can claim mistake of fact', 'Must be warned first'], 'b', 'easy', "Ignorantia juris non excusat."),
            ]),
            ('RSN1', 'Logical Reasoning', 1, 0.25, [
                ("Argument: 'Since crime fell after more streetlights were installed, streetlights reduce crime.' The flaw is ___.", ['Correlation assumed as causation', 'Circular reasoning', 'Ad hominem', 'False dilemma'], 'a', 'medium', "Other causes possible."),
                ("If all judges are lawyers and some lawyers are teachers, which must be true?", ['Some judges are teachers', 'All teachers are lawyers', 'All judges are lawyers', 'No judge is a teacher'], 'c', 'easy', "Only the given premise is certain."),
                ("Assumption in 'Make voting compulsory to improve democracy':", ['Higher participation improves democracy', 'Voting is easy', 'People dislike voting', 'Elections are rare'], 'a', 'medium', "Hidden premise."),
            ]),
            ('QNT1', 'Quantitative Techniques', 1, 0.25, [
                ("A fine of ₹2,000 rises by 10% every year. After 2 years it is ___.", ['₹2,400', '₹2,420', '₹2,200', '₹2,440'], 'b', 'medium', "2000 × 1.21."),
                ("Of 200 cases, 35% were civil. Number of non-civil cases = ___.", ['70', '130', '65', '135'], 'b', 'easy', "200 × 0.65."),
                ("The ratio of judges to cases is 1 : 250. For 10,000 cases, judges needed = ___.", ['40', '25', '400', '250'], 'a', 'easy', "10,000/250."),
            ]),
        ],
    },
    {
        'exam': 'CTET', 'difficulty': 'medium', 'minutes': 20,
        'pattern': "CTET Paper I (Classes 1–5): 150 questions (Child Development & Pedagogy, Language I, Language II, Maths, EVS – 30 each), 150 minutes. +1, no negative marking.",
        'sections': [
            ('CDP1', 'Child Development & Pedagogy', 1, 0, [
                ("According to Piaget, a child of 7–11 years is in the ___ stage.", ['Sensorimotor', 'Pre-operational', 'Concrete operational', 'Formal operational'], 'c', 'easy', "Logical thinking about concrete events."),
                ("Vygotsky's 'Zone of Proximal Development' refers to what a child can do ___.", ['Alone', 'With guidance', 'Never', 'Only in adolescence'], 'b', 'easy', "With help from a more capable other."),
                ("Continuous and Comprehensive Evaluation (CCE) mainly aims to ___.", ['Rank students', 'Assess all-round development regularly', 'Reduce teaching time', 'Replace teachers'], 'b', 'easy', "Scholastic and co-scholastic."),
                ("A learner who reverses letters like 'b' and 'd' may have ___.", ['Dyscalculia', 'Dyslexia', 'Dysgraphia only', 'ADHD'], 'b', 'medium', "Reading difficulty."),
            ]),
            ('ENG1', 'Language I (English)', 1, 0, [
                ("The best way to develop reading skills in young learners is through ___.", ['Rote memorisation', 'Story-based and print-rich activities', 'Grammar drills only', 'Punishment'], 'b', 'easy', "Meaningful exposure."),
                ("Phonemic awareness means ___.", ['Knowing spellings', 'Recognising individual sounds in words', 'Writing neatly', 'Reading fast'], 'b', 'medium', "Sound units."),
                ("Remedial teaching is meant for ___.", ['Gifted learners', 'Learners with specific difficulties', 'Teachers', 'Parents'], 'b', 'easy', "Addresses learning gaps."),
                ("Which is a 'receptive' language skill?", ['Speaking', 'Writing', 'Listening', 'Spelling'], 'c', 'easy', "Listening and reading."),
            ]),
            ('HIN1', 'भाषा II (हिंदी)', 1, 0, [
                ("बच्चों में भाषा सीखने का सबसे स्वाभाविक तरीका क्या है?", ['व्याकरण रटना', 'सुनना और बोलना', 'केवल लिखना', 'अनुवाद'], 'b', 'easy', "स्वाभाविक वातावरण।"),
                ("'बहुभाषिकता' को कक्षा में ___ माना जाना चाहिए।", ['बाधा', 'संसाधन', 'समस्या', 'अनुशासनहीनता'], 'b', 'easy', "NCF 2005।"),
                ("पठन का मुख्य उद्देश्य क्या है?", ['तेज़ बोलना', 'अर्थ ग्रहण करना', 'शब्द गिनना', 'उच्चारण सुधारना मात्र'], 'b', 'easy', "समझ।"),
                ("भाषा आकलन में किस पर अधिक ध्यान देना चाहिए?", ['केवल वर्तनी', 'अभिव्यक्ति और समझ', 'सुलेख', 'रटंत'], 'b', 'medium', "समग्र भाषा क्षमता।"),
            ]),
            ('MAT1', 'Mathematics & Pedagogy', 1, 0, [
                ("The best way to teach place value to Class 2 children is using ___.", ['Abstract rules', 'Bundles of sticks/blocks', 'Memorising tables', 'Calculators'], 'b', 'easy', "Concrete materials."),
                ("Which number is divisible by both 2 and 3?", ['14', '18', '21', '25'], 'b', 'easy', "18."),
                ("Errors made by children in maths should be treated as ___.", ['Signs of failure', 'Windows into their thinking', 'Reasons for punishment', 'Unimportant'], 'b', 'medium', "Diagnostic value."),
                ("The value of 3,005 − 1,999 is ___.", ['1,006', '1,016', '1,106', '996'], 'a', 'easy', "1,006."),
            ]),
            ('EVS1', 'Environmental Studies & Pedagogy', 1, 0, [
                ("EVS at the primary level should be taught mainly through ___.", ['Lectures', 'Activities, observation and field trips', 'Dictation', 'Textbook reading only'], 'b', 'easy', "Experiential learning."),
                ("Which animal is a nocturnal bird?", ['Sparrow', 'Owl', 'Crow', 'Pigeon'], 'b', 'easy', "Owl."),
                ("Which of these is a renewable resource?", ['Coal', 'Petroleum', 'Forests', 'Natural gas'], 'c', 'easy', "Can regenerate."),
                ("The 'Chipko Movement' was about ___.", ['Saving trees', 'Saving rivers', 'Building dams', 'Women\'s voting'], 'a', 'easy', "Hugging trees, Uttarakhand."),
            ]),
        ],
    },
    {
        'exam': 'UGC NET', 'difficulty': 'hard', 'minutes': 24,
        'pattern': "UGC NET Paper 1 (Teaching & Research Aptitude): 50 questions, 100 marks; Paper 1 + 2 together 150 questions in 3 hours. +2, no negative marking.",
        'sections': [
            ('TCH1', 'Teaching Aptitude', 2, 0, [
                ("Which is the most important factor in effective teaching?", ['Teacher\'s salary', 'Student engagement', 'Classroom size alone', 'Textbook price'], 'b', 'easy', "Active learners."),
                ("Formative evaluation is conducted ___.", ['At the end of a course', 'During the teaching-learning process', 'Before admission', 'Only once a year'], 'b', 'easy', "Ongoing feedback."),
                ("'Bloom's taxonomy' classifies ___.", ['Teaching aids', 'Educational objectives', 'Schools', 'Universities'], 'b', 'easy', "Cognitive, affective, psychomotor."),
                ("SWAYAM is India's platform for ___.", ['Online courses (MOOCs)', 'Scholarships', 'Exam results', 'Teacher salaries'], 'a', 'easy', "Massive open online courses."),
            ]),
            ('TCH1', 'Research Aptitude', 2, 0, [
                ("A hypothesis is ___.", ['A proven fact', 'A tentative statement to be tested', 'A conclusion', 'A data table'], 'b', 'easy', "Testable proposition."),
                ("Which sampling method gives every member an equal chance?", ['Purposive', 'Simple random', 'Quota', 'Snowball'], 'b', 'easy', "Probability sampling."),
                ("Plagiarism means ___.", ['Citing sources', 'Presenting others\' work as your own', 'Peer review', 'Paraphrasing with citation'], 'b', 'easy', "Academic dishonesty."),
                ("Action research is mainly aimed at ___.", ['Theory building', 'Solving immediate practical problems', 'Historical analysis', 'Large surveys'], 'b', 'medium', "Practitioner-led improvement."),
            ]),
            ('RSN1', 'Logical Reasoning & Mathematical Aptitude', 2, 0, [
                ("In Indian logic (Nyaya), 'pratyaksha' means ___.", ['Inference', 'Perception', 'Testimony', 'Comparison'], 'b', 'medium', "Direct perception."),
                ("If all A are B and no B is C, then ___.", ['Some A are C', 'No A is C', 'All C are A', 'Cannot say'], 'b', 'easy', "A ⊂ B, B ∩ C = ∅."),
                ("Find the next: 3, 8, 15, 24, ?", ['33', '35', '36', '30'], 'b', 'easy', "n² − 1."),
                ("A's salary is 20% more than B's. B's is less than A's by ___.", ['20%', '16.67%', '25%', '18%'], 'b', 'medium', "20/120."),
            ]),
            ('CMP1', 'ICT, Communication & Higher Education', 2, 0, [
                ("1 kilobyte equals ___ bytes.", ['1,000', '1,024', '512', '2,048'], 'b', 'easy', "2¹⁰ (binary convention)."),
                ("Which is NOT a barrier to communication?", ['Noise', 'Jargon', 'Feedback', 'Prejudice'], 'c', 'easy', "Feedback helps."),
                ("The National Education Policy 2020 proposes a school structure of ___.", ['10+2', '5+3+3+4', '8+4', '6+3+3'], 'b', 'easy', "5+3+3+4."),
                ("Which body grants recognition to universities in India?", ['AICTE', 'UGC', 'NCERT', 'CBSE'], 'b', 'easy', "University Grants Commission."),
            ]),
            ('EVS1', 'People, Development & Environment', 2, 0, [
                ("The Paris Agreement aims to limit global warming to well below ___.", ['1°C', '2°C', '3°C', '4°C'], 'b', 'easy', "Pursue 1.5°C."),
                ("Which is a greenhouse gas?", ['Nitrogen', 'Methane', 'Oxygen', 'Argon'], 'b', 'easy', "CH₄."),
                ("The Sustainable Development Goals number ___.", ['8', '12', '17', '20'], 'c', 'easy', "17 SDGs, 2030 agenda."),
                ("India's National Action Plan on Climate Change has ___ missions.", ['6', '8', '10', '12'], 'b', 'medium', "Eight national missions."),
            ]),
        ],
    },
    {
        'exam': 'CA Foundation', 'difficulty': 'hard', 'minutes': 20,
        'pattern': "ICAI CA Foundation: Paper 1 Accounting & Paper 2 Business Laws (subjective, 100 each); Paper 3 Quantitative Aptitude & Paper 4 Business Economics (MCQ, 100 each, −0.25). This mock uses MCQs for all four with +1 / −0.25.",
        'sections': [
            ('ACC1', 'Accounting', 1, 0.25, [
                ("Which concept assumes the business will continue for the foreseeable future?", ['Money measurement', 'Going concern', 'Accrual', 'Consistency'], 'b', 'easy', "Going concern."),
                ("Outstanding salary is a ___.", ['Current asset', 'Current liability', 'Fixed asset', 'Revenue'], 'b', 'easy', "Owed but unpaid."),
                ("Under WDV method, depreciation each year ___.", ['Is constant', 'Decreases', 'Increases', 'Is zero'], 'b', 'easy', "Charged on reducing balance."),
                ("A bill of exchange is drawn by the ___.", ['Drawee', 'Drawer', 'Payee only', 'Bank'], 'b', 'medium', "The creditor draws it."),
                ("Goods sent on consignment are owned by the ___ until sold.", ['Consignee', 'Consignor', 'Customer', 'Transporter'], 'b', 'medium', "Ownership stays with consignor."),
            ]),
            ('LAW1', 'Business Laws', 1, 0.25, [
                ("Under the Indian Contract Act, 1872, an agreement without consideration is generally ___.", ['Valid', 'Void', 'Voidable', 'Illegal'], 'b', 'easy', "Section 25, with exceptions."),
                ("A partnership firm is governed by the ___.", ['Companies Act, 2013', 'Indian Partnership Act, 1932', 'LLP Act, 2008', 'Contract Act only'], 'b', 'easy', "1932 Act."),
                ("Under the Sale of Goods Act, 1930, 'caveat emptor' means ___.", ['Let the seller beware', 'Let the buyer beware', 'Goods must be returned', 'Price is fixed'], 'b', 'easy', "Buyer beware."),
                ("A minor's agreement is ___.", ['Valid', 'Void ab initio', 'Voidable', 'Enforceable at majority'], 'b', 'medium', "Mohori Bibee case."),
                ("Minimum number of members for a public company is ___.", ['2', '5', '7', '50'], 'c', 'medium', "Seven."),
            ]),
            ('QNT1', 'Quantitative Aptitude (Maths, LR, Statistics)', 1, 0.25, [
                ("The present value of ₹1,100 due in 1 year at 10% is ___.", ['₹900', '₹1,000', '₹1,010', '₹990'], 'b', 'medium', "1100/1.1."),
                ("The mean of 2, 4, 6, 8, 10 is ___ and the median is ___.", ['6, 6', '5, 6', '6, 5', '30, 6'], 'a', 'easy', "Symmetric data."),
                ("If ⁿP₂ = 56, n = ___.", ['7', '8', '9', '14'], 'b', 'medium', "8 × 7."),
                ("Pointing to a photo, A says 'Her mother is my mother's only daughter.' A is the person's ___.", ['Sister', 'Mother', 'Aunt', 'Daughter'], 'b', 'hard', "My mother's only daughter is me (A is female)."),
                ("The standard deviation of 5, 5, 5, 5 is ___.", ['5', '0', '1', '25'], 'b', 'easy', "No variation."),
            ]),
            ('ECO1', 'Business Economics', 1, 0.25, [
                ("When demand is perfectly inelastic, the demand curve is ___.", ['Horizontal', 'Vertical', 'Downward sloping', 'Upward sloping'], 'b', 'easy', "Quantity does not change."),
                ("In the long run, a firm under perfect competition earns ___.", ['Supernormal profit', 'Normal profit', 'Losses', 'Monopoly profit'], 'b', 'medium', "Free entry and exit."),
                ("The law of diminishing marginal utility was explained by ___.", ['Adam Smith', 'Marshall', 'Keynes', 'Ricardo'], 'b', 'medium', "Alfred Marshall's cardinal analysis."),
                ("A business cycle phase with falling output and employment is ___.", ['Expansion', 'Recession', 'Peak', 'Recovery'], 'b', 'easy', "Contraction."),
                ("Cross elasticity between substitutes is ___.", ['Negative', 'Positive', 'Zero', 'Infinite'], 'b', 'medium', "Price of one up, demand for other up."),
            ]),
        ],
    },
]
