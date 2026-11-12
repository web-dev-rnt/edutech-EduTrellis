"""Professional and specialist topics: medicine, nursing, dentistry, commerce, law, teaching, engineering core subjects,
Hindi grammar and primary EVS. Fact tables plus hand-written questions; accounting and engineering numericals are computed."""
from fractions import Fraction as F

from .core import fmt, generator, inr, mcq, near, register, table_topics


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


# ================================================================== Medicine (NEET PG, FMGE, CMS)
MED = 'MED1'
DRUG_CLASS = rows("""
Metformin|Biguanide (oral antidiabetic)
Glibenclamide|Sulfonylurea
Atenolol|Selective β1-blocker
Propranolol|Non-selective β-blocker
Amlodipine|Calcium channel blocker
Enalapril|ACE inhibitor
Losartan|Angiotensin II receptor blocker
Furosemide|Loop diuretic
Hydrochlorothiazide|Thiazide diuretic
Spironolactone|Aldosterone antagonist (potassium-sparing diuretic)
Atorvastatin|HMG-CoA reductase inhibitor
Warfarin|Vitamin K antagonist (oral anticoagulant)
Heparin|Indirect thrombin inhibitor (via antithrombin III)
Aspirin|Irreversible COX inhibitor
Omeprazole|Proton pump inhibitor
Ranitidine|H2-receptor antagonist
Ondansetron|5-HT3 antagonist (antiemetic)
Salbutamol|β2-agonist (bronchodilator)
Diazepam|Benzodiazepine
Fluoxetine|Selective serotonin reuptake inhibitor
Haloperidol|Typical antipsychotic (D2 blocker)
Levodopa|Dopamine precursor
Phenytoin|Sodium channel blocker (antiepileptic)
Morphine|Opioid agonist
Naloxone|Opioid antagonist
Atropine|Muscarinic antagonist
Neostigmine|Reversible cholinesterase inhibitor
Amoxicillin|Penicillin (β-lactam antibiotic)
Ciprofloxacin|Fluoroquinolone
Azithromycin|Macrolide
Doxycycline|Tetracycline
Vancomycin|Glycopeptide antibiotic
Isoniazid|First-line anti-tubercular drug
Fluconazole|Azole antifungal
Acyclovir|Antiviral (guanosine analogue)
Methotrexate|Folate antagonist
Prednisolone|Glucocorticoid
Levothyroxine|Thyroid hormone (T4)
Allopurinol|Xanthine oxidase inhibitor
Sildenafil|PDE-5 inhibitor
""")
table_topics('medicine.pharmacology', MED, 'Pharmacology – Drug Classes', DRUG_CLASS, [
    ("{a} belongs to which class of drugs?", 'b', "{a}: {b}."),
    ("Which of these drugs is a {b}?", 'a', "{a}: {b}."),
])

ANTIDOTES = rows("""
Paracetamol poisoning|N-acetylcysteine
Organophosphate poisoning|Atropine (with pralidoxime)
Opioid overdose|Naloxone
Benzodiazepine overdose|Flumazenil
Heparin overdose|Protamine sulphate
Warfarin overdose|Vitamin K
Methanol poisoning|Fomepizole (or ethanol)
Cyanide poisoning|Hydroxocobalamin
Iron poisoning|Desferrioxamine
Lead poisoning|Calcium disodium EDTA / succimer
Digoxin toxicity|Digoxin-specific antibody fragments
Malignant hyperthermia|Dantrolene
""")
table_topics('medicine.antidotes', MED, 'Toxicology – Antidotes', ANTIDOTES, [
    ("The antidote of choice for {a} is ___.", 'b', "{a}: {b}."),
])

SIGNS = rows("""
Kernig's sign|Meningitis
Murphy's sign|Acute cholecystitis
McBurney's point tenderness|Acute appendicitis
Koplik's spots|Measles
Chvostek's sign|Hypocalcaemia
Trousseau's sign|Hypocalcaemia
Kussmaul breathing|Diabetic ketoacidosis
Battle's sign|Basal skull fracture
Cullen's sign|Acute haemorrhagic pancreatitis
Beck's triad|Cardiac tamponade
Virchow's node|Metastatic gastric carcinoma
Reed–Sternberg cells|Hodgkin lymphoma
Auer rods|Acute myeloid leukaemia
Negri bodies|Rabies
Kayser–Fleischer ring|Wilson disease
Charcot's triad|Ascending cholangitis
""")
table_topics('medicine.clinical_signs', MED, 'Medicine – Signs & Clinical Clues', SIGNS, [
    ("{a} is classically associated with ___.", 'b', "{a}: {b}."),
])

NERVES = rows("""
Wrist drop|Radial nerve
Claw hand|Ulnar nerve
Ape thumb deformity|Median nerve
Foot drop|Common peroneal nerve
Winging of the scapula|Long thoracic nerve
Erb's palsy (waiter's tip)|Upper trunk of brachial plexus (C5–C6)
Klumpke's palsy|Lower trunk of brachial plexus (C8–T1)
Bell's palsy|Facial nerve
""")
table_topics('medicine.anatomy', MED, 'Anatomy – Nerve Injuries', NERVES, [
    ("{a} results from injury to the ___.", 'b', "{a}: {b}."),
])

MEDICINE = [
    ("The most common cause of community-acquired pneumonia is ___.", ['Streptococcus pneumoniae', 'Staphylococcus aureus', 'Klebsiella', 'Mycoplasma'], 'easy', "Pneumococcus."),
    ("The drug of choice for anaphylactic shock is ___.", ['Adrenaline (intramuscular)', 'Hydrocortisone', 'Antihistamine', 'Atropine'], 'easy', "IM adrenaline 0.5 mg (1:1000) in adults."),
    ("The normal range of serum potassium is ___.", ['3.5–5.0 mEq/L', '1.5–2.5 mEq/L', '135–145 mEq/L', '8.5–10.5 mg/dL'], 'easy', "Sodium is 135–145."),
    ("HbA1c reflects the average blood glucose over about ___.", ['2–3 months', '1 week', '2 days', '1 year'], 'easy', "RBC life span ≈ 120 days."),
    ("Diagnosis of diabetes by fasting plasma glucose requires a value of at least ___.", ['126 mg/dL', '100 mg/dL', '110 mg/dL', '200 mg/dL'], 'medium', "ADA/WHO criterion."),
    ("The most common site of carcinoma of the colon is the ___.", ['Rectosigmoid', 'Caecum', 'Transverse colon', 'Ascending colon'], 'medium', "Rectum and sigmoid."),
    ("The most common type of thyroid cancer is ___.", ['Papillary carcinoma', 'Follicular carcinoma', 'Medullary carcinoma', 'Anaplastic carcinoma'], 'easy', "About 80%."),
    ("Philadelphia chromosome t(9;22) is characteristic of ___.", ['Chronic myeloid leukaemia', 'Acute lymphoblastic leukaemia', 'Hodgkin lymphoma', 'Multiple myeloma'], 'easy', "BCR-ABL fusion."),
    ("The most common cause of mitral stenosis is ___.", ['Rheumatic heart disease', 'Congenital', 'Infective endocarditis', 'Calcification'], 'easy', "Post-streptococcal."),
    ("The classic ECG change in hyperkalaemia is ___.", ['Tall peaked T waves', 'U waves', 'ST depression', 'Prolonged QT'], 'medium', "U waves suggest hypokalaemia."),
    ("The first-line drug for absence seizures is ___.", ['Ethosuximide (or valproate)', 'Phenytoin', 'Carbamazepine', 'Phenobarbitone'], 'medium', "Carbamazepine can worsen absence seizures."),
    ("Pellagra is caused by deficiency of ___.", ['Niacin', 'Thiamine', 'Riboflavin', 'Vitamin B12'], 'easy', "Dermatitis, diarrhoea, dementia."),
    ("Wernicke's encephalopathy is due to deficiency of ___.", ['Thiamine', 'Niacin', 'Folate', 'Pyridoxine'], 'easy', "Vitamin B1."),
    ("The most common site of ectopic pregnancy is the ___.", ['Ampulla of the fallopian tube', 'Ovary', 'Cervix', 'Isthmus of the tube'], 'easy', "Ampullary region."),
    ("The causative organism of syphilis is ___.", ['Treponema pallidum', 'Neisseria gonorrhoeae', 'Chlamydia trachomatis', 'Haemophilus ducreyi'], 'easy', "A spirochaete."),
    ("Gram-positive bacteria stain ___ in Gram staining.", ['Purple/violet', 'Pink/red', 'Green', 'Unstained'], 'easy', "Thick peptidoglycan retains crystal violet."),
    ("The incubation period of rabies is usually ___.", ['1–3 months (variable)', '24 hours', '2–3 days', 'Exactly 10 days'], 'medium', "Depends on the site of the bite."),
    ("BCG vaccine is given at ___.", ['Birth', '6 weeks', '9 months', '5 years'], 'easy', "Under India's Universal Immunisation Programme."),
    ("The cold chain temperature for most vaccines is ___.", ['+2 °C to +8 °C', '−20 °C to −10 °C', '0 °C to 4 °C', '10 °C to 15 °C'], 'easy', "OPV can be stored frozen."),
    ("Infant Mortality Rate is calculated per ___ live births.", ['1,000', '100', '10,000', '1,00,000'], 'easy', "MMR uses 1,00,000 live births."),
    ("The 'gold standard' for diagnosing pulmonary tuberculosis is ___.", ['Sputum culture', 'Chest X-ray', 'Mantoux test', 'ESR'], 'medium', "CBNAAT/GeneXpert is the rapid molecular test."),
    ("A Glasgow Coma Scale score of 8 or less usually indicates the need for ___.", ['Airway protection (intubation)', 'Discharge', 'Oral fluids', 'Physiotherapy'], 'medium', "'GCS 8 – intubate'."),
    ("The universal donor for plasma is blood group ___.", ['AB', 'O', 'A', 'B'], 'hard', "AB plasma has no anti-A or anti-B antibodies."),
    ("Cushing's syndrome is due to excess ___.", ['Cortisol', 'Aldosterone', 'Thyroxine', 'Insulin'], 'easy', "Exogenous steroids are the commonest cause."),
    ("Addison's disease is ___.", ['Primary adrenal insufficiency', 'Excess cortisol', 'Thyroid failure', 'Pituitary tumour'], 'easy', "Hyperpigmentation, hypotension."),
    ("The most common cause of hypothyroidism in iodine-sufficient areas is ___.", ["Hashimoto's thyroiditis", "Graves' disease", 'Thyroid cancer', 'Iodine excess'], 'medium', "Autoimmune."),
    ("Normal adult respiratory rate is ___ breaths per minute.", ['12–20', '30–40', '5–10', '25–35'], 'easy', "At rest."),
    ("The largest organ of the human body is the ___.", ['Skin', 'Liver', 'Lungs', 'Brain'], 'easy', "By surface area and weight."),
    ("The commonest cause of maternal mortality in India is ___.", ['Haemorrhage (mainly postpartum)', 'Sepsis', 'Anaemia alone', 'Obstructed labour'], 'medium', "PPH is the leading direct cause."),
    ("APGAR score is assessed at ___.", ['1 and 5 minutes after birth', '10 and 20 minutes', '1 hour', '24 hours'], 'easy', "Appearance, Pulse, Grimace, Activity, Respiration."),
]
register('medicine.clinical', MED, 'Clinical Medicine & Allied Subjects', rows=MEDICINE)

NURSING = [
    ("The normal adult pulse rate is ___ beats per minute.", ['60–100', '40–60', '100–140', '20–40'], 'easy', "Resting heart rate."),
    ("The first step of the nursing process is ___.", ['Assessment', 'Planning', 'Implementation', 'Evaluation'], 'easy', "ADPIE."),
    ("The correct site for an intramuscular injection in infants is the ___.", ['Vastus lateralis', 'Deltoid', 'Dorsogluteal', 'Ventrogluteal'], 'medium', "Best developed muscle in infants."),
    ("The angle of needle insertion for an intradermal injection is ___.", ['10–15°', '45°', '90°', '30–45°'], 'medium', "Mantoux test."),
    ("The angle of needle insertion for an intramuscular injection is ___.", ['90°', '15°', '45°', '5°'], 'easy', "Perpendicular to the skin."),
    ("Hand hygiene with alcohol rub should take about ___.", ['20–30 seconds', '5 seconds', '2 minutes', '10 minutes'], 'easy', "WHO recommendation."),
    ("The position used to prevent aspiration in an unconscious patient is ___.", ['Recovery (lateral) position', 'Supine', 'Prone', 'Trendelenburg'], 'easy', "Keeps the airway clear."),
    ("Fowler's position is used mainly to ___.", ['Ease breathing', 'Treat shock', 'Examine the back', 'Deliver a baby'], 'easy', "Head end raised 45–60°."),
    ("The ratio of chest compressions to breaths in adult CPR (single rescuer) is ___.", ['30 : 2', '15 : 2', '5 : 1', '10 : 1'], 'easy', "AHA guidelines."),
    ("The recommended depth of chest compression in adult CPR is ___.", ['5–6 cm', '2–3 cm', '8–10 cm', '1 cm'], 'medium', "At 100–120 per minute."),
    ("Bed sores most commonly develop over the ___.", ['Sacrum', 'Abdomen', 'Chest', 'Forearm'], 'easy', "Bony prominences under pressure."),
    ("The colour code for infectious waste bags (e.g. soiled dressings) under BMW Rules 2016 is ___.", ['Yellow', 'Red', 'Blue', 'Black'], 'medium', "Red is for contaminated recyclable plastics."),
    ("Sharps are disposed of in a ___ puncture-proof container.", ['White (translucent)', 'Yellow', 'Black', 'Green'], 'medium', "BMW Rules 2016."),
    ("The normal urine output of an adult is about ___.", ['1–2 litres per day', '200 mL per day', '5 litres per day', '50 mL per day'], 'easy', "Oliguria is < 400 mL/day."),
    ("Exclusive breastfeeding is recommended for the first ___ months.", ['6', '3', '9', '12'], 'easy', "WHO/UNICEF."),
    ("Kangaroo mother care is mainly for ___.", ['Low-birth-weight babies', 'Post-operative adults', 'Elderly patients', 'Burns'], 'easy', "Skin-to-skin contact."),
    ("The 'five rights' of medication administration include right patient, drug, dose, route and ___.", ['Time', 'Cost', 'Colour', 'Brand'], 'easy', "Some lists add more rights."),
    ("The first nursing action for a patient with a seizure is to ___.", ['Protect from injury and maintain the airway', 'Restrain the limbs', 'Put a spoon in the mouth', 'Give water'], 'easy', "Never put anything in the mouth."),
    ("Florence Nightingale is known as ___.", ['The Lady with the Lamp', 'The Mother of Medicine', 'The Angel of Mercy only', 'The Founder of WHO'], 'easy', "Crimean War."),
    ("International Nurses Day is observed on ___.", ['12 May', '7 April', '1 July', '5 June'], 'easy', "Florence Nightingale's birthday."),
]
register('nursing.core', 'NUR1', 'Nursing Foundations', rows=NURSING)

DENTAL = [
    ("The total number of permanent teeth in an adult is ___.", ['32', '20', '28', '36'], 'easy', "Deciduous teeth: 20."),
    ("The hardest substance in the human body is ___.", ['Enamel', 'Dentine', 'Bone', 'Cementum'], 'easy', "About 96% mineral."),
    ("The first permanent tooth to erupt is usually the ___.", ['First molar', 'Central incisor', 'Canine', 'Second premolar'], 'easy', "Around 6 years."),
    ("Dental caries is mainly caused by ___.", ['Streptococcus mutans', 'Staphylococcus aureus', 'E. coli', 'Candida'], 'easy', "Acid from sugar fermentation."),
    ("The ideal fluoride concentration in drinking water is about ___.", ['0.7–1.2 ppm', '5 ppm', '0.01 ppm', '10 ppm'], 'medium', "Higher levels cause fluorosis."),
    ("Black's classification is used for ___.", ['Carious lesions/cavity preparations', 'Malocclusion', 'Periodontal disease', 'Fractures'], 'medium', "Class I–V (VI added later)."),
    ("Angle's classification is used for ___.", ['Malocclusion', 'Caries', 'Gingivitis', 'Jaw fractures'], 'easy', "Based on the first molar relation."),
    ("The most common cause of tooth loss in adults over 35 is ___.", ['Periodontal disease', 'Caries only', 'Trauma', 'Attrition'], 'medium', "Gum disease."),
    ("Local anaesthetic most commonly used in dentistry is ___.", ['Lignocaine (lidocaine)', 'Bupivacaine', 'Procaine', 'Cocaine'], 'easy', "Often with adrenaline."),
    ("The 'pulp' of a tooth contains ___.", ['Nerves and blood vessels', 'Only enamel', 'Cementum', 'Saliva'], 'easy', "Root canal treatment removes it."),
    ("Mottled enamel is a sign of ___.", ['Dental fluorosis', 'Caries', 'Scurvy', 'Rickets'], 'easy', "Excess fluoride."),
    ("The nerve anaesthetised for an inferior alveolar nerve block is a branch of the ___.", ['Mandibular nerve', 'Maxillary nerve', 'Facial nerve', 'Hypoglossal nerve'], 'medium', "V3."),
]
register('dentistry.core', 'DEN1', 'Dental Sciences', rows=DENTAL)

# ================================================================== Commerce
ACC, ECO, BST, LAW, TAX = 'ACC1', 'ECO1', 'BST1', 'LAW1', 'TAX1'


@generator('commerce.accounting', ACC, 'Accountancy (Computed)')
def accounting(rng):
    kind = rng.randrange(5)
    if kind == 0:
        cost, scrap, life = rng.randrange(50000, 500000, 10000), rng.randrange(0, 40000, 5000), rng.choice([4, 5, 8, 10])
        dep = F(cost - scrap, life)
        return mcq(rng, f"A machine costs {inr(cost)} with a scrap value of {inr(scrap)} and a life of {life} years. Annual depreciation (straight line) is ___.",
                   inr(dep), [inr(x) for x in (F(cost, life), dep + 1000, F(cost - scrap, life + 1))], 'easy', f"({cost} − {scrap})/{life}.")
    if kind == 1:
        cost, rate = rng.randrange(100000, 500000, 20000), rng.choice([10, 15, 20])
        y2 = F(cost) * (100 - rate) / 100 * rate / 100
        return mcq(rng, f"A machine costing {inr(cost)} is depreciated at {rate}% p.a. on the written down value. Depreciation for the 2nd year is ___.",
                   inr(y2), [inr(x) for x in (F(cost * rate, 100), y2 + 500, F(cost) * rate / 100 * 2)], 'medium', "Second year is charged on the reduced balance.")
    if kind == 2:
        ca, cl = rng.randrange(100000, 600000, 10000), rng.randrange(50000, 300000, 10000)
        r = F(ca, cl)
        return mcq(rng, f"Current assets are {inr(ca)} and current liabilities are {inr(cl)}. The current ratio is ___.", f"{float(r):.2f} : 1",
                   [f"{float(x):.2f} : 1" for x in (1 / r, r + F(1, 2), r * 2)], 'easy', "Current assets ÷ current liabilities.")
    if kind == 3:
        assets, liab = rng.randrange(200000, 900000, 10000), rng.randrange(50000, 190000, 10000)
        return mcq(rng, f"Total assets are {inr(assets)} and liabilities are {inr(liab)}. Capital is ___.", inr(assets - liab),
                   [inr(x) for x in (assets + liab, liab, assets)], 'easy', "Accounting equation: Assets = Liabilities + Capital.")
    fc, price, vc = rng.randrange(100000, 500000, 10000), rng.randrange(50, 200, 10), rng.randrange(20, 45, 5)
    while (price - vc) <= 0 or fc % (price - vc):
        fc += 10000
        if fc > 2000000:
            fc, price, vc = 300000, 100, 40
    bep = fc // (price - vc)
    return mcq(rng, f"Fixed costs are {inr(fc)}, selling price ₹{price} and variable cost ₹{vc} per unit. Break-even point is ___ units.", f"{bep:,}",
               [f"{x:,}" for x in (fc // price, bep * 2, bep + 500)], 'medium', "BEP = Fixed cost ÷ contribution per unit.")


@generator('commerce.gst', TAX, 'GST & Taxation (Computed)')
def gst(rng):
    price, rate = rng.randrange(1000, 50000, 500), rng.choice([5, 12, 18, 28])
    tax = F(price * rate, 100)
    if rng.random() < 0.5:
        return mcq(rng, f"An item worth {inr(price)} attracts GST at {rate}%. For an intra-state sale, CGST is ___.", inr(tax / 2),
                   [inr(x) for x in (tax, tax / 4, F(price * rate, 200) + 100)], 'medium', "Intra-state: GST is split equally into CGST and SGST.")
    return mcq(rng, f"An item worth {inr(price)} is sold inter-state with GST at {rate}%. The invoice value is ___.", inr(price + tax),
               [inr(x) for x in (price + tax / 2, price, price + tax * 2)], 'easy', "Inter-state sales attract IGST at the full rate.")


ECONOMICS = [
    ("The law of demand states that, other things equal, ___.", ['Quantity demanded falls as price rises', 'Demand rises with price', 'Supply equals demand', 'Price is fixed'], 'easy', "Inverse relation."),
    ("Price elasticity of demand greater than 1 means demand is ___.", ['Elastic', 'Inelastic', 'Unitary', 'Perfectly inelastic'], 'easy', "Responsive to price."),
    ("In perfect competition, firms are ___.", ['Price takers', 'Price makers', 'Monopolists', 'Oligopolists'], 'easy', "Many sellers, identical goods."),
    ("A market with a single seller is ___.", ['Monopoly', 'Oligopoly', 'Monopsony', 'Duopoly'], 'easy', "Monopsony: single buyer."),
    ("GDP at market price minus net indirect taxes equals GDP at ___.", ['Factor cost', 'Constant prices', 'Current prices', 'Basic price only'], 'medium', "Factor cost = MP − (indirect taxes − subsidies)."),
    ("The marginal propensity to consume (MPC) plus MPS equals ___.", ['1', '0', 'The multiplier', 'Income'], 'easy', "Every extra rupee is spent or saved."),
    ("If MPC = 0.8, the investment multiplier is ___.", ['5', '8', '1.25', '0.2'], 'medium', "1/(1 − MPC)."),
    ("A decrease in CRR by the RBI ___ money supply.", ['Increases', 'Decreases', 'Does not affect', 'Freezes'], 'medium', "Banks can lend more."),
    ("The opportunity cost of a choice is ___.", ['The value of the next best alternative given up', 'The money price', 'The total cost', 'The sunk cost'], 'easy', "Basic economic idea."),
    ("Giffen goods are an exception to the law of ___.", ['Demand', 'Supply', 'Diminishing returns', 'Variable proportions'], 'medium', "Demand rises with price."),
    ("Balance of trade refers to ___.", ['Exports minus imports of goods', 'Capital flows', 'Services only', 'Foreign reserves'], 'easy', "Visible trade."),
    ("Who wrote 'The Wealth of Nations'?", ['Adam Smith', 'J. M. Keynes', 'Karl Marx', 'Alfred Marshall'], 'easy', "1776."),
    ("Stagflation is a combination of ___.", ['High inflation and stagnant growth', 'Deflation and growth', 'Low inflation and high growth', 'Falling prices and boom'], 'medium', "As in the 1970s."),
    ("The Lorenz curve measures ___.", ['Income inequality', 'Inflation', 'Unemployment', 'Elasticity'], 'medium', "Gini coefficient is derived from it."),
]
register('commerce.economics', ECO, 'Economics', rows=ECONOMICS)

BUSINESS = [
    ("Who is known as the father of scientific management?", ['F. W. Taylor', 'Henri Fayol', 'Peter Drucker', 'Elton Mayo'], 'easy', "Taylor."),
    ("Henri Fayol gave ___ principles of management.", ['14', '10', '12', '7'], 'easy', "General administrative principles."),
    ("Maslow's hierarchy places ___ needs at the top.", ['Self-actualisation', 'Safety', 'Physiological', 'Esteem'], 'easy', "Highest level."),
    ("'Planning' is the ___ function of management.", ['First (primary)', 'Last', 'Optional', 'Controlling'], 'easy', "Comes before the others."),
    ("Span of control refers to ___.", ['Number of subordinates a manager supervises', 'Length of a plan', 'Market share', 'Budget size'], 'easy', "Narrow vs wide span."),
    ("Marketing mix (4 Ps) includes Product, Price, Place and ___.", ['Promotion', 'People', 'Packaging', 'Profit'], 'easy', "McCarthy's 4 Ps."),
    ("A sole proprietor has ___ liability.", ['Unlimited', 'Limited', 'No', 'Shared'], 'easy', "Personal assets are at risk."),
    ("The minimum number of members for a public company is ___.", ['7', '2', '1', '50'], 'medium', "Private company: 2; One Person Company: 1."),
    ("Working capital equals ___.", ['Current assets − current liabilities', 'Fixed assets − long-term debt', 'Total assets', 'Capital + reserves'], 'easy', "Short-term liquidity."),
    ("SEBI regulates ___.", ['The securities market', 'Banks', 'Insurance companies', 'Pension funds'], 'easy', "Securities and Exchange Board of India."),
    ("Consumer Protection Act, 2019 replaced the Act of ___.", ['1986', '1976', '1995', '2005'], 'medium', "Consumer Protection Act, 1986."),
    ("Which of these is a source of long-term finance?", ['Equity shares', 'Trade credit', 'Bank overdraft', 'Commercial paper'], 'easy', "Permanent capital."),
]
register('commerce.business', BST, 'Business Studies & Management', rows=BUSINESS)

ACCOUNTING_THEORY = [
    ("The rule for a real account is ___.", ['Debit what comes in, credit what goes out', 'Debit the receiver, credit the giver', 'Debit expenses, credit incomes', 'Credit all assets'], 'easy', "Golden rules."),
    ("The rule for a personal account is ___.", ['Debit the receiver, credit the giver', 'Debit what comes in', 'Debit all losses', 'Credit the receiver'], 'easy', "Golden rules."),
    ("Outstanding salary is a ___.", ['Current liability', 'Current asset', 'Expense paid', 'Fixed asset'], 'easy', "Owed but not paid."),
    ("Prepaid insurance is shown as ___.", ['A current asset', 'A liability', 'An income', 'Capital'], 'easy', "Paid in advance."),
    ("A trial balance is prepared to check the ___ accuracy of accounts.", ['Arithmetical', 'Complete', 'Legal', 'Tax'], 'easy', "Errors of principle are not revealed."),
    ("Goodwill is a(n) ___ asset.", ['Intangible', 'Current', 'Fictitious', 'Liquid'], 'easy', "No physical form."),
    ("The partnership deed is silent on profit sharing: partners share profits ___.", ['Equally', 'In capital ratio', 'In the ratio of time worked', 'At 6% interest'], 'medium', "Indian Partnership Act, 1932."),
    ("If the deed is silent, interest on partners' loans is allowed at ___ p.a.", ['6%', '10%', '12%', 'No interest'], 'medium', "Section 13 of the Partnership Act."),
    ("Accounting standards in India for companies (Ind AS) are converged with ___.", ['IFRS', 'US GAAP', 'Japanese GAAP', 'None'], 'medium', "International Financial Reporting Standards."),
    ("Depreciation is charged because of ___.", ['Wear and tear, obsolescence and passage of time', 'Rise in market value', 'Profit motive only', 'Tax only'], 'easy', "Matching principle."),
]
register('commerce.accounting_theory', ACC, 'Accounting Principles', rows=ACCOUNTING_THEORY)

BUSINESS_LAW = [
    ("Under the Indian Contract Act, 1872, an agreement enforceable by law is a ___.", ['Contract', 'Promise', 'Proposal', 'Offer'], 'easy', "Section 2(h)."),
    ("A contract with a minor is ___.", ['Void ab initio', 'Voidable', 'Valid', 'Illegal but enforceable'], 'medium', "Mohori Bibee v. Dharmodas Ghose."),
    ("Consideration must move at the desire of the ___.", ['Promisor', 'Court', 'Third party only', 'Government'], 'medium', "Section 2(d)."),
    ("The Sale of Goods Act was enacted in ___.", ['1930', '1872', '1932', '1956'], 'medium', "Formerly part of the Contract Act."),
    ("A cheque is a bill of exchange drawn on a ___ and payable on demand.", ['Specified banker', 'Customer', 'Court', 'Company'], 'easy', "Section 6, NI Act."),
    ("The Negotiable Instruments Act was passed in ___.", ['1881', '1872', '1930', '1956'], 'medium', "Covers promissory notes, bills and cheques."),
    ("Dishonour of a cheque for insufficient funds is an offence under Section ___ of the NI Act.", ['138', '420', '302', '13'], 'medium', "Section 138."),
    ("The Companies Act currently in force is the Act of ___.", ['2013', '1956', '2002', '2019'], 'easy', "Replaced the 1956 Act."),
    ("An agreement in restraint of marriage is ___.", ['Void', 'Valid', 'Voidable', 'Enforceable with conditions'], 'medium', "Section 26."),
    ("Free consent is absent if consent is caused by ___.", ['Coercion, undue influence, fraud, misrepresentation or mistake', 'Consideration', 'Offer and acceptance', 'Writing'], 'easy', "Section 14."),
]
register('commerce.business_law', LAW, 'Business & Corporate Laws', rows=BUSINESS_LAW)

# ================================================================== Law (CLAT, AILET, Judiciary)
LGL = 'LGL1'
MAXIMS = rows("""
Ignorantia juris non excusat|Ignorance of the law is no excuse
Audi alteram partem|Hear the other side
Nemo judex in causa sua|No one should be a judge in their own cause
Res judicata|A matter already decided cannot be re-litigated
Actus non facit reum nisi mens sit rea|An act is not guilty unless the mind is guilty
Ubi jus ibi remedium|Where there is a right, there is a remedy
Volenti non fit injuria|To a willing person no injury is done
Damnum sine injuria|Damage without legal injury
Injuria sine damno|Legal injury without actual damage
Res ipsa loquitur|The thing speaks for itself
Caveat emptor|Let the buyer beware
Pacta sunt servanda|Agreements must be kept
Habeas corpus|You may have the body
Obiter dictum|A remark made in passing by a judge
Ratio decidendi|The reason for the decision
""")
table_topics('law.maxims', LGL, 'Legal Maxims', MAXIMS, [
    ("The legal maxim '{a}' means ___.", 'b', "{a}: {b}."),
    ("Which maxim means '{b}'?", 'a', "{a}: {b}."),
])

CASES = rows("""
Kesavananda Bharati v. State of Kerala (1973)|Basic structure doctrine
Maneka Gandhi v. Union of India (1978)|Wide reading of Article 21 (procedure must be fair, just and reasonable)
Vishaka v. State of Rajasthan (1997)|Guidelines against sexual harassment at the workplace
Indra Sawhney v. Union of India (1992)|50% ceiling on reservations and the creamy layer
K. S. Puttaswamy v. Union of India (2017)|Right to privacy is a fundamental right
S. R. Bommai v. Union of India (1994)|Limits on President's Rule under Article 356
Navtej Singh Johar v. Union of India (2018)|Decriminalisation of consensual same-sex relations
Shayara Bano v. Union of India (2017)|Instant triple talaq held unconstitutional
M. C. Mehta v. Union of India (1987)|Absolute liability for hazardous industries
Minerva Mills v. Union of India (1980)|Balance between Fundamental Rights and Directive Principles
Golaknath v. State of Punjab (1967)|Parliament cannot amend Fundamental Rights (later overruled)
Donoghue v. Stevenson (1932)|Neighbour principle in negligence
""")
table_topics('law.cases', LGL, 'Landmark Judgments', CASES, [
    ("{a} is known for ___.", 'b', "{a}: {b}."),
    ("Which case laid down: {b}?", 'a', "{a}: {b}."),
], difficulty='medium')

LEGAL_REASONING = [
    ("Principle: A person is liable for negligence if they owe a duty of care, breach it, and cause damage.\nFacts: A doctor leaves a swab inside a patient during surgery, causing infection.\nIs the doctor liable?",
     ['Yes, all three elements are present', 'No, doctors are never liable', 'No, infection is natural', 'Only if the patient paid'], 'easy', "Duty, breach and resulting damage are all present."),
    ("Principle: An offer must be communicated to be accepted.\nFacts: X finds a lost dog and returns it without knowing a reward was announced. Can X claim the reward?",
     ['No, X did not know of the offer', 'Yes, X did the act', 'Yes, rewards are always payable', 'Only half the reward'], 'medium', "Lalman Shukla v. Gauri Dutt."),
    ("Principle: Consent obtained by coercion makes a contract voidable at the option of the party coerced.\nFacts: A threatens to harm B's son unless B sells his car to A. B agrees.\nThe contract is ___.",
     ['Voidable at B\'s option', 'Void', 'Valid', 'Illegal for both'], 'easy', "Section 19, Contract Act."),
    ("Principle: Private defence allows reasonable force to protect oneself, but not more force than necessary.\nFacts: A slaps B; B shoots A dead.\nCan B claim private defence?",
     ['No, the force used was excessive', 'Yes, any force is allowed', 'Yes, because A started it', 'Only if B is a police officer'], 'easy', "Force must be proportionate."),
    ("Principle: Trespass is the unlawful entry onto another's land.\nFacts: A enters B's garden to rescue a child drowning in B's pond.\nWhich is most appropriate?",
     ['A may raise the defence of necessity', 'A is guilty of criminal trespass and must be punished', 'B must pay A', 'A has committed theft'], 'medium', "Necessity can justify entry to save life."),
    ("Principle: A minor's agreement is void.\nFacts: A 16-year-old borrows money by mortgaging his house and later refuses to repay.\nCan the lender recover the money?",
     ['No, the agreement is void', 'Yes, with interest', 'Yes, from the minor personally', 'Only if the minor agrees'], 'medium', "Mohori Bibee v. Dharmodas Ghose."),
]
register('law.legal_reasoning', LGL, 'Legal Reasoning', rows=LEGAL_REASONING)

# ================================================================== Teaching (CTET, TET, KVS, UGC NET Paper 1)
CDP, TCH = 'CDP1', 'TCH1'
THEORISTS = rows("""
Jean Piaget|Stages of cognitive development
Lev Vygotsky|Zone of Proximal Development and social constructivism
Lawrence Kohlberg|Stages of moral development
Howard Gardner|Theory of multiple intelligences
B. F. Skinner|Operant conditioning
Ivan Pavlov|Classical conditioning
Edward Thorndike|Laws of learning (trial and error)
Albert Bandura|Social learning (observational learning)
Erik Erikson|Psychosocial stages of development
Jerome Bruner|Discovery learning and scaffolding (spiral curriculum)
Benjamin Bloom|Taxonomy of educational objectives
Sigmund Freud|Psychoanalytic theory
David Ausubel|Meaningful verbal learning (advance organisers)
Wolfgang Köhler|Insight learning
""")
table_topics('teaching.theorists', CDP, 'Child Development – Theorists', THEORISTS, [
    ("{a} is associated with ___.", 'b', "{a}: {b}."),
    ("Who proposed: {b}?", 'a', "{a}: {b}."),
])

PEDAGOGY = [
    ("According to Piaget, a child in the pre-operational stage (2–7 years) shows ___.", ['Egocentrism', 'Abstract reasoning', 'Hypothetico-deductive thinking', 'Conservation of volume'], 'easy', "Conservation develops in the concrete operational stage."),
    ("Piaget's concrete operational stage covers ages ___.", ['7–11 years', '0–2 years', '2–7 years', '11 years and above'], 'easy', "Logical thinking about concrete objects."),
    ("'Zone of Proximal Development' refers to ___.", ['What a learner can do with help but not yet alone', 'What a learner cannot learn', 'IQ range', 'Age-appropriate syllabus'], 'easy', "Vygotsky."),
    ("Scaffolding in teaching means ___.", ['Temporary support withdrawn as the learner becomes capable', 'Punishment', 'Rote learning', 'Building a stage'], 'easy', "Bruner/Vygotsky."),
    ("Continuous and Comprehensive Evaluation (CCE) focuses on ___.", ['Both scholastic and co-scholastic areas throughout the year', 'Only final exams', 'Only sports', 'Ranking students'], 'easy', "RTE Act 2009 context."),
    ("Formative assessment is mainly used to ___.", ['Improve learning during instruction', 'Certify students', 'Rank schools', 'Select toppers'], 'easy', "Assessment for learning."),
    ("Dyslexia is a learning disability related to ___.", ['Reading', 'Writing only', 'Mathematics', 'Motor skills'], 'easy', "Dyscalculia: maths; dysgraphia: writing."),
    ("Dyscalculia affects ___.", ['Mathematical ability', 'Reading', 'Speech', 'Hearing'], 'easy', "Number sense."),
    ("The RTE Act, 2009 provides free and compulsory education for children aged ___.", ['6–14 years', '3–6 years', '5–15 years', '14–18 years'], 'easy', "Article 21A."),
    ("Under the RTE Act, private unaided schools must reserve ___ seats for disadvantaged children.", ['25%', '10%', '15%', '50%'], 'medium', "Section 12(1)(c)."),
    ("NEP 2020 replaces the 10+2 structure with ___.", ['5+3+3+4', '4+4+4', '6+3+3', '5+5+2'], 'easy', "Foundational, preparatory, middle and secondary stages."),
    ("Under NEP 2020, the medium of instruction till at least Class 5 should preferably be ___.", ['Home language/mother tongue', 'English', 'Hindi only', 'Sanskrit'], 'medium', "Wherever possible."),
    ("Inclusive education means ___.", ['Educating children with diverse needs together in regular schools', 'Separate schools for disabled children', 'Only gifted children', 'Home schooling'], 'easy', "Equity in classrooms."),
    ("A child-centred classroom emphasises ___.", ['Active learning and children\'s experiences', 'Teacher lectures only', 'Strict memorisation', 'Punishment'], 'easy', "NCF 2005."),
    ("Kohlberg's highest level of moral development is ___.", ['Post-conventional', 'Pre-conventional', 'Conventional', 'Concrete'], 'medium', "Universal ethical principles."),
    ("Gardner's 'bodily-kinaesthetic' intelligence is shown by ___.", ['Dancers and athletes', 'Mathematicians', 'Poets', 'Philosophers'], 'easy', "Control of body movements."),
    ("Which is the best way to deal with a student's mistake?", ['Use it as an opportunity for learning', 'Punish the student', 'Ignore it', 'Inform the parents immediately'], 'easy', "Errors show children's thinking."),
    ("Heuristic method of teaching was advocated by ___.", ['H. E. Armstrong', 'Froebel', 'Montessori', 'Dewey'], 'medium', "Learning by discovery in science."),
    ("'Kindergarten' was started by ___.", ['Friedrich Froebel', 'Maria Montessori', 'John Dewey', 'Rousseau'], 'easy', "Children's garden."),
    ("'Learning by doing' is associated with ___.", ['John Dewey', 'Skinner', 'Pavlov', 'Freud'], 'easy', "Pragmatism."),
]
register('teaching.pedagogy', CDP, 'Pedagogy & Inclusive Education', rows=PEDAGOGY)

RESEARCH_APTITUDE = [
    ("A hypothesis is ___.", ['A testable tentative statement', 'A proven fact', 'A conclusion', 'A data set'], 'easy', "Tested by research."),
    ("Which sampling method gives every member an equal chance of selection?", ['Simple random sampling', 'Quota sampling', 'Convenience sampling', 'Snowball sampling'], 'easy', "Probability sampling."),
    ("The arithmetic mean is affected most by ___.", ['Extreme values', 'The mode', 'Sample size only', 'The median'], 'easy', "Outliers pull the mean."),
    ("Plagiarism means ___.", ['Using others\' work without acknowledgement', 'Citing sources', 'Peer review', 'Data analysis'], 'easy', "Academic dishonesty."),
    ("An independent variable is the one that ___.", ['The researcher manipulates', 'Is measured as the outcome', 'Is kept constant', 'Is ignored'], 'easy', "Cause in an experiment."),
    ("Which is a qualitative research method?", ['Ethnography', 'Experiment', 'Survey with scales', 'Regression'], 'medium', "In-depth observation."),
    ("SWAYAM is a platform for ___.", ['Online courses (MOOCs)', 'Scholarships', 'Exam results', 'Teacher recruitment'], 'easy', "Government of India MOOCs."),
    ("ICT in education stands for ___.", ['Information and Communication Technology', 'Indian Council of Teachers', 'Internet Content Tools', 'Integrated Class Teaching'], 'easy', "Technology for learning."),
    ("Communication is most effective when it is ___.", ['Two-way with feedback', 'One-way', 'Long and formal', 'Only written'], 'easy', "Feedback closes the loop."),
    ("The highest level in Bloom's (revised) cognitive taxonomy is ___.", ['Creating', 'Evaluating', 'Applying', 'Remembering'], 'medium', "Anderson & Krathwohl, 2001."),
]
register('teaching.research', TCH, 'Teaching & Research Aptitude', rows=RESEARCH_APTITUDE)

# ================================================================== Engineering core (computed + facts)
CIV = 'CIV1'


@generator('engineering.electrical', 'PHY1', 'Electrical Engineering (Computed)')
def electrical(rng):
    kind = rng.randrange(4)
    if kind == 0:
        f, p = rng.choice([50, 60]), rng.choice([2, 4, 6, 8, 12])
        ns = 120 * f // p
        return mcq(rng, f"The synchronous speed of a {p}-pole, {f} Hz induction motor is ___.", f"{ns} rpm", [f"{x} rpm" for x in (60 * f // p, ns * 2, 120 * p // f * 10)],
                   'easy', "Nₛ = 120f/P.")
    if kind == 1:
        n1, n2, v1 = rng.choice([(1000, 100), (500, 50), (200, 400), (100, 1000), (300, 150)]) + (rng.choice([110, 220, 230, 440]),)
        v2 = F(v1 * n2, n1)
        return mcq(rng, f"A transformer has {n1} primary and {n2} secondary turns. With {v1} V on the primary, the secondary voltage is ___.", f"{fmt(v2)} V",
                   [f"{fmt(x)} V" for x in (F(v1 * n1, n2), v1, v2 + 10)], 'easy', "V₂/V₁ = N₂/N₁.")
    if kind == 2:
        v, i, pf = rng.choice([230, 400, 440]), rng.choice([5, 10, 20]), rng.choice([F(8, 10), F(6, 10), F(9, 10), F(1)])
        p = v * i * pf
        return mcq(rng, f"A single-phase load draws {i} A at {v} V with power factor {fmt(pf)}. The real power is ___.", f"{fmt(p)} W",
                   [f"{fmt(x)} W" for x in (v * i, p / 2, v * i * (1 - pf) or v)], 'medium', "P = VI cos φ.")
    s, ns = rng.choice([(1440, 1500), (960, 1000), (2880, 3000), (720, 750), (1455, 1500)])
    slip = F(ns - s, ns) * 100
    return mcq(rng, f"An induction motor with synchronous speed {ns} rpm runs at {s} rpm. The slip is ___.", f"{fmt(slip)}%",
               [f"{fmt(x)}%" for x in (slip * 2, F(ns - s, s) * 100, 100 - slip)], 'medium', "s = (Nₛ − N)/Nₛ.")


@generator('engineering.mechanical', 'PHY1', 'Mechanical Engineering (Computed)')
def mechanical(rng):
    kind = rng.randrange(3)
    if kind == 0:
        th, tc = rng.choice([500, 600, 800, 1000, 1200]), rng.choice([300, 350, 400])
        eff = (1 - F(tc, th)) * 100
        return mcq(rng, f"A Carnot engine works between {th} K and {tc} K. Its efficiency is ___.", f"{fmt(eff)}%",
                   [f"{fmt(x)}%" for x in (F(tc, th) * 100, eff / 2, 100 - eff / 2)], 'easy', "η = 1 − T_c/T_h.")
    if kind == 1:
        force, area = rng.choice([10, 20, 50, 100]) * 1000, rng.choice([100, 200, 250, 500])
        stress = F(force, area)
        return mcq(rng, f"A bar of cross-section {area} mm² carries an axial load of {force // 1000} kN. The stress is ___.", f"{fmt(stress)} N/mm²",
                   [f"{fmt(x)} N/mm²" for x in (stress * 10, stress / 2, F(force // 1000, area))], 'easy', "σ = P/A (1 N/mm² = 1 MPa).")
    stress, e = rng.choice([100, 150, 200, 250]), 200000
    strain = F(stress, e)
    return mcq(rng, f"Steel (E = 200 GPa) is stressed to {stress} MPa. The strain is ___.", f"{float(strain):.5f}",
               [f"{float(x):.5f}" for x in (strain * 10, strain / 2, strain * 2)], 'medium', "ε = σ/E.")


ENGG_FACTS = [
    ("The standard consistency test of cement is done with the ___.", ['Vicat apparatus', 'Le Chatelier apparatus', 'Slump cone', 'Compaction factor apparatus'], 'easy', "Le Chatelier tests soundness."),
    ("The slump test measures the ___ of concrete.", ['Workability', 'Strength', 'Durability', 'Setting time'], 'easy', "Fresh concrete."),
    ("M20 concrete has a characteristic compressive strength of ___.", ['20 N/mm² at 28 days', '20 N/mm² at 7 days', '200 N/mm²', '2 N/mm²'], 'easy', "Cube strength at 28 days."),
    ("The void ratio e and porosity n are related by ___.", ['n = e/(1 + e)', 'e = n/(1 + n)', 'n = 1 + e', 'n = e²'], 'medium', "Soil mechanics."),
    ("Bernoulli's equation applies to ___ flow.", ['Steady, incompressible, non-viscous', 'Turbulent viscous', 'Compressible unsteady', 'Any'], 'medium', "Along a streamline."),
    ("Reynolds number is the ratio of ___.", ['Inertia force to viscous force', 'Viscous force to inertia force', 'Gravity to inertia', 'Pressure to inertia'], 'easy', "Laminar below ~2000 in pipes."),
    ("The Otto cycle is the ideal cycle for ___ engines.", ['Petrol (spark-ignition)', 'Diesel', 'Gas turbine', 'Steam'], 'easy', "Diesel cycle for CI engines."),
    ("The Rankine cycle is used in ___.", ['Steam power plants', 'Petrol engines', 'Refrigerators', 'Jet engines'], 'easy', "Vapour power cycle."),
    ("COP of a refrigerator is ___.", ['Refrigerating effect ÷ work input', 'Work ÷ heat rejected', 'Always less than 1', 'Heat input ÷ work'], 'medium', "Can exceed 1."),
    ("The unit of dynamic viscosity in SI is ___.", ['Pa·s', 'm²/s', 'N/m', 'J/s'], 'medium', "Kinematic viscosity: m²/s."),
    ("A DC series motor should never be started ___.", ['Without load', 'With load', 'With a starter', 'At low voltage'], 'medium', "It can over-speed dangerously."),
    ("The efficiency of a transformer is maximum when ___.", ['Copper loss equals iron loss', 'Copper loss is zero', 'Iron loss is zero', 'Load is zero'], 'medium', "Condition for maximum efficiency."),
    ("Kirchhoff's current law is based on conservation of ___.", ['Charge', 'Energy', 'Momentum', 'Flux'], 'easy', "KVL: energy."),
    ("The 'Hooke's law' region is where stress is ___ to strain.", ['Proportional', 'Inversely proportional', 'Unrelated', 'Square of'], 'easy', "Below the proportional limit."),
    ("Poisson's ratio for most metals is about ___.", ['0.25–0.35', '1.5', '0.9', '0.01'], 'medium', "Steel ≈ 0.3."),
]
register('engineering.core', CIV, 'Engineering Core Concepts', rows=ENGG_FACTS)

# ================================================================== Hindi (school & TET)
HIN = 'HIN1'
PARYAYVACHI = rows("""
जल|नीर
अग्नि|अनल
पवन|समीर
सूर्य|दिनकर
चंद्रमा|शशि
पृथ्वी|धरा
आकाश|गगन
पर्वत|गिरि
नदी|सरिता
वृक्ष|तरु
फूल|सुमन
घर|गृह
माता|जननी
पिता|जनक
आँख|नयन
हाथी|गज
घोड़ा|अश्व
शेर|सिंह
बादल|मेघ
रात|निशा
दिन|दिवस
सोना|स्वर्ण
समुद्र|सागर
कमल|पंकज
""")
table_topics('hindi.paryayvachi', HIN, 'पर्यायवाची शब्द', PARYAYVACHI, [
    ("'{a}' का पर्यायवाची शब्द है ___", 'b', "'{a}' का पर्यायवाची '{b}' है।"),
], difficulty='easy')

VILOM = rows("""
दिन|रात
सुख|दुख
आदि|अंत
उदय|अस्त
आशा|निराशा
जीवन|मरण
प्रकाश|अंधकार
सत्य|असत्य
धनी|निर्धन
उत्तम|अधम
स्वतंत्र|परतंत्र
आय|व्यय
आयात|निर्यात
प्राचीन|नवीन
मित्र|शत्रु
विजय|पराजय
उन्नति|अवनति
सजीव|निर्जीव
आकर्षण|विकर्षण
स्वदेश|विदेश
""")
table_topics('hindi.vilom', HIN, 'विलोम शब्द', VILOM, [
    ("'{a}' का विलोम शब्द है ___", 'b', "'{a}' का विलोम '{b}' है।"),
    ("'{b}' का विलोम शब्द है ___", 'a', "'{b}' का विलोम '{a}' है।"),
], difficulty='easy')

MUHAVARE = rows("""
आँखों का तारा|बहुत प्यारा
नाक में दम करना|बहुत परेशान करना
दाँतों तले उँगली दबाना|आश्चर्यचकित होना
आसमान सिर पर उठाना|बहुत शोर मचाना
ईद का चाँद होना|बहुत दिनों बाद दिखाई देना
घी के दिए जलाना|खुशियाँ मनाना
अपने मुँह मियाँ मिट्ठू बनना|अपनी प्रशंसा स्वयं करना
उल्टी गंगा बहाना|नियम के विरुद्ध काम करना
आग बबूला होना|बहुत क्रोधित होना
हाथ पीले करना|विवाह करना
नौ दो ग्यारह होना|भाग जाना
कान भरना|चुगली करना
""")
table_topics('hindi.muhavare', HIN, 'मुहावरे', MUHAVARE, [
    ("मुहावरे '{a}' का अर्थ है ___", 'b', "'{a}' का अर्थ: {b}।"),
], difficulty='medium')

SANDHI = rows("""
विद्यालय|विद्या + आलय
हिमालय|हिम + आलय
सूर्योदय|सूर्य + उदय
महेश|महा + ईश
सदैव|सदा + एव
इत्यादि|इति + आदि
स्वागत|सु + आगत
जगन्नाथ|जगत् + नाथ
सज्जन|सत् + जन
नमस्ते|नमः + ते
""")
table_topics('hindi.sandhi', HIN, 'संधि-विच्छेद', SANDHI, [
    ("'{a}' का संधि-विच्छेद है ___", 'b', "{a} = {b}।"),
], difficulty='medium')

HINDI_GRAMMAR = [
    ("'राजपुत्र' में कौन-सा समास है?", ['तत्पुरुष', 'द्वंद्व', 'बहुव्रीहि', 'अव्ययीभाव'], 'medium', "राजा का पुत्र – तत्पुरुष।"),
    ("'माता-पिता' में कौन-सा समास है?", ['द्वंद्व', 'तत्पुरुष', 'कर्मधारय', 'द्विगु'], 'easy', "दोनों पद प्रधान – द्वंद्व।"),
    ("'चौराहा' में कौन-सा समास है?", ['द्विगु', 'द्वंद्व', 'तत्पुरुष', 'अव्ययीभाव'], 'medium', "संख्यावाचक पूर्वपद – द्विगु।"),
    ("'यथाशक्ति' में कौन-सा समास है?", ['अव्ययीभाव', 'तत्पुरुष', 'बहुव्रीहि', 'द्वंद्व'], 'medium', "पहला पद अव्यय।"),
    ("'नीलकंठ' (शिव) में कौन-सा समास है?", ['बहुव्रीहि', 'कर्मधारय', 'तत्पुरुष', 'द्विगु'], 'hard', "नीला है कंठ जिसका – अन्य पद (शिव) प्रधान।"),
    ("'लड़का' शब्द का स्त्रीलिंग है ___", ['लड़की', 'लड़कन', 'लड़िकी', 'लड़काइन'], 'easy', "लिंग परिवर्तन।"),
    ("'पुस्तक' शब्द का बहुवचन है ___", ['पुस्तकें', 'पुस्तकों', 'पुस्तके', 'पुस्तकाएँ'], 'easy', "वचन परिवर्तन।"),
    ("'सुंदर' शब्द किस प्रकार का शब्द है?", ['विशेषण', 'संज्ञा', 'क्रिया', 'सर्वनाम'], 'easy', "संज्ञा की विशेषता बताता है।"),
    ("'वह' शब्द है ___", ['सर्वनाम', 'संज्ञा', 'विशेषण', 'अव्यय'], 'easy', "संज्ञा के स्थान पर आता है।"),
    ("हिंदी वर्णमाला में स्वरों की संख्या (मानक रूप से) है ___", ['11', '13', '10', '52'], 'medium', "अ से औ तक 11 स्वर।"),
    ("'रामचरितमानस' के रचयिता हैं ___", ['तुलसीदास', 'सूरदास', 'कबीर', 'मीराबाई'], 'easy', "अवधी में रचित।"),
    ("'गोदान' उपन्यास के लेखक हैं ___", ['प्रेमचंद', 'जयशंकर प्रसाद', 'निराला', 'महादेवी वर्मा'], 'easy', "1936।"),
    ("'कामायनी' किसकी रचना है?", ['जयशंकर प्रसाद', 'सुमित्रानंदन पंत', 'निराला', 'मैथिलीशरण गुप्त'], 'medium', "छायावादी महाकाव्य।"),
    ("'जो ईश्वर में विश्वास रखता हो' – के लिए एक शब्द है ___", ['आस्तिक', 'नास्तिक', 'धार्मिक', 'भक्त'], 'easy', "एक शब्द।"),
    ("'जिसका कोई शत्रु न हो' – के लिए एक शब्द है ___", ['अजातशत्रु', 'शत्रुघ्न', 'मित्रवान', 'निर्भय'], 'medium', "एक शब्द।"),
]
register('hindi.grammar', HIN, 'हिंदी व्याकरण एवं साहित्य', rows=HINDI_GRAMMAR)

# ================================================================== Primary EVS & kids GK
EVS = 'EVS1'
ANIMAL_HOMES = rows("""
Dog|Kennel
Horse|Stable
Cow|Shed
Bird|Nest
Bee|Hive
Lion|Den
Spider|Web
Rabbit|Burrow
Pig|Sty
Hen|Coop
""")
table_topics('evs.animals', EVS, 'Animals & Their Homes', ANIMAL_HOMES, [
    ("Where does a {a} live?", 'b', "A {a} lives in a {b}."),
], difficulty='easy')

YOUNG_ONES = rows("""
Cow|Calf
Dog|Puppy
Cat|Kitten
Hen|Chick
Horse|Foal
Sheep|Lamb
Goat|Kid
Frog|Tadpole
Lion|Cub
Duck|Duckling
""")
table_topics('evs.young_ones', EVS, 'Young Ones of Animals', YOUNG_ONES, [
    ("The young one of a {a} is called a ___.", 'b', "{a} → {b}."),
], difficulty='easy')

EVS_BANK = [
    ("Which part of the plant makes food?", ['Leaf', 'Root', 'Stem', 'Flower'], 'easy', "Leaves make food using sunlight."),
    ("Which part of the plant absorbs water from the soil?", ['Root', 'Leaf', 'Flower', 'Fruit'], 'easy', "Roots take in water."),
    ("We should drink water that is ___.", ['Clean and safe', 'Muddy', 'From a puddle', 'Salty'], 'easy', "Clean water keeps us healthy."),
    ("Which of these is a source of light?", ['Sun', 'Moon', 'Mirror', 'Table'], 'easy', "The Moon only reflects sunlight."),
    ("How many days are there in a week?", ['7', '5', '10', '12'], 'easy', "Monday to Sunday."),
    ("How many months are there in a year?", ['12', '10', '7', '15'], 'easy', "January to December."),
    ("Which animal gives us milk?", ['Cow', 'Lion', 'Dog', 'Crow'], 'easy', "Cows, buffaloes and goats give milk."),
    ("We see with our ___.", ['Eyes', 'Ears', 'Nose', 'Tongue'], 'easy', "Sense of sight."),
    ("Which season is the hottest?", ['Summer', 'Winter', 'Spring', 'Autumn'], 'easy', "Summer."),
    ("Which of these is a fruit?", ['Mango', 'Potato', 'Carrot', 'Onion'], 'easy', "Mango grows from a flower."),
    ("Which bird is the national bird of India?", ['Peacock', 'Parrot', 'Sparrow', 'Crow'], 'easy', "Peacock."),
    ("Which is the national animal of India?", ['Tiger', 'Lion', 'Elephant', 'Cow'], 'easy', "Bengal tiger."),
    ("Which is the national flower of India?", ['Lotus', 'Rose', 'Sunflower', 'Marigold'], 'easy', "Lotus."),
    ("Who is known as the 'Father of the Nation' in India?", ['Mahatma Gandhi', 'Jawaharlal Nehru', 'Bhagat Singh', 'Subhas Chandra Bose'], 'easy', "Bapu."),
    ("Which of these keeps our teeth healthy?", ['Brushing twice a day', 'Eating many sweets', 'Not rinsing the mouth', 'Biting nails'], 'easy', "Good habits."),
    ("Which gas do we breathe in to live?", ['Oxygen', 'Carbon dioxide', 'Smoke', 'Nitrogen only'], 'easy', "We breathe out carbon dioxide."),
    ("Which of these is a means of water transport?", ['Ship', 'Bus', 'Train', 'Aeroplane'], 'easy', "Boats and ships."),
    ("The festival of lights is ___.", ['Diwali', 'Holi', 'Eid', 'Christmas'], 'easy', "Deepawali."),
    ("Which planet do we live on?", ['Earth', 'Mars', 'Jupiter', 'Venus'], 'easy', "Earth."),
    ("Which of these is a wild animal?", ['Fox', 'Cow', 'Dog', 'Hen'], 'easy', "Lives in the forest."),
    ("Water turns into ice when it is ___.", ['Cooled (frozen)', 'Boiled', 'Stirred', 'Coloured'], 'easy', "Freezes at 0 °C."),
    ("We should cross the road at the ___.", ['Zebra crossing', 'Middle of the road', 'Turning', 'Parking'], 'easy', "Road safety."),
    ("A doctor who treats animals is a ___.", ['Veterinarian', 'Dentist', 'Surgeon', 'Pharmacist'], 'easy', "Vet."),
    ("Which of these is a living thing?", ['Plant', 'Stone', 'Chair', 'Pen'], 'easy', "Plants grow and breathe."),
]
register('evs.general', EVS, 'Environmental Studies', rows=EVS_BANK)
