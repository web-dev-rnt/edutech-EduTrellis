# Teacher recruitment/eligibility and school-level competitive exams.
# Section: (subject code, section name, marks, negative marks, questions)

EXAMS = [
    {
        'exam': 'State TET', 'icon': 'chalkboard-user', 'color': '#6d28d9', 'difficulty': 'medium', 'minutes': 20,
        'pattern': "State TETs (UPTET, REET, HTET, MAHA TET…) Paper I for Classes 1–5: 150 questions (Child Development & Pedagogy, Language I, Language II, Maths, EVS – 30 each) in 150 minutes. +1, no negative marking.",
        'sections': [
            ('CDP1', 'Child Development & Pedagogy', 1, 0, [
                ("Kohlberg's theory is about ___ development.", ['Physical', 'Moral', 'Language', 'Motor'], 'b', 'easy', "Stages of moral reasoning."),
                ("'Learning by doing' is associated with ___.", ['Pavlov', 'John Dewey', 'Freud', 'Skinner'], 'b', 'easy', "Progressive education."),
                ("Inclusive education means ___.", ['Separate schools for disabled children', 'Educating all children, including those with disabilities, together', 'Only gifted children', 'Home schooling'], 'b', 'easy', "Everyone in the same classroom."),
                ("The RTE Act guarantees free and compulsory education for ages ___.", ['3–6', '6–14', '14–18', '5–15'], 'b', 'easy', "6 to 14 years."),
            ]),
            ('HIN1', 'भाषा I (हिंदी)', 1, 0, [
                ("'जल' का पर्यायवाची क्या है?", ['नीर', 'अनल', 'पवन', 'भूमि'], 'a', 'easy', "नीर।"),
                ("'सत्य' का विलोम क्या है?", ['असत्य', 'सच', 'धर्म', 'न्याय'], 'a', 'easy', "असत्य।"),
                ("बच्चे में सबसे पहले विकसित होने वाला भाषा कौशल कौन सा है?", ['पढ़ना', 'सुनना', 'लिखना', 'बोलना'], 'b', 'easy', "सुनना।"),
                ("'विद्यालय' में कौन सी संधि है?", ['गुण', 'दीर्घ', 'यण', 'वृद्धि'], 'b', 'medium', "विद्या + आलय।"),
            ]),
            ('ENG1', 'Language II (English)', 1, 0, [
                ("Receptive language skills are ___.", ['Speaking and writing', 'Listening and reading', 'Writing and reading', 'Speaking only'], 'b', 'easy', "Input skills."),
                ("The best way to teach English to young learners is ___.", ['Grammar rules only', 'Activity-based, communicative tasks', 'Translation only', 'Rote memorisation'], 'b', 'easy', "Meaningful use."),
                ("Choose the synonym of 'HAPPY':", ['Sad', 'Joyful', 'Angry', 'Tired'], 'b', 'easy', "Joyful."),
                ("Phonics instruction mainly helps children to ___.", ['Spell long words only', 'Decode words using letter–sound links', 'Write neatly', 'Memorise stories'], 'b', 'medium', "Decoding."),
            ]),
            ('MAT1', 'Mathematics & Pedagogy', 1, 0, [
                ("The place value of 5 in 3,527 is ___.", ['5', '50', '500', '5,000'], 'c', 'easy', "Hundreds place."),
                ("The best sequence for teaching a maths concept is ___.", ['Abstract → concrete → pictorial', 'Concrete → pictorial → abstract', 'Pictorial → abstract → concrete', 'Abstract only'], 'b', 'easy', "CPA approach."),
                ("1/2 + 1/4 = ___", ['2/6', '3/4', '1/6', '2/4'], 'b', 'easy', "2/4 + 1/4."),
                ("A pentagon has ___ sides.", ['4', '5', '6', '8'], 'b', 'easy', "Five."),
            ]),
            ('EVS1', 'Environmental Studies & Pedagogy', 1, 0, [
                ("A good source of protein is ___.", ['Rice', 'Pulses', 'Sugar', 'Oil'], 'b', 'easy', "Dals."),
                ("At the primary stage, EVS is taught as ___.", ['Separate science and history', 'An integrated subject', 'Only through textbooks', 'An optional subject'], 'b', 'medium', "Science + social studies together."),
                ("The water cycle involves ___.", ['Evaporation and condensation', 'Only melting', 'Only freezing', 'Burning'], 'a', 'easy', "Evaporation, condensation, precipitation."),
                ("India's national animal is the ___.", ['Lion', 'Tiger', 'Elephant', 'Peacock'], 'b', 'easy', "Tiger."),
            ]),
        ],
    },
    {
        'exam': 'KVS Teacher', 'icon': 'school', 'color': '#1d4ed8', 'difficulty': 'medium', 'minutes': 20,
        'pattern': "KVS PRT/TGT/PGT (recent pattern): about 180 questions in 3 hours – English, Hindi, GK & current affairs, reasoning, computer literacy, perspectives on education & leadership, and subject/pedagogy. No negative marking.",
        'sections': [
            ('ENG1', 'General English', 1, 0, [
                ("Choose the synonym of 'PRUDENT':", ['Foolish', 'Wise', 'Rash', 'Lazy'], 'b', 'easy', "Wise."),
                ("Spot the error: 'Each of the students (A) / have a book (B) / in the class (C) / No error (D)'", ['A', 'B', 'C', 'D'], 'b', 'easy', "has."),
            ]),
            ('HIN1', 'सामान्य हिंदी', 1, 0, [
                ("'पुस्तक' का पर्यायवाची क्या है?", ['ग्रंथ', 'कलम', 'पत्र', 'कागज़'], 'a', 'easy', "ग्रंथ।"),
                ("'उत्थान' का विलोम क्या है?", ['पतन', 'उन्नति', 'विकास', 'प्रगति'], 'a', 'easy', "पतन।"),
            ]),
            ('GA1', 'GK & Current Affairs', 1, 0, [
                ("Kendriya Vidyalaya Sangathan was set up in ___.", ['1947', '1963', '1975', '1986'], 'b', 'medium', "1963."),
                ("NEP 2020 proposes the school structure ___.", ['10+2', '5+3+3+4', '8+4', '6+6'], 'b', 'easy', "5+3+3+4."),
            ]),
            ('RSN1', 'Reasoning', 1, 0, [
                ("Next term: 2, 6, 12, 20, ?", ['28', '30', '32', '26'], 'b', 'easy', "n(n + 1)."),
                ("Odd one out: Chalk, Duster, Board, Banana", ['Chalk', 'Duster', 'Board', 'Banana'], 'd', 'easy', "Not classroom material."),
            ]),
            ('CMP1', 'Computer Literacy', 1, 0, [
                ("RAM is ___ memory.", ['Permanent', 'Volatile', 'Read-only', 'Optical'], 'b', 'easy', "Lost when power is off."),
                ("1 byte = ___ bits.", ['4', '8', '16', '1,024'], 'b', 'easy', "8."),
            ]),
            ('CDP1', 'Perspectives on Education & Pedagogy', 1, 0, [
                ("The National Curriculum Framework for School Education (NCF-SE) was released in ___.", ['2005', '2020', '2023', '2015'], 'c', 'medium', "2023."),
                ("Under NEP 2020, the Foundational Stage covers ages ___.", ['3–8', '6–10', '8–11', '11–14'], 'a', 'easy', "3 years pre-school + Classes 1–2."),
                ("NIPUN Bharat aims at ___ by Grade 3.", ['Board exam readiness', 'Foundational literacy and numeracy', 'Coding skills', 'Sports excellence'], 'b', 'easy', "FLN."),
                ("Formative assessment is mainly used to ___.", ['Rank students', 'Improve learning during instruction', 'Certify at the end', 'Select for jobs'], 'b', 'easy', "Assessment for learning."),
                ("The highest level of the revised Bloom's taxonomy is ___.", ['Evaluate', 'Create', 'Analyse', 'Apply'], 'b', 'medium', "Create."),
                ("The theory of multiple intelligences was given by ___.", ['Piaget', 'Howard Gardner', 'Skinner', 'Binet'], 'b', 'easy', "Gardner, 1983."),
                ("Maslow is known for the ___.", ['Stages of cognitive development', 'Hierarchy of needs', 'Classical conditioning', 'Zone of proximal development'], 'b', 'easy', "Needs pyramid."),
                ("Constructivism holds that learners ___.", ['Passively receive knowledge', 'Actively construct knowledge', 'Only memorise', 'Learn only by punishment'], 'b', 'easy', "Active meaning-making."),
                ("Teaching the same topic at different levels for diverse learners is ___.", ['Rote learning', 'Differentiated instruction', 'Streaming', 'Detention'], 'b', 'medium', "Meets varied needs."),
                ("PISA is conducted by the ___.", ['UNESCO', 'OECD', 'World Bank', 'NCERT'], 'b', 'medium', "OECD."),
            ]),
        ],
    },
    {
        'exam': 'DSSSB', 'icon': 'person-chalkboard', 'color': '#9d174d', 'difficulty': 'medium', 'minutes': 12,
        'pattern': "DSSSB PRT/TGT one-tier exam: 200 questions (General Awareness, Reasoning, Arithmetic, Hindi, English – 20 each – and subject/pedagogy 100) in 2 hours. +1 / −0.25.",
        'sections': [
            ('GA1', 'General Awareness', 1, 0.25, [
                ("DSSSB stands for ___.", ['Delhi Subordinate Services Selection Board', 'Delhi State School Selection Board', 'Delhi Secondary School Service Board', 'Delhi Staff Selection Service Board'], 'a', 'easy', "Recruits Delhi government staff."),
                ("The Lieutenant Governor of Delhi is appointed by the ___.", ['Chief Minister', 'President', 'Prime Minister', 'Chief Justice'], 'b', 'easy', "President."),
            ]),
            ('RSN1', 'General Mental Ability & Reasoning', 1, 0.25, [
                ("Next term: 5, 11, 17, 23, ?", ['27', '29', '31', '28'], 'b', 'easy', "+6."),
                ("If BOOK is coded CPPL, DESK is coded ___.", ['EFTL', 'EFSL', 'CDRJ', 'EGTL'], 'a', 'easy', "+1."),
            ]),
            ('QNT1', 'Arithmetic & Numerical Ability', 1, 0.25, [
                ("18% of 500 = ___", ['80', '90', '95', '85'], 'b', 'easy', "500 × 0.18."),
                ("Average of 3, 5, 7, 9 = ___", ['5', '6', '7', '24'], 'b', 'easy', "24/4."),
            ]),
            ('HIN1', 'हिंदी भाषा', 1, 0.25, [
                ("'आकाश' का पर्यायवाची क्या है?", ['गगन', 'धरा', 'सागर', 'वन'], 'a', 'easy', "गगन।"),
                ("'गुण' का विलोम क्या है?", ['दोष', 'अच्छाई', 'शील', 'धर्म'], 'a', 'easy', "दोष।"),
            ]),
            ('ENG1', 'English Language', 1, 0.25, [
                ("Choose the antonym of 'ARRIVE':", ['Reach', 'Depart', 'Come', 'Land'], 'b', 'easy', "Depart."),
                ("Fill in: She is good ___ mathematics.", ['in', 'at', 'on', 'with'], 'b', 'easy', "Good at."),
            ]),
            ('CDP1', 'Child Development & Pedagogy', 1, 0.25, [
                ("The 'zone of proximal development' was proposed by ___.", ['Piaget', 'Vygotsky', 'Kohlberg', 'Erikson'], 'b', 'easy', "Vygotsky."),
                ("Operant conditioning is associated with ___.", ['Pavlov', 'Skinner', 'Thorndike', 'Bandura'], 'b', 'easy', "Reinforcement."),
                ("Classical conditioning is associated with ___.", ['Pavlov', 'Skinner', 'Gagne', 'Bruner'], 'a', 'easy', "Dogs and bells."),
                ("Piaget's formal operational stage begins at about ___ years.", ['2', '7', '11', '18'], 'c', 'easy', "Abstract thinking."),
                ("Child-centred education emphasises ___.", ['The syllabus only', "The learner's needs and interests", 'Exams only', 'Teacher authority'], 'b', 'easy', "Learner first."),
                ("Dyscalculia is a difficulty in ___.", ['Reading', 'Writing', 'Mathematics', 'Speaking'], 'c', 'easy', "Numbers."),
                ("IQ = ___", ['CA/MA × 100', 'MA/CA × 100', 'MA × CA', 'MA − CA'], 'b', 'easy', "Mental age ÷ chronological age."),
                ("A learning disability in writing is called ___.", ['Dyslexia', 'Dysgraphia', 'Dyscalculia', 'Dyspraxia'], 'b', 'easy', "Handwriting/spelling."),
                ("The best way to help a slow learner is ___.", ['Punishment', 'Individual attention and extra practice', 'Ignoring them', 'Detaining them'], 'b', 'easy', "Remedial support."),
                ("Assessment for learning is another name for ___ assessment.", ['Summative', 'Formative', 'Norm-referenced', 'Placement'], 'b', 'easy', "Formative."),
            ]),
        ],
    },
    {
        'exam': 'JNVST (Navodaya)', 'icon': 'child-reaching', 'color': '#ea580c', 'difficulty': 'easy', 'minutes': 30,
        'pattern': "Jawahar Navodaya Vidyalaya Selection Test (Class 6): 80 questions, 100 marks, 2 hours – Mental Ability 40 Qs (50 marks), Arithmetic 20 Qs (25), Language 20 Qs (25). No negative marking. (1.25 marks per question officially; 1 mark here.)",
        'sections': [
            ('RSN1', 'Mental Ability', 1, 0, [
                ("Odd one out: 2, 4, 6, 9", ['2', '4', '6', '9'], 'd', 'easy', "Not even."),
                ("Next letter: A, C, E, G, ?", ['H', 'I', 'J', 'K'], 'b', 'easy', "Skip one."),
                ("Which letter looks the same in a vertical mirror?", ['A', 'B', 'C', 'D'], 'a', 'medium', "Symmetric."),
                ("Next term: 1, 2, 4, 8, ?", ['10', '12', '16', '14'], 'c', 'easy', "×2."),
                ("Hand : Glove :: Foot : ?", ['Leg', 'Sock', 'Toe', 'Shoe lace'], 'b', 'easy', "Covering."),
                ("A chessboard has ___ small squares.", ['32', '48', '64', '81'], 'c', 'easy', "8 × 8."),
                ("Odd one out: Circle, Square, Triangle, Cube", ['Circle', 'Square', 'Triangle', 'Cube'], 'd', 'easy', "3-D shape."),
                ("Next letter: Z, Y, X, ?", ['V', 'W', 'U', 'A'], 'b', 'easy', "Backwards."),
                ("Next term: 3, 6, 9, 12, ?", ['14', '15', '16', '18'], 'b', 'easy', "+3."),
                ("If CAT is written DBU, DOG is written ___.", ['EPH', 'EOH', 'CNF', 'FPH'], 'a', 'easy', "+1."),
            ]),
            ('MAT1', 'Arithmetic', 1, 0, [
                ("3/4 of 20 = ___", ['12', '15', '16', '18'], 'b', 'easy', "20 ÷ 4 × 3."),
                ("1 metre = ___ cm", ['10', '100', '1,000', '50'], 'b', 'easy', "100 cm."),
                ("LCM of 2 and 3 = ___", ['5', '6', '1', '12'], 'b', 'easy', "6."),
                ("Perimeter of a square of side 5 cm = ___", ['10', '20', '25', '15'], 'b', 'easy', "4 × 5."),
                ("0.5 + 0.25 = ___", ['0.30', '0.75', '0.70', '0.55'], 'b', 'easy', "0.75."),
            ]),
            ('ENG1', 'Language Test', 1, 0, [
                ("Choose the word that means 'SMALL':", ['Huge', 'Little', 'Tall', 'Wide'], 'b', 'easy', "Little."),
                ("Opposite of 'DAY' is ___.", ['Morning', 'Night', 'Noon', 'Evening'], 'b', 'easy', "Night."),
                ("Plural of 'child' is ___.", ['Childs', 'Children', 'Childrens', 'Childes'], 'b', 'easy', "Children."),
                ("Fill in: The cat is ___ the box.", ['in', 'of', 'to', 'from'], 'a', 'easy', "In."),
                ("Choose the correctly spelt word:", ['Beautifull', 'Beautiful', 'Butiful', 'Beutiful'], 'b', 'easy', "Beautiful."),
            ]),
        ],
    },
    {
        'exam': 'Sainik School (AISSEE)', 'icon': 'person-military-rifle', 'color': '#3f6212', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "AISSEE (Class 6), NTA: 125 questions, 300 marks, 150 minutes – Language 25 Qs (2 marks each), Mathematics 50 Qs (3 marks each), Intelligence 25 Qs (2 marks each), GK 25 Qs (2 marks each). No negative marking.",
        'sections': [
            ('ENG1', 'Language', 2, 0, [
                ("Choose the synonym of 'BRAVE':", ['Weak', 'Courageous', 'Afraid', 'Lazy'], 'b', 'easy', "Courageous."),
                ("Choose the antonym of 'STRONG':", ['Mighty', 'Weak', 'Tough', 'Hard'], 'b', 'easy', "Weak."),
                ("Fill in: We ___ to school every day.", ['goes', 'go', 'going', 'gone'], 'b', 'easy', "We go."),
                ("Plural of 'mouse' is ___.", ['Mouses', 'Mice', 'Mices', 'Mouse'], 'b', 'easy', "Mice."),
            ]),
            ('MAT1', 'Mathematics', 3, 0, [
                ("LCM of 12 and 18 = ___", ['6', '36', '72', '216'], 'b', 'easy', "36."),
                ("49 in Roman numerals is ___.", ['IL', 'XLIX', 'XXXXIX', 'LIX'], 'b', 'medium', "XL + IX."),
                ("A straight angle measures ___.", ['90°', '180°', '360°', '45°'], 'b', 'easy', "180°."),
                ("Area of a triangle with base 6 cm and height 4 cm = ___.", ['24', '12', '10', '20'], 'b', 'easy', "½ × 6 × 4."),
                ("0.6 as a fraction in lowest terms is ___.", ['6/100', '3/5', '6/10', '2/3'], 'b', 'easy', "6/10 = 3/5."),
                ("CP ₹50, SP ₹60. Profit % = ___.", ['10%', '20%', '15%', '25%'], 'b', 'easy', "10/50."),
                ("Volume of a cube of side 3 cm = ___.", ['9', '18', '27', '81'], 'c', 'easy', "3³."),
                ("Divide 50 in the ratio 2 : 3. The larger part is ___.", ['20', '30', '25', '35'], 'b', 'easy', "3/5 × 50."),
            ]),
            ('RSN1', 'Intelligence', 2, 0, [
                ("Next term: 3, 7, 11, 15, ?", ['17', '19', '21', '18'], 'b', 'easy', "+4."),
                ("Odd one out: Rose, Lily, Lotus, Mango", ['Rose', 'Lily', 'Lotus', 'Mango'], 'd', 'easy', "Fruit."),
                ("If PEN is coded QFO, INK is coded ___.", ['JOL', 'JOK', 'HMJ', 'JNL'], 'a', 'easy', "+1."),
                ("Bird : Fly :: Fish : ?", ['Water', 'Swim', 'Fins', 'Sea'], 'b', 'easy', "Movement."),
            ]),
            ('GK1', 'General Knowledge', 2, 0, [
                ("Sainik Schools are run by the Sainik Schools Society under the Ministry of ___.", ['Education', 'Defence', 'Home Affairs', 'Sports'], 'b', 'easy', "MoD."),
                ("The first Sainik Schools were set up in ___.", ['1947', '1961', '1971', '1985'], 'b', 'medium', "1961."),
                ("India's national bird is the ___.", ['Parrot', 'Peacock', 'Sparrow', 'Eagle'], 'b', 'easy', "Peacock."),
                ("The top band of the Indian flag is ___.", ['Green', 'White', 'Saffron', 'Blue'], 'c', 'easy', "Saffron."),
            ]),
        ],
    },
    {
        'exam': 'NMMS', 'icon': 'award', 'color': '#ca8a04', 'difficulty': 'medium', 'minutes': 20,
        'pattern': "National Means-cum-Merit Scholarship (Class 8): Mental Ability Test (90 Qs, 90 min) and Scholastic Aptitude Test (90 Qs on Science, Maths, Social Science, 90 min). +1, no negative marking.",
        'sections': [
            ('RSN1', 'Mental Ability Test (MAT)', 1, 0, [
                ("Next term: 2, 5, 10, 17, ?", ['24', '26', '28', '25'], 'b', 'easy', "n² + 1."),
                ("Odd one out: 17, 19, 23, 27", ['17', '19', '23', '27'], 'd', 'easy', "Not prime."),
                ("If BIRD is coded CJSE, FISH is coded ___.", ['GJTI', 'GJSI', 'EHRG', 'GKTI'], 'a', 'easy', "+1."),
                ("Book : Library :: Painting : ?", ['Artist', 'Museum/Gallery', 'Brush', 'Colour'], 'b', 'easy', "Where kept."),
                ("Riya is 8th from the top in a class of 40. Her rank from the bottom is ___.", ['32nd', '33rd', '31st', '34th'], 'b', 'easy', "40 − 8 + 1."),
                ("Facing east, you turn right twice. You now face ___.", ['North', 'South', 'West', 'East'], 'c', 'easy', "180°."),
                ("Missing term: 4, 16, 36, 64, ?", ['81', '100', '121', '96'], 'b', 'medium', "Squares of 2, 4, 6, 8, 10."),
                ("Angle between clock hands at 6:00 is ___.", ['90°', '120°', '180°', '0°'], 'c', 'easy', "Opposite."),
                ("If A = 1, B = 2 …, the value of BED is ___.", ['9', '11', '13', '10'], 'b', 'easy', "2 + 5 + 4."),
                ("Odd one out: Square, Rhombus, Rectangle, Triangle", ['Square', 'Rhombus', 'Rectangle', 'Triangle'], 'd', 'easy', "Not a quadrilateral."),
            ]),
            ('SCI1', 'SAT – Science', 1, 0, [
                ("The SI unit of pressure is ___.", ['Newton', 'Pascal', 'Joule', 'Watt'], 'b', 'easy', "Pa."),
                ("Proteins are made on ___.", ['Ribosomes', 'Lysosomes', 'Vacuoles', 'Cell wall'], 'a', 'easy', "Ribosomes."),
                ("The chemical formula of baking soda is ___.", ['Na₂CO₃', 'NaHCO₃', 'NaCl', 'CaCO₃'], 'b', 'medium', "Sodium bicarbonate."),
                ("Sound travels fastest in ___.", ['Air', 'Water', 'Solids', 'Vacuum'], 'c', 'easy', "Solids."),
            ]),
            ('MAT1', 'SAT – Mathematics', 1, 0, [
                ("(−3) × (−4) = ___", ['−12', '12', '−7', '7'], 'b', 'easy', "Positive."),
                ("If 2x + 3 = 11, x = ___.", ['3', '4', '5', '7'], 'b', 'easy', "2x = 8."),
                ("√0.04 = ___", ['0.02', '0.2', '2', '0.002'], 'b', 'medium', "0.2² = 0.04."),
            ]),
            ('SST1', 'SAT – Social Science', 1, 0, [
                ("The Battle of Plassey was fought in ___.", ['1757', '1764', '1857', '1707'], 'a', 'easy', "1757."),
                ("Fundamental Rights are in Part ___ of the Constitution.", ['II', 'III', 'IV', 'V'], 'b', 'easy', "Part III."),
                ("The largest ocean is the ___.", ['Atlantic', 'Pacific', 'Indian', 'Arctic'], 'b', 'easy', "Pacific."),
            ]),
        ],
    },
    {
        'exam': 'Olympiad', 'icon': 'trophy', 'color': '#d97706', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "Science & Maths Olympiads (SOF NSO/IMO style, Classes 6–8): 50 questions in 60 minutes – Logical Reasoning, subject sections and an Achiever's section (3 marks each). No negative marking.",
        'sections': [
            ('RSN1', 'Logical Reasoning', 1, 0, [
                ("Next term: 1, 1, 2, 3, 5, 8, ?", ['11', '12', '13', '15'], 'c', 'easy', "Fibonacci."),
                ("Odd one out: 121, 144, 169, 200", ['121', '144', '169', '200'], 'd', 'easy', "Not a square."),
                ("MATHS written backwards is ___.", ['SHTAM', 'SHATM', 'SMTAH', 'HTAMS'], 'a', 'easy', "Reverse."),
                ("Facing north, you turn right three times. You now face ___.", ['East', 'South', 'West', 'North'], 'c', 'medium', "N → E → S → W."),
                ("Kilogram : Mass :: Litre : ?", ['Length', 'Volume', 'Weight', 'Time'], 'b', 'easy', "Unit : quantity."),
                ("Next prime: 2, 3, 5, 7, 11, ?", ['12', '13', '15', '17'], 'b', 'easy', "13."),
            ]),
            ('MAT1', 'Mathematics', 1, 0, [
                ("The smallest prime number is ___.", ['0', '1', '2', '3'], 'c', 'easy', "2."),
                ("HCF of 24 and 36 = ___", ['6', '12', '18', '72'], 'b', 'easy', "12."),
                ("−7 + 4 = ___", ['−11', '−3', '3', '11'], 'b', 'easy', "−3."),
                ("Two angles of a triangle are 50° and 60°. The third is ___.", ['60°', '70°', '80°', '90°'], 'b', 'easy', "180 − 110."),
                ("1/3 + 1/6 = ___", ['2/9', '1/2', '1/9', '2/3'], 'b', 'easy', "2/6 + 1/6."),
            ]),
            ('SCI1', 'Science', 1, 0, [
                ("In photosynthesis, plants take in ___.", ['Oxygen', 'Carbon dioxide', 'Nitrogen', 'Hydrogen'], 'b', 'easy', "CO₂."),
                ("A magnet attracts ___.", ['Wood', 'Iron', 'Plastic', 'Glass'], 'b', 'easy', "Iron."),
                ("The metal that is liquid at room temperature is ___.", ['Iron', 'Mercury', 'Silver', 'Lead'], 'b', 'easy', "Mercury."),
                ("Our skin makes vitamin ___ in sunlight.", ['A', 'C', 'D', 'K'], 'c', 'easy', "Vitamin D."),
                ("Shadows are formed by ___ objects.", ['Transparent', 'Opaque', 'Translucent', 'Luminous'], 'b', 'easy', "Opaque."),
            ]),
            ('MAT1', "Achiever's Section", 3, 0, [
                ("A 20 m × 15 m garden has a 2 m wide path inside along its edges. Area of the path = ___.", ['124 m²', '140 m²', '176 m²', '100 m²'], 'a', 'hard', "300 − 16 × 11."),
                ("The sum of interior angles of an octagon is ___.", ['900°', '1080°', '1260°', '720°'], 'b', 'medium', "(8 − 2) × 180."),
                ("Which is a chemical change?", ['Melting ice', 'Dissolving sugar', 'Burning wood', 'Cutting paper'], 'c', 'easy', "New substances form."),
                ("A car uses 8 L of petrol per 100 km. Petrol needed for 350 km = ___.", ['24 L', '28 L', '30 L', '35 L'], 'b', 'medium', "3.5 × 8."),
            ]),
        ],
    },
]
