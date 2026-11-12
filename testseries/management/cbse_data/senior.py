# CBSE Classes 11-12 (NCERT). Tests are shared between streams where the paper is common (English, Economics, Maths).
# Each test: (subject code, title, description, [(question, [a, b, c, d], answer, difficulty, explanation)])

PHY_11 = ('PHY1', 'Physics – Mechanics & Thermodynamics', 'Units, kinematics, laws of motion, gravitation and heat.', [
    ("The SI unit of luminous intensity is ___.", ['Lumen', 'Candela', 'Lux', 'Watt'], 'b', 'medium', "Candela is one of the seven SI base units."),
    ("The dimensional formula of force is ___.", ['[MLT⁻¹]', '[MLT⁻²]', '[ML²T⁻²]', '[M⁰LT⁻²]'], 'b', 'easy', "F = ma → [M][LT⁻²]."),
    ("The slope of a velocity–time graph gives ___.", ['Displacement', 'Acceleration', 'Speed', 'Jerk'], 'b', 'easy', "a = dv/dt."),
    ("The horizontal range of a projectile is maximum at an angle of ___.", ['30°', '45°', '60°', '90°'], 'b', 'medium', "R = u² sin 2θ / g is largest when 2θ = 90°."),
    ("Newton's first law is also called the law of ___.", ['Momentum', 'Inertia', 'Action–reaction', 'Gravitation'], 'b', 'easy', "A body keeps its state unless a force acts."),
    ("Work done by a centripetal force in uniform circular motion is ___.", ['Maximum', 'Zero', 'Negative', 'Infinite'], 'b', 'hard', "Force is perpendicular to displacement."),
    ("Escape velocity from Earth's surface is about ___.", ['7.9 km/s', '11.2 km/s', '3 km/s', '25 km/s'], 'b', 'medium', "vₑ = √(2gR) ≈ 11.2 km/s."),
    ("The SI unit of Young's modulus is ___.", ['N', 'N/m²', 'N·m', 'J'], 'b', 'medium', "Stress/strain has units of stress (Pa)."),
    ("The first law of thermodynamics is a statement of ___.", ['Conservation of momentum', 'Conservation of energy', 'Increase of entropy', 'Conservation of mass'], 'b', 'medium', "ΔQ = ΔU + ΔW."),
    ("Time period of a simple pendulum is ___.", ['2π√(g/l)', '2π√(l/g)', '√(l/g)', '2πlg'], 'b', 'hard', "T = 2π√(l/g)."),
])

CHE_11 = ('CHE1', 'Chemistry – Basic Concepts to Organic', 'Mole concept, atomic structure, bonding, equilibrium and nomenclature.', [
    ("How many moles are there in 18 g of water?", ['0.5', '1', '2', '18'], 'b', 'easy', "Molar mass of H₂O = 18 g/mol."),
    ("Avogadro's number is ___.", ['6.022 × 10²³', '3 × 10⁸', '6.626 × 10⁻³⁴', '1.6 × 10⁻¹⁹'], 'a', 'easy', "Particles in one mole."),
    ("Maximum electrons in the shell n = 3 is ___.", ['8', '18', '32', '9'], 'b', 'medium', "2n² = 18."),
    ("The most electronegative element is ___.", ['Oxygen', 'Fluorine', 'Chlorine', 'Nitrogen'], 'b', 'easy', "Fluorine has the highest electronegativity."),
    ("The shape of a methane (CH₄) molecule is ___.", ['Linear', 'Tetrahedral', 'Trigonal planar', 'Bent'], 'b', 'medium', "sp³ carbon, bond angle 109.5°."),
    ("The hybridisation of carbon in ethyne (C₂H₂) is ___.", ['sp³', 'sp²', 'sp', 'dsp²'], 'c', 'medium', "A triple bond means sp hybridisation."),
    ("The pH of 0.01 M HCl is ___.", ['1', '2', '12', '0.01'], 'b', 'medium', "[H⁺] = 10⁻² → pH 2."),
    ("The oxidation number of Mn in KMnO₄ is ___.", ['+2', '+4', '+6', '+7'], 'd', 'hard', "+1 + x + 4(−2) = 0 → x = +7."),
    ("The IUPAC name of CH₃CH₂OH is ___.", ['Methanol', 'Ethanol', 'Ethanal', 'Propanol'], 'b', 'easy', "Two carbons + -ol."),
    ("The ideal gas equation is ___.", ['PV = RT/n', 'PV = nRT', 'P = nRTV', 'PV = n/RT'], 'b', 'easy', "PV = nRT."),
])

MAT_11 = ('MAT1', 'Mathematics – Class 11 Core', 'Sets, trigonometry, complex numbers, P&C, sequences, limits and conics.', [
    ("How many subsets does a set with 3 elements have?", ['3', '6', '8', '9'], 'c', 'easy', "2³ = 8."),
    ("sin 30° = ?", ['1', '1/2', '√3/2', '1/√2'], 'b', 'easy', "Standard value."),
    ("i² = ?", ['1', '−1', 'i', '0'], 'b', 'easy', "i = √−1."),
    ("⁵P₂ = ?", ['10', '20', '25', '60'], 'b', 'medium', "5 × 4 = 20."),
    ("⁶C₂ = ?", ['12', '15', '30', '36'], 'b', 'medium', "6 × 5 / 2 = 15."),
    ("The slope of the line y = 3x + 2 is ___.", ['2', '3', '−3', '1/3'], 'b', 'easy', "y = mx + c form."),
    ("Sum of the infinite GP 1 + 1/2 + 1/4 + … is ___.", ['1', '2', '∞', '3/2'], 'b', 'medium', "a/(1 − r) = 1/(1/2) = 2."),
    ("lim (x→0) sin x / x = ?", ['0', '1', '∞', 'Does not exist'], 'b', 'medium', "Standard limit."),
    ("d/dx (x³) = ?", ['x²', '3x²', '3x³', 'x⁴/4'], 'b', 'easy', "Power rule."),
    ("The radius of the circle x² + y² = 25 is ___.", ['25', '5', '√5', '12.5'], 'b', 'hard', "x² + y² = r²."),
])

BIO_11 = ('BIO1', 'Biology – Diversity, Cell & Physiology', 'Classification, cell biology, plant and human physiology.', [
    ("Who proposed the five-kingdom classification?", ['Linnaeus', 'R.H. Whittaker', 'Darwin', 'Haeckel'], 'b', 'medium', "Whittaker, 1969."),
    ("Who is called the 'Father of Taxonomy'?", ['Aristotle', 'Carolus Linnaeus', 'Mendel', 'Hooke'], 'b', 'easy', "Linnaeus gave binomial nomenclature."),
    ("Protein synthesis takes place on ___.", ['Lysosomes', 'Ribosomes', 'Golgi bodies', 'Vacuoles'], 'b', 'easy', "Ribosomes translate mRNA."),
    ("The fluid mosaic model of the membrane was given by ___.", ['Watson and Crick', 'Singer and Nicolson', 'Schleiden and Schwann', 'Robertson'], 'b', 'medium', "Singer and Nicolson, 1972."),
    ("The light reactions of photosynthesis occur in the ___.", ['Stroma', 'Thylakoids', 'Cytoplasm', 'Mitochondria'], 'b', 'medium', "In the grana thylakoid membranes."),
    ("Which is a C₄ plant?", ['Wheat', 'Maize', 'Rice', 'Pea'], 'b', 'hard', "Maize, sugarcane and sorghum are C₄."),
    ("The enzyme in saliva that digests starch is ___.", ['Pepsin', 'Salivary amylase', 'Trypsin', 'Lipase'], 'b', 'easy', "Also called ptyalin."),
    ("How many chambers does the human heart have?", ['2', '3', '4', '5'], 'c', 'easy', "Two atria and two ventricles."),
    ("Gametes are formed by ___.", ['Mitosis', 'Meiosis', 'Budding', 'Fission'], 'b', 'medium', "Meiosis halves the chromosome number."),
    ("Which hormone lowers blood glucose?", ['Glucagon', 'Insulin', 'Adrenaline', 'Thyroxine'], 'b', 'easy', "Insulin from β-cells of the pancreas."),
])

ENG_11 = ('ENG1', 'English – Hornbill & Snapshots', 'Authors, poets and language skills from the NCERT Class 11 books.', [
    ("Who wrote 'The Portrait of a Lady'?", ['R.K. Narayan', 'Khushwant Singh', 'Ruskin Bond', 'Mulk Raj Anand'], 'b', 'easy', "Khushwant Singh, about his grandmother."),
    ("In 'We're Not Afraid to Die', the family's boat was called ___.", ['Seagull', 'Wavewalker', 'Ocean Queen', 'Sea Breeze'], 'b', 'medium', "The Wavewalker."),
    ("Tutankhamun ('Discovering Tut') was a pharaoh of ___.", ['Greece', 'Egypt', 'Persia', 'Rome'], 'b', 'easy', "Ancient Egypt."),
    ("Who wrote 'The Summer of the Beautiful White Horse'?", ['O. Henry', 'William Saroyan', 'Mark Twain', 'Saki'], 'b', 'medium', "William Saroyan."),
    ("Who wrote the poem 'A Photograph'?", ['Shirley Toulson', 'Kamala Das', 'Pablo Neruda', 'John Updike'], 'a', 'medium', "Shirley Toulson."),
    ("Which word means the same as 'gregarious'?", ['Shy', 'Sociable', 'Angry', 'Greedy'], 'b', 'medium', "Gregarious means fond of company."),
    ("What is the opposite of 'frugal'?", ['Thrifty', 'Extravagant', 'Careful', 'Poor'], 'b', 'medium', "Frugal means economical."),
    ("Fill in: No sooner had I reached the station ___ the train left.", ['when', 'than', 'then', 'that'], 'b', 'hard', "'No sooner … than' is fixed."),
    ("Who wrote 'The Browning Version'?", ['Terence Rattigan', 'J.B. Priestley', 'Bernard Shaw', 'Oscar Wilde'], 'a', 'medium', "Terence Rattigan."),
    ("Who wrote the play 'Mother's Day'?", ['J.B. Priestley', 'Arthur Miller', 'Anton Chekhov', 'Rattigan'], 'a', 'hard', "J.B. Priestley."),
])

ACC_11 = ('ACC1', 'Accountancy – Financial Accounting I', 'Accounting equation, journal, ledger, trial balance and depreciation.', [
    ("The accounting equation is ___.", ['Assets = Liabilities − Capital', 'Assets = Liabilities + Capital', 'Capital = Assets + Liabilities', 'Liabilities = Assets + Capital'], 'b', 'easy', "A = L + C."),
    ("Goods taken by the owner for personal use are called ___.", ['Sales', 'Drawings', 'Purchases', 'Capital'], 'b', 'easy', "Drawings reduce capital."),
    ("The book of original entry is the ___.", ['Ledger', 'Journal', 'Trial balance', 'Balance sheet'], 'b', 'easy', "Transactions are first recorded in the journal."),
    ("A trial balance checks the ___ of the books.", ['Profit', 'Arithmetical accuracy', 'Cash position', 'Legal validity'], 'b', 'medium', "It checks that debits equal credits."),
    ("Under the Straight Line Method, depreciation is ___ every year.", ['Increasing', 'A fixed amount', 'Decreasing', 'Zero'], 'b', 'medium', "Same amount on original cost."),
    ("Rent paid is debited to which type of account?", ['Real', 'Personal', 'Nominal', 'Suspense'], 'c', 'medium', "Expenses are nominal accounts."),
    ("The rule for a real account is ___.", ['Debit the receiver, credit the giver', 'Debit what comes in, credit what goes out', 'Debit expenses, credit incomes', 'Debit the giver'], 'b', 'medium', "Golden rule for real accounts."),
    ("A Bank Reconciliation Statement is prepared by the ___.", ['Bank', 'Account holder', 'RBI', 'Auditor only'], 'b', 'hard', "The business reconciles its cash book with the passbook."),
    ("Purchase of machinery is a ___.", ['Revenue expenditure', 'Capital expenditure', 'Deferred revenue', 'Drawing'], 'b', 'medium', "It gives long-term benefit."),
    ("Bad debts are a ___ for the business.", ['Gain', 'Loss', 'Liability', 'Asset'], 'b', 'easy', "Amounts that cannot be recovered."),
])

BST_11 = ('BST1', 'Business Studies – Forms & Environment', 'Business organisations, companies, services and social responsibility.', [
    ("The liability of a sole proprietor is ___.", ['Limited', 'Unlimited', 'Nil', 'Shared'], 'b', 'easy', "Personal assets can be used to pay debts."),
    ("Minimum members needed to form a private company is ___.", ['1', '2', '7', '50'], 'b', 'medium', "Two (one for an OPC)."),
    ("Maximum partners allowed in a partnership firm is ___.", ['10', '20', '50', '100'], 'c', 'hard', "50 under the Companies Rules, 2014."),
    ("Business risk arises mainly due to ___.", ['Profits', 'Uncertainties', 'Taxes only', 'Advertising'], 'b', 'easy', "Future events are uncertain."),
    ("Which is an auxiliary to trade?", ['Mining', 'Banking', 'Farming', 'Manufacturing'], 'b', 'medium', "Banking supports trade."),
    ("A Joint Hindu Family business is managed by the ___.", ['Partner', 'Karta', 'Director', 'Coparcener'], 'b', 'medium', "The eldest member, the Karta."),
    ("Which is an example of e-business?", ['Door-to-door sales', 'Online shopping', 'Weekly market', 'Hawking'], 'b', 'easy', "Buying and selling over the internet."),
    ("A public sector enterprise is owned by the ___.", ['Shareholders', 'Government', 'Partners', 'Foreign firms'], 'b', 'easy', "Government holds the majority."),
    ("Which document defines a company's relation with outsiders?", ['Articles of Association', 'Memorandum of Association', 'Prospectus', 'Certificate of Incorporation'], 'b', 'hard', "The MoA is the company's charter."),
    ("Debenture holders are the company's ___.", ['Owners', 'Creditors', 'Directors', 'Employees'], 'b', 'medium', "They lend money to the company."),
])

ECO_11 = ('ECO1', 'Economics – Statistics & Microeconomics', 'Data, central tendency, demand, markets and Indian economic development.', [
    ("The mean of 10, 20 and 30 is ___.", ['15', '20', '25', '60'], 'b', 'easy', "60 ÷ 3 = 20."),
    ("The median of 3, 7, 9, 11, 15 is ___.", ['7', '9', '11', '9.5'], 'b', 'easy', "The middle value."),
    ("The law of demand shows a ___ relation between price and quantity demanded.", ['Direct', 'Inverse', 'Constant', 'No'], 'b', 'easy', "Price up, demand down."),
    ("A market with a single seller is called ___.", ['Oligopoly', 'Monopoly', 'Perfect competition', 'Duopoly'], 'b', 'easy', "Mono = one."),
    ("In 2015 the Planning Commission was replaced by ___.", ['Finance Commission', 'NITI Aayog', 'RBI', 'SEBI'], 'b', 'medium', "NITI Aayog, January 2015."),
    ("The 1991 economic reforms are known as ___.", ['LPG', 'GST', 'MSP', 'PDS'], 'a', 'medium', "Liberalisation, Privatisation, Globalisation."),
    ("Opportunity cost is the value of the ___.", ['Total cost', 'Next best alternative forgone', 'Fixed cost', 'Money spent'], 'b', 'medium', "What you give up by choosing."),
    ("Total utility is maximum when marginal utility is ___.", ['Maximum', 'Zero', 'Negative', 'Equal to price'], 'b', 'hard', "TU stops rising when MU = 0."),
    ("A production function shows the relation between ___.", ['Price and demand', 'Inputs and output', 'Cost and revenue', 'Income and saving'], 'b', 'medium', "Q = f(L, K)."),
    ("Data collected first-hand by the investigator is ___ data.", ['Secondary', 'Primary', 'Census', 'Sample'], 'b', 'easy', "Primary data is original."),
])

HIS_11 = ('HIS1', 'History – Themes in World History', 'Early societies, empires, the Mongols, Renaissance and industrialisation.', [
    ("Writing first developed in ___.", ['Egypt', 'Mesopotamia', 'China', 'India'], 'b', 'medium', "Around 3200 BCE in Mesopotamia."),
    ("Cuneiform script was used in ___.", ['Rome', 'Mesopotamia', 'Greece', 'Persia only'], 'b', 'medium', "Wedge-shaped signs on clay tablets."),
    ("Who was the first Roman emperor?", ['Julius Caesar', 'Augustus', 'Nero', 'Constantine'], 'b', 'medium', "Augustus, 27 BCE."),
    ("Genghis Khan was the leader of the ___.", ['Turks', 'Mongols', 'Huns', 'Persians'], 'b', 'easy', "He united the Mongol tribes."),
    ("The Renaissance began in ___.", ['France', 'Italy', 'England', 'Spain'], 'b', 'easy', "In Italian city-states like Florence."),
    ("The Industrial Revolution began in ___.", ['Germany', 'Britain', 'USA', 'France'], 'b', 'easy', "Britain, from the 1780s."),
    ("The earliest human fossils have been found in ___.", ['Asia', 'Africa', 'Europe', 'Australia'], 'b', 'medium', "East Africa."),
    ("Who invented the movable-type printing press in Europe?", ['Caxton', 'Gutenberg', 'Galileo', 'Columbus'], 'b', 'medium', "Johannes Gutenberg, c. 1450."),
    ("The Inca empire was located in ___.", ['North America', 'South America', 'Africa', 'Asia'], 'b', 'hard', "Centred in Peru."),
    ("Islam began in ___.", ['Persia', 'Arabia', 'Egypt', 'Turkey'], 'b', 'easy', "Mecca, Arabia, 7th century."),
])

POL_11 = ('POL1', 'Political Science – Constitution at Work', 'Constituent Assembly, rights, executive, legislature and local government.', [
    ("The Constituent Assembly first met on ___.", ['15 August 1947', '9 December 1946', '26 January 1950', '26 November 1949'], 'b', 'medium', "9 December 1946."),
    ("'Socialist' and 'Secular' were added to the Preamble by the ___ Amendment.", ['24th', '42nd', '44th', '73rd'], 'b', 'hard', "42nd Amendment, 1976."),
    ("The Right to Constitutional Remedies is in Article ___.", ['14', '21', '32', '370'], 'c', 'medium', "Article 32."),
    ("The President of India is elected by ___.", ['The people directly', 'An electoral college', 'The Prime Minister', 'Lok Sabha only'], 'b', 'medium', "Elected MPs and MLAs."),
    ("Maximum strength of the Rajya Sabha is ___.", ['245', '250', '545', '552'], 'b', 'hard', "Up to 250 members."),
    ("The Chief Justice of India is appointed by the ___.", ['Prime Minister', 'President', 'Parliament', 'Law Minister'], 'b', 'easy', "The President appoints judges."),
    ("Panchayati Raj got constitutional status through the ___ Amendment.", ['42nd', '61st', '73rd', '86th'], 'c', 'medium', "73rd Amendment, 1992."),
    ("Elections in India are conducted by the ___.", ['Supreme Court', 'Election Commission', 'Parliament', 'President'], 'b', 'easy', "An independent constitutional body."),
    ("Directive Principles were borrowed from the constitution of ___.", ['USA', 'Ireland', 'UK', 'Canada'], 'b', 'medium', "Ireland."),
    ("Fundamental Duties are in Part ___ of the Constitution.", ['III', 'IV', 'IV-A', 'V'], 'c', 'hard', "Part IV-A, Article 51A."),
])

GEO_11 = ('GEO1', 'Geography – Physical Geography & India', 'Earth, interior, atmosphere and the physical geography of India.', [
    ("The approximate age of the Earth is ___.", ['4.6 million years', '4.6 billion years', '13.8 billion years', '460 million years'], 'b', 'medium', "About 4.6 billion years."),
    ("The ozone layer lies in the ___.", ['Troposphere', 'Stratosphere', 'Mesosphere', 'Thermosphere'], 'b', 'easy', "Stratosphere."),
    ("Earthquakes are recorded by a ___.", ['Barometer', 'Seismograph', 'Hygrometer', 'Anemometer'], 'b', 'easy', "Seismograph."),
    ("The largest lithospheric plate is the ___.", ['Eurasian', 'Pacific', 'African', 'Indian'], 'b', 'medium', "Pacific Plate."),
    ("India lies in the ___ hemispheres.", ['Northern and Western', 'Northern and Eastern', 'Southern and Eastern', 'Southern and Western'], 'b', 'easy', "North of the Equator, east of Greenwich."),
    ("Which state has the longest coastline in India?", ['Tamil Nadu', 'Gujarat', 'Andhra Pradesh', 'Kerala'], 'b', 'medium', "Gujarat."),
    ("India's climate is broadly described as ___.", ['Mediterranean', 'Tropical monsoon', 'Equatorial', 'Polar'], 'b', 'easy', "Monsoon type."),
    ("The highest peak of the Western Ghats is ___.", ['Doddabetta', 'Anamudi', 'Mahendragiri', 'Kalsubai'], 'b', 'hard', "Anamudi, 2,695 m, Kerala."),
    ("Sambhar, a saline lake, is in ___.", ['Gujarat', 'Rajasthan', 'Odisha', 'Ladakh'], 'b', 'medium', "Rajasthan."),
    ("The Himalayas are an example of ___ mountains.", ['Block', 'Fold', 'Volcanic', 'Residual'], 'b', 'easy', "Young fold mountains."),
])

PHY_12 = ('PHY1', 'Physics – Electricity, Optics & Modern Physics', 'Electrostatics, current, magnetism, EMI, optics and semiconductors.', [
    ("The SI unit of electric charge is ___.", ['Ampere', 'Coulomb', 'Volt', 'Ohm'], 'b', 'easy', "Coulomb."),
    ("By Coulomb's law, force between charges varies as ___.", ['r', '1/r', '1/r²', 'r²'], 'c', 'easy', "Inverse square law."),
    ("The electric field inside a charged conductor is ___.", ['Maximum', 'Zero', 'Infinite', 'Uniform but non-zero'], 'b', 'medium', "Charges reside on the surface."),
    ("The SI unit of capacitance is ___.", ['Henry', 'Farad', 'Tesla', 'Weber'], 'b', 'easy', "Farad."),
    ("Lenz's law follows from conservation of ___.", ['Charge', 'Energy', 'Momentum', 'Mass'], 'b', 'medium', "Induced current opposes the change."),
    ("The unit of power of a lens is ___.", ['Metre', 'Dioptre', 'Watt', 'Lux'], 'b', 'easy', "P = 1/f (in metres)."),
    ("The photoelectric effect was explained by ___.", ['Newton', 'Einstein', 'Bohr', 'Maxwell'], 'b', 'medium', "Einstein, 1905."),
    ("A semiconductor doped with a pentavalent impurity is ___.", ['p-type', 'n-type', 'Intrinsic', 'Insulator'], 'b', 'hard', "Extra electrons → n-type."),
    ("Speed of electromagnetic waves in vacuum is ___.", ['3 × 10⁶ m/s', '3 × 10⁸ m/s', '343 m/s', '3 × 10¹⁰ m/s'], 'b', 'easy', "c = 3 × 10⁸ m/s."),
    ("The SI unit of magnetic field is ___.", ['Weber', 'Tesla', 'Gauss', 'Henry'], 'b', 'medium', "Tesla."),
])

CHE_12 = ('CHE1', 'Chemistry – Physical, Inorganic & Organic', 'Solutions, electrochemistry, kinetics, d-block, organic and biomolecules.', [
    ("Which is a colligative property?", ['Density', 'Osmotic pressure', 'Viscosity', 'Colour'], 'b', 'easy', "Depends on number of solute particles."),
    ("Half-life of a first-order reaction is independent of ___.", ['Rate constant', 'Initial concentration', 'Temperature', 'Catalyst'], 'b', 'medium', "t½ = 0.693/k."),
    ("The electrolyte in a lead storage battery is ___.", ['HCl', 'H₂SO₄', 'NaOH', 'HNO₃'], 'b', 'medium', "Dilute sulphuric acid."),
    ("Which element has the configuration [Ar] 3d¹⁰ 4s¹?", ['Zinc', 'Copper', 'Nickel', 'Iron'], 'b', 'hard', "Copper (exception to filling order)."),
    ("Benzene with Cl₂ in the presence of FeCl₃ gives ___.", ['Benzoic acid', 'Chlorobenzene', 'Phenol', 'Toluene'], 'b', 'medium', "Electrophilic substitution."),
    ("Aldehydes give a silver mirror with ___.", ["Fehling's solution", "Tollens' reagent", 'Lucas reagent', 'Iodoform'], 'b', 'medium', "Ag⁺ is reduced to silver."),
    ("The molecular formula of glucose is ___.", ['C₁₂H₂₂O₁₁', 'C₆H₁₂O₆', 'C₆H₁₀O₅', 'C₅H₁₀O₅'], 'b', 'easy', "C₆H₁₂O₆."),
    ("Nylon-6,6 is a ___.", ['Polyester', 'Polyamide', 'Polyolefin', 'Natural rubber'], 'b', 'medium', "Amide links between monomers."),
    ("Which test identifies primary amines?", ['Biuret test', 'Carbylamine test', 'Iodoform test', 'Molisch test'], 'b', 'hard', "Gives a foul-smelling isocyanide."),
    ("The SI unit of molar conductivity is ___.", ['S cm⁻¹', 'S m² mol⁻¹', 'Ω m', 'mol L⁻¹'], 'b', 'hard', "Λm = κ/c."),
])

MAT_12 = ('MAT1', 'Mathematics – Class 12 Core', 'Matrices, determinants, calculus, differential equations, vectors and probability.', [
    ("A matrix with 2 rows and 3 columns has order ___.", ['3 × 2', '2 × 3', '6', '5'], 'b', 'easy', "Rows × columns."),
    ("The determinant of [[2, 3], [1, 4]] is ___.", ['5', '11', '8', '−5'], 'a', 'easy', "2×4 − 3×1 = 5."),
    ("d/dx (sin x) = ?", ['−cos x', 'cos x', 'sin x', 'tan x'], 'b', 'easy', "Standard derivative."),
    ("∫ (1/x) dx = ?", ['x²/2 + C', 'log|x| + C', '−1/x² + C', 'eˣ + C'], 'b', 'easy', "Standard integral."),
    ("∫₀¹ x dx = ?", ['1', '1/2', '0', '2'], 'b', 'medium', "[x²/2] from 0 to 1."),
    ("d/dx (eˣ) = ?", ['xeˣ⁻¹', 'eˣ', 'log x', '1/x'], 'b', 'easy', "eˣ is its own derivative."),
    ("The order of d²y/dx² + y = 0 is ___.", ['0', '1', '2', '3'], 'c', 'medium', "Highest derivative is second order."),
    ("The dot product of two perpendicular vectors is ___.", ['1', '0', '−1', 'Their product'], 'b', 'medium', "cos 90° = 0."),
    ("For independent events, P(A ∩ B) = ___.", ['P(A) + P(B)', 'P(A) × P(B)', 'P(A) − P(B)', 'P(A)/P(B)'], 'b', 'medium', "Multiplication rule."),
    ("f(x) = x² from R to R is ___.", ['One-one', 'Not one-one', 'Onto', 'Bijective'], 'b', 'hard', "f(2) = f(−2)."),
])

BIO_12 = ('BIO1', 'Biology – Genetics, Reproduction & Ecology', 'Reproduction, inheritance, molecular biology, biotechnology and ecology.', [
    ("The double-helix model of DNA was proposed by ___.", ['Mendel', 'Watson and Crick', 'Darwin', 'Griffith'], 'b', 'easy', "1953."),
    ("The number of chromosomes in a human body cell is ___.", ['23', '44', '46', '48'], 'c', 'easy', "23 pairs."),
    ("The sex of a human child is determined by the ___.", ["Mother's X chromosome", "Father's X or Y chromosome", 'Diet', 'Temperature'], 'b', 'medium', "Sperm carries X or Y."),
    ("Restriction enzymes cut ___.", ['Proteins', 'DNA', 'Lipids', 'RNA only'], 'b', 'medium', "At specific sequences."),
    ("The first vaccine (against smallpox) was developed by ___.", ['Pasteur', 'Edward Jenner', 'Fleming', 'Koch'], 'b', 'medium', "1796."),
    ("The lac operon was described in ___.", ['Yeast', 'E. coli', 'Humans', 'Pea plant'], 'b', 'hard', "Jacob and Monod."),
    ("The pyramid of energy is always ___.", ['Inverted', 'Upright', 'Spindle-shaped', 'Irregular'], 'b', 'medium', "Energy decreases at each level."),
    ("The toxin in Bt cotton comes from ___.", ['Agrobacterium', 'Bacillus thuringiensis', 'E. coli', 'Rhizobium'], 'b', 'medium', "Cry proteins."),
    ("Implantation of the embryo occurs in the ___.", ['Ovary', 'Uterus', 'Fallopian tube', 'Cervix'], 'b', 'easy', "In the uterine wall."),
    ("AIDS is caused by ___.", ['A bacterium', 'HIV', 'A fungus', 'A protozoan'], 'b', 'easy', "Human Immunodeficiency Virus."),
])

ENG_12 = ('ENG1', 'English – Flamingo & Vistas', 'Board-pattern authors, poets and vocabulary from the NCERT Class 12 books.', [
    ("Who wrote 'The Last Lesson'?", ['Anees Jung', 'Alphonse Daudet', 'Selma Lagerlöf', 'Pearl S. Buck'], 'b', 'easy', "Alphonse Daudet."),
    ("Who wrote 'Lost Spring'?", ['Anees Jung', 'Kamala Das', 'Louis Fischer', 'A.R. Barton'], 'a', 'easy', "Anees Jung."),
    ("Who wrote 'My Mother at Sixty-six'?", ['Kamala Das', 'Adrienne Rich', 'Pablo Neruda', 'Stephen Spender'], 'a', 'easy', "Kamala Das."),
    ("Who wrote 'The Rattrap'?", ['Selma Lagerlöf', 'Asokamitran', 'Jack Finney', 'Kalki'], 'a', 'medium', "Selma Lagerlöf."),
    ("'Indigo' describes Gandhi's work at ___.", ['Dandi', 'Champaran', 'Kheda', 'Sabarmati'], 'b', 'medium', "Champaran, 1917."),
    ("Who wrote the poem 'Keeping Quiet'?", ['John Keats', 'Pablo Neruda', 'Robert Frost', 'Kamala Das'], 'b', 'easy', "Pablo Neruda."),
    ("Who wrote 'The Enemy'?", ['Pearl S. Buck', 'Jack Finney', 'Susan Sontag', 'Tishani Doshi'], 'a', 'medium', "Pearl S. Buck."),
    ("Which word means the same as 'ambiguous'?", ['Clear', 'Unclear', 'Certain', 'Simple'], 'b', 'medium', "Open to more than one meaning."),
    ("Who wrote 'Aunt Jennifer's Tigers'?", ['Adrienne Rich', 'Kamala Das', 'Shirley Toulson', 'Sylvia Plath'], 'a', 'medium', "Adrienne Rich."),
    ("Who wrote 'Deep Water'?", ['William Douglas', 'Louis Fischer', 'William Saroyan', 'Ernest Hemingway'], 'a', 'hard', "William O. Douglas."),
])

ACC_12 = ('ACC1', 'Accountancy – Partnership & Company Accounts', 'Partnership, goodwill, shares, ratios and cash flow.', [
    ("Goodwill is an ___ asset.", ['Tangible', 'Intangible', 'Current', 'Fictitious'], 'b', 'easy', "It has no physical form."),
    ("Without a partnership deed, profits are shared ___.", ['In capital ratio', 'Equally', 'As per seniority', 'Not at all'], 'b', 'easy', "Indian Partnership Act, 1932."),
    ("Without a deed, interest on capital is ___.", ['6% p.a.', 'Not allowed', '12% p.a.', 'At bank rate'], 'b', 'medium', "No interest on capital."),
    ("Without a deed, interest on a partner's loan is ___.", ['Not allowed', '6% p.a.', '9% p.a.', '12% p.a.'], 'b', 'medium', "6% per annum."),
    ("Shares issued above face value are issued at a ___.", ['Discount', 'Premium', 'Par', 'Loss'], 'b', 'easy', "The extra is securities premium."),
    ("Securities premium can be used to ___.", ['Pay dividends', 'Issue fully paid bonus shares', 'Pay salaries', 'Buy stock'], 'b', 'hard', "As per Section 52."),
    ("Current ratio = ___", ['Current assets ÷ Current liabilities', 'Liquid assets ÷ Current liabilities', 'Debt ÷ Equity', 'Sales ÷ Assets'], 'a', 'medium', "Ideal is 2 : 1."),
    ("A cash flow statement is prepared as per ___.", ['AS-1', 'AS-3', 'AS-6', 'AS-26'], 'b', 'hard', "AS-3 (Ind AS 7)."),
    ("Sacrificing ratio = ___", ['New ratio − Old ratio', 'Old ratio − New ratio', 'Old ratio + New ratio', 'Gaining ratio'], 'b', 'medium', "What old partners give up."),
    ("After reissue, the balance of Forfeited Shares A/c goes to ___.", ['General Reserve', 'Capital Reserve', 'Profit & Loss A/c', 'Share Capital'], 'b', 'hard', "It is a capital profit."),
])

BST_12 = ('BST1', 'Business Studies – Management & Finance', 'Principles, functions of management, marketing and financial markets.', [
    ("Which function of management comes first?", ['Organising', 'Planning', 'Staffing', 'Controlling'], 'b', 'easy', "Planning is the primary function."),
    ("How many principles of management did Henri Fayol give?", ['10', '12', '14', '16'], 'c', 'medium', "14 principles."),
    ("The 'Father of Scientific Management' is ___.", ['Henri Fayol', 'F.W. Taylor', 'Peter Drucker', 'Maslow'], 'b', 'easy', "Frederick Winslow Taylor."),
    ("The highest need in Maslow's hierarchy is ___.", ['Safety', 'Esteem', 'Self-actualisation', 'Belonging'], 'c', 'medium', "Reaching one's full potential."),
    ("Span of management relates to ___.", ['Planning', 'Organising', 'Directing', 'Controlling'], 'b', 'hard', "Number of subordinates under a manager."),
    ("The 4 Ps of marketing are product, price, place and ___.", ['People', 'Promotion', 'Profit', 'Packaging'], 'b', 'easy', "The marketing mix."),
    ("The current Consumer Protection Act was passed in ___.", ['1986', '2005', '2019', '2020'], 'c', 'medium', "Consumer Protection Act, 2019."),
    ("SEBI got statutory powers in ___.", ['1988', '1992', '2000', '1956'], 'b', 'hard', "SEBI Act, 1992."),
    ("The capital market deals in ___ funds.", ['Short-term', 'Long-term', 'Overnight', 'Foreign only'], 'b', 'medium', "Shares and debentures."),
    ("Recruitment is part of which function?", ['Planning', 'Staffing', 'Controlling', 'Directing'], 'b', 'easy', "Staffing."),
])

ECO_12 = ('ECO1', 'Economics – Macroeconomics', 'National income, money and banking, budget, BoP and income determination.', [
    ("GDP measures the value of final goods and services produced ___.", ['By citizens abroad', 'Within the domestic territory', 'Only by government', 'Including intermediate goods'], 'b', 'medium', "Domestic territory, one year."),
    ("The central bank of India is the ___.", ['SBI', 'RBI', 'NABARD', 'SEBI'], 'b', 'easy', "Reserve Bank of India."),
    ("Repo rate is the rate at which ___.", ['Banks lend to people', 'RBI lends to commercial banks', 'Banks deposit with RBI', 'Government borrows abroad'], 'b', 'medium', "Short-term lending by RBI."),
    ("The Union Budget is presented under Article ___.", ['110', '112', '280', '356'], 'b', 'hard', "Annual Financial Statement."),
    ("Fiscal deficit = total expenditure − ___.", ['Revenue receipts', 'Total receipts excluding borrowings', 'Capital receipts', 'Tax receipts'], 'b', 'hard', "It equals government borrowing."),
    ("Balance of Payments records transactions ___.", ['Within the country', 'With the rest of the world', 'Of the government only', 'Of banks only'], 'b', 'easy', "Between residents and non-residents."),
    ("MPC + MPS = ___", ['0', '1', 'Income', 'Investment'], 'b', 'medium', "Extra income is either consumed or saved."),
    ("Firms under perfect competition are price ___.", ['Makers', 'Takers', 'Leaders', 'Setters'], 'b', 'medium', "Price is set by the market."),
    ("A normal demand curve slopes ___.", ['Upward', 'Downward', 'Vertically', 'Horizontally'], 'b', 'easy', "Law of demand."),
    ("The investment multiplier = ___", ['1/MPC', '1/(1 − MPC)', 'MPC/MPS', '1 − MPC'], 'b', 'medium', "k = 1/MPS."),
])

HIS_12 = ('HIS1', 'History – Themes in Indian History', 'Harappa, inscriptions, Mughals, Vijayanagara, colonialism and the Constitution.', [
    ("The Harappan site with a dockyard is ___.", ['Harappa', 'Lothal', 'Kalibangan', 'Banawali'], 'b', 'medium', "Lothal, Gujarat."),
    ("Who deciphered the Brahmi script?", ['Alexander Cunningham', 'James Prinsep', 'John Marshall', 'Max Müller'], 'b', 'medium', "James Prinsep, 1838."),
    ("The critical edition of the Mahabharata was led by ___.", ['V.S. Sukthankar', 'R.G. Bhandarkar', 'D.D. Kosambi', 'Romila Thapar'], 'a', 'hard', "V.S. Sukthankar, from 1919."),
    ("Who wrote the Ain-i-Akbari?", ['Badauni', 'Abul Fazl', 'Birbal', 'Faizi'], 'b', 'easy', "Part of the Akbarnama."),
    ("The capital of the Vijayanagara empire was at ___.", ['Hampi', 'Mysore', 'Madurai', 'Bijapur'], 'a', 'easy', "Hampi, Karnataka."),
    ("Ibn Battuta came from ___.", ['Persia', 'Morocco', 'Turkey', 'Egypt'], 'b', 'medium', "Tangier, Morocco."),
    ("The Permanent Settlement (1793) was introduced by ___.", ['Warren Hastings', 'Lord Cornwallis', 'Lord Dalhousie', 'Lord Wellesley'], 'b', 'medium', "In Bengal."),
    ("The Constituent Assembly adopted the Constitution on ___.", ['26 January 1950', '26 November 1949', '15 August 1947', '9 December 1946'], 'b', 'medium', "Constitution Day."),
    ("The Sufi shrine at Ajmer is of ___.", ['Nizamuddin Auliya', 'Khwaja Muinuddin Chishti', 'Salim Chishti', 'Baba Farid'], 'b', 'easy', "Khwaja Muinuddin Chishti."),
    ("After 1857, Bahadur Shah Zafar was exiled to ___.", ['Andaman', 'Rangoon', 'Ceylon', 'London'], 'b', 'medium', "Rangoon (Yangon)."),
])

POL_12 = ('POL1', 'Political Science – World & Indian Politics', 'Cold War, NAM, UN, regional bodies and politics in India since independence.', [
    ("The Cold War was between ___.", ['USA and China', 'USA and USSR', 'UK and Germany', 'India and Pakistan'], 'b', 'easy', "1945–1991."),
    ("The first NAM summit was held in 1961 at ___.", ['New Delhi', 'Belgrade', 'Cairo', 'Jakarta'], 'b', 'medium', "Belgrade, Yugoslavia."),
    ("The United Nations was founded in ___.", ['1919', '1945', '1950', '1961'], 'b', 'easy', "24 October 1945."),
    ("The SAARC Secretariat is at ___.", ['New Delhi', 'Kathmandu', 'Dhaka', 'Colombo'], 'b', 'medium', "Kathmandu."),
    ("India's first general elections were held in ___.", ['1947', '1951–52', '1957', '1962'], 'b', 'medium', "1951–52."),
    ("The national Emergency was declared in ___.", ['1971', '1975', '1977', '1984'], 'b', 'easy', "25 June 1975."),
    ("The currency of the European Union is the ___.", ['Pound', 'Euro', 'Franc', 'Mark'], 'b', 'easy', "Euro."),
    ("The Kyoto Protocol deals with ___.", ['Nuclear weapons', 'Climate change', 'Trade', 'Human rights'], 'b', 'medium', "Greenhouse gas reduction."),
    ("The Mandal Commission dealt with reservation for ___.", ['SCs', 'OBCs', 'Women', 'Minorities'], 'b', 'medium', "Other Backward Classes."),
    ("Early one-party dominance in India is called the ___.", ['Coalition era', 'Congress system', 'Two-party system', 'Janata wave'], 'b', 'hard', "Rajni Kothari's term."),
])

GEO_12 = ('GEO1', 'Geography – Human Geography & India', 'Population, agriculture, resources, transport and trade.', [
    ("Population density is the number of people per ___.", ['Household', 'Square kilometre', 'Village', 'Family'], 'b', 'easy', "Persons per sq km."),
    ("The most populous state of India is ___.", ['Maharashtra', 'Uttar Pradesh', 'Bihar', 'West Bengal'], 'b', 'easy', "Uttar Pradesh."),
    ("In India, sex ratio means females per ___ males.", ['100', '1,000', '10,000', '500'], 'b', 'medium', "Per 1,000 males."),
    ("The largest rice-producing state of India is usually ___.", ['Punjab', 'West Bengal', 'Kerala', 'Rajasthan'], 'b', 'medium', "West Bengal."),
    ("The Golden Quadrilateral connects ___.", ['Delhi, Mumbai, Chennai, Kolkata', 'Delhi, Jaipur, Agra, Lucknow', 'Mumbai, Pune, Goa, Bengaluru', 'Kolkata, Patna, Guwahati, Delhi'], 'a', 'medium', "The four metro cities."),
    ("The Konkan Railway runs along the ___ coast.", ['Eastern', 'Western', 'Northern', 'Southern'], 'b', 'medium', "Maharashtra, Goa, Karnataka."),
    ("The Suez Canal links the Mediterranean Sea with the ___.", ['Arabian Sea', 'Red Sea', 'Black Sea', 'Caspian Sea'], 'b', 'medium', "Through Egypt."),
    ("The Bhakra Nangal dam is on the river ___.", ['Beas', 'Sutlej', 'Ravi', 'Chenab'], 'b', 'hard', "Sutlej."),
    ("The leading iron-ore producing state of India is ___.", ['Jharkhand', 'Odisha', 'Goa', 'Karnataka'], 'b', 'hard', "Odisha."),
    ("The Trans-Siberian Railway is in ___.", ['Canada', 'Russia', 'China', 'USA'], 'b', 'easy', "Russia."),
])

# grade -> stream -> tests
STREAMS = {
    11: {
        'Science': [PHY_11, CHE_11, MAT_11, BIO_11, ENG_11],
        'Commerce': [ACC_11, BST_11, ECO_11, MAT_11, ENG_11],
        'Arts': [HIS_11, POL_11, GEO_11, ECO_11, ENG_11],
    },
    12: {
        'Science': [PHY_12, CHE_12, MAT_12, BIO_12, ENG_12],
        'Commerce': [ACC_12, BST_12, ECO_12, MAT_12, ENG_12],
        'Arts': [HIS_12, POL_12, GEO_12, ECO_12, ENG_12],
    },
}
