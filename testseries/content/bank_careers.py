"""Pools for the professional and entrance exams added in late 2026: pharmacy (GPAT, NIPER, pharmacist posts), nursing,
agriculture (ICAR), hotel management (NCHM JEE), design (UCEED, CEED, NID), legal reasoning (CLAT, AIBE),
plus more English usage and reading passages for every exam. Static facts only.

Rows are (question, [correct, wrong, wrong, wrong], difficulty, explanation); the correct option is shuffled at build time.
"""
from .core import register, table_topics

PHA, NUR, ARD, HSP, DSG, LGL, ENG, CDP = 'PHA1', 'NUR1', 'ARD1', 'HSP1', 'DSG1', 'LGL1', 'ENG1', 'CDP1'


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


# ------------------------------------------------------------------ Pharmacy
DRUG_SOURCES = rows("""
Quinine|Cinchona bark
Morphine|Opium poppy (Papaver somniferum)
Digoxin|Foxglove (Digitalis lanata)
Reserpine|Rauwolfia serpentina
Atropine|Atropa belladonna
Vincristine|Madagascar periwinkle (Catharanthus roseus)
Paclitaxel (Taxol)|Pacific yew (Taxus brevifolia)
Artemisinin|Sweet wormwood (Artemisia annua)
Ephedrine|Ephedra
Colchicine|Autumn crocus (Colchicum autumnale)
Emetine|Ipecac (Carapichea ipecacuanha)
Cocaine|Coca (Erythroxylum coca)
Physostigmine|Calabar bean (Physostigma venenosum)
Pilocarpine|Jaborandi (Pilocarpus)
Ergotamine|Ergot fungus (Claviceps purpurea)
Tubocurarine|Curare (Chondrodendron tomentosum)
Strychnine|Nux vomica (Strychnos nux-vomica)
Penicillin|Penicillium mould
Streptomycin|Streptomyces griseus
Sennosides|Senna (Cassia angustifolia)
""")
table_topics('pharmacy.pharmacognosy', PHA, 'Pharmacognosy – Drugs & Sources', DRUG_SOURCES, [
    ("{a} is obtained from ___.", 'b', "{a} comes from {b}."),
    ("Which drug is obtained from {b}?", 'a', "{a} comes from {b}."),
])

DC_SCHEDULES = rows("""
Schedule H|Prescription drugs to be sold only on a doctor's prescription
Schedule X|Narcotic and psychotropic drugs needing special prescription records
Schedule M|Good Manufacturing Practices (GMP)
Schedule Y|Requirements for clinical trials (now under the New Drugs and Clinical Trials Rules, 2019)
Schedule C|Biological and special products such as vaccines and sera
Schedule G|Drugs to be used under medical supervision
""")
table_topics('pharmacy.jurisprudence', PHA, 'Pharmaceutical Jurisprudence', DC_SCHEDULES, [
    ("Under the Drugs and Cosmetics Rules, {a} deals with ___.", 'b', "{a}: {b}."),
    ("Which schedule of the Drugs and Cosmetics Rules covers: {b}?", 'a', "{a}: {b}."),
], difficulty='medium')

register('pharmacy.core', PHA, 'Pharmaceutics & Pharmacology', rows=[
    ("The Drugs and Cosmetics Act was passed in ___.", ['1940', '1948', '1955', '1985'], 'easy', "Rules followed in 1945."),
    ("The Pharmacy Act, which set up the Pharmacy Council of India, was passed in ___.", ['1948', '1940', '1956', '1961'], 'easy', "Pharmacy Act, 1948."),
    ("The NDPS Act was enacted in ___.", ['1985', '1940', '1971', '2000'], 'easy', "Narcotic Drugs and Psychotropic Substances Act."),
    ("The first edition of the Indian Pharmacopoeia was published in ___.", ['1955', '1947', '1966', '1985'], 'medium', "IP 1955."),
    ("The bioavailability of a drug given intravenously is ___.", ['100%', '50%', '75%', 'Zero'], 'easy', "It enters circulation directly."),
    ("In first-order kinetics, the rate of elimination is ___.", ['Proportional to drug concentration', 'Constant regardless of concentration', 'Zero', 'Independent of dose'], 'medium', "A constant fraction is eliminated per unit time."),
    ("In zero-order kinetics, the drug is eliminated at ___.", ['A constant amount per unit time', 'A constant fraction per unit time', 'An increasing rate', 'No measurable rate'], 'medium', "Example: ethanol at usual doses."),
    ("About how many half-lives are needed to eliminate ~97% of a drug?", ['5', '2', '3', '10'], 'medium', "After 5 half-lives about 3% remains."),
    ("The Noyes–Whitney equation describes the ___.", ['Rate of dissolution', 'Rate of sedimentation', 'Flow of powders', 'Viscosity of liquids'], 'medium', "dC/dt = DA(Cs − C)/h."),
    ("Stokes' law is used to describe ___.", ['Sedimentation velocity of particles', 'Dissolution rate', 'Drug absorption', 'Partition coefficient'], 'medium', "Suspensions."),
    ("The Henderson–Hasselbalch equation relates pH to ___.", ['pKa and the ratio of ionised to un-ionised drug', 'Viscosity', 'Particle size', 'Melting point'], 'medium', "Predicts ionisation."),
    ("The angle of repose is a measure of ___.", ['Flowability of powders', 'Tablet hardness', 'Solubility', 'pH'], 'easy', "Lower angle = better flow."),
    ("Magnesium stearate is used in tablets as a ___.", ['Lubricant', 'Disintegrant', 'Binder', 'Coating agent'], 'easy', "Reduces friction during ejection."),
    ("Croscarmellose sodium is used in tablets as a ___.", ['Superdisintegrant', 'Lubricant', 'Glidant', 'Sweetener'], 'medium', "Promotes break-up."),
    ("Cellulose acetate phthalate is used for ___.", ['Enteric coating', 'Sugar coating', 'Lubrication', 'Granulation only'], 'medium', "Resists gastric acid."),
    ("Cocoa butter (theobroma oil) is used as a ___.", ['Suppository base', 'Tablet binder', 'Ointment preservative', 'Emulsifier'], 'easy', "Melts at body temperature."),
    ("An isotonic sodium chloride solution has a concentration of ___.", ['0.9% w/v', '9% w/v', '0.09% w/v', '5% w/v'], 'easy', "Normal saline."),
    ("Standard autoclave conditions are ___.", ['121 °C at 15 psi for 15 minutes', '100 °C for 5 minutes', '160 °C for 2 hours', '70 °C for 30 minutes'], 'easy', "Moist-heat sterilisation."),
    ("Dry-heat (hot-air oven) sterilisation is usually done at ___.", ['160 °C for 2 hours', '121 °C for 15 minutes', '60 °C for 1 hour', '250 °C for 5 minutes'], 'medium', "Glassware and powders."),
    ("The biological indicator for autoclave validation is spores of ___.", ['Geobacillus stearothermophilus', 'Bacillus atrophaeus', 'E. coli', 'Staphylococcus aureus'], 'hard', "Heat-resistant spores."),
    ("The LAL test detects ___.", ['Bacterial endotoxins', 'Fungal spores', 'Heavy metals', 'Particulate matter'], 'medium', "Limulus amoebocyte lysate."),
    ("HLB values of emulsifiers suitable for oil-in-water emulsions are about ___.", ['8–18', '1–3', '3–6', '20–30'], 'hard', "Low HLB (3–6) suits water-in-oil."),
    ("Paracetamol overdose is treated with ___.", ['N-acetylcysteine', 'Naloxone', 'Atropine', 'Flumazenil'], 'easy', "Replenishes glutathione."),
    ("Aspirin acts by irreversibly inhibiting ___.", ['Cyclooxygenase (COX)', 'Lipoxygenase', 'Acetylcholinesterase', 'MAO'], 'medium', "Reduces prostaglandin and thromboxane synthesis."),
    ("Metformin belongs to the class ___.", ['Biguanides', 'Sulfonylureas', 'Thiazolidinediones', 'DPP-4 inhibitors'], 'easy', "First-line in type 2 diabetes."),
    ("Omeprazole is a ___.", ['Proton pump inhibitor', 'H2 blocker', 'Antacid', 'Prokinetic'], 'easy', "Blocks H⁺/K⁺-ATPase."),
    ("Warfarin acts by antagonising ___.", ['Vitamin K', 'Vitamin C', 'Vitamin D', 'Thrombin directly'], 'medium', "Reduces clotting factors II, VII, IX, X."),
    ("Which drug is a beta-lactam antibiotic?", ['Amoxicillin', 'Ciprofloxacin', 'Azithromycin', 'Doxycycline'], 'easy', "Penicillin group."),
    ("Salbutamol is used in asthma as a ___.", ['β2-agonist bronchodilator', 'Corticosteroid', 'Antihistamine', 'Leukotriene antagonist'], 'easy', "Short-acting β2 agonist."),
    ("Therapeutic drug monitoring is essential for drugs with a ___.", ['Narrow therapeutic index', 'Wide therapeutic index', 'Short shelf life', 'High solubility'], 'medium', "e.g. digoxin, lithium, phenytoin."),
])

# ------------------------------------------------------------------ Nursing
register('nursing.core', NUR, 'Nursing Foundations', rows=[
    ("The normal resting pulse rate of an adult is ___.", ['60–100 beats/min', '40–60 beats/min', '100–140 beats/min', '20–40 beats/min'], 'easy', "Adult normal range."),
    ("The normal respiratory rate of an adult is ___.", ['12–20 breaths/min', '30–40 breaths/min', '5–10 breaths/min', '25–35 breaths/min'], 'easy', "Adult normal range."),
    ("Normal body temperature (oral) is about ___.", ['37 °C (98.6 °F)', '35 °C (95 °F)', '39 °C (102.2 °F)', '36 °C (94 °F)'], 'easy', "Average oral temperature."),
    ("The normal fetal heart rate is ___.", ['110–160 beats/min', '60–100 beats/min', '160–200 beats/min', '80–110 beats/min'], 'medium', "Per current obstetric guidelines."),
    ("The APGAR score is assessed at ___.", ['1 and 5 minutes after birth', '10 and 20 minutes', 'Only at 24 hours', 'Before birth'], 'easy', "Repeated at 10 minutes if low."),
    ("The Mantoux test is read after ___.", ['48–72 hours', '6 hours', '7 days', '15 minutes'], 'medium', "Induration measured in mm."),
    ("Intradermal injections are given at an angle of ___.", ['10–15°', '45°', '90°', '60°'], 'easy', "Bevel up, just under the epidermis."),
    ("Intramuscular injections are given at an angle of ___.", ['90°', '15°', '30°', '5°'], 'easy', "Straight into the muscle."),
    ("The Z-track technique is used to give ___.", ['Irritating IM drugs such as iron', 'Insulin', 'Intradermal vaccines', 'IV fluids'], 'medium', "Prevents leakage into tissue."),
    ("Fowler's position means the patient is ___.", ['Semi-sitting with the head raised 45–60°', 'Lying flat on the back', 'Lying on the abdomen', 'In the left lateral position'], 'easy', "Eases breathing."),
    ("The left lateral (Sims') position is commonly used for ___.", ['Giving an enema', 'Lumbar puncture only', 'Childbirth', 'Chest physiotherapy'], 'medium', "Follows the descending colon."),
    ("In adult CPR, the compression-to-ventilation ratio (single rescuer) is ___.", ['30:2', '15:2', '5:1', '10:1'], 'easy', "Per BLS guidelines."),
    ("The recommended chest compression rate in CPR is ___.", ['100–120 per minute', '60–80 per minute', '140–160 per minute', '40–60 per minute'], 'easy', "BLS guidelines."),
    ("By the 'Rule of Nines', each upper limb of an adult represents ___ of body surface area.", ['9%', '18%', '1%', '4.5%'], 'medium', "Each lower limb is 18%."),
    ("Colostrum is especially rich in ___.", ['IgA antibodies', 'Fat only', 'Iron only', 'Vitamin C only'], 'easy', "Protects the newborn's gut."),
    ("Exclusive breastfeeding is recommended for the first ___.", ['6 months', '3 months', '12 months', '1 month'], 'easy', "WHO recommendation."),
    ("BCG vaccine is given ___.", ['Intradermally at birth', 'Orally at 6 weeks', 'Intramuscularly at 9 months', 'Subcutaneously at 5 years'], 'easy', "Left upper arm."),
    ("A normal pregnancy lasts about ___.", ['40 weeks (280 days)', '36 weeks', '44 weeks', '32 weeks'], 'easy', "From the last menstrual period."),
    ("The minimum normal urine output for an adult is about ___.", ['0.5 mL/kg/hour', '5 mL/kg/hour', '0.05 mL/kg/hour', '3 mL/kg/hour'], 'medium', "About 30 mL/hour for an average adult."),
    ("Hand hygiene is the single most important measure to prevent ___.", ['Hospital-acquired infections', 'Pressure sores', 'Falls', 'Medication errors'], 'easy', "WHO 'My 5 Moments'."),
    ("Bedsores (pressure ulcers) are prevented mainly by ___.", ['Changing the patient\'s position every 2 hours', 'Giving antibiotics', 'Keeping the patient NPO', 'Using hot water bottles'], 'easy', "Relieve pressure regularly."),
    ("A sphygmomanometer measures ___.", ['Blood pressure', 'Body temperature', 'Blood sugar', 'Oxygen saturation'], 'easy', "With a stethoscope."),
    ("A pulse oximeter measures ___.", ['Oxygen saturation (SpO₂)', 'Blood pressure', 'Respiratory rate only', 'Haemoglobin type'], 'easy', "Normal 95–100%."),
    ("Oral rehydration solution is used mainly to treat ___.", ['Dehydration due to diarrhoea', 'Hypertension', 'Anaemia', 'Asthma'], 'easy', "WHO low-osmolarity ORS."),
    ("The universal blood donor group is ___.", ['O negative', 'AB positive', 'A positive', 'B negative'], 'easy', "No A, B or Rh antigens on red cells."),
])

# ------------------------------------------------------------------ Agriculture
AGRI_INSTITUTES = rows("""
Indian Agricultural Research Institute (IARI)|New Delhi
National Rice Research Institute|Cuttack
National Dairy Research Institute|Karnal
Indian Institute of Horticultural Research|Bengaluru
Central Potato Research Institute|Shimla
Sugarcane Breeding Institute|Coimbatore
Central Arid Zone Research Institute|Jodhpur
Indian Veterinary Research Institute|Izatnagar (Bareilly)
Central Institute of Fisheries Education|Mumbai
National Research Centre for Banana|Tiruchirappalli
Indian Institute of Pulses Research|Kanpur
Central Tobacco Research Institute|Rajahmundry
Indian Institute of Spices Research|Kozhikode
Central Coffee Research Institute|Chikmagalur
""")
table_topics('agriculture.institutes', ARD, 'Agricultural Research Institutes', AGRI_INSTITUTES, [
    ("The {a} is located at ___.", 'b', "{a}: {b}."),
    ("Which institute is located at {b}?", 'a', "{a}: {b}."),
])

REVOLUTIONS = rows("""
Green Revolution|Foodgrains (wheat and rice)
White Revolution|Milk
Blue Revolution|Fish
Yellow Revolution|Oilseeds
Silver Revolution|Eggs
Round Revolution|Potato
Brown Revolution|Leather / cocoa
""")
table_topics('agriculture.revolutions', ARD, 'Agricultural Revolutions', REVOLUTIONS, [
    ("The {a} is associated with ___.", 'b', "{a}: {b}."),
    ("Which revolution is associated with {b}?", 'a', "{a}: {b}."),
], difficulty='easy')

register('agriculture.core', ARD, 'Agriculture & Rural Development', rows=[
    ("Kharif crops are sown at the onset of the ___.", ['South-west monsoon (June–July)', 'Winter (October–November)', 'Summer (March–April)', 'Spring (February)'], 'easy', "Rice, maize, cotton."),
    ("Which is a rabi crop?", ['Wheat', 'Rice', 'Cotton', 'Maize'], 'easy', "Sown in winter, harvested in spring."),
    ("Which is a zaid crop?", ['Watermelon', 'Wheat', 'Mustard', 'Gram'], 'easy', "Short summer season."),
    ("Nitrogen-fixing bacteria in the root nodules of legumes belong to the genus ___.", ['Rhizobium', 'Azotobacter', 'Lactobacillus', 'Clostridium'], 'easy', "Symbiotic fixation."),
    ("Azolla is used as a biofertiliser mainly in ___ fields.", ['Paddy', 'Wheat', 'Cotton', 'Sugarcane'], 'medium', "Hosts the cyanobacterium Anabaena."),
    ("Urea contains about ___ nitrogen.", ['46%', '16%', '21%', '60%'], 'easy', "Highest N content among solid fertilisers."),
    ("DAP (diammonium phosphate) has an N–P₂O₅ ratio of ___.", ['18–46', '46–0', '10–26', '20–20'], 'medium', "18% N, 46% P₂O₅."),
    ("Muriate of potash contains about ___ K₂O.", ['60%', '46%', '18%', '30%'], 'medium', "Potassium chloride."),
    ("Bt cotton contains a gene from ___.", ['Bacillus thuringiensis', 'Agrobacterium tumefaciens', 'E. coli', 'Rhizobium'], 'easy', "Cry toxin against bollworms."),
    ("Golden rice is enriched with ___.", ['β-carotene (provitamin A)', 'Iron', 'Vitamin C', 'Protein'], 'easy', "To fight vitamin A deficiency."),
    ("Laterite soil is suitable for ___.", ['Tea, coffee and cashew', 'Wheat', 'Cotton', 'Mustard'], 'medium', "Leached, acidic soil."),
    ("The ideal soil pH for most crops is ___.", ['6.0–7.5', '3.0–4.0', '9.0–10.0', '1.0–2.0'], 'medium', "Near neutral."),
    ("Gypsum is applied to reclaim ___ soils.", ['Alkaline (sodic)', 'Acidic', 'Peaty', 'Laterite'], 'medium', "Calcium replaces sodium."),
    ("Lime is applied to correct ___ soils.", ['Acidic', 'Alkaline', 'Saline', 'Waterlogged'], 'medium', "Raises soil pH."),
    ("ICAR was established in ___.", ['1929', '1947', '1965', '1905'], 'medium', "As the Imperial Council of Agricultural Research."),
    ("NABARD is the apex institution for ___.", ['Agriculture and rural development credit', 'Industrial finance', 'Housing finance', 'Export credit'], 'easy', "Set up in 1982."),
    ("The minimum support price (MSP) is recommended by the ___.", ['Commission for Agricultural Costs and Prices', 'NABARD', 'FCI', 'NITI Aayog'], 'medium', "CACP."),
    ("India's largest producer of milk among states (recent years) is ___.", ['Uttar Pradesh', 'Punjab', 'Gujarat', 'Kerala'], 'medium', "UP leads total milk production."),
    ("Drip irrigation mainly helps to ___.", ['Save water by delivering it at the root zone', 'Flood the field', 'Drain excess water', 'Increase soil salinity'], 'easy', "Up to 40–60% water saving."),
    ("Kisan Credit Card provides farmers with ___.", ['Short-term crop credit', 'Free seeds', 'Crop insurance only', 'Land titles'], 'easy', "Revolving credit."),
    ("PM-KISAN gives eligible farmers ___ per year.", ['₹6,000 in three instalments', '₹10,000 at once', '₹2,000 once', '₹12,000 monthly'], 'easy', "Direct benefit transfer."),
    ("Vermicompost is prepared with the help of ___.", ['Earthworms', 'Honeybees', 'Silkworms', 'Termites'], 'easy', "Organic manure."),
    ("Sericulture is the rearing of ___.", ['Silkworms', 'Bees', 'Fish', 'Lac insects'], 'easy', "For silk."),
    ("Apiculture refers to ___.", ['Beekeeping', 'Fish farming', 'Silk farming', 'Fruit farming'], 'easy', "For honey and wax."),
    ("Which crop is called the 'golden fibre'?", ['Jute', 'Cotton', 'Silk', 'Coir'], 'easy', "Jute."),
])

# ------------------------------------------------------------------ Hotel management (NCHM JEE)
register('hospitality.aptitude', HSP, 'Aptitude for Service Sector', rows=[
    ("'Mise en place' in a kitchen means ___.", ['Everything in its place before service', 'Main course', 'Cleaning after service', 'A type of sauce'], 'easy', "Preparation and organisation."),
    ("An 'à la carte' menu means ___.", ['Each dish is priced separately', 'A fixed menu at a fixed price', 'A buffet', 'A children\'s menu'], 'easy', "Order item by item."),
    ("A 'table d'hôte' menu is ___.", ['A set menu at a fixed price', 'Dishes priced individually', 'Only desserts', 'A drinks list'], 'medium', "Fixed courses."),
    ("A 'sommelier' is a ___.", ['Wine steward', 'Pastry chef', 'Room attendant', 'Front-office manager'], 'easy', "Wine service."),
    ("The 'sous chef' is the ___.", ['Second-in-command in the kitchen', 'Head of housekeeping', 'Junior trainee cook', 'Bar manager'], 'easy', "Under the executive chef."),
    ("A 'commis' in the kitchen is a ___.", ['Junior cook', 'Head chef', 'Restaurant manager', 'Wine waiter'], 'easy', "Entry-level chef."),
    ("Under the American Plan (AP), the room tariff includes ___.", ['Room and all three meals', 'Room only', 'Room and breakfast', 'Room and dinner only'], 'medium', "Full board."),
    ("Under the Continental Plan (CP), the tariff includes ___.", ['Room and breakfast', 'Room only', 'Room and all meals', 'Room, breakfast and dinner'], 'medium', "Bed and breakfast."),
    ("Under the European Plan (EP), the tariff includes ___.", ['Room only', 'Room and breakfast', 'Room and all meals', 'Room and lunch'], 'medium', "No meals."),
    ("Under the Modified American Plan (MAP), the tariff includes ___.", ['Room, breakfast and one major meal', 'Room only', 'All meals', 'Breakfast only'], 'medium', "Half board."),
    ("Cutting vegetables into thin matchstick strips is called ___.", ['Julienne', 'Brunoise', 'Chiffonade', 'Paysanne'], 'easy', "Classical cut."),
    ("A 'roux' is made of ___.", ['Flour and fat cooked together', 'Egg yolk and oil', 'Milk and sugar', 'Stock and wine'], 'easy', "Thickens sauces."),
    ("Hollandaise sauce is an emulsion of ___.", ['Egg yolk and butter', 'Flour and milk', 'Tomato and stock', 'Brown stock and roux'], 'medium', "One of the mother sauces."),
    ("Béchamel sauce is made from ___.", ['Milk thickened with a white roux', 'Brown stock', 'Egg yolk and butter', 'Tomatoes'], 'easy', "White sauce."),
    ("The 'danger zone' for bacterial growth in food is about ___.", ['5 °C to 60 °C', '−18 °C to 0 °C', '70 °C to 100 °C', '0 °C to 2 °C'], 'medium', "Keep hot food hot, cold food cold."),
    ("FSSAI is the regulator for ___.", ['Food safety and standards', 'Hotel star ratings', 'Tourism visas', 'Restaurant taxes'], 'easy', "Food Safety and Standards Authority of India."),
    ("A guest complains that the room is not clean. The best first response is to ___.", ['Apologise and arrange cleaning or a room change at once', 'Argue that it was cleaned', 'Ask the guest to clean it', 'Ignore the complaint'], 'easy', "Service recovery."),
    ("The 'concierge' in a hotel ___.", ['Assists guests with bookings, directions and services', 'Cooks the meals', 'Cleans rooms', 'Handles payroll'], 'easy', "Guest services."),
    ("A 'DND' card on a room door means ___.", ['Do Not Disturb', 'Daily Night Delivery', 'Do Not Dine', 'Door Needs Damage repair'], 'easy', "Housekeeping must not enter."),
    ("A room with two single beds is called a ___ room.", ['Twin', 'Double', 'Suite', 'Studio'], 'easy', "Twin room."),
])

# ------------------------------------------------------------------ Design
register('design.aptitude', DSG, 'Design & Visual Aptitude', rows=[
    ("The primary colours of light (additive model) are ___.", ['Red, green and blue', 'Red, yellow and blue', 'Cyan, magenta and yellow', 'Orange, green and violet'], 'easy', "RGB, used in screens."),
    ("The colour model used in printing is ___.", ['CMYK', 'RGB', 'HSB', 'LAB only'], 'easy', "Cyan, magenta, yellow, key (black)."),
    ("In the traditional colour wheel, the complementary colour of blue is ___.", ['Orange', 'Green', 'Violet', 'Red'], 'easy', "Opposite on the RYB wheel."),
    ("The golden ratio is approximately ___.", ['1.618', '1.414', '3.142', '2.718'], 'easy', "φ = (1 + √5)/2."),
    ("A drawing with a single vanishing point uses ___ perspective.", ['One-point', 'Two-point', 'Three-point', 'Isometric'], 'easy', "Lines converge to one point."),
    ("In isometric projection, the three axes are drawn at ___ to each other.", ['120°', '90°', '60°', '45°'], 'medium', "Equal angles."),
    ("The Bauhaus school was founded by ___.", ['Walter Gropius', 'Le Corbusier', 'Frank Lloyd Wright', 'Charles Eames'], 'medium', "Weimar, 1919."),
    ("The city of Chandigarh was planned by ___.", ['Le Corbusier', 'Edwin Lutyens', 'Charles Correa', 'B. V. Doshi'], 'easy', "1950s."),
    ("The Lotus Temple in Delhi was designed by ___.", ['Fariborz Sahba', 'Charles Correa', 'Laurie Baker', 'Raj Rewal'], 'medium', "Bahá'í House of Worship."),
    ("'Kerning' in typography refers to ___.", ['Adjusting space between individual letters', 'Spacing between lines', 'Font weight', 'Text colour'], 'medium', "Letter-pair spacing."),
    ("'Leading' in typography refers to ___.", ['Spacing between lines of text', 'Spacing between letters', 'The first letter of a paragraph', 'Font size'], 'medium', "Line spacing."),
    ("A typeface with small strokes at the ends of letters is called ___.", ['Serif', 'Sans-serif', 'Monospace', 'Script'], 'easy', "e.g. Times New Roman."),
    ("Vector graphics, unlike raster images, ___.", ['Scale without losing quality', 'Are made of pixels', 'Cannot be coloured', 'Are always photographs'], 'easy', "Defined by paths."),
    ("Which shape gives the greatest area for a fixed perimeter?", ['Circle', 'Square', 'Equilateral triangle', 'Rectangle'], 'medium', "Isoperimetric property."),
    ("The 'rule of thirds' is a guideline used in ___.", ['Composition of images', 'Colour mixing', 'Font selection', 'Printing'], 'easy', "Place subjects on the grid lines."),
])

# ------------------------------------------------------------------ Legal reasoning (principle → facts)
register('law.legal_reasoning', LGL, 'Legal Reasoning', rows=[
    ("Principle: A person is liable for negligence if he owes a duty of care, breaches it, and the breach causes harm.\n"
     "Facts: A shopkeeper leaves a wet floor without a warning sign. A customer slips and breaks her arm.\nIs the shopkeeper liable?",
     ['Yes, he breached his duty of care and caused the injury', 'No, customers enter at their own risk', 'No, floors are always wet', 'Yes, but only if the customer bought something'], 'easy', "All three elements are present."),
    ("Principle: An offer must be accepted unconditionally for a contract to arise; a conditional acceptance is a counter-offer.\n"
     "Facts: A offers to sell his car to B for ₹5 lakh. B replies, 'I accept if you reduce it to ₹4.5 lakh.'\nIs there a contract?",
     ['No, B made a counter-offer', 'Yes, at ₹5 lakh', 'Yes, at ₹4.5 lakh', 'Yes, at ₹4.75 lakh'], 'easy', "Acceptance must mirror the offer."),
    ("Principle: Silence does not amount to acceptance.\n"
     "Facts: A writes to B, 'If I hear nothing from you by Monday, I shall consider my horse sold to you for ₹50,000.' B does not reply.\nIs there a contract?",
     ['No, silence is not acceptance', 'Yes, B accepted by silence', 'Yes, because A set a deadline', 'Only if the horse is delivered'], 'medium', "Felthouse v. Bindley."),
    ("Principle: A person who voluntarily consents to a risk cannot claim damages for harm arising from that risk (volenti non fit injuria).\n"
     "Facts: A spectator at a cricket match is hit by a ball struck over the boundary in the normal course of play.\nCan the spectator claim damages?",
     ['No, he consented to the ordinary risks of watching', 'Yes, the batsman is liable', 'Yes, the stadium is always liable', 'Only if the match was lost'], 'medium', "Ordinary risks of the game."),
    ("Principle: Trespass to land is any unjustified intrusion on land in another's possession.\n"
     "Facts: X, without permission, walks across Y's fenced farm as a shortcut. No damage is done.\nHas X committed trespass?",
     ['Yes, trespass is actionable without proof of damage', 'No, because no damage was caused', 'No, shortcuts are allowed', 'Only if Y was present'], 'medium', "Trespass is actionable per se."),
    ("Principle: A person who keeps a dangerous thing on his land is liable if it escapes and causes damage, even without negligence.\n"
     "Facts: A stores large quantities of water in a reservoir. It bursts and floods B's mine.\nIs A liable?",
     ['Yes, under strict liability', 'No, A was not negligent', 'No, floods are acts of God', 'Only if A built it himself'], 'medium', "Rylands v. Fletcher."),
    ("Principle: An agreement made under coercion is voidable at the option of the party coerced.\n"
     "Facts: P signs a sale deed after Q threatens to harm P's son.\nWhat is the status of the agreement?",
     ['Voidable at P\'s option', 'Valid and binding', 'Void from the start', 'Valid only if registered'], 'medium', "Section 19, Indian Contract Act."),
    ("Principle: An employer is vicariously liable for wrongs committed by an employee in the course of employment.\n"
     "Facts: A delivery driver, while delivering a parcel for his company, negligently hits a pedestrian.\nWho is liable?",
     ['The company, as the employer', 'Only the pedestrian', 'No one', 'Only the parcel\'s recipient'], 'easy', "Course of employment."),
    ("Principle: A person has a right of private defence of his body against an assault that causes reasonable fear of death or grievous hurt.\n"
     "Facts: A attacks B with a knife. B pushes A away, and A falls and is hurt.\nIs B guilty of an offence?",
     ['No, B acted in private defence', 'Yes, B caused hurt', 'Yes, B should have run away', 'Only if A was seriously injured'], 'easy', "Reasonable, proportionate force."),
    ("Principle: Nobody can transfer a better title than he himself has (nemo dat quod non habet).\n"
     "Facts: A steals B's bicycle and sells it to C, who does not know it was stolen.\nWho owns the bicycle?",
     ['B', 'C', 'A', 'The police'], 'medium', "A thief has no title to pass."),
    ("Principle: Ignorance of the law is no excuse.\n"
     "Facts: A foreign tourist carries a banned item into India, claiming he did not know it was illegal.\nCan he avoid liability on this ground?",
     ['No, ignorance of the law is no excuse', 'Yes, he is a foreigner', 'Yes, if he apologises', 'Only if he leaves the country'], 'easy', "Ignorantia juris non excusat."),
    ("Principle: Defamation is the publication of a false statement that harms a person's reputation; truth is a defence.\n"
     "Facts: A newspaper truthfully reports that a minister was convicted of bribery.\nIs the newspaper liable for defamation?",
     ['No, truth is a defence', 'Yes, it harmed his reputation', 'Yes, ministers cannot be criticised', 'Only if the article was on the front page'], 'easy', "Justification by truth."),
])

# ------------------------------------------------------------------ English usage (all exams)
register('english.error_spotting', ENG, 'Error Spotting', rows=[
    ("Spot the error: Neither the manager (A) / nor his assistants (B) / was present. (C) / No error (D)", ['C', 'A', 'B', 'D'], 'medium', "With 'neither…nor', the verb agrees with the nearer subject: 'were present'."),
    ("Spot the error: He is senior (A) / than me (B) / in the office. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "'Senior to me'."),
    ("Spot the error: I prefer tea (A) / than coffee (B) / in the morning. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "'Prefer … to'."),
    ("Spot the error: The news (A) / are very (B) / encouraging. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "'News' takes a singular verb: 'is'."),
    ("Spot the error: She has been (A) / living here (B) / since five years. (C) / No error (D)", ['C', 'A', 'B', 'D'], 'easy', "'For five years' – 'for' with a period of time."),
    ("Spot the error: If I was (A) / you, I would (B) / accept the offer. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'medium', "Subjunctive: 'If I were you'."),
    ("Spot the error: The police (A) / has arrested (B) / the thief. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Police' is plural: 'have arrested'."),
    ("Spot the error: Hardly had he left (A) / when it started (B) / to rain heavily. (C) / No error (D)", ['D', 'A', 'B', 'C'], 'hard', "'Hardly … when' is correct."),
    ("Spot the error: He gave me (A) / an advice (B) / on my career. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "'Advice' is uncountable: 'some advice' / 'a piece of advice'."),
    ("Spot the error: Each boy and each girl (A) / were given (B) / a prize. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Each … and each' takes a singular verb: 'was given'."),
])

register('english.sentence_improvement', ENG, 'Sentence Improvement', rows=[
    ("Improve the underlined part: 'He did not attend the meeting because of he was ill.'", ['because he was ill', 'due to he was ill', 'because of being he ill', 'No improvement'], 'easy', "'Because' + clause."),
    ("Improve the underlined part: 'I am looking forward to meet you.'", ['to meeting you', 'for meeting you', 'meet you', 'No improvement'], 'easy', "'Look forward to' + -ing."),
    ("Improve the underlined part: 'She is one of those who always speaks the truth.'", ['who always speak the truth', 'who always is speaking the truth', 'whom always speaks the truth', 'No improvement'], 'hard', "'Who' refers to 'those' (plural)."),
    ("Improve the underlined part: 'Scarcely had I reached the station than the train left.'", ['when the train left', 'then the train left', 'and the train left', 'No improvement'], 'medium', "'Scarcely … when'."),
    ("Improve the underlined part: 'He is too weak that he cannot walk.'", ['so weak that he cannot walk', 'very weak that he cannot walk', 'too weak so he cannot walk', 'No improvement'], 'medium', "'So … that' or 'too … to'."),
    ("Improve the underlined part: 'The teacher as well as the students were present.'", ['was present', 'are present', 'have been present', 'No improvement'], 'medium', "'As well as' – verb agrees with the first subject."),
    ("Improve the underlined part: 'Let us discuss about the plan.'", ['discuss the plan', 'discuss on the plan', 'discuss over the plan', 'No improvement'], 'easy', "'Discuss' takes a direct object."),
    ("Improve the underlined part: 'He has returned back from Mumbai.'", ['has returned from Mumbai', 'has came back from Mumbai', 'had returned back', 'No improvement'], 'easy', "'Returned back' is redundant."),
])

register('english.voice_narration', ENG, 'Active-Passive & Narration', rows=[
    ("Change into passive voice: 'They have completed the project.'", ['The project has been completed by them.', 'The project was completed by them.', 'The project had been completed by them.', 'The project is completed by them.'], 'easy', "Present perfect passive: has/have been + V3."),
    ("Change into passive voice: 'Who wrote this letter?'", ['By whom was this letter written?', 'Who was this letter written?', 'By whom this letter was written?', 'Who has written this letter?'], 'medium', "Interrogative passive."),
    ("Change into passive voice: 'Close the door.'", ['Let the door be closed.', 'The door is closed.', 'The door should closed.', 'Let the door closed.'], 'medium', "Imperative passive: Let + object + be + V3."),
    ("Change into indirect speech: He said, 'I am tired.'", ['He said that he was tired.', 'He said that I am tired.', 'He said that he is tired.', 'He told that he was tired.'], 'easy', "Present → past; 'I' → 'he'."),
    ("Change into indirect speech: She said to me, 'Where do you live?'", ['She asked me where I lived.', 'She asked me where do I live.', 'She said to me where I lived.', 'She asked where did I live.'], 'medium', "Question → statement order; tense back-shifted."),
    ("Change into indirect speech: The teacher said, 'The earth revolves around the sun.'", ['The teacher said that the earth revolves around the sun.', 'The teacher said that the earth revolved around the sun.', 'The teacher told the earth revolves around the sun.', 'The teacher said that the earth had revolved around the sun.'], 'medium', "Universal truths keep the present tense."),
    ("Change into indirect speech: He said to me, 'Please help me.'", ['He requested me to help him.', 'He said me to help him.', 'He told me that please help him.', 'He requested me that help him.'], 'easy', "Imperative with 'please' → 'requested … to'."),
])

register('english.comprehension', ENG, 'Reading Comprehension', rows=[
    ("Read the passage and answer.\n\nSolar panels convert sunlight directly into electricity. Their cost has fallen sharply over the last decade, "
     "so many farmers now use solar pumps to irrigate fields during the day without depending on diesel or the power grid.\n\n"
     "Why have many farmers started using solar pumps?",
     ['Solar panels have become cheaper and free them from diesel or grid power', 'Diesel is not sold in villages', 'Solar pumps work only at night', 'The government bans electric pumps'],
     'easy', "Falling costs and independence from diesel/grid."),
    ("Read the passage and answer.\n\nHoneybees communicate the location of food through a 'waggle dance'. The angle of the dance shows the "
     "direction relative to the sun, while its duration indicates the distance to the flowers.\n\n"
     "What does the duration of the waggle dance indicate?",
     ['The distance to the food', 'The direction of the sun', 'The type of flower', 'The number of bees needed'],
     'easy', "Stated directly."),
    ("Read the passage and answer.\n\nThe Indian Railways carries over two crore passengers a day. Because it connects remote villages to "
     "large cities, it is often called the lifeline of the nation, supporting trade, tourism and jobs.\n\n"
     "Why is the Indian Railways called the lifeline of the nation?",
     ['It links remote areas with cities and supports trade, tourism and jobs', 'It is the oldest railway in the world', 'It carries only goods', 'It runs only in big cities'],
     'easy', "The passage gives connectivity and economic support."),
    ("Read the passage and answer.\n\nScientists warn that overusing antibiotics allows bacteria to evolve resistance. When this happens, "
     "common infections become harder to treat, and doctors must rely on stronger drugs with more side effects.\n\n"
     "What is the main concern raised in the passage?",
     ['Overuse of antibiotics leads to resistant bacteria', 'Antibiotics are too expensive', 'Bacteria are always harmless', 'Doctors prescribe too few drugs'],
     'medium', "Antibiotic resistance."),
    ("Read the passage and answer.\n\nA good leader listens more than she speaks. By understanding the concerns of her team, she can make "
     "decisions that people trust and follow willingly rather than out of fear.\n\n"
     "According to the passage, people follow a good leader because ___.",
     ['They trust decisions made after listening to them', 'They are afraid of her', 'She speaks more than others', 'She never makes decisions'],
     'medium', "Trust built through listening."),
    ("Read the passage and answer.\n\nWetlands act like natural sponges. During heavy rain they soak up excess water, reducing floods, and in "
     "dry months they slowly release it, keeping streams flowing. Draining them for construction removes this protection.\n\n"
     "What is the tone of the last sentence?",
     ['Cautionary', 'Celebratory', 'Humorous', 'Indifferent'],
     'medium', "It warns about the loss of protection."),
    ("Read the passage and answer.\n\nThe Chipko movement of the 1970s saw villagers in the Himalayan region hug trees to stop them from being "
     "cut. Their non-violent protest drew national attention to forest conservation.\n\n"
     "The villagers' method of protest can best be described as ___.",
     ['Non-violent', 'Armed', 'Secret', 'Legalistic'],
     'easy', "They hugged trees peacefully."),
])

# ------------------------------------------------------------------ Teaching (CTET / TET / B.Ed)
register('teaching.pedagogy', CDP, 'Pedagogy & Inclusive Education', rows=[
    ("The National Curriculum Framework 2005 emphasises ___.", ['Connecting knowledge to life outside school', 'Rote learning', 'Textbook-centred teaching', 'Annual exams only'], 'easy', "Learning without burden."),
    ("The RTE Act, 2009 provides free and compulsory education to children aged ___.", ['6–14 years', '3–10 years', '5–15 years', '10–18 years'], 'easy', "Article 21A."),
    ("Under the RTE Act, private unaided schools must reserve ___ seats for disadvantaged children.", ['25%', '10%', '15%', '50%'], 'medium', "Section 12(1)(c)."),
    ("Continuous and Comprehensive Evaluation (CCE) covers ___.", ['Scholastic and co-scholastic areas', 'Only term-end exams', 'Only sports', 'Only homework'], 'easy', "Whole-child assessment."),
    ("Formative assessment is mainly used to ___.", ['Improve learning during instruction', 'Rank students at the end', 'Select toppers', 'Fail weak students'], 'easy', "Assessment for learning."),
    ("Dyslexia is a learning difficulty related to ___.", ['Reading', 'Writing numbers', 'Motor skills', 'Hearing'], 'easy', "Dyscalculia relates to maths; dysgraphia to writing."),
    ("Dyscalculia is a learning difficulty related to ___.", ['Mathematics', 'Reading', 'Speech', 'Vision'], 'easy', "Number sense."),
    ("Inclusive education means ___.", ['Children with diverse needs learn together in regular classrooms', 'Separate schools for every disability', 'Only gifted children are taught', 'Home schooling for all'], 'easy', "Equity in the mainstream."),
    ("The National Education Policy 2020 proposes the school structure ___.", ['5+3+3+4', '10+2', '5+5+2', '4+4+4'], 'easy', "Foundational, preparatory, middle, secondary."),
    ("According to NEP 2020, the medium of instruction should preferably be the mother tongue at least until ___.", ['Grade 5', 'Grade 2', 'Grade 10', 'Grade 12'], 'medium', "Preferably till Grade 8 and beyond."),
    ("A teacher who uses group work and peer learning is applying ___.", ['Collaborative learning', 'Rote learning', 'Behaviour punishment', 'Lecture method only'], 'easy', "Vygotsky's social constructivism."),
    ("'Learning by doing' is associated with ___.", ['John Dewey', 'Pavlov', 'Skinner', 'Freud'], 'easy', "Progressive education."),
])
