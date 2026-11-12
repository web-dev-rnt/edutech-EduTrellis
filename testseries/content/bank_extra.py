"""More NEET/JEE science, medical subjects, environment, design, decision making and agriculture."""
from .core import register, table_topics


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


PHY, CHE, BIO, MED = 'PHY1', 'CHE1', 'BIO1', 'MED1'

register('physics.modern', PHY, 'Modern Physics & Electronics', rows=[
    ("The energy of a photon is given by ___.", ['E = hν', 'E = mc', 'E = ½mv²', 'E = qV²'], 'easy', "Planck's relation."),
    ("The work function of a metal is the ___.", ['Minimum energy needed to eject an electron', 'Maximum KE of photoelectrons', 'Energy of a photon', 'Stopping potential'], 'easy', "φ = hν₀."),
    ("Stopping potential in the photoelectric effect depends on ___.", ['Frequency of light', 'Intensity of light', 'Area of the plate', 'Time of exposure'], 'medium', "eV₀ = hν − φ."),
    ("Photoelectric current increases with ___ (above threshold frequency).", ['Intensity of light', 'Frequency only', 'Work function', 'Wavelength'], 'medium', "More photons → more electrons."),
    ("The de Broglie wavelength of a particle is ___.", ['h/p', 'p/h', 'hp', 'h/m'], 'easy', "λ = h/mv."),
    ("In Bohr's model, the angular momentum of an electron is an integral multiple of ___.", ['h/2π', 'h', '2πh', 'h/π'], 'medium', "mvr = nh/2π."),
    ("The radius of the nth Bohr orbit is proportional to ___.", ['n²', 'n', '1/n', '1/n²'], 'medium', "rₙ ∝ n²/Z."),
    ("The energy of the electron in the nth orbit of hydrogen is ___.", ['−13.6/n² eV', '13.6n² eV', '−13.6n eV', '−136/n eV'], 'easy', "Ground state −13.6 eV."),
    ("Which series of the hydrogen spectrum lies in the visible region?", ['Balmer', 'Lyman', 'Paschen', 'Brackett'], 'easy', "Transitions to n = 2."),
    ("The Lyman series lies in the ___ region.", ['Ultraviolet', 'Visible', 'Infrared', 'Microwave'], 'easy', "Transitions to n = 1."),
    ("Half-life T and decay constant λ are related by ___.", ['T = 0.693/λ', 'T = λ/0.693', 'T = 1/λ²', 'T = 0.693λ'], 'easy', "T½ = ln 2/λ."),
    ("After three half-lives, the fraction of a radioactive sample left is ___.", ['1/8', '1/3', '1/6', '1/9'], 'easy', "(1/2)³."),
    ("Alpha particles are ___.", ['Helium nuclei', 'Electrons', 'Photons', 'Neutrons'], 'easy', "Two protons + two neutrons."),
    ("In β⁻ decay, the atomic number ___.", ['Increases by 1', 'Decreases by 1', 'Decreases by 2', 'Stays the same'], 'medium', "A neutron becomes a proton."),
    ("The binding energy per nucleon is maximum for ___.", ['Iron-56', 'Uranium-235', 'Hydrogen', 'Helium-4'], 'medium', "Most stable nucleus."),
    ("A p-n junction diode in forward bias has ___.", ['Low resistance', 'Very high resistance', 'No current', 'Infinite capacitance'], 'easy', "Depletion layer narrows."),
    ("A Zener diode is mainly used as a ___.", ['Voltage regulator', 'Rectifier', 'Amplifier', 'Oscillator'], 'easy', "Works in reverse breakdown."),
    ("A full-wave rectifier gives an output frequency of ___ for a 50 Hz input.", ['100 Hz', '50 Hz', '25 Hz', '200 Hz'], 'medium', "Both half cycles are used."),
    ("The universal logic gates are ___.", ['NAND and NOR', 'AND and OR', 'XOR and XNOR', 'NOT and AND'], 'easy', "Any gate can be built from them."),
    ("The current gain β of a transistor is ___.", ['I_C / I_B', 'I_B / I_C', 'I_E / I_B', 'I_C / I_E'], 'medium', "Common-emitter gain."),
    ("Mass–energy equivalence is given by ___.", ['E = mc²', 'E = mv', 'E = hν/c', 'E = mgh'], 'easy', "Einstein."),
    ("Electromagnetic waves are ___.", ['Transverse', 'Longitudinal', 'Mechanical', 'Stationary only'], 'easy', "E and B perpendicular to propagation."),
    ("Which has the highest frequency?", ['Gamma rays', 'X-rays', 'Ultraviolet', 'Microwaves'], 'easy', "Electromagnetic spectrum."),
    ("The phenomenon showing that light is a transverse wave is ___.", ['Polarisation', 'Interference', 'Diffraction', 'Reflection'], 'medium', "Only transverse waves can be polarised."),
    ("In Young's double-slit experiment, fringe width is ___.", ['λD/d', 'λd/D', 'D/λd', 'dD/λ'], 'medium', "β = λD/d."),
])

register('chemistry.organic', CHE, 'Organic Chemistry', rows=[
    ("The IUPAC name of CH₃CH₂CHO is ___.", ['Propanal', 'Propanone', 'Propanol', 'Ethanal'], 'easy', "Three carbons + aldehyde."),
    ("Markovnikov's rule applies to the addition of HBr to ___.", ['Unsymmetrical alkenes', 'Alkanes', 'Benzene', 'Symmetrical alkynes only'], 'medium', "H goes to the carbon with more H."),
    ("Anti-Markovnikov addition of HBr happens in the presence of ___.", ['Peroxide', 'Water', 'Acid', 'Light only'], 'medium', "Kharasch (peroxide) effect."),
    ("SN2 reactions proceed with ___.", ['Inversion of configuration', 'Retention of configuration', 'Racemisation', 'No change'], 'medium', "Backside attack (Walden inversion)."),
    ("SN1 reactions are fastest for ___ alkyl halides.", ['Tertiary', 'Primary', 'Methyl', 'Vinyl'], 'medium', "Most stable carbocation."),
    ("Benzene undergoes mainly ___ reactions.", ['Electrophilic substitution', 'Nucleophilic addition', 'Free radical addition', 'Elimination'], 'easy', "Aromaticity is retained."),
    ("The –NO₂ group on benzene is ___ directing.", ['Meta', 'Ortho/para', 'Only ortho', 'Only para'], 'medium', "Deactivating, meta-directing."),
    ("The –OH group on benzene is ___ directing.", ['Ortho/para', 'Meta', 'Only meta', 'Non'], 'medium', "Activating."),
    ("Tollens' reagent gives a silver mirror with ___.", ['Aldehydes', 'Ketones', 'Alcohols', 'Ethers'], 'easy', "Aldehydes are oxidised."),
    ("The iodoform test is given by compounds containing ___.", ['CH₃CO– group (methyl ketones) or CH₃CH(OH)–', 'Only phenols', 'Only aldehydes', 'Carboxylic acids'], 'medium', "Yellow CHI₃ precipitate."),
    ("Lucas reagent is ___.", ['Anhydrous ZnCl₂ + conc. HCl', 'NaOH + I₂', 'AgNO₃ + NH₃', 'KMnO₄ + H₂SO₄'], 'medium', "Distinguishes 1°, 2°, 3° alcohols."),
    ("Which is the strongest base in water?", ['(CH₃)₂NH', 'NH₃', 'C₆H₅NH₂', '(C₆H₅)₂NH'], 'hard', "Secondary aliphatic amines are strongest in water."),
    ("Aniline is ___ basic than ammonia.", ['Less', 'More', 'Equally', 'Infinitely more'], 'medium', "Lone pair delocalised into the ring."),
    ("Glucose is an ___.", ['Aldohexose', 'Ketohexose', 'Aldopentose', 'Disaccharide'], 'easy', "C₆H₁₂O₆ with –CHO."),
    ("Sucrose on hydrolysis gives ___.", ['Glucose and fructose', 'Two glucose', 'Glucose and galactose', 'Only fructose'], 'easy', "Invert sugar."),
    ("The monomer of natural rubber is ___.", ['Isoprene', 'Styrene', 'Ethene', 'Chloroprene'], 'easy', "cis-polyisoprene."),
    ("Nylon-6,6 is made from ___.", ['Hexamethylenediamine and adipic acid', 'Caprolactam', 'Ethylene glycol and terephthalic acid', 'Vinyl chloride'], 'medium', "Condensation polymer."),
    ("Teflon is a polymer of ___.", ['Tetrafluoroethene', 'Vinyl chloride', 'Propene', 'Styrene'], 'easy', "Non-stick coating."),
    ("The number of σ bonds in ethene (C₂H₄) is ___.", ['5', '4', '6', '3'], 'medium', "4 C–H + 1 C–C σ; one π."),
    ("Wurtz reaction forms ___.", ['Alkanes from alkyl halides with Na', 'Alcohols from alkenes', 'Aldehydes from alcohols', 'Esters from acids'], 'medium', "2RX + 2Na → R–R."),
    ("Esters are formed from ___.", ['Carboxylic acid + alcohol', 'Aldehyde + ketone', 'Alkane + alkene', 'Amine + acid chloride only'], 'easy', "Esterification."),
    ("Which vitamin is water-soluble?", ['Vitamin C', 'Vitamin A', 'Vitamin D', 'Vitamin K'], 'easy', "B-complex and C."),
    ("Optical isomerism requires a ___.", ['Chiral (asymmetric) centre', 'Double bond', 'Ring', 'Metal'], 'medium', "Non-superimposable mirror images."),
    ("Geometrical (cis–trans) isomerism is shown by ___.", ['But-2-ene', 'But-1-ene', 'Propene', 'Ethene'], 'medium', "Different groups on each double-bonded carbon."),
])

register('biology.genetics', BIO, 'Genetics & Molecular Biology', rows=[
    ("Who is known as the father of genetics?", ['Gregor Mendel', 'T. H. Morgan', 'Watson', 'Darwin'], 'easy', "Pea plant experiments."),
    ("The double-helix model of DNA was proposed by ___.", ['Watson and Crick', 'Mendel', 'Meselson and Stahl', 'Griffith'], 'easy', "1953."),
    ("Adenine pairs with ___ in DNA.", ['Thymine', 'Cytosine', 'Guanine', 'Uracil'], 'easy', "Two hydrogen bonds."),
    ("Guanine pairs with cytosine by ___ hydrogen bonds.", ['Three', 'Two', 'One', 'Four'], 'easy', "G≡C."),
    ("Transformation in bacteria was first shown by ___.", ['Frederick Griffith', 'Avery', 'Hershey and Chase', 'Morgan'], 'medium', "Streptococcus pneumoniae, 1928."),
    ("Hershey and Chase proved that ___ is the genetic material.", ['DNA', 'Protein', 'RNA', 'Lipid'], 'medium', "Radioactive labelling of phage."),
    ("The enzyme that joins Okazaki fragments is ___.", ['DNA ligase', 'DNA polymerase', 'Helicase', 'Primase'], 'medium', "Seals nicks."),
    ("Transcription produces ___ from DNA.", ['RNA', 'Protein', 'DNA', 'Lipid'], 'easy', "RNA polymerase."),
    ("Translation takes place on ___.", ['Ribosomes', 'Nucleus', 'Golgi body', 'Lysosomes'], 'easy', "mRNA → protein."),
    ("Stop codons are ___.", ['UAA, UAG, UGA', 'AUG, UAA, UAG', 'GUG, UGA, UAG', 'AAA, UUU, GGG'], 'medium', "Do not code for amino acids."),
    ("The lac operon is an example of ___ regulation.", ['Inducible (negative)', 'Repressible only', 'Post-translational', 'Translational only'], 'medium', "Lactose acts as inducer."),
    ("Incomplete dominance is shown by flower colour in ___.", ['Snapdragon (Antirrhinum)', 'Pea', 'Rose', 'Mango'], 'medium', "Red × white → pink."),
    ("ABO blood groups show ___.", ['Co-dominance and multiple alleles', 'Incomplete dominance only', 'Polygenic inheritance', 'Epistasis only'], 'medium', "Iᴬ and Iᴮ are co-dominant."),
    ("Colour blindness is ___.", ['X-linked recessive', 'Y-linked', 'Autosomal dominant', 'Mitochondrial'], 'easy', "More common in males."),
    ("Sickle-cell anaemia is caused by substitution of ___ by valine in the β-globin chain.", ['Glutamic acid', 'Lysine', 'Glycine', 'Alanine'], 'hard', "6th position."),
    ("Turner's syndrome has the karyotype ___.", ['45, XO', '47, XXY', '47, XXX', '47, +21'], 'easy', "Klinefelter: 47, XXY."),
    ("Klinefelter's syndrome karyotype is ___.", ['47, XXY', '45, XO', '47, XYY', '46, XX'], 'easy', "Extra X chromosome in males."),
    ("The Human Genome Project estimated about ___ protein-coding genes.", ['20,000–25,000', '1,00,000', '3,000', '5 lakh'], 'medium', "Far fewer than once thought."),
    ("DNA fingerprinting relies on ___.", ['Variable number tandem repeats (VNTRs)', 'Exons only', 'Ribosomal RNA', 'Proteins'], 'medium', "Alec Jeffreys."),
    ("The vector most widely used in genetic engineering is ___.", ['Plasmid', 'Ribosome', 'Mitochondrion', 'Nucleolus'], 'easy', "e.g. pBR322."),
    ("The first restriction enzyme isolated was ___.", ['Hind II', 'EcoRI', 'BamHI', 'Taq polymerase'], 'hard', "1968."),
    ("Taq polymerase is obtained from ___.", ['Thermus aquaticus', 'E. coli', 'Bacillus subtilis', 'Agrobacterium'], 'easy', "Heat-stable, used in PCR."),
    ("Golden rice is rich in ___.", ['β-carotene (provitamin A)', 'Iron only', 'Vitamin C', 'Protein'], 'easy', "Genetically modified rice."),
    ("Gene therapy was first used for ___ deficiency.", ['Adenosine deaminase (ADA)', 'Insulin', 'Haemoglobin', 'Growth hormone'], 'hard', "1990, a 4-year-old girl."),
    ("Crossing over occurs during ___ of meiosis I.", ['Pachytene', 'Leptotene', 'Diakinesis', 'Anaphase'], 'medium', "Recombination nodules."),
])

register('biology.human_physiology', BIO, 'Human Physiology', rows=[
    ("The total volume of blood in an adult human is about ___.", ['5–6 litres', '2 litres', '10 litres', '1 litre'], 'easy', "About 7% of body weight."),
    ("Red blood cells are produced in the ___ in adults.", ['Red bone marrow', 'Liver', 'Spleen', 'Kidney'], 'easy', "Erythropoiesis."),
    ("The life span of human RBCs is about ___.", ['120 days', '30 days', '1 year', '10 days'], 'easy', "Destroyed in the spleen."),
    ("The 'graveyard of RBCs' is the ___.", ['Spleen', 'Liver', 'Kidney', 'Heart'], 'easy', "Old RBCs are broken down."),
    ("The hormone that regulates blood calcium (raises it) is ___.", ['Parathormone', 'Calcitonin', 'Insulin', 'Thyroxine'], 'medium', "Calcitonin lowers it."),
    ("ADH (vasopressin) acts mainly on the ___.", ['Collecting duct and DCT of the nephron', 'Loop of Henle only', 'Glomerulus', 'Bowman\'s capsule'], 'medium', "Increases water reabsorption."),
    ("Glomerular filtration rate in a healthy adult is about ___.", ['125 mL/min', '1 L/min', '25 mL/min', '500 mL/min'], 'medium', "≈180 L/day."),
    ("Most of the digestion and absorption of food occurs in the ___.", ['Small intestine', 'Stomach', 'Large intestine', 'Oesophagus'], 'easy', "Villi increase surface area."),
    ("Trypsin is secreted by the ___.", ['Pancreas', 'Stomach', 'Liver', 'Salivary glands'], 'easy', "As trypsinogen."),
    ("Salivary amylase acts on ___.", ['Starch', 'Proteins', 'Fats', 'Nucleic acids'], 'easy', "Ptyalin."),
    ("The vital capacity of human lungs is about ___.", ['3.5–4.5 litres', '500 mL', '10 litres', '1 litre'], 'medium', "Max exhale after max inhale."),
    ("Tidal volume is about ___.", ['500 mL', '1500 mL', '3000 mL', '100 mL'], 'easy', "Normal breath."),
    ("Most CO₂ is transported in blood as ___.", ['Bicarbonate ions', 'Carbaminohaemoglobin', 'Dissolved CO₂', 'Carbonic acid'], 'medium', "About 70%."),
    ("The neurotransmitter at the neuromuscular junction is ___.", ['Acetylcholine', 'Dopamine', 'Serotonin', 'GABA'], 'easy', "Released from motor neurons."),
    ("The resting membrane potential of a neuron is about ___.", ['−70 mV', '+70 mV', '0 mV', '−200 mV'], 'easy', "Inside negative."),
    ("Myelin sheath in the PNS is formed by ___.", ['Schwann cells', 'Oligodendrocytes', 'Astrocytes', 'Microglia'], 'medium', "Oligodendrocytes in the CNS."),
    ("The functional unit of muscle contraction is the ___.", ['Sarcomere', 'Myofibril', 'Fascicle', 'Tendon'], 'easy', "Between two Z lines."),
    ("During muscle contraction, calcium binds to ___.", ['Troponin', 'Myosin', 'Actin directly', 'Tropomyosin directly'], 'medium', "Exposes binding sites on actin."),
    ("The master gland of the body is the ___.", ['Pituitary', 'Thyroid', 'Adrenal', 'Pineal'], 'easy', "Controlled by the hypothalamus."),
    ("Which part of the eye controls the amount of light entering?", ['Iris', 'Lens', 'Retina', 'Cornea'], 'easy', "Pupil size."),
    ("The yellow spot (fovea) of the retina has ___.", ['Only cones', 'Only rods', 'No photoreceptors', 'Blood vessels'], 'medium', "Sharpest vision."),
    ("The organ of Corti is found in the ___.", ['Cochlea', 'Semicircular canals', 'Middle ear', 'Eustachian tube'], 'medium', "Hearing receptor."),
    ("Menstrual cycle in humans lasts about ___.", ['28 days', '14 days', '7 days', '40 days'], 'easy', "Ovulation around day 14."),
    ("Ovulation is triggered by a surge of ___.", ['LH', 'FSH', 'Progesterone', 'Prolactin'], 'medium', "Mid-cycle LH surge."),
    ("Which immunoglobulin crosses the placenta?", ['IgG', 'IgM', 'IgA', 'IgE'], 'medium', "Passive immunity to the foetus."),
    ("HIV mainly attacks ___.", ['Helper T cells (CD4)', 'B cells', 'RBCs', 'Platelets'], 'easy', "Weakens immunity."),
    ("ELISA is used to diagnose ___.", ['HIV infection', 'Diabetes', 'Fractures', 'Myopia'], 'easy', "Detects antibodies/antigens."),
    ("Normal fasting blood glucose is about ___.", ['70–100 mg/dL', '200–300 mg/dL', '20–40 mg/dL', '150–180 mg/dL'], 'easy', "Regulated by insulin and glucagon."),
])

register('biology.ecology', BIO, 'Ecology & Environment', rows=[
    ("The primary producers in an ecosystem are ___.", ['Green plants', 'Herbivores', 'Decomposers', 'Carnivores'], 'easy', "They make food by photosynthesis."),
    ("Which pyramid can be inverted in a pond ecosystem?", ['Pyramid of biomass', 'Pyramid of energy', 'Pyramid of numbers in all cases', 'None'], 'hard', "Phytoplankton biomass can be less than zooplankton."),
    ("Biomagnification refers to ___.", ['Increase in toxin concentration up the food chain', 'Increase in population', 'Increase in biomass', 'Increase in species'], 'easy', "e.g. DDT."),
    ("Ozone depletion is mainly caused by ___.", ['CFCs', 'CO₂', 'Methane', 'Nitrogen'], 'easy', "Chlorine radicals."),
    ("The Montreal Protocol (1987) deals with ___.", ['Ozone-depleting substances', 'Greenhouse gases', 'Biodiversity', 'Wetlands'], 'easy', "Phase-out of CFCs."),
    ("The Kyoto Protocol is related to ___.", ['Greenhouse gas emissions', 'Ozone layer', 'Wetlands', 'Whaling'], 'easy', "1997."),
    ("The Ramsar Convention is about ___.", ['Wetlands', 'Deserts', 'Forests', 'Oceans'], 'easy', "1971, Iran."),
    ("Biodiversity hotspots in India include ___.", ['Western Ghats and the Himalaya', 'Thar desert and Deccan', 'Gangetic plain and Punjab', 'Rann of Kutch only'], 'medium', "India has parts of four hotspots."),
    ("Ex-situ conservation includes ___.", ['Botanical gardens and seed banks', 'National parks', 'Biosphere reserves', 'Sacred groves'], 'easy', "Outside natural habitat."),
    ("The Red Data Book is maintained by ___.", ['IUCN', 'WWF', 'UNEP', 'UNESCO'], 'easy', "Threatened species list."),
    ("Eutrophication of lakes is caused by excess ___.", ['Nutrients (nitrates and phosphates)', 'Oxygen', 'Salt', 'Sand'], 'easy', "Algal blooms."),
    ("BOD is a measure of ___.", ['Organic pollution in water', 'Air quality', 'Soil fertility', 'Noise'], 'medium', "Biochemical oxygen demand."),
    ("The 'Chipko Movement' was associated with ___.", ['Protection of trees', 'Water conservation', 'Wildlife protection', 'Anti-dam protest'], 'easy', "Uttarakhand, 1970s."),
    ("Secondary succession starts on ___.", ['Areas where life existed before', 'Bare rock', 'New volcanic islands', 'Sand dunes only'], 'medium', "Faster than primary succession."),
    ("The interaction where one benefits and the other is unaffected is ___.", ['Commensalism', 'Mutualism', 'Parasitism', 'Amensalism'], 'easy', "(+, 0)."),
    ("Lichen is an example of ___.", ['Mutualism between alga and fungus', 'Parasitism', 'Predation', 'Competition'], 'easy', "Both benefit."),
    ("The largest biome on Earth by area is the ___.", ['Marine (ocean) biome', 'Tropical rainforest', 'Desert', 'Taiga'], 'medium', "About 70% of the surface."),
    ("Global warming is mainly due to an increase in ___.", ['Greenhouse gases such as CO₂', 'Oxygen', 'Ozone in the stratosphere', 'Nitrogen'], 'easy', "Enhanced greenhouse effect."),
    ("The 10% law of energy flow means ___.", ['Only about 10% of energy passes to the next trophic level', '10% of organisms survive', '10% biomass is lost', 'Producers use 10% of sunlight'], 'easy', "Lindeman."),
    ("Which gas is the main contributor to acid rain?", ['Sulphur dioxide', 'Carbon monoxide', 'Ozone', 'Argon'], 'easy', "With nitrogen oxides."),
])
register('environment.ecology', 'GA1', 'Environment & Ecology', rows=[])
from .core import TOPICS  # noqa: E402
TOPICS['environment.ecology'].rows = TOPICS['biology.ecology'].rows

register('biology.taxonomy', BIO, 'Diversity of Living Organisms', rows=[
    ("The five-kingdom classification was proposed by ___.", ['R. H. Whittaker', 'Linnaeus', 'Haeckel', 'Copeland'], 'easy', "1969."),
    ("Bacteria belong to kingdom ___.", ['Monera', 'Protista', 'Fungi', 'Plantae'], 'easy', "Prokaryotes."),
    ("The cell wall of fungi is made of ___.", ['Chitin', 'Cellulose', 'Peptidoglycan', 'Lignin'], 'easy', "Plants: cellulose."),
    ("Amphibians of the plant kingdom are ___.", ['Bryophytes', 'Pteridophytes', 'Gymnosperms', 'Algae'], 'easy', "Need water for fertilisation."),
    ("The first vascular plants were ___.", ['Pteridophytes', 'Bryophytes', 'Gymnosperms', 'Angiosperms'], 'easy', "Ferns."),
    ("Gymnosperms have ___.", ['Naked seeds', 'Seeds inside fruits', 'No seeds', 'Spores only'], 'easy', "e.g. Pinus, Cycas."),
    ("Viruses that infect bacteria are called ___.", ['Bacteriophages', 'Viroids', 'Prions', 'Mycoplasma'], 'easy', "e.g. T4 phage."),
    ("Prions are infectious ___.", ['Proteins', 'RNA molecules', 'DNA', 'Lipids'], 'medium', "e.g. mad cow disease."),
    ("Which phylum shows radial symmetry and cnidoblasts?", ['Cnidaria', 'Porifera', 'Annelida', 'Mollusca'], 'medium', "Stinging cells."),
    ("Water vascular system is characteristic of ___.", ['Echinodermata', 'Mollusca', 'Arthropoda', 'Chordata'], 'medium', "e.g. starfish."),
    ("The excretory organs of insects are ___.", ['Malpighian tubules', 'Nephridia', 'Kidneys', 'Flame cells'], 'medium', "Arthropods."),
    ("Earthworms belong to phylum ___.", ['Annelida', 'Nematoda', 'Platyhelminthes', 'Arthropoda'], 'easy', "Segmented worms."),
    ("Which of these is a mammal?", ['Bat', 'Penguin', 'Shark', 'Crocodile'], 'easy', "Bats suckle their young."),
    ("Binomial nomenclature uses ___ names.", ['Genus and species', 'Family and order', 'Class and phylum', 'Kingdom and genus'], 'easy', "e.g. Homo sapiens."),
    ("The scientific name of mango is ___.", ['Mangifera indica', 'Solanum tuberosum', 'Panthera leo', 'Oryza sativa'], 'easy', "Written in italics."),
    ("Heterocysts in Anabaena help in ___.", ['Nitrogen fixation', 'Photosynthesis', 'Reproduction', 'Respiration'], 'medium', "Cyanobacteria."),
    ("Diatoms have cell walls of ___.", ['Silica', 'Chitin', 'Cellulose only', 'Calcium carbonate'], 'medium', "Form diatomaceous earth."),
    ("Which is a fish?", ['Seahorse', 'Starfish', 'Jellyfish', 'Cuttlefish'], 'medium', "Others are not vertebrates."),
])

# ------------------------------------------------------------------ medicine (more subjects)
table_topics('medicine.microbiology', MED, 'Microbiology', rows("""
Ziehl–Neelsen stain|Acid-fast bacilli (e.g. Mycobacterium tuberculosis)
India ink preparation|Cryptococcus neoformans capsule
Löwenstein–Jensen medium|Culture of Mycobacterium tuberculosis
Thayer–Martin medium|Neisseria gonorrhoeae
TCBS agar|Vibrio cholerae
Widal test|Typhoid fever
VDRL test|Syphilis (screening)
Weil–Felix test|Rickettsial infections
Paul–Bunnell test|Infectious mononucleosis
Elek's test|Toxigenicity of Corynebacterium diphtheriae
Mantoux test|Tuberculin hypersensitivity (TB exposure)
Nagler reaction|Clostridium perfringens
""".replace('', '')), [
    ("{a} is used for ___.", 'b', "{a}: {b}."),
    ("Which test, stain or medium is used for: {b}?", 'a', "{a}: {b}."),
])

table_topics('medicine.pathology', MED, 'Pathology & Tumour Markers', rows("""
Alpha-fetoprotein (AFP)|Hepatocellular carcinoma and germ-cell tumours
CA-125|Ovarian carcinoma
PSA|Prostate carcinoma
CEA|Colorectal carcinoma
CA 19-9|Pancreatic carcinoma
β-hCG|Choriocarcinoma
Calcitonin|Medullary carcinoma of thyroid
Bence Jones proteins|Multiple myeloma
Psammoma bodies|Papillary carcinoma of thyroid
Mallory bodies|Alcoholic hepatitis
Aschoff bodies|Rheumatic heart disease
Councilman bodies|Viral hepatitis (yellow fever)
"""), [
    ("{a} is characteristically associated with ___.", 'b', "{a}: {b}."),
])

table_topics('medicine.side_effects', MED, 'Pharmacology – Adverse Effects', rows("""
Aminoglycosides|Ototoxicity and nephrotoxicity
Chloramphenicol|Grey baby syndrome and aplastic anaemia
Isoniazid|Peripheral neuropathy (prevented by pyridoxine)
Ethambutol|Optic neuritis (red–green colour blindness)
Rifampicin|Orange-red discolouration of urine
ACE inhibitors|Dry cough and angioedema
Amiodarone|Pulmonary fibrosis and thyroid dysfunction
Phenytoin|Gingival hyperplasia
Thalidomide|Phocomelia (limb defects in the foetus)
Tetracyclines|Discolouration of children's teeth
Statins|Myopathy
Metformin|Lactic acidosis
Fluoroquinolones|Tendon rupture
Vincristine|Peripheral neuropathy
"""), [
    ("A characteristic adverse effect of {a} is ___.", 'b', "{a}: {b}."),
    ("{b} is a characteristic adverse effect of ___.", 'a', "{a}: {b}."),
])

register('medicine.psm', MED, 'Community Medicine (PSM)', rows=[
    ("Herd immunity is most relevant for diseases that ___.", ['Spread from person to person', 'Are non-infectious', 'Are genetic', 'Spread only by vectors with animal reservoirs'], 'medium', "Immunised people protect the rest."),
    ("The incubation period of measles is about ___.", ['10–14 days', '1–2 days', '1 month', '6 months'], 'medium', "Rash appears around day 14."),
    ("Measles vaccine (MR) is first given at ___ under India's UIP.", ['9–12 months', 'Birth', '6 weeks', '5 years'], 'easy', "Second dose at 16–24 months."),
    ("Oral rehydration solution (WHO low-osmolarity) has a total osmolarity of ___.", ['245 mOsm/L', '311 mOsm/L', '150 mOsm/L', '500 mOsm/L'], 'hard', "Reduced osmolarity ORS."),
    ("The most sensitive indicator of a community's health is the ___.", ['Infant mortality rate', 'Crude death rate', 'Life expectancy', 'Birth rate'], 'medium', "IMR."),
    ("Sensitivity of a screening test is its ability to ___.", ['Correctly identify those with the disease', 'Correctly identify those without the disease', 'Predict outcome', 'Cost less'], 'easy', "True positive rate."),
    ("Specificity is the ability to ___.", ['Correctly identify those without the disease', 'Detect all cases', 'Measure incidence', 'Measure prevalence'], 'easy', "True negative rate."),
    ("Prevalence equals incidence multiplied by ___.", ['Mean duration of disease', 'Population', 'Mortality', 'Attack rate'], 'medium', "P = I × D."),
    ("Chlorine demand of water is ___.", ['The amount used up by impurities before free residual chlorine appears', 'The free residual chlorine', 'Chlorine added for taste', 'Chlorine in tap water'], 'hard', "Break-point chlorination."),
    ("The recommended free residual chlorine after 1 hour of contact is ___.", ['0.5 mg/L', '5 mg/L', '0.05 mg/L', '2 mg/L'], 'medium', "WHO."),
    ("A case-control study proceeds from ___.", ['Effect to cause', 'Cause to effect', 'Population to sample', 'Exposure to outcome over time'], 'medium', "Retrospective."),
    ("The vector of Japanese encephalitis is ___.", ['Culex mosquito', 'Anopheles mosquito', 'Aedes mosquito', 'Sandfly'], 'easy', "Pigs are amplifier hosts."),
    ("The vector of kala-azar is the ___.", ['Sandfly (Phlebotomus)', 'Tsetse fly', 'Housefly', 'Culex'], 'easy', "Leishmania donovani."),
    ("Iodised salt under the NIDDCP must contain at least ___ of iodine at the consumer level.", ['15 ppm', '30 ppm', '5 ppm', '50 ppm'], 'hard', "30 ppm at production."),
    ("The 'cold chain' for vaccines is meant to ___.", ['Keep vaccines at the right temperature from maker to recipient', 'Freeze all vaccines', 'Transport only by air', 'Store for 5 years'], 'easy', "Potency protection."),
])

register('medicine.obg_paeds', MED, 'Obstetrics, Gynaecology & Paediatrics', rows=[
    ("Normal duration of pregnancy is about ___.", ['280 days (40 weeks) from LMP', '200 days', '365 days', '30 weeks'], 'easy', "Naegele's rule."),
    ("Naegele's rule: EDD = LMP + 9 months + ___.", ['7 days', '14 days', '3 days', '21 days'], 'easy', "For a 28-day cycle."),
    ("The most common cause of postpartum haemorrhage is ___.", ['Uterine atony', 'Trauma', 'Retained tissue', 'Coagulopathy'], 'easy', "Four Ts: tone is commonest."),
    ("The drug of choice for eclamptic seizures is ___.", ['Magnesium sulphate', 'Diazepam', 'Phenytoin', 'Phenobarbitone'], 'easy', "Pritchard regimen."),
    ("Folic acid supplementation before conception prevents ___.", ['Neural tube defects', 'Cleft lip only', 'Down syndrome', 'Anaemia only'], 'easy', "400 µg daily."),
    ("Normal birth weight of an Indian newborn is about ___.", ['2.5–3.5 kg', '1.5 kg', '4.5 kg', '1 kg'], 'easy', "LBW is < 2.5 kg."),
    ("A baby normally doubles its birth weight by ___.", ['5–6 months', '1 month', '1 year', '2 years'], 'easy', "Triples by 1 year."),
    ("Social smile develops by about ___.", ['6–8 weeks', '6 months', '1 year', '2 weeks'], 'medium', "Developmental milestone."),
    ("A child can sit without support at about ___.", ['8 months', '3 months', '15 months', '2 years'], 'medium', "Gross motor milestone."),
    ("Physiological jaundice in a term newborn usually appears on ___.", ['Day 2–3', 'Day 1 (within 24 hours)', 'Day 10', 'Day 30'], 'medium', "Jaundice within 24 hours is pathological."),
    ("The most common cause of bronchiolitis in infants is ___.", ['Respiratory syncytial virus', 'Streptococcus pneumoniae', 'Influenza B', 'Adenovirus only'], 'medium', "RSV."),
    ("Oral polio vaccine is given at birth as the ___ dose.", ['Zero', 'First booster', 'Third', 'Final'], 'easy', "OPV-0."),
    ("Kwashiorkor is mainly due to deficiency of ___.", ['Protein', 'Calories only', 'Vitamin A', 'Iron'], 'easy', "Oedema is characteristic."),
    ("The commonest site of endometriosis is the ___.", ['Ovary', 'Lung', 'Umbilicus', 'Bladder'], 'medium', "Chocolate cyst."),
    ("Pap smear is used to screen for ___.", ['Cervical cancer', 'Breast cancer', 'Ovarian cancer', 'Endometrial cancer'], 'easy', "Cytology of the cervix."),
])

# ------------------------------------------------------------------ design, management, agriculture
register('design.aptitude', 'DSG1', 'Design & Visual Aptitude', rows=[
    ("Which of these are primary colours in the traditional (RYB) colour wheel?", ['Red, yellow, blue', 'Red, green, blue', 'Orange, green, violet', 'Cyan, magenta, yellow'], 'easy', "RGB is for light; CMY for print."),
    ("Mixing blue and yellow pigments gives ___.", ['Green', 'Orange', 'Purple', 'Brown'], 'easy', "Secondary colour."),
    ("Complementary colours lie ___ on the colour wheel.", ['Opposite each other', 'Next to each other', 'In a triangle', 'In the centre'], 'easy', "e.g. red and green."),
    ("Colours next to each other on the wheel are ___.", ['Analogous', 'Complementary', 'Triadic', 'Neutral'], 'easy', "e.g. blue, blue-green, green."),
    ("A cube has how many edges?", ['12', '8', '6', '24'], 'easy', "8 vertices, 6 faces."),
    ("A three-point perspective drawing has ___ vanishing points.", ['Three', 'One', 'Two', 'None'], 'medium', "Used for tall buildings seen from below/above."),
    ("The 'golden ratio' is approximately ___.", ['1.618', '3.142', '2.718', '1.414'], 'medium', "φ."),
    ("Which shape has the maximum area for a given perimeter?", ['Circle', 'Square', 'Triangle', 'Rectangle'], 'medium', "Isoperimetric property."),
    ("An isometric drawing shows the axes at ___ to each other.", ['120°', '90°', '45°', '60°'], 'medium', "Equal foreshortening."),
    ("Warm colours include ___.", ['Red, orange and yellow', 'Blue and green', 'Purple and blue', 'Grey and black'], 'easy', "They appear to advance."),
    ("The number of faces of a hexagonal prism is ___.", ['8', '6', '12', '10'], 'medium', "2 hexagons + 6 rectangles."),
    ("A logo that uses negative space well relies on ___.", ['The empty area around and between shapes', 'Bright colours only', 'Many fonts', '3-D effects'], 'medium', "Figure–ground relationship."),
    ("Serif fonts have ___.", ['Small strokes at the ends of letters', 'No strokes', 'Only capital letters', 'Rounded letters only'], 'easy', "e.g. Times New Roman."),
    ("In design, 'hierarchy' means ___.", ['Arranging elements to show their order of importance', 'Using only one colour', 'Symmetry', 'Repetition'], 'easy', "Guides the eye."),
    ("Rotational symmetry of order 4 is shown by a ___.", ['Square', 'Rectangle', 'Equilateral triangle', 'Kite'], 'medium', "Looks the same 4 times in a full turn."),
])
register('design.architecture', 'DSG1', 'Architecture & Design Awareness', rows=[
    ("The Lotus Temple in Delhi was designed by ___.", ['Fariborz Sahba', 'Le Corbusier', 'Charles Correa', 'B. V. Doshi'], 'medium', "Bahá'í House of Worship, 1986."),
    ("Chandigarh was planned by ___.", ['Le Corbusier', 'Edwin Lutyens', 'Laurie Baker', 'Frank Lloyd Wright'], 'easy', "1950s."),
    ("New Delhi's Rashtrapati Bhavan was designed by ___.", ['Edwin Lutyens', 'Herbert Baker', 'Le Corbusier', 'Charles Correa'], 'easy', "Baker designed the Secretariat buildings."),
    ("The first Indian to win the Pritzker Prize was ___.", ['B. V. Doshi', 'Charles Correa', 'Raj Rewal', 'Laurie Baker'], 'medium', "2018."),
    ("The Sun Temple at Konark is in ___.", ['Odisha', 'Gujarat', 'Rajasthan', 'Tamil Nadu'], 'easy', "Kalinga style."),
    ("The Charminar is in ___.", ['Hyderabad', 'Lucknow', 'Delhi', 'Bhopal'], 'easy', "Built 1591."),
    ("Fatehpur Sikri was built by ___.", ['Akbar', 'Shah Jahan', 'Babur', 'Humayun'], 'easy', "Buland Darwaza."),
    ("The architectural style of the Khajuraho temples is ___.", ['Nagara', 'Dravida', 'Vesara', 'Indo-Saracenic'], 'medium', "North Indian temple style."),
    ("The 'Gateway of India' is in ___.", ['Mumbai', 'Delhi', 'Kolkata', 'Chennai'], 'easy', "1924."),
    ("Laurie Baker is known for ___.", ['Low-cost, sustainable architecture in Kerala', 'Skyscrapers', 'Mughal gardens', 'Bridges'], 'medium', "Brick jali walls."),
])
register('management.decision', 'DM1', 'Decision Making & Ethics', rows=[
    ("A colleague asks you to share confidential client data 'just this once'. You should ___.", ['Politely refuse and follow the data-protection policy', 'Share it quietly', 'Share it if they are senior', 'Ignore the request and say nothing to anyone'], 'easy', "Confidentiality comes first."),
    ("Your team misses a deadline because of your error. The best response is to ___.", ['Own the mistake, inform stakeholders and propose a recovery plan', 'Blame a junior', 'Hide it until asked', 'Resign immediately'], 'easy', "Accountability."),
    ("A supplier offers you an expensive gift during a tender. You should ___.", ['Decline it and report as per the company policy', 'Accept it privately', 'Accept and favour them', 'Ask for cash instead'], 'easy', "Avoid conflict of interest."),
    ("Two team members are in conflict, hurting work. As manager you should first ___.", ['Talk to both, understand the issue and mediate', 'Fire one of them', 'Ignore it', 'Take sides with the senior one'], 'easy', "Address root cause."),
    ("A cost-cutting option saves money but harms nearby villagers' water supply. The best decision is to ___.", ['Choose a solution that avoids the harm even at some extra cost', 'Go ahead since it is legal', 'Hide the impact', 'Pay a small fee to villagers and continue'], 'medium', "Sustainability and stakeholder interest."),
    ("You discover a minor calculation error in a report already sent to the client. You should ___.", ['Inform the client promptly with the corrected figures', 'Wait for the client to notice', 'Change it silently next time', 'Deny the error'], 'easy', "Transparency builds trust."),
    ("When resources are limited, priorities should be decided by ___.", ['Impact and urgency', 'Personal preference', 'Who complains loudest', 'Random choice'], 'easy', "Rational prioritisation."),
    ("A high performer repeatedly ignores safety rules. You should ___.", ['Enforce the rules consistently', 'Ignore it because of results', 'Change the rules for them', 'Reward them'], 'easy', "Rules apply to everyone."),
    ("A loan applicant is your relative. The most ethical step is to ___.", ['Declare the relationship and step away from the decision', 'Approve quickly', 'Reject to avoid suspicion', 'Process it without telling anyone'], 'easy', "Recuse yourself."),
    ("Customer complaints rise after a product launch. The first step should be to ___.", ['Analyse complaints to find the root cause', 'Withdraw all ads', 'Cut prices immediately', 'Ignore them'], 'medium', "Diagnose before acting."),
])
register('agriculture.core', 'ARD1', 'Agriculture & Rural Development', rows=[
    ("Kharif crops are sown in ___.", ['June–July (monsoon)', 'October–November', 'March–April', 'December'], 'easy', "e.g. rice, maize, cotton."),
    ("Rabi crops are sown in ___.", ['October–December', 'June–July', 'March', 'August'], 'easy', "e.g. wheat, mustard, gram."),
    ("The Green Revolution in India is associated with ___.", ['High-yielding varieties of wheat and rice', 'Milk production', 'Fisheries', 'Oilseeds'], 'easy', "1960s."),
    ("The father of the Green Revolution in India is ___.", ['M. S. Swaminathan', 'Verghese Kurien', 'Norman Borlaug', 'C. Subramaniam'], 'easy', "Borlaug globally."),
    ("Operation Flood is related to ___.", ['Dairy development', 'Flood control', 'Irrigation', 'Fisheries'], 'easy', "White Revolution."),
    ("The Blue Revolution relates to ___.", ['Fisheries', 'Dairy', 'Oilseeds', 'Poultry'], 'easy', "Aquaculture."),
    ("The Yellow Revolution relates to ___.", ['Oilseeds', 'Eggs', 'Honey', 'Fruits'], 'medium', "Edible oils."),
    ("Minimum Support Price (MSP) is announced by the government on the advice of ___.", ['CACP', 'NABARD', 'FCI', 'RBI'], 'medium', "Commission for Agricultural Costs and Prices."),
    ("Kisan Credit Card scheme was launched in ___.", ['1998', '2005', '1991', '2014'], 'medium', "Short-term crop loans."),
    ("PM-KISAN provides eligible farmer families ___ per year.", ['₹6,000 in three instalments', '₹12,000 monthly', '₹2,000 once', '₹1 lakh'], 'easy', "Direct benefit transfer."),
    ("The most suitable soil for tea cultivation is ___.", ['Acidic, well-drained soil on slopes', 'Alkaline black soil', 'Saline soil', 'Sandy desert soil'], 'medium', "Assam, Darjeeling."),
    ("Leguminous crops improve soil fertility by ___.", ['Fixing atmospheric nitrogen', 'Adding phosphorus', 'Reducing pH', 'Removing water'], 'easy', "Rhizobium in root nodules."),
    ("Drip irrigation mainly helps to ___.", ['Save water by delivering it at the roots', 'Flood fields', 'Increase salinity', 'Drain water'], 'easy', "Micro-irrigation."),
    ("India is the largest producer of ___ in the world.", ['Milk', 'Wheat', 'Coffee', 'Rubber'], 'medium', "Also the largest producer of pulses."),
    ("Self-Help Groups (SHGs) are linked to banks under a programme pioneered by ___.", ['NABARD', 'SEBI', 'SIDBI', 'IRDAI'], 'medium', "SHG–Bank Linkage Programme, 1992."),
])
