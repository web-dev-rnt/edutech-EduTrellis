# Previous-year-pattern papers: questions on topics that past papers ask again and again, in the real marking
# scheme. These are original practice questions, not reproductions of official papers.
# 'series' selects the TestSeries to add the paper to. Section: (subject code, section name, marks, negative, questions)

PAPERS = [
    {
        'series': {'board': 'cbse', 'grade': 10, 'stream': ''},
        'name': 'CBSE Class 10 board exam', 'minutes': 20,
        'sections': [
            ('MAT1', 'Mathematics', 1, 0, [
                ("The HCF of 96 and 404 is ___.", ['4', '8', '12', '2'], 'a', 'easy', "96 = 2⁵ × 3 and 404 = 2² × 101, so HCF = 2² = 4."),
                ("The roots of x² − 3x − 10 = 0 are ___.", ['5 and −2', '−5 and 2', '5 and 2', '−5 and −2'], 'a', 'easy', "(x − 5)(x + 2) = 0."),
                ("The 10th term of the AP 2, 7, 12, … is ___.", ['45', '47', '49', '52'], 'b', 'easy', "a + 9d = 2 + 45."),
                ("If sin A = 3/5 and A is acute, then cos A = ___.", ['3/4', '4/5', '5/4', '5/3'], 'b', 'easy', "√(1 − 9/25) = 4/5."),
                ("The distance between the points (2, 3) and (4, 1) is ___.", ['2', '2√2', '4', '√2'], 'b', 'medium', "√(2² + 2²) = √8 = 2√2."),
            ]),
            ('SCI1', 'Science', 1, 0, [
                ("Fe₂O₃ + 2Al → Al₂O₃ + 2Fe is an example of a ___ reaction.", ['Combination', 'Decomposition', 'Displacement', 'Double displacement'], 'c', 'easy', "Aluminium displaces iron from its oxide (thermit reaction)."),
                ("A concave mirror has a radius of curvature of 20 cm. Its focal length is ___.", ['5 cm', '10 cm', '20 cm', '40 cm'], 'b', 'easy', "f = R/2."),
                ("The correct path of urine in the human body is ___.", ['Kidney → ureter → urinary bladder → urethra', 'Kidney → urethra → bladder → ureter', 'Bladder → kidney → ureter → urethra', 'Ureter → kidney → bladder → urethra'], 'a', 'easy', "Urine is made in the kidneys and stored in the bladder."),
                ("A 10 Ω resistor carries a current of 0.5 A. The potential difference across it is ___.", ['2 V', '5 V', '10 V', '20 V'], 'b', 'easy', "V = IR."),
                ("A solution that turns blue litmus red has a pH ___.", ['Less than 7', 'Of exactly 7', 'More than 7', 'Of exactly 14'], 'a', 'easy', "It is acidic."),
            ]),
            ('SST1', 'Social Science', 1, 0, [
                ("The Civil Disobedience Movement began with the ___.", ['Champaran Satyagraha', 'Dandi March', 'Kheda Satyagraha', 'Quit India Movement'], 'b', 'easy', "Gandhi's Salt March, 1930."),
                ("Which soil is best suited to growing cotton?", ['Alluvial soil', 'Black soil', 'Laterite soil', 'Arid soil'], 'b', 'easy', "Black (regur) soil holds moisture well."),
                ("Power shared among the legislature, executive and judiciary is called ___ distribution of power.", ['Vertical', 'Horizontal', 'Federal', 'Community'], 'b', 'medium', "Organs at the same level share power horizontally."),
                ("Agriculture, fishing and mining belong to the ___ sector.", ['Primary', 'Secondary', 'Tertiary', 'Quaternary'], 'a', 'easy', "They use natural resources directly."),
                ("The Treaty of Vienna (1815) was drawn up after the defeat of ___.", ['Bismarck', 'Napoleon', 'Mazzini', 'Garibaldi'], 'b', 'medium', "European powers undid Napoleon's changes."),
            ]),
        ],
    },
    {
        'series': {'board': 'cbse', 'grade': 12, 'stream': 'science'},
        'name': 'CBSE Class 12 board exam', 'minutes': 25,
        'sections': [
            ('PHY1', 'Physics', 1, 0, [
                ("The SI unit of electric flux is ___.", ['N/C', 'N m²/C', 'C/m²', 'V/m'], 'b', 'easy', "Flux = field × area."),
                ("Resistors of 4 Ω and 12 Ω are connected in parallel. The equivalent resistance is ___.", ['3 Ω', '8 Ω', '16 Ω', '0.33 Ω'], 'a', 'easy', "(4 × 12) ÷ (4 + 12) = 3 Ω."),
                ("The power of a lens of focal length +25 cm is ___.", ['+0.25 D', '+2.5 D', '+4 D', '−4 D'], 'c', 'easy', "P = 1/f (in metres) = 1/0.25."),
                ("In Young's double-slit experiment, the fringe width β = ___.", ['λd/D', 'λD/d', 'Dd/λ', 'λ/(Dd)'], 'b', 'medium', "β = λD/d."),
                ("A forward-biased p–n junction diode has ___.", ['Very high resistance', 'Low resistance', 'Zero current', 'No depletion region at all'], 'b', 'easy', "Forward bias narrows the depletion layer and current flows."),
            ]),
            ('CHE1', 'Chemistry', 1, 0, [
                ("The number of atoms per unit cell in a body-centred cubic lattice is ___.", ['1', '2', '4', '6'], 'b', 'easy', "8 × 1/8 + 1 = 2."),
                ("For a first-order reaction, the half-life is ___.", ['Directly proportional to the initial concentration', 'Independent of the initial concentration', 'Inversely proportional to the initial concentration', 'Proportional to the square of the initial concentration'], 'b', 'medium', "t½ = 0.693/k."),
                ("Which of these is a colligative property?", ['Osmotic pressure', 'Density', 'Viscosity', 'Surface tension'], 'a', 'easy', "It depends only on the number of solute particles."),
                ("The IUPAC name of CH₃CH₂CHO is ___.", ['Propanal', 'Propanone', 'Ethanal', 'Propan-1-ol'], 'a', 'easy', "A three-carbon aldehyde."),
                ("Heating glucose with HI for a long time gives ___.", ['n-Hexane', 'Gluconic acid', 'Sorbitol', 'Saccharic acid'], 'a', 'medium', "This shows glucose has a straight chain of six carbons."),
            ]),
            ('MAT1', 'Mathematics', 1, 0, [
                ("d/dx [sin(x²)] = ___", ['cos(x²)', '2x cos(x²)', '2 sin x cos x', '−2x cos(x²)'], 'b', 'easy', "Chain rule."),
                ("∫ (1/x) dx = ___", ['x + C', 'ln|x| + C', '1/x² + C', '−1/x² + C'], 'b', 'easy', "Standard integral."),
                ("A is a 3 × 3 matrix with |A| = 5. Then |adj A| = ___.", ['5', '15', '25', '125'], 'c', 'medium', "|adj A| = |A|ⁿ⁻¹ = 5²."),
                ("The order of the differential equation d²y/dx² + (dy/dx)³ = 0 is ___.", ['1', '2', '3', '6'], 'b', 'easy', "The highest derivative is the second."),
                ("A and B are independent, with P(A) = 0.4 and P(B) = 0.5. P(A ∩ B) = ___.", ['0.9', '0.2', '0.1', '0.45'], 'b', 'easy', "P(A) × P(B)."),
            ]),
        ],
    },
    {
        'series': {'exam': 'JEE Main'},
        'name': 'JEE Main', 'minutes': 36,
        'sections': [
            ('PHY1', 'Physics', 4, 1, [
                ("A ball is thrown straight up at 20 m/s (g = 10 m/s²). The maximum height reached is ___.", ['10 m', '20 m', '40 m', '80 m'], 'b', 'easy', "h = v²/2g = 400/20."),
                ("The dimensional formula of Planck's constant is ___.", ['[ML²T⁻²]', '[ML²T⁻¹]', '[MLT⁻¹]', '[ML²T⁻³]'], 'b', 'medium', "h = E/ν, so energy × time."),
                ("The escape velocity from the Earth's surface is about ___.", ['7.9 km/s', '11.2 km/s', '3.0 km/s', '42.1 km/s'], 'b', 'easy', "√(2gR) ≈ 11.2 km/s."),
                ("A Carnot engine works between 500 K and 300 K. Its efficiency is ___.", ['40%', '60%', '25%', '50%'], 'a', 'easy', "1 − 300/500."),
                ("The de Broglie wavelength of a particle of momentum p is ___.", ['h/p', 'p/h', 'hp', 'h/(mc²)'], 'a', 'easy', "λ = h/p."),
            ]),
            ('CHE1', 'Chemistry', 4, 1, [
                ("The hybridisation of carbon in ethyne (C₂H₂) is ___.", ['sp', 'sp²', 'sp³', 'sp³d'], 'a', 'easy', "A triple bond: linear, sp."),
                ("The number of unpaired electrons in Fe³⁺ (Z = 26) is ___.", ['3', '4', '5', '6'], 'c', 'medium', "Fe³⁺ is 3d⁵."),
                ("Which has the highest first ionisation enthalpy?", ['Li', 'Be', 'B', 'N'], 'd', 'medium', "Nitrogen has a half-filled, stable 2p³ shell."),
                ("The shape of the XeF₄ molecule is ___.", ['Tetrahedral', 'Square planar', 'See-saw', 'Octahedral'], 'b', 'medium', "4 bond pairs and 2 lone pairs (sp³d²)."),
                ("Which reagent distinguishes an aldehyde from a ketone?", ["Tollens' reagent", 'NaBH₄', 'LiAlH₄', 'H₂/Ni'], 'a', 'easy', "Aldehydes give a silver mirror; ketones do not."),
            ]),
            ('MAT1', 'Mathematics', 4, 1, [
                ("The roots of x² − 5x + k = 0 differ by 1. Then k = ___.", ['4', '6', '8', '9'], 'b', 'medium', "The roots are 3 and 2, so k = 6."),
                ("lim (x→0) sin 3x / x = ___", ['0', '1', '3', '1/3'], 'c', 'easy', "3 × (sin 3x)/(3x) → 3."),
                ("The number of ways to choose 3 people from 7 is ___.", ['21', '35', '42', '210'], 'b', 'easy', "⁷C₃ = 35."),
                ("The line through (1, 2) with slope 3 is ___.", ['y = 3x + 2', 'y = 3x − 1', 'y = 3x + 1', 'y = x + 3'], 'b', 'easy', "y − 2 = 3(x − 1)."),
                ("∫₀^(π/2) sin x dx = ___", ['0', '1', 'π/2', '2'], 'b', 'easy', "[−cos x] from 0 to π/2."),
            ]),
        ],
    },
    {
        'series': {'exam': 'NEET UG'},
        'name': 'NEET UG', 'minutes': 16,
        'sections': [
            ('PHY1', 'Physics', 4, 1, [
                ("A 5 kg body moves at 4 m/s. Its kinetic energy is ___.", ['20 J', '40 J', '80 J', '10 J'], 'b', 'easy', "½ × 5 × 16."),
                ("The SI unit of magnetic field (B) is the ___.", ['Weber', 'Tesla', 'Henry', 'Gauss'], 'b', 'easy', "Tesla (T)."),
                ("Total internal reflection happens when light travels ___.", ['From a rarer to a denser medium', 'From a denser to a rarer medium at more than the critical angle', 'In any medium at any angle', 'From a denser to a rarer medium at less than the critical angle'], 'b', 'medium', "Both conditions are needed."),
                ("A radioactive substance has a half-life of 10 days. The fraction left after 30 days is ___.", ['1/2', '1/4', '1/8', '1/16'], 'c', 'easy', "Three half-lives: (1/2)³."),
            ]),
            ('CHE1', 'Chemistry', 4, 1, [
                ("The number of moles in 22 g of CO₂ is ___.", ['0.5', '1', '2', '0.25'], 'a', 'easy', "22 ÷ 44."),
                ("Which is the strongest acid?", ['CH₃COOH', 'ClCH₂COOH', 'Cl₂CHCOOH', 'Cl₃CCOOH'], 'd', 'medium', "More electron-withdrawing Cl atoms stabilise the anion."),
                ("The oxidation state of Mn in KMnO₄ is ___.", ['+2', '+4', '+6', '+7'], 'd', 'easy', "1 + x − 8 = 0."),
                ("Which of these is aromatic?", ['Cyclohexane', 'Benzene', 'Hexane', 'Cyclohexene'], 'b', 'easy', "A planar ring with 6 π electrons (Hückel's rule)."),
            ]),
            ('BIO1', 'Biology', 4, 1, [
                ("The 'powerhouse' of the cell is the ___.", ['Ribosome', 'Mitochondrion', 'Golgi apparatus', 'Lysosome'], 'b', 'easy', "It makes ATP by aerobic respiration."),
                ("Crossing over takes place during ___ of prophase I.", ['Leptotene', 'Zygotene', 'Pachytene', 'Diplotene'], 'c', 'medium', "Between non-sister chromatids of homologous chromosomes."),
                ("The 'fight or flight' hormone is ___.", ['Insulin', 'Adrenaline', 'Thyroxine', 'Oxytocin'], 'b', 'easy', "Secreted by the adrenal medulla."),
                ("The phenotypic ratio of the F₂ generation in a monohybrid cross (Tt × Tt) is ___.", ['1 : 2 : 1', '3 : 1', '9 : 3 : 3 : 1', '1 : 1'], 'b', 'easy', "3 tall : 1 dwarf."),
                ("Which blood group is the universal donor?", ['A', 'B', 'AB', 'O'], 'd', 'easy', "O (strictly, O negative): its red cells carry no A or B antigens."),
                ("The light reactions of photosynthesis take place in the ___.", ['Stroma', 'Thylakoid membranes', 'Mitochondria', 'Cytoplasm'], 'b', 'medium', "The dark reactions happen in the stroma."),
                ("Which sexually transmitted infection is caused by a bacterium?", ['AIDS', 'Syphilis', 'Genital herpes', 'Hepatitis B'], 'b', 'medium', "Treponema pallidum; the others are viral."),
                ("The Ti plasmid used in plant genetic engineering comes from ___.", ['Escherichia coli', 'Agrobacterium tumefaciens', 'Bacillus thuringiensis', 'Thermus aquaticus'], 'b', 'medium', "A natural genetic engineer of plants."),
            ]),
        ],
    },
    {
        'series': {'exam': 'SSC CGL'},
        'name': 'SSC CGL Tier 1', 'minutes': 12,
        'sections': [
            ('RSN1', 'General Intelligence & Reasoning', 2, 0.5, [
                ("Which number replaces '?': 4, 9, 25, 49, 121, ?", ['144', '169', '196', '225'], 'b', 'medium', "Squares of primes 2, 3, 5, 7, 11, 13."),
                ("DOCTOR : HOSPITAL :: TEACHER : ?", ['Student', 'School', 'Book', 'Class'], 'b', 'easy', "Professional : workplace."),
                ("If MANGO is coded as NBOHP, how is APPLE coded?", ['BQQMF', 'BOQMF', 'BQQME', 'ZOOKD'], 'a', 'easy', "Each letter +1."),
                ("Find the odd one out: 27, 64, 125, 150", ['27', '64', '125', '150'], 'd', 'easy', "The others are perfect cubes."),
                ("A is B's father and C is A's mother. How is C related to B?", ['Mother', 'Aunt', 'Grandmother', 'Sister'], 'c', 'easy', "C is the mother of B's father."),
            ]),
            ('GA1', 'General Awareness', 2, 0.5, [
                ("Who was the first Governor-General of independent India?", ['C. Rajagopalachari', 'Lord Mountbatten', 'Rajendra Prasad', 'Lord Wavell'], 'b', 'medium', "Rajagopalachari was the first Indian Governor-General."),
                ("Which Article of the Constitution abolishes untouchability?", ['Article 14', 'Article 17', 'Article 21', 'Article 32'], 'b', 'easy', "Article 17."),
                ("The 'Great Bath' was found at ___.", ['Harappa', 'Mohenjo-daro', 'Lothal', 'Kalibangan'], 'b', 'easy', "Indus Valley Civilisation."),
                ("Ascorbic acid is vitamin ___.", ['A', 'B12', 'C', 'D'], 'c', 'easy', "Vitamin C."),
                ("The largest gland in the human body is the ___.", ['Pancreas', 'Liver', 'Thyroid', 'Pituitary'], 'b', 'easy', "Liver."),
            ]),
            ('QNT1', 'Quantitative Aptitude', 2, 0.5, [
                ("20% of a number is 60. What is 35% of it?", ['90', '105', '120', '140'], 'b', 'easy', "The number is 300; 35% of it is 105."),
                ("An article bought for ₹400 is sold for ₹500. The profit is ___.", ['20%', '25%', '30%', '15%'], 'b', 'easy', "100 ÷ 400."),
                ("The average of the first 10 natural numbers is ___.", ['5', '5.5', '6', '10'], 'b', 'easy', "55 ÷ 10."),
                ("If sin θ = cos θ (0° < θ < 90°), then θ = ___.", ['30°', '45°', '60°', '90°'], 'b', 'easy', "tan θ = 1."),
                ("A 150 m train passes a pole in 10 seconds. Its speed is ___.", ['45 km/h', '54 km/h', '60 km/h', '72 km/h'], 'b', 'medium', "15 m/s × 18/5."),
            ]),
            ('ENG1', 'English Comprehension', 2, 0.5, [
                ("Select the synonym of ABUNDANT.", ['Scarce', 'Plentiful', 'Rare', 'Empty'], 'b', 'easy', "Abundant means plentiful."),
                ("Select the antonym of TRANSPARENT.", ['Clear', 'Opaque', 'Visible', 'Bright'], 'b', 'easy', "Opaque lets no light through."),
                ("Select the correctly spelt word.", ['Accomodate', 'Accommodate', 'Acommodate', 'Accommadate'], 'b', 'medium', "Double c, double m."),
                ("'To bury the hatchet' means ___.", ['To make peace', 'To start a fight', 'To hide something', 'To dig a hole'], 'a', 'easy', "To end a quarrel."),
                ("One word for 'a person who cannot be corrected':", ['Incorrigible', 'Invincible', 'Infallible', 'Illegible'], 'a', 'medium', "Incorrigible."),
            ]),
        ],
    },
    {
        'series': {'exam': 'UPSC Civil Services'},
        'name': 'UPSC Civil Services Prelims (GS Paper I)', 'minutes': 18,
        'sections': [
            ('GA1', 'General Studies', 2, 0.66, [
                ("Which Article of the Constitution of India deals with the Finance Commission?", ['Article 270', 'Article 280', 'Article 300A', 'Article 324'], 'b', 'medium', "Article 280."),
                ("The Directive Principles of State Policy were borrowed from the Constitution of ___.", ['the USA', 'Ireland', 'the UK', 'Canada'], 'b', 'easy', "Irish Constitution."),
                ("The Chief Election Commissioner of India is appointed by the ___.", ['Prime Minister', 'President', 'Chief Justice of India', 'Parliament'], 'b', 'easy', "The President appoints the CEC."),
                ("The Permanent Settlement of land revenue was introduced by ___.", ['Lord Wellesley', 'Lord Cornwallis', 'Lord Dalhousie', 'Warren Hastings'], 'b', 'easy', "1793, in Bengal."),
                ("The 'Purna Swaraj' resolution was adopted at the ___ session of the Congress.", ['Lucknow (1916)', 'Lahore (1929)', 'Karachi (1931)', 'Haripura (1938)'], 'b', 'easy', "Lahore, 1929, under Nehru."),
                ("The Buddhist council at Pataliputra was held during the reign of ___.", ['Ajatashatru', 'Ashoka', 'Kanishka', 'Kalasoka'], 'b', 'medium', "The Third Buddhist Council."),
                ("The Tropic of Cancer does NOT pass through ___.", ['Rajasthan', 'Odisha', 'Tripura', 'Jharkhand'], 'b', 'medium', "It crosses Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, West Bengal, Tripura and Mizoram."),
                ("Which is a cold desert in India?", ['Thar', 'Ladakh', 'Rann of Kutch', 'Deccan'], 'b', 'easy', "Ladakh."),
                ("The repo rate is the rate at which ___.", ['Commercial banks lend to the public', 'The RBI lends to commercial banks', 'Banks borrow from the public', 'The government borrows from the RBI'], 'b', 'easy', "A short-term loan against securities."),
                ("Which of these is a direct tax?", ['GST', 'Customs duty', 'Income tax', 'Excise duty'], 'c', 'easy', "Paid directly by the person it is levied on."),
                ("Which gases are mainly responsible for ozone layer depletion?", ['Carbon dioxide', 'Chlorofluorocarbons', 'Methane', 'Nitrogen'], 'b', 'easy', "CFCs release chlorine in the stratosphere."),
                ("The Chipko Movement is associated with ___.", ['Forest conservation', "Women's suffrage", 'Land reform', 'Anti-dam protests'], 'a', 'easy', "Villagers hugged trees to stop felling."),
                ("Which of these is a biodiversity hotspot in India?", ['Thar Desert', 'Western Ghats', 'Deccan Plateau', 'Gangetic Plain'], 'b', 'easy', "Western Ghats and Sri Lanka."),
                ("Who is known as the 'Father of the Indian Constitution'?", ['Jawaharlal Nehru', 'B. R. Ambedkar', 'Rajendra Prasad', 'Sardar Patel'], 'b', 'easy', "Chairman of the Drafting Committee."),
                ("Which Indian state has the longest coastline?", ['Tamil Nadu', 'Gujarat', 'Andhra Pradesh', 'Maharashtra'], 'b', 'easy', "Gujarat, about 1,600 km."),
            ]),
        ],
    },
]
