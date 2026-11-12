# School-level Olympiads and admission tests (Classes 6–9).
# Section: (subject code, section name, marks, negative marks, questions)

EXAMS = [
    {
        'exam': 'NSO Science Olympiad', 'icon': 'flask', 'color': '#16a34a', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "SOF National Science Olympiad (Classes 1–12, held in schools): Classes 5–12 get 50 questions for 60 marks in 60 minutes – Logical Reasoning, Science and an Achievers Section (3 marks each). No negative marking. This mock is set at Class 6–8 level.",
        'sections': [
            ('RSN1', 'Logical Reasoning', 1, 0, [
                ("Find the missing number: 3, 9, 27, 81, ?", ['162', '243', '324', '729'], 'b', 'easy', "Each term is 3 times the previous one."),
                ("If CAT is coded as DBU, then DOG is coded as ___.", ['EPH', 'EPF', 'DPH', 'FQI'], 'a', 'easy', "Each letter moves one place forward."),
                ("Which word does not belong: Rose, Lotus, Mango, Lily?", ['Rose', 'Lotus', 'Mango', 'Lily'], 'c', 'easy', "The others are flowers; mango is a fruit."),
                ("Ravi is taller than Amit, and Amit is taller than Sohan. Who is the shortest?", ['Ravi', 'Amit', 'Sohan', 'Cannot be determined'], 'c', 'easy', "Ravi > Amit > Sohan."),
            ]),
            ('SCI1', 'Science', 1, 0, [
                ("Which part of a plant carries water from the roots to the leaves?", ['Phloem', 'Xylem', 'Stomata', 'Root hair'], 'b', 'easy', "Xylem conducts water; phloem conducts food."),
                ("The SI unit of force is the ___.", ['Joule', 'Watt', 'Newton', 'Pascal'], 'c', 'easy', "Force is measured in newtons."),
                ("Which of these is a non-renewable source of energy?", ['Solar', 'Wind', 'Coal', 'Tidal'], 'c', 'easy', "Coal is a fossil fuel that cannot be replaced quickly."),
                ("A lack of iodine in the diet causes ___.", ['Scurvy', 'Goitre', 'Rickets', 'Night blindness'], 'b', 'easy', "Iodine is needed by the thyroid gland."),
                ("Which gas turns lime water milky?", ['Oxygen', 'Nitrogen', 'Carbon dioxide', 'Hydrogen'], 'c', 'easy', "CO₂ forms insoluble calcium carbonate."),
                ("The image formed by a plane mirror is ___.", ['Real and inverted', 'Virtual and erect', 'Real and erect', 'Virtual and inverted'], 'b', 'easy', "Same size, upright and behind the mirror."),
                ("Water vapour changing into liquid water is called ___.", ['Evaporation', 'Condensation', 'Sublimation', 'Melting'], 'b', 'easy', "Gas to liquid is condensation."),
                ("Which of these conducts electricity?", ['Rubber', 'Glass', 'Copper', 'Plastic'], 'c', 'easy', "Metals such as copper are good conductors."),
                ("The pH of pure water is ___.", ['0', '5', '7', '14'], 'c', 'easy', "Pure water is neutral."),
                ("Which organ filters waste from the blood?", ['Heart', 'Lungs', 'Kidneys', 'Stomach'], 'c', 'easy', "Kidneys filter blood and make urine."),
                ("Sound cannot travel through ___.", ['Water', 'Steel', 'Air', 'A vacuum'], 'd', 'easy', "Sound needs a medium."),
                ("Which planet is called the Red Planet?", ['Venus', 'Mars', 'Jupiter', 'Saturn'], 'b', 'easy', "Iron oxide on its surface makes Mars look red."),
            ]),
            ('SCI1', 'Achievers Section', 3, 0, [
                ("A car covers 150 km in 2.5 hours. Its average speed is ___.", ['50 km/h', '60 km/h', '65 km/h', '75 km/h'], 'b', 'medium', "150 ÷ 2.5 = 60 km/h."),
                ("When a bar magnet is cut into two pieces, each piece ___.", ['Has only a north pole', 'Has only a south pole', 'Has both a north and a south pole', 'Loses its magnetism'], 'c', 'medium', "Magnetic poles always exist in pairs."),
                ("Which change is physical and reversible?", ['Burning paper', 'Rusting of iron', 'Melting of wax', 'Cooking an egg'], 'c', 'medium', "Melted wax sets again; no new substance forms."),
                ("A net force of 10 N acts on a 2 kg body. Its acceleration is ___.", ['2 m/s²', '5 m/s²', '10 m/s²', '20 m/s²'], 'b', 'hard', "a = F/m = 10/2."),
            ]),
        ],
    },
    {
        'exam': 'IMO Maths Olympiad', 'icon': 'square-root-variable', 'color': '#2563eb', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "SOF International Mathematics Olympiad (Classes 1–12, held in schools): Classes 5–12 get 50 questions for 60 marks in 60 minutes – Logical Reasoning, Mathematical Reasoning, Everyday Mathematics and an Achievers Section (3 marks each). No negative marking. This mock is set at Class 6–8 level.",
        'sections': [
            ('RSN1', 'Logical Reasoning', 1, 0, [
                ("Find the next term: 2, 6, 12, 20, 30, ?", ['40', '42', '44', '36'], 'b', 'easy', "Differences are 4, 6, 8, 10, 12."),
                ("In a row of 25 students, Meena is 9th from the left. Her position from the right is ___.", ['15th', '16th', '17th', '18th'], 'c', 'easy', "25 − 9 + 1 = 17."),
                ("1 January of a non-leap year is a Monday. 1 February of that year is a ___.", ['Wednesday', 'Thursday', 'Friday', 'Tuesday'], 'b', 'medium', "31 days = 4 weeks + 3 days; Monday + 3 = Thursday."),
                ("A line is drawn from one vertex of a triangle to the opposite side. How many triangles are there now?", ['2', '3', '4', '5'], 'b', 'easy', "Two small triangles and the whole one."),
            ]),
            ('MAT1', 'Mathematical Reasoning', 1, 0, [
                ("LCM of 12, 18 and 30 = ___", ['90', '180', '360', '60'], 'b', 'easy', "2² × 3² × 5 = 180."),
                ("(−3)³ = ___", ['−9', '9', '−27', '27'], 'c', 'easy', "An odd power of a negative number is negative."),
                ("If 3x − 7 = 11, then x = ___.", ['4', '5', '6', '7'], 'c', 'easy', "3x = 18."),
                ("The area of a triangle with base 12 cm and height 9 cm is ___.", ['54 cm²', '108 cm²', '42 cm²', '21 cm²'], 'a', 'easy', "½ × 12 × 9."),
                ("Which of these is a perfect square?", ['1225', '1250', '1300', '1350'], 'a', 'medium', "35² = 1225."),
                ("36 : 48 in its simplest form is ___.", ['3 : 4', '4 : 3', '6 : 8', '9 : 16'], 'a', 'easy', "Divide both by 12."),
                ("Each interior angle of a regular hexagon is ___.", ['108°', '120°', '135°', '144°'], 'b', 'medium', "(6 − 2) × 180 ÷ 6."),
                ("0.25 as a fraction in its lowest terms is ___.", ['1/4', '25/10', '2/5', '1/25'], 'a', 'easy', "25/100 = 1/4."),
            ]),
            ('MAT1', 'Everyday Mathematics', 1, 0, [
                ("A shirt marked ₹800 is sold at a 15% discount. The selling price is ___.", ['₹680', '₹700', '₹720', '₹785'], 'a', 'easy', "800 − 120 = 680."),
                ("A train leaves at 10:45 a.m. and arrives at 2:20 p.m. The journey takes ___.", ['3 h 25 min', '3 h 35 min', '4 h 25 min', '3 h 45 min'], 'b', 'medium', "10:45 → 2:45 is 4 h; minus 25 min."),
                ("Simple interest on ₹5,000 at 8% per annum for 3 years is ___.", ['₹1,000', '₹1,200', '₹1,500', '₹400'], 'b', 'easy', "5000 × 8 × 3 ÷ 100."),
                ("5 notebooks cost ₹175. The cost of 8 notebooks is ___.", ['₹260', '₹270', '₹280', '₹300'], 'c', 'easy', "₹35 each × 8."),
            ]),
            ('MAT1', 'Achievers Section', 3, 0, [
                ("The sum of three consecutive even numbers is 78. The largest is ___.", ['24', '26', '28', '30'], 'c', 'medium', "n + (n + 2) + (n + 4) = 78 gives n = 24."),
                ("A rectangle has a perimeter of 50 cm and a length of 15 cm. Its area is ___.", ['100 cm²', '125 cm²', '150 cm²', '175 cm²'], 'c', 'medium', "Breadth = 25 − 15 = 10 cm."),
                ("The average of 5 numbers is 18. Removing one number makes the average 16. The removed number is ___.", ['22', '24', '26', '28'], 'c', 'hard', "90 − 4 × 16 = 26."),
                ("How many two-digit numbers are divisible by 7?", ['12', '13', '14', '15'], 'b', 'hard', "14, 21, …, 98: (98 − 14) ÷ 7 + 1 = 13."),
            ]),
        ],
    },
    {
        'exam': 'IEO English Olympiad', 'icon': 'spell-check', 'color': '#db2777', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "SOF International English Olympiad (Classes 1–12, held in schools): Classes 5–12 get 50 questions for 60 marks in 60 minutes – Word and Structure Knowledge, Reading, Spoken and Written Expression, and an Achievers Section (3 marks each). No negative marking. This mock is set at Class 6–8 level.",
        'sections': [
            ('ENG1', 'Word and Structure Knowledge', 1, 0, [
                ("Choose the synonym of ENORMOUS.", ['Tiny', 'Huge', 'Weak', 'Quick'], 'b', 'easy', "Enormous means very large."),
                ("Choose the antonym of ANCIENT.", ['Old', 'Modern', 'Historic', 'Antique'], 'b', 'easy', "Ancient means very old."),
                ("She ___ to school every day.", ['go', 'goes', 'going', 'gone'], 'b', 'easy', "Third person singular, simple present."),
                ("He is good ___ mathematics.", ['in', 'at', 'on', 'with'], 'b', 'easy', "'Good at' a subject or skill."),
                ("Choose the correctly spelt word.", ['Recieve', 'Receive', 'Receeve', 'Riceive'], 'b', 'easy', "'i' before 'e' except after 'c'."),
                ("The plural of 'child' is ___.", ['Childs', 'Childes', 'Children', 'Childrens'], 'c', 'easy', "An irregular plural."),
                ("Identify the adverb: 'The tortoise moved slowly across the road.'", ['tortoise', 'moved', 'slowly', 'road'], 'c', 'easy', "'Slowly' tells how it moved."),
                ("She is ___ honest girl.", ['a', 'an', 'the', 'no article'], 'b', 'medium', "'Honest' begins with a vowel sound."),
                ("The past tense of 'write' is ___.", ['writed', 'wrote', 'written', 'writes'], 'b', 'easy', "write – wrote – written."),
                ("A person who writes books is called an ___.", ['Editor', 'Author', 'Publisher', 'Reader'], 'b', 'easy', "Author."),
            ]),
            ('ENG1', 'Reading', 1, 0, [
                ("Read: 'Honeybees live in large groups called colonies. Each colony has one queen, thousands of workers and a few drones. The workers collect nectar and make honey.' Who makes the honey?", ['The queen', 'The drones', 'The workers', 'All bees equally'], 'c', 'easy', "The passage says the workers make honey."),
                ("In the honeybee passage, how many queens does a colony have?", ['One', 'Two', 'A few', 'Thousands'], 'a', 'easy', "'Each colony has one queen.'"),
                ("Read: 'Ravi missed the bus, so he walked to school and reached late. His teacher asked him to leave home earlier.' Why did Ravi reach late?", ['He was ill', 'He missed the bus', 'School started early', 'He lost his way'], 'b', 'easy', "He missed the bus and had to walk."),
                ("In the passage about Ravi, what did the teacher advise?", ['Take a taxi', 'Leave home earlier', 'Skip school', 'Run faster'], 'b', 'easy', "'Asked him to leave home earlier.'"),
            ]),
            ('ENG1', 'Spoken and Written Expression', 1, 0, [
                ("Which is the most polite way to ask for help?", ['Help me now.', 'Could you please help me?', 'You must help me.', 'Help me, quick.'], 'b', 'easy', "'Could you please' is polite."),
                ("Your friend says, 'I won the race!' The best reply is ___.", ['So what?', 'Congratulations, well done!', "I don't care.", 'Who asked?'], 'b', 'easy', "A warm, appropriate response."),
                ("Choose the correctly punctuated sentence.", ['where are you going', 'Where are you going?', 'Where are you going.', 'where are you going?'], 'b', 'easy', "A capital letter and a question mark."),
            ]),
            ('ENG1', 'Achievers Section', 3, 0, [
                ("Choose the passive form of 'The boy kicked the ball.'", ['The ball is kicked by the boy.', 'The ball was kicked by the boy.', 'The ball has been kicked by the boy.', 'The boy was kicked by the ball.'], 'b', 'medium', "Simple past active becomes 'was + past participle'."),
                ("'A piece of cake' means ___.", ['Something very easy', 'A tasty dessert', 'A small share', 'A difficult task'], 'a', 'medium', "An idiom for an easy task."),
                ("Choose the indirect speech: He said, 'I am tired.'", ['He said that he is tired.', 'He said that he was tired.', 'He said that I was tired.', 'He says he was tired.'], 'b', 'hard', "Past reporting verb: 'am' becomes 'was' and 'I' becomes 'he'."),
            ]),
        ],
    },
    {
        'exam': 'NCO Cyber Olympiad', 'icon': 'laptop-code', 'color': '#475569', 'difficulty': 'medium', 'minutes': 24,
        'pattern': "SOF National Cyber Olympiad (Classes 1–12, held in schools): Classes 5–12 get 50 questions for 60 marks in 60 minutes – Logical Reasoning, Computers & IT and an Achievers Section (3 marks each). No negative marking. This mock is set at Class 6–8 level.",
        'sections': [
            ('RSN1', 'Logical Reasoning', 1, 0, [
                ("Find the odd one out: Keyboard, Mouse, Scanner, Printer", ['Keyboard', 'Mouse', 'Scanner', 'Printer'], 'd', 'easy', "The printer is the only output device."),
                ("Find the next letter: A, C, F, J, O, ?", ['S', 'T', 'U', 'V'], 'c', 'medium', "Gaps of +2, +3, +4, +5, +6: O (15) + 6 = U (21)."),
                ("If PEN = 35 (P = 16, E = 5, N = 14), then INK = ___.", ['32', '33', '34', '35'], 'c', 'medium', "9 + 14 + 11 = 34."),
                ("Pointing to a boy, Neha says, 'He is the son of my mother's only son.' The boy is Neha's ___.", ['Brother', 'Cousin', 'Nephew', 'Son'], 'c', 'medium', "Her mother's only son is her brother; his son is her nephew."),
            ]),
            ('CMP1', 'Computers and IT', 1, 0, [
                ("The 'brain' of a computer is the ___.", ['Monitor', 'CPU', 'Keyboard', 'Hard disk'], 'b', 'easy', "The CPU processes instructions."),
                ("1 kilobyte (KB) = ___ bytes.", ['1000', '1024', '100', '512'], 'b', 'easy', "2¹⁰ bytes."),
                ("Which of these is an input device?", ['Monitor', 'Printer', 'Microphone', 'Speaker'], 'c', 'easy', "A microphone sends sound into the computer."),
                ("Which memory loses its data when the power is switched off?", ['ROM', 'RAM', 'Hard disk', 'Pen drive'], 'b', 'easy', "RAM is volatile."),
                ("The shortcut to copy selected text is ___.", ['Ctrl + V', 'Ctrl + X', 'Ctrl + C', 'Ctrl + Z'], 'c', 'easy', "C for copy."),
                ("Which of these is an operating system?", ['MS Word', 'Windows', 'Google Chrome', 'MS Paint'], 'b', 'easy', "Windows manages the computer's hardware and software."),
                ("In a spreadsheet, the meeting point of a row and a column is a ___.", ['Cell', 'Table', 'Sheet', 'Range'], 'a', 'easy', "For example cell B3."),
                ("URL stands for ___.", ['Uniform Resource Locator', 'Universal Resource Link', 'Uniform Router Locator', 'United Resource Locator'], 'a', 'easy', "A web address."),
                ("Binary numbers use the digits ___.", ['0 and 1', '0 to 7', '0 to 9', '1 and 2'], 'a', 'easy', "Base 2."),
                ("Which file extension is used for a PowerPoint presentation?", ['.docx', '.xlsx', '.pptx', '.txt'], 'c', 'easy', ".pptx."),
                ("Sending fake emails to steal passwords is called ___.", ['Phishing', 'Browsing', 'Streaming', 'Formatting'], 'a', 'easy', "Phishing is a cyber fraud."),
                ("Which of these is a web browser?", ['Google Chrome', 'MS Excel', 'Windows', 'Linux'], 'a', 'easy', "Chrome opens web pages."),
            ]),
            ('CMP1', 'Achievers Section', 3, 0, [
                ("Binary 1011 = decimal ___.", ['9', '10', '11', '13'], 'c', 'medium', "8 + 0 + 2 + 1 = 11."),
                ("In a spreadsheet, =SUM(A1:A4) adds ___.", ['A1 and A4 only', 'Cells A1 to A4', 'Columns A to D', 'Rows 1 to 4 of every column'], 'b', 'medium', "A colon gives a range."),
                ("Which is the strongest password?", ['password123', '12345678', 'Ravi2010', 'T#9vq!2Lm'], 'd', 'easy', "It mixes cases, digits and symbols."),
                ("Decimal 25 in binary is ___.", ['11001', '10101', '11011', '10011'], 'a', 'hard', "16 + 8 + 1 = 25."),
            ]),
        ],
    },
    {
        'exam': 'IOQM', 'icon': 'infinity', 'color': '#9333ea', 'difficulty': 'hard', 'minutes': 60,
        'pattern': "Indian Olympiad Qualifier in Mathematics (HBCSE/MTA, Classes 8–12; first stage towards INMO and the IMO): 30 questions in 3 hours – 10 × 2 marks, 10 × 3 marks and 10 × 5 marks (100 marks). Every answer is an integer from 00 to 99. No negative marking. In this mock the integer answers are given as options.",
        'sections': [
            ('MAT1', '2-mark questions', 2, 0, [
                ("How many positive divisors does 72 have?", ['10', '12', '14', '16'], 'b', 'medium', "72 = 2³ × 3², so (3 + 1)(2 + 1) = 12."),
                ("Find the remainder when 2¹⁰ is divided by 7.", ['1', '2', '4', '6'], 'b', 'medium', "2³ ≡ 1 (mod 7), so 2¹⁰ = (2³)³ × 2 ≡ 2."),
                ("Find the sum of the digits of 2¹⁰.", ['5', '7', '8', '9'], 'b', 'easy', "2¹⁰ = 1024 and 1 + 0 + 2 + 4 = 7."),
                ("How many positive integers less than 100 are divisible by 3 or 5?", ['43', '46', '47', '49'], 'b', 'medium', "33 + 19 − 6 = 46 (inclusion–exclusion)."),
            ]),
            ('MAT1', '3-mark questions', 3, 0, [
                ("If x + y = 10 and xy = 21, find x² + y².", ['42', '58', '62', '79'], 'b', 'medium', "(x + y)² − 2xy = 100 − 42."),
                ("In how many ways can the letters of LEVEL be arranged?", ['20', '30', '60', '120'], 'b', 'medium', "5! ÷ (2! × 2!) = 30."),
                ("Find the last two digits of 7¹⁰⁰.", ['01', '07', '43', '49'], 'a', 'hard', "7⁴ = 2401 ≡ 01 (mod 100), so 7¹⁰⁰ = (7⁴)²⁵ ≡ 01."),
            ]),
            ('MAT1', '5-mark questions', 5, 0, [
                ("A right triangle has integer sides and hypotenuse 25. What is its largest possible perimeter?", ['56', '60', '62', '70'], 'b', 'hard', "The triangles are 7-24-25 (56) and 15-20-25 (60)."),
                ("Find the smallest integer n > 1 that leaves remainder 1 when divided by each of 2, 3, 4, 5 and 6.", ['59', '61', '121', '31'], 'b', 'hard', "n − 1 is a multiple of LCM(2, …, 6) = 60."),
                ("How many zeros are at the end of 100! (100 factorial)?", ['20', '22', '24', '25'], 'c', 'hard', "⌊100/5⌋ + ⌊100/25⌋ = 20 + 4."),
            ]),
        ],
    },
    {
        'exam': 'JNVST Class 9', 'icon': 'school-flag', 'color': '#0f766e', 'difficulty': 'medium', 'minutes': 30,
        'pattern': "Navodaya Vidyalaya Lateral Entry Selection Test for Class IX (NVS): an objective test of 100 marks in 2½ hours – English 15, Hindi 15, Mathematics 35 and General Science 35, at Class 8 level. No negative marking.",
        'sections': [
            ('ENG1', 'English', 1, 0, [
                ("Choose the correct sentence.", ["He don't like tea.", "He doesn't like tea.", "He not like tea.", "He doesn't likes tea."], 'b', 'easy', "'Does not' + base verb."),
                ("Choose the synonym of RAPID.", ['Slow', 'Fast', 'Lazy', 'Heavy'], 'b', 'easy', "Rapid means fast."),
                ("Neither Ram nor his friends ___ present.", ['was', 'were', 'is', 'has'], 'b', 'medium', "With 'neither…nor', the verb agrees with the nearer subject (friends)."),
            ]),
            ('HIN1', 'Hindi', 1, 0, [
                ("'सूर्य' का पर्यायवाची शब्द है ___ ।", ['चंद्रमा', 'दिनकर', 'आकाश', 'तारा'], 'b', 'easy', "दिनकर, रवि, भानु – सूर्य के पर्यायवाची।"),
                ("'दिन' का विलोम शब्द है ___ ।", ['सुबह', 'रात', 'शाम', 'दोपहर'], 'b', 'easy', "दिन – रात।"),
                ("'अनुपस्थित' शब्द में उपसर्ग है ___ ।", ['अन', 'अनु', 'स्थित', 'उप'], 'a', 'medium', "अन + उपस्थित।"),
            ]),
            ('MAT1', 'Mathematics', 1, 0, [
                ("√144 + √81 = ___", ['21', '15', '23', '19'], 'a', 'easy', "12 + 9."),
                ("If 2x + 3 = 15, then x = ___.", ['5', '6', '7', '9'], 'b', 'easy', "2x = 12."),
                ("The HCF of 54 and 90 is ___.", ['9', '18', '27', '6'], 'b', 'easy', "54 = 2 × 3³ and 90 = 2 × 3² × 5."),
                ("A sum doubles in 8 years at simple interest. The rate is ___.", ['10%', '12.5%', '8%', '15%'], 'b', 'medium', "Interest = principal in 8 years, so 100% ÷ 8."),
                ("The volume of a cube of side 5 cm is ___.", ['25 cm³', '75 cm³', '125 cm³', '150 cm³'], 'c', 'easy', "5³."),
                ("(a + b)² − (a − b)² = ___", ['2ab', '4ab', '2a² + 2b²', '0'], 'b', 'medium', "Expand both squares and subtract."),
                ("The probability of getting a head when a fair coin is tossed is ___.", ['0', '1/2', '1', '1/4'], 'b', 'easy', "One of two equally likely outcomes."),
            ]),
            ('SCI1', 'General Science', 1, 0, [
                ("The basic unit of life is the ___.", ['Tissue', 'Cell', 'Organ', 'Nucleus'], 'b', 'easy', "All living things are made of cells."),
                ("Which of these is a chemical change?", ['Freezing water', 'Rusting of iron', 'Breaking glass', 'Dissolving salt'], 'b', 'easy', "Rust is a new substance."),
                ("The acceleration due to gravity at the Earth's surface is about ___.", ['9.8 m/s²', '98 m/s²', '0.98 m/s²', '1.6 m/s²'], 'a', 'easy', "g ≈ 9.8 m/s²."),
                ("Which blood cells fight infection?", ['Red blood cells', 'White blood cells', 'Platelets', 'Plasma'], 'b', 'easy', "WBCs are part of the immune system."),
                ("The chemical formula of common salt is ___.", ['NaCl', 'KCl', 'NaOH', 'HCl'], 'a', 'easy', "Sodium chloride."),
                ("Light travels fastest in ___.", ['Water', 'Glass', 'A vacuum', 'Diamond'], 'c', 'easy', "About 3 × 10⁸ m/s in a vacuum."),
                ("Which gas is released during photosynthesis?", ['CO₂', 'O₂', 'N₂', 'H₂'], 'b', 'easy', "Oxygen is a by-product."),
            ]),
        ],
    },
]
