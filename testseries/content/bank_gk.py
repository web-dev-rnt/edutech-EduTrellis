"""General awareness: static facts only (nothing that goes out of date), as fact tables + hand-written questions."""
from .core import register, table_topics

GA = 'GA1'


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


# ------------------------------------------------------------------ Indian polity
ARTICLES = rows("""
Article 14|Equality before law
Article 15|Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth
Article 16|Equality of opportunity in public employment
Article 17|Abolition of untouchability
Article 19|Protection of six freedoms including speech and expression
Article 21|Protection of life and personal liberty
Article 21A|Right to free and compulsory education for children aged 6–14
Article 24|Prohibition of employment of children in factories
Article 32|Right to constitutional remedies
Article 44|Uniform Civil Code for citizens
Article 51A|Fundamental Duties
Article 72|Pardoning power of the President
Article 76|Attorney General of India
Article 110|Definition of Money Bills
Article 112|Annual Financial Statement (Budget)
Article 123|Ordinance-making power of the President
Article 143|President's power to consult the Supreme Court
Article 148|Comptroller and Auditor General of India
Article 280|Finance Commission
Article 300A|Right to property as a legal right
Article 312|All India Services
Article 324|Election Commission
Article 352|National Emergency
Article 356|President's Rule in states
Article 360|Financial Emergency
Article 368|Amendment of the Constitution
Article 370|Temporary provisions for Jammu and Kashmir (abrogated in 2019)
""")
table_topics('ga.polity_articles', GA, 'Indian Polity – Articles', ARTICLES, [
    ("Which Article of the Indian Constitution deals with: {b}?", 'a', "{a}: {b}."),
    ("{a} of the Indian Constitution deals with ___.", 'b', "{a}: {b}."),
])

POLITY = [
    ("The Constitution of India was adopted on ___.", ['26 November 1949', '26 January 1950', '15 August 1947', '2 October 1949'], 'easy', "Adopted on 26 Nov 1949 (Constitution Day); came into force on 26 Jan 1950."),
    ("Who was the Chairman of the Drafting Committee of the Constitution?", ['Dr B. R. Ambedkar', 'Dr Rajendra Prasad', 'Jawaharlal Nehru', 'K. M. Munshi'], 'easy', "Dr Ambedkar chaired the Drafting Committee."),
    ("Who presided over the Constituent Assembly as its permanent President?", ['Dr Rajendra Prasad', 'Dr B. R. Ambedkar', 'Sachchidananda Sinha', 'Sardar Patel'], 'medium', "Dr Rajendra Prasad; Sachchidananda Sinha was the interim President."),
    ("The idea of Fundamental Duties was borrowed from the Constitution of ___.", ['USSR', 'USA', 'UK', 'Ireland'], 'medium', "Added by the 42nd Amendment (1976), inspired by the USSR."),
    ("The Directive Principles of State Policy were borrowed from the Constitution of ___.", ['Ireland', 'USA', 'Canada', 'Australia'], 'medium', "Irish Constitution."),
    ("The concept of judicial review in India is taken from the Constitution of ___.", ['USA', 'UK', 'Ireland', 'Japan'], 'medium', "United States."),
    ("The Parliamentary form of government in India is borrowed from ___.", ['UK', 'USA', 'France', 'Germany'], 'easy', "British Westminster model."),
    ("How many Fundamental Duties are there in the Indian Constitution now?", ['11', '10', '12', '9'], 'medium', "10 added in 1976; the 11th by the 86th Amendment (2002)."),
    ("The words 'Socialist' and 'Secular' were added to the Preamble by the ___ Amendment.", ['42nd', '44th', '24th', '52nd'], 'medium', "42nd Amendment, 1976."),
    ("The Right to Property was removed from Fundamental Rights by the ___ Amendment.", ['44th', '42nd', '52nd', '61st'], 'hard', "44th Amendment (1978); now a legal right under Article 300A."),
    ("The voting age was lowered from 21 to 18 by the ___ Amendment.", ['61st', '42nd', '73rd', '86th'], 'medium', "61st Amendment, 1988."),
    ("The 73rd Constitutional Amendment relates to ___.", ['Panchayati Raj', 'Municipalities', 'Anti-defection', 'GST'], 'easy', "Panchayati Raj institutions (1992)."),
    ("The 74th Constitutional Amendment relates to ___.", ['Urban local bodies', 'Panchayati Raj', 'Official languages', 'Fundamental Duties'], 'easy', "Municipalities."),
    ("The 101st Constitutional Amendment introduced ___.", ['Goods and Services Tax', 'Anti-defection law', 'Right to Education', 'NJAC'], 'medium', "GST, 2016."),
    ("The Anti-defection law is contained in the ___ Schedule.", ['Tenth', 'Ninth', 'Eighth', 'Seventh'], 'medium', "Added by the 52nd Amendment (1985)."),
    ("The Eighth Schedule of the Constitution lists ___.", ['Official languages', 'Union, State and Concurrent lists', 'Oaths and affirmations', 'Anti-defection provisions'], 'easy', "It now has 22 languages."),
    ("How many languages are listed in the Eighth Schedule?", ['22', '18', '24', '20'], 'easy', "22 languages."),
    ("The division of powers between the Union and the States is in the ___ Schedule.", ['Seventh', 'Sixth', 'Fifth', 'Eighth'], 'medium', "Union, State and Concurrent Lists."),
    ("The minimum age to become President of India is ___ years.", ['35', '30', '25', '40'], 'easy', "Article 58."),
    ("The minimum age to be a member of the Rajya Sabha is ___ years.", ['30', '25', '35', '21'], 'easy', "Lok Sabha: 25; Rajya Sabha: 30."),
    ("The Vice-President of India is the ex-officio Chairman of the ___.", ['Rajya Sabha', 'Lok Sabha', 'NITI Aayog', 'Planning Commission'], 'easy', "Article 64."),
    ("A Money Bill can be introduced only in the ___.", ['Lok Sabha', 'Rajya Sabha', 'Either House', 'Joint sitting'], 'easy', "Article 109."),
    ("The Rajya Sabha can delay a Money Bill for at most ___ days.", ['14', '30', '60', '90'], 'medium', "It must return it within 14 days."),
    ("Who decides whether a bill is a Money Bill?", ['Speaker of the Lok Sabha', 'President', 'Chairman of the Rajya Sabha', 'Prime Minister'], 'medium', "The Speaker's decision is final."),
    ("A joint sitting of both Houses of Parliament is presided over by the ___.", ['Speaker of the Lok Sabha', 'President', 'Vice-President', 'Prime Minister'], 'medium', "Article 108."),
    ("The Supreme Court of India was established on ___.", ['28 January 1950', '26 January 1950', '15 August 1947', '26 November 1949'], 'hard', "Two days after the Constitution came into force."),
    ("Writs are issued by the Supreme Court under Article ___.", ['32', '226', '19', '21'], 'easy', "High Courts issue writs under Article 226."),
    ("The writ issued to release a person unlawfully detained is ___.", ['Habeas Corpus', 'Mandamus', 'Certiorari', 'Quo Warranto'], 'easy', "'You may have the body'."),
    ("The writ that commands a public official to perform a duty is ___.", ['Mandamus', 'Habeas Corpus', 'Prohibition', 'Quo Warranto'], 'medium', "'We command'."),
    ("Who appoints the Governor of a state?", ['President', 'Prime Minister', 'Chief Minister', 'Chief Justice of India'], 'easy', "Article 155."),
    ("The Preamble describes India as a Sovereign, Socialist, Secular, Democratic ___.", ['Republic', 'Federation', 'Union', 'Monarchy'], 'easy', "Preamble text."),
    ("The Constituent Assembly took about ___ to draft the Constitution.", ['2 years 11 months 18 days', '1 year 6 months', '3 years 2 months', '4 years'], 'hard', "From 9 Dec 1946 to 26 Nov 1949."),
    ("The National Human Rights Commission was set up in ___.", ['1993', '1985', '2000', '1975'], 'hard', "Under the Protection of Human Rights Act, 1993."),
    ("Who is the constitutional head of the Union executive?", ['President', 'Prime Minister', 'Chief Justice', 'Speaker'], 'easy', "Article 53."),
    ("The maximum strength of the Lok Sabha prescribed by the Constitution is ___.", ['550', '545', '552', '500'], 'hard', "Article 81 sets 550 elected members (after the 104th Amendment ended nominated Anglo-Indian seats)."),
    ("Members of the Rajya Sabha are elected for a term of ___ years.", ['6', '5', '4', '3'], 'easy', "One-third retire every two years."),
    ("The Election Commission of India is a ___ body.", ['Constitutional', 'Statutory', 'Executive', 'Judicial'], 'easy', "Article 324."),
    ("NITI Aayog replaced the ___ in 2015.", ['Planning Commission', 'Finance Commission', 'National Development Council', 'Inter-State Council'], 'easy', "1 January 2015."),
]
register('ga.polity', GA, 'Indian Polity', rows=POLITY)

# ------------------------------------------------------------------ History
HISTORY = [
    ("The Indus Valley site of Lothal is in present-day ___.", ['Gujarat', 'Rajasthan', 'Punjab', 'Haryana'], 'medium', "Lothal had a dockyard."),
    ("The Great Bath was found at ___.", ['Mohenjo-daro', 'Harappa', 'Kalibangan', 'Lothal'], 'easy', "Mohenjo-daro, Sindh."),
    ("The oldest Veda is the ___.", ['Rigveda', 'Samaveda', 'Yajurveda', 'Atharvaveda'], 'easy', "Rigveda."),
    ("Gautama Buddha delivered his first sermon at ___.", ['Sarnath', 'Bodh Gaya', 'Kushinagar', 'Lumbini'], 'easy', "Dharmachakra Pravartana at Sarnath."),
    ("Buddha attained enlightenment at ___.", ['Bodh Gaya', 'Sarnath', 'Kushinagar', 'Vaishali'], 'easy', "Under the Bodhi tree."),
    ("The 24th Tirthankara of Jainism was ___.", ['Mahavira', 'Rishabhanatha', 'Parshvanatha', 'Neminatha'], 'easy', "Vardhamana Mahavira."),
    ("Who was the founder of the Maurya Empire?", ['Chandragupta Maurya', 'Ashoka', 'Bindusara', 'Bimbisara'], 'easy', "c. 321 BCE, with Chanakya."),
    ("The Kalinga War was fought by ___.", ['Ashoka', 'Chandragupta Maurya', 'Samudragupta', 'Harsha'], 'easy', "c. 261 BCE; led Ashoka to Buddhism."),
    ("'Arthashastra' was written by ___.", ['Kautilya', 'Kalidasa', 'Megasthenes', 'Banabhatta'], 'easy', "Kautilya (Chanakya)."),
    ("Megasthenes, author of 'Indica', was the ambassador of ___.", ['Seleucus Nicator', 'Alexander', 'Darius', 'Ptolemy'], 'medium', "At Chandragupta Maurya's court."),
    ("Samudragupta is called the 'Napoleon of India' by ___.", ['V. A. Smith', 'R. C. Majumdar', 'James Mill', 'A. L. Basham'], 'hard', "Historian Vincent Arthur Smith."),
    ("Nalanda University was founded during the rule of the ___.", ['Guptas', 'Mauryas', 'Kushanas', 'Cholas'], 'medium', "By Kumaragupta I (5th century)."),
    ("The Chinese pilgrim who visited India during Harsha's reign was ___.", ['Xuanzang (Hiuen Tsang)', 'Fa-Hien', 'I-Tsing', 'Marco Polo'], 'medium', "7th century."),
    ("The Brihadeeswara Temple at Thanjavur was built by ___.", ['Rajaraja Chola I', 'Rajendra Chola', 'Krishnadevaraya', 'Narasimhavarman'], 'medium', "c. 1010 CE."),
    ("The First Battle of Panipat (1526) was fought between Babur and ___.", ['Ibrahim Lodi', 'Rana Sanga', 'Hemu', 'Sher Shah'], 'easy', "It founded the Mughal Empire."),
    ("The Battle of Haldighati (1576) was fought between Akbar's army and ___.", ['Maharana Pratap', 'Rana Sanga', 'Shivaji', 'Hemu'], 'easy', "Led by Man Singh for Akbar."),
    ("Who built the Qutub Minar's first storey?", ['Qutb-ud-din Aibak', 'Iltutmish', 'Alauddin Khalji', 'Firoz Shah Tughlaq'], 'medium', "Completed by Iltutmish."),
    ("The Mughal emperor who introduced 'Din-i-Ilahi' was ___.", ['Akbar', 'Jahangir', 'Aurangzeb', 'Humayun'], 'easy', "1582."),
    ("The Taj Mahal was built by ___.", ['Shah Jahan', 'Akbar', 'Jahangir', 'Aurangzeb'], 'easy', "In memory of Mumtaz Mahal."),
    ("Shivaji was crowned Chhatrapati in ___.", ['1674', '1627', '1680', '1707'], 'medium', "At Raigad."),
    ("The Battle of Plassey was fought in ___.", ['1757', '1764', '1857', '1761'], 'easy', "Robert Clive defeated Siraj-ud-Daulah."),
    ("The Battle of Buxar was fought in ___.", ['1764', '1757', '1799', '1857'], 'medium', "Gave the Company the Diwani of Bengal."),
    ("The Third Battle of Panipat (1761) was fought between the Marathas and ___.", ['Ahmad Shah Abdali', 'Nadir Shah', 'The British', 'The Mughals'], 'medium', "Ahmad Shah Durrani."),
    ("The Doctrine of Lapse was introduced by ___.", ['Lord Dalhousie', 'Lord Wellesley', 'Lord Curzon', 'Lord Ripon'], 'easy', "Annexed states without natural heirs."),
    ("The Subsidiary Alliance system was introduced by ___.", ['Lord Wellesley', 'Lord Dalhousie', 'Lord Cornwallis', 'Warren Hastings'], 'medium', "1798."),
    ("The Permanent Settlement of Bengal (1793) was introduced by ___.", ['Lord Cornwallis', 'Lord Wellesley', 'Warren Hastings', 'Lord Hastings'], 'medium', "Zamindari system."),
    ("The Revolt of 1857 began at ___.", ['Meerut', 'Delhi', 'Kanpur', 'Lucknow'], 'easy', "10 May 1857."),
    ("The Indian National Congress was founded in ___.", ['1885', '1905', '1857', '1920'], 'easy', "Bombay, by A. O. Hume and others."),
    ("The first President of the Indian National Congress was ___.", ['W. C. Bonnerjee', 'Dadabhai Naoroji', 'A. O. Hume', 'Surendranath Banerjee'], 'medium', "1885 session at Bombay."),
    ("The Partition of Bengal took place in ___.", ['1905', '1911', '1919', '1947'], 'easy', "By Lord Curzon; annulled in 1911."),
    ("The Muslim League was founded in ___.", ['1906', '1905', '1916', '1919'], 'medium', "At Dhaka."),
    ("The Jallianwala Bagh massacre took place in ___.", ['1919', '1920', '1930', '1942'], 'easy', "13 April 1919, Amritsar."),
    ("The Non-Cooperation Movement was withdrawn after the incident at ___.", ['Chauri Chaura', 'Champaran', 'Bardoli', 'Kheda'], 'medium', "February 1922."),
    ("Gandhiji's first Satyagraha in India was at ___.", ['Champaran', 'Kheda', 'Ahmedabad', 'Dandi'], 'medium', "1917, for indigo farmers."),
    ("The Dandi March began in ___.", ['1930', '1920', '1942', '1919'], 'easy', "12 March 1930, against the salt tax."),
    ("The Quit India Movement was launched in ___.", ['1942', '1930', '1920', '1946'], 'easy', "8 August 1942."),
    ("'Do or Die' was Gandhiji's call during the ___.", ['Quit India Movement', 'Non-Cooperation Movement', 'Civil Disobedience Movement', 'Khilafat Movement'], 'easy', "1942."),
    ("Who gave the slogan 'Swaraj is my birthright and I shall have it'?", ['Bal Gangadhar Tilak', 'Lala Lajpat Rai', 'Gandhiji', 'Bipin Chandra Pal'], 'easy', "Lokmanya Tilak."),
    ("Who founded the Indian National Army (Azad Hind Fauj) in its revived form?", ['Subhas Chandra Bose', 'Rash Behari Bose', 'Mohan Singh', 'Bhagat Singh'], 'medium', "Bose took command in 1943; it was first formed by Mohan Singh in 1942."),
    ("The Simon Commission came to India in ___.", ['1928', '1919', '1935', '1942'], 'medium', "All-British; boycotted with 'Simon Go Back'."),
    ("The Poona Pact (1932) was signed between Gandhiji and ___.", ['Dr B. R. Ambedkar', 'Jinnah', 'Nehru', 'Tilak'], 'medium', "On reserved seats for depressed classes."),
    ("The Government of India Act 1935 provided for ___.", ['Provincial autonomy', 'Dyarchy in provinces', 'Separate electorates for the first time', 'Complete independence'], 'hard', "Dyarchy in provinces had come in 1919; 1935 gave provincial autonomy."),
    ("Who was the first Governor-General of independent India?", ['Lord Mountbatten', 'C. Rajagopalachari', 'Lord Wavell', 'Lord Linlithgow'], 'medium', "Rajagopalachari was the first (and last) Indian Governor-General."),
    ("Who founded the Arya Samaj?", ['Swami Dayananda Saraswati', 'Raja Ram Mohan Roy', 'Swami Vivekananda', 'Keshab Chandra Sen'], 'easy', "1875."),
    ("Who founded the Brahmo Samaj?", ['Raja Ram Mohan Roy', 'Debendranath Tagore', 'Dayananda Saraswati', 'Jyotiba Phule'], 'easy', "1828."),
    ("Sati was abolished in 1829 by ___.", ['Lord William Bentinck', 'Lord Dalhousie', 'Lord Canning', 'Lord Ripon'], 'medium', "Supported by Raja Ram Mohan Roy."),
    ("Who wrote 'Gitanjali'?", ['Rabindranath Tagore', 'Bankim Chandra Chatterjee', 'Sarojini Naidu', 'Sri Aurobindo'], 'easy', "Nobel Prize 1913."),
    ("'Vande Mataram' was written by ___.", ['Bankim Chandra Chatterjee', 'Rabindranath Tagore', 'Muhammad Iqbal', 'Sarojini Naidu'], 'easy', "From 'Anandamath'."),
    ("Who is known as the 'Iron Man of India'?", ['Sardar Vallabhbhai Patel', 'Bhagat Singh', 'Subhas Chandra Bose', 'Lal Bahadur Shastri'], 'easy', "He integrated the princely states."),
    ("Bhagat Singh, Rajguru and Sukhdev were executed in ___.", ['1931', '1928', '1929', '1942'], 'medium', "23 March 1931."),
]
register('ga.history', GA, 'History', rows=HISTORY)

# ------------------------------------------------------------------ Geography
CAPITALS = rows("""
Andhra Pradesh|Amaravati
Arunachal Pradesh|Itanagar
Assam|Dispur
Bihar|Patna
Chhattisgarh|Raipur
Goa|Panaji
Gujarat|Gandhinagar
Haryana|Chandigarh
Himachal Pradesh|Shimla
Jharkhand|Ranchi
Karnataka|Bengaluru
Kerala|Thiruvananthapuram
Madhya Pradesh|Bhopal
Maharashtra|Mumbai
Manipur|Imphal
Meghalaya|Shillong
Mizoram|Aizawl
Nagaland|Kohima
Odisha|Bhubaneswar
Rajasthan|Jaipur
Sikkim|Gangtok
Tamil Nadu|Chennai
Telangana|Hyderabad
Tripura|Agartala
Uttar Pradesh|Lucknow
Uttarakhand|Dehradun
West Bengal|Kolkata
""")
table_topics('ga.states', GA, 'States & Capitals', CAPITALS, [
    ("What is the capital of {a}?", 'b', "{b} is the capital of {a}."),
    ("{b} is the capital of which state?", 'a', "{b} is the capital of {a}."),
], difficulty='easy')

NATIONAL_PARKS = rows("""
Jim Corbett National Park|Uttarakhand
Kaziranga National Park|Assam
Gir National Park|Gujarat
Sundarbans National Park|West Bengal
Ranthambore National Park|Rajasthan
Bandhavgarh National Park|Madhya Pradesh
Kanha National Park|Madhya Pradesh
Periyar National Park|Kerala
Bandipur National Park|Karnataka
Keoladeo National Park|Rajasthan
Dachigam National Park|Jammu and Kashmir
Hemis National Park|Ladakh
Manas National Park|Assam
Silent Valley National Park|Kerala
Simlipal National Park|Odisha
Tadoba Andhari Tiger Reserve|Maharashtra
Valley of Flowers National Park|Uttarakhand
Great Himalayan National Park|Himachal Pradesh
Namdapha National Park|Arunachal Pradesh
Dudhwa National Park|Uttar Pradesh
""")
table_topics('ga.national_parks', GA, 'National Parks & Wildlife', NATIONAL_PARKS, [
    ("{a} is located in ___.", 'b', "{a} is in {b}."),
])

DANCES = rows("""
Bharatanatyam|Tamil Nadu
Kathakali|Kerala
Mohiniyattam|Kerala
Kuchipudi|Andhra Pradesh
Odissi|Odisha
Manipuri|Manipur
Sattriya|Assam
Kathak|Uttar Pradesh
Garba|Gujarat
Bhangra|Punjab
Ghoomar|Rajasthan
Bihu|Assam
Lavani|Maharashtra
Yakshagana|Karnataka
Giddha|Punjab
Rouf|Jammu and Kashmir
Dandiya Raas|Gujarat
""")
table_topics('ga.culture', GA, 'Art & Culture', DANCES, [
    ("The dance form '{a}' belongs to ___.", 'b', "{a} is from {b}."),
    ("Which of these dance forms belongs to {b}?", 'a', "{a} is from {b}."),
])

RIVERS = rows("""
Ganga|Gangotri glacier (Gaumukh)
Yamuna|Yamunotri glacier
Godavari|Trimbakeshwar, Nashik
Krishna|Mahabaleshwar
Narmada|Amarkantak
Kaveri|Talakaveri, Brahmagiri hills
Mahanadi|Sihawa, Chhattisgarh
Brahmaputra|Chemayungdung glacier, Tibet
Tapti|Multai, Betul
Sutlej|Rakshastal lake, Tibet
Chambal|Janapav hills, Mhow
Son|Amarkantak plateau (near the Son–Narmada divide)
""")
table_topics('ga.rivers', GA, 'Rivers of India', RIVERS, [
    ("The river {a} originates at ___.", 'b', "{a} rises at {b}."),
    ("Which river originates at {b}?", 'a', "{a} rises at {b}."),
], difficulty='medium')

GEOGRAPHY = [
    ("The Tropic of Cancer passes through how many Indian states?", ['8', '7', '9', '6'], 'medium', "Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, West Bengal, Tripura and Mizoram."),
    ("The largest state of India by area is ___.", ['Rajasthan', 'Madhya Pradesh', 'Maharashtra', 'Uttar Pradesh'], 'easy', "Rajasthan."),
    ("The smallest state of India by area is ___.", ['Goa', 'Sikkim', 'Tripura', 'Mizoram'], 'easy', "Goa."),
    ("The longest river flowing entirely within India is ___.", ['Godavari', 'Narmada', 'Krishna', 'Mahanadi'], 'medium', "The Ganga is longer but flows into Bangladesh; the Godavari stays wholly in India."),
    ("Which river is known as the 'Dakshin Ganga'?", ['Godavari', 'Kaveri', 'Krishna', 'Mahanadi'], 'easy', "Godavari."),
    ("The Palk Strait separates India from ___.", ['Sri Lanka', 'Maldives', 'Myanmar', 'Bangladesh'], 'easy', "Between Tamil Nadu and Sri Lanka."),
    ("Which is the largest freshwater lake in India?", ['Wular Lake', 'Dal Lake', 'Chilika Lake', 'Loktak Lake'], 'medium', "Chilika is a brackish lagoon."),
    ("Chilika Lake is in ___.", ['Odisha', 'Andhra Pradesh', 'West Bengal', 'Tamil Nadu'], 'easy', "Largest coastal lagoon in India."),
    ("Loktak Lake, with floating 'phumdis', is in ___.", ['Manipur', 'Assam', 'Meghalaya', 'Tripura'], 'medium', "Keibul Lamjao, the floating national park, is on it."),
    ("Black soil is most suitable for growing ___.", ['Cotton', 'Rice', 'Tea', 'Wheat'], 'easy', "Regur soil."),
    ("Which is the southernmost point of India?", ['Indira Point', 'Kanyakumari', 'Rameswaram', 'Port Blair'], 'medium', "In Great Nicobar."),
    ("The Western Ghats are also known as the ___.", ['Sahyadri', 'Nilgiri', 'Vindhya', 'Satpura'], 'easy', "Sahyadri range."),
    ("The largest planet in the solar system is ___.", ['Jupiter', 'Saturn', 'Neptune', 'Earth'], 'easy', "Jupiter."),
    ("The planet known as the 'Red Planet' is ___.", ['Mars', 'Venus', 'Jupiter', 'Mercury'], 'easy', "Iron oxide on its surface."),
    ("The hottest planet in the solar system is ___.", ['Venus', 'Mercury', 'Mars', 'Jupiter'], 'medium', "Its thick CO₂ atmosphere traps heat."),
    ("The largest ocean is the ___.", ['Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'], 'easy', "Pacific."),
    ("The longest river in the world is generally given as the ___.", ['Nile', 'Amazon', 'Yangtze', 'Mississippi'], 'medium', "The Nile (the Amazon is the largest by discharge)."),
    ("The largest desert in the world (hot) is the ___.", ['Sahara', 'Thar', 'Gobi', 'Kalahari'], 'easy', "Sahara."),
    ("The International Date Line roughly follows the ___ meridian.", ['180°', '0°', '90° E', '82.5° E'], 'medium', "180° longitude."),
    ("Indian Standard Time is based on the ___ meridian.", ['82.5° E', '90° E', '75° E', '0°'], 'medium', "Passes near Mirzapur (Prayagraj)."),
    ("The layer of the atmosphere containing the ozone layer is the ___.", ['Stratosphere', 'Troposphere', 'Mesosphere', 'Thermosphere'], 'easy', "Stratosphere."),
    ("Mawsynram, one of the wettest places on Earth, is in ___.", ['Meghalaya', 'Assam', 'Kerala', 'Sikkim'], 'easy', "Khasi Hills."),
    ("The Thar Desert lies mostly in ___.", ['Rajasthan', 'Gujarat', 'Punjab', 'Haryana'], 'easy', "Great Indian Desert."),
    ("India shares its longest international border with ___.", ['Bangladesh', 'China', 'Pakistan', 'Nepal'], 'medium', "About 4,096 km."),
    ("The Duncan Passage separates ___.", ['South Andaman and Little Andaman', 'India and Sri Lanka', 'Andaman and Nicobar', 'Lakshadweep and Maldives'], 'hard', "The Ten Degree Channel separates the Andaman and Nicobar groups."),
    ("Which state has the longest coastline in India?", ['Gujarat', 'Andhra Pradesh', 'Tamil Nadu', 'Maharashtra'], 'medium', "Gujarat."),
]
register('ga.geography', GA, 'Geography', rows=GEOGRAPHY)

# ------------------------------------------------------------------ Economy & banking
ECONOMY = [
    ("The Reserve Bank of India was established in ___.", ['1935', '1947', '1949', '1969'], 'easy', "1 April 1935; nationalised in 1949."),
    ("The headquarters of the RBI is in ___.", ['Mumbai', 'New Delhi', 'Kolkata', 'Chennai'], 'easy', "Mumbai."),
    ("Who signs the ₹10 currency note?", ['Governor of the RBI', 'Finance Secretary', 'Finance Minister', 'President'], 'easy', "The ₹1 note is signed by the Finance Secretary."),
    ("Who signs the ₹1 currency note?", ['Finance Secretary', 'Governor of the RBI', 'Finance Minister', 'Prime Minister'], 'medium', "It is issued by the Government of India."),
    ("The repo rate is the rate at which ___.", ['RBI lends to commercial banks', 'Banks lend to the public', 'RBI borrows from banks', 'Banks lend to each other overnight'], 'medium', "Reverse repo: RBI borrows from banks."),
    ("CRR stands for ___.", ['Cash Reserve Ratio', 'Credit Reserve Ratio', 'Central Reserve Rate', 'Cash Recovery Rate'], 'easy', "Share of deposits banks keep with the RBI."),
    ("SLR stands for ___.", ['Statutory Liquidity Ratio', 'Standard Lending Rate', 'State Liquidity Reserve', 'Secured Loan Ratio'], 'easy', "Liquid assets banks must hold themselves."),
    ("Fourteen major banks were nationalised in India in ___.", ['1969', '1980', '1955', '1991'], 'medium', "Six more in 1980."),
    ("The New Economic Policy (LPG reforms) was introduced in ___.", ['1991', '1985', '1999', '2001'], 'easy', "Liberalisation, Privatisation, Globalisation."),
    ("GST was rolled out in India on ___.", ['1 July 2017', '1 April 2017', '8 November 2016', '1 January 2018'], 'easy', "101st Amendment."),
    ("The GST Council is chaired by the ___.", ['Union Finance Minister', 'Prime Minister', 'RBI Governor', 'President'], 'medium', "Article 279A."),
    ("GDP measures ___.", ['The value of final goods and services produced within a country', 'Income of residents abroad', 'Government revenue', 'Exports minus imports'], 'easy', "Gross Domestic Product."),
    ("Inflation measured by WPI refers to ___.", ['Wholesale Price Index', 'Weighted Price Index', 'World Price Index', 'Wage Price Index'], 'easy', "CPI is the Consumer Price Index."),
    ("The RBI uses ___ inflation as its main target under inflation targeting.", ['CPI (Combined)', 'WPI', 'GDP deflator', 'Core WPI'], 'medium', "4% ± 2% CPI target."),
    ("The Monetary Policy Committee has ___ members.", ['6', '5', '7', '9'], 'medium', "Three from the RBI, three appointed by the Government."),
    ("NABARD was set up in ___.", ['1982', '1969', '1975', '1990'], 'medium', "Apex bank for agriculture and rural development."),
    ("SEBI was given statutory status in ___.", ['1992', '1988', '1995', '2000'], 'medium', "Set up in 1988; statutory under the SEBI Act, 1992."),
    ("The 'Finance Commission' is constituted every ___ years.", ['5', '4', '6', '10'], 'easy', "Article 280."),
    ("Which tax is a direct tax?", ['Income tax', 'GST', 'Customs duty', 'Excise duty'], 'easy', "Paid directly to the government by the taxpayer."),
    ("The fiscal deficit is ___.", ['Total expenditure minus total receipts excluding borrowings', 'Revenue expenditure minus revenue receipts', 'Imports minus exports', 'Primary deficit plus interest'], 'hard', "It equals the government's borrowing requirement."),
    ("Jan Dhan Yojana is mainly about ___.", ['Financial inclusion through bank accounts', 'Housing for all', 'Crop insurance', 'Skill development'], 'easy', "Launched in 2014."),
    ("Which bank is the largest public sector bank in India?", ['State Bank of India', 'Punjab National Bank', 'Bank of Baroda', 'Canara Bank'], 'easy', "SBI."),
    ("The headquarters of the World Bank is in ___.", ['Washington, D.C.', 'New York', 'Geneva', 'Paris'], 'easy', "So is the IMF."),
    ("The Asian Development Bank is headquartered in ___.", ['Manila', 'Tokyo', 'Beijing', 'Singapore'], 'medium', "Philippines."),
    ("UPI was developed by ___.", ['NPCI', 'RBI', 'SBI', 'SEBI'], 'easy', "National Payments Corporation of India."),
]
register('ga.economy', GA, 'Indian Economy & Banking', rows=ECONOMY)

ABBREVIATIONS = rows("""
NPCI|National Payments Corporation of India
NEFT|National Electronic Funds Transfer
RTGS|Real Time Gross Settlement
IMPS|Immediate Payment Service
KYC|Know Your Customer
NPA|Non-Performing Asset
IFSC|Indian Financial System Code
MICR|Magnetic Ink Character Recognition
CASA|Current Account Savings Account
ATM|Automated Teller Machine
ECS|Electronic Clearing Service
SIDBI|Small Industries Development Bank of India
EXIM Bank|Export-Import Bank of India
IRDAI|Insurance Regulatory and Development Authority of India
PFRDA|Pension Fund Regulatory and Development Authority
MSME|Micro, Small and Medium Enterprises
FDI|Foreign Direct Investment
FPI|Foreign Portfolio Investment
GDP|Gross Domestic Product
MCLR|Marginal Cost of Funds based Lending Rate
""")
table_topics('ga.banking_terms', 'GA1', 'Banking Terms & Abbreviations', ABBREVIATIONS, [
    ("{a} stands for ___.", 'b', "{a}: {b}."),
], difficulty='easy')

# ------------------------------------------------------------------ General science (for GA papers)
SCIENCE = [
    ("The SI unit of force is ___.", ['Newton', 'Joule', 'Pascal', 'Watt'], 'easy', "1 N = 1 kg·m/s²."),
    ("The SI unit of electric current is ___.", ['Ampere', 'Volt', 'Ohm', 'Coulomb'], 'easy', "Base unit."),
    ("Sound cannot travel through ___.", ['Vacuum', 'Water', 'Steel', 'Air'], 'easy', "It needs a medium."),
    ("The speed of light in vacuum is about ___.", ['3 × 10⁸ m/s', '3 × 10⁶ m/s', '3 × 10⁵ m/s', '340 m/s'], 'easy', "c ≈ 3 × 10⁸ m/s."),
    ("Which mirror is used as a rear-view mirror in vehicles?", ['Convex', 'Concave', 'Plane', 'Cylindrical'], 'easy', "Wide field of view."),
    ("The instrument used to measure atmospheric pressure is the ___.", ['Barometer', 'Hygrometer', 'Thermometer', 'Ammeter'], 'easy', "Barometer."),
    ("The chemical formula of common salt is ___.", ['NaCl', 'KCl', 'NaOH', 'Na₂CO₃'], 'easy', "Sodium chloride."),
    ("Baking soda is chemically ___.", ['Sodium bicarbonate', 'Sodium carbonate', 'Calcium carbonate', 'Sodium chloride'], 'easy', "NaHCO₃."),
    ("The most abundant gas in Earth's atmosphere is ___.", ['Nitrogen', 'Oxygen', 'Argon', 'Carbon dioxide'], 'easy', "About 78%."),
    ("Which gas is known as laughing gas?", ['Nitrous oxide', 'Nitrogen dioxide', 'Carbon monoxide', 'Methane'], 'easy', "N₂O."),
    ("Which metal is liquid at room temperature?", ['Mercury', 'Sodium', 'Aluminium', 'Lead'], 'easy', "Mercury."),
    ("The hardest natural substance is ___.", ['Diamond', 'Graphite', 'Iron', 'Quartz'], 'easy', "A form of carbon."),
    ("Vinegar contains ___.", ['Acetic acid', 'Citric acid', 'Lactic acid', 'Formic acid'], 'easy', "Ethanoic acid."),
    ("The pH of pure water at 25 °C is ___.", ['7', '0', '14', '1'], 'easy', "Neutral."),
    ("The powerhouse of the cell is the ___.", ['Mitochondria', 'Nucleus', 'Ribosome', 'Golgi body'], 'easy', "ATP is made there."),
    ("Deficiency of vitamin C causes ___.", ['Scurvy', 'Rickets', 'Night blindness', 'Beriberi'], 'easy', "Scurvy."),
    ("Deficiency of vitamin D causes ___.", ['Rickets', 'Scurvy', 'Pellagra', 'Anaemia'], 'easy', "Rickets in children."),
    ("Deficiency of iodine causes ___.", ['Goitre', 'Anaemia', 'Scurvy', 'Rickets'], 'easy', "Thyroid swelling."),
    ("The largest gland in the human body is the ___.", ['Liver', 'Pancreas', 'Thyroid', 'Pituitary'], 'easy', "Liver."),
    ("The universal blood donor group is ___.", ['O negative', 'AB positive', 'A positive', 'B negative'], 'medium', "No A, B or Rh antigens."),
    ("Normal human body temperature is about ___.", ['37 °C', '98 °C', '35 °C', '40 °C'], 'easy', "98.6 °F."),
    ("Malaria is caused by ___.", ['Plasmodium', 'A virus', 'A bacterium', 'A fungus'], 'easy', "Spread by female Anopheles mosquitoes."),
    ("Which disease is caused by a virus?", ['Measles', 'Tuberculosis', 'Typhoid', 'Cholera'], 'easy', "The others are bacterial."),
    ("Photosynthesis takes place in the ___.", ['Chloroplast', 'Mitochondria', 'Nucleus', 'Vacuole'], 'easy', "Chlorophyll is there."),
    ("The number of bones in an adult human body is ___.", ['206', '208', '212', '300'], 'easy', "A newborn has about 300."),
    ("The smallest bone in the human body is the ___.", ['Stapes', 'Femur', 'Incus', 'Radius'], 'medium', "In the middle ear."),
    ("Insulin is produced by the ___.", ['Pancreas', 'Liver', 'Kidney', 'Thyroid'], 'easy', "Beta cells of the islets of Langerhans."),
    ("Which blood cells help in clotting?", ['Platelets', 'RBCs', 'WBCs', 'Plasma'], 'easy', "Thrombocytes."),
    ("Electric current is measured with an ___.", ['Ammeter', 'Voltmeter', 'Galvanometer', 'Ohmmeter'], 'easy', "Connected in series."),
    ("The process by which plants lose water through leaves is ___.", ['Transpiration', 'Respiration', 'Photosynthesis', 'Osmosis'], 'easy', "Through stomata."),
]
register('ga.science', GA, 'General Science', rows=SCIENCE)

# ------------------------------------------------------------------ Static GK tables
BOOKS = rows("""
Discovery of India|Jawaharlal Nehru
Wings of Fire|A. P. J. Abdul Kalam
Godaan|Munshi Premchand
Gitanjali|Rabindranath Tagore
Arthashastra|Kautilya
Abhijnanasakuntalam|Kalidasa
Train to Pakistan|Khushwant Singh
The God of Small Things|Arundhati Roy
Midnight's Children|Salman Rushdie
The White Tiger|Aravind Adiga
Malgudi Days|R. K. Narayan
India Wins Freedom|Maulana Abul Kalam Azad
My Experiments with Truth|Mahatma Gandhi
Anandamath|Bankim Chandra Chatterjee
Ramcharitmanas|Tulsidas
Akbarnama|Abul Fazl
Baburnama|Babur
Rajatarangini|Kalhana
Kamayani|Jaishankar Prasad
The Guide|R. K. Narayan
Hind Swaraj|Mahatma Gandhi
Annihilation of Caste|B. R. Ambedkar
Indica|Megasthenes
Harshacharita|Banabhatta
""")
table_topics('ga.books', GA, 'Books & Authors', BOOKS, [
    ("Who wrote '{a}'?", 'b', "'{a}' was written by {b}."),
    ("Which of these was written by {b}?", 'a', "'{a}' was written by {b}."),
])

INVENTIONS = rows("""
Telephone|Alexander Graham Bell
Electric bulb (practical incandescent lamp)|Thomas Edison
Radio (wireless telegraphy)|Guglielmo Marconi
Penicillin|Alexander Fleming
Theory of relativity|Albert Einstein
Laws of motion|Isaac Newton
Dynamite|Alfred Nobel
Steam engine (improved)|James Watt
Vaccination (smallpox)|Edward Jenner
World Wide Web|Tim Berners-Lee
Raman effect|C. V. Raman
Polio vaccine (injectable)|Jonas Salk
X-rays|Wilhelm Röntgen
Radioactivity|Henri Becquerel
Electron|J. J. Thomson
Neutron|James Chadwick
Periodic table|Dmitri Mendeleev
Aeroplane (first powered flight)|Wright brothers
""")
table_topics('ga.inventions', GA, 'Inventions & Discoveries', INVENTIONS, [
    ("{a} is credited to ___.", 'b', "{a}: {b}."),
    ("Which of these is associated with {b}?", 'a', "{a}: {b}."),
])

TROPHIES = rows("""
Durand Cup|Football
Ranji Trophy|Cricket
Santosh Trophy|Football
Thomas Cup|Badminton
Uber Cup|Badminton
Davis Cup|Tennis
Wimbledon|Tennis
Ryder Cup|Golf
Beighton Cup|Hockey
Agha Khan Cup|Hockey
Stanley Cup|Ice hockey
Duleep Trophy|Cricket
Subroto Cup|Football
Federation Cup (India)|Football
""")
table_topics('ga.sports', GA, 'Sports', TROPHIES, [
    ("The {a} is associated with ___.", 'b', "{a}: {b}."),
], difficulty='easy')

ORG_HQ = rows("""
United Nations|New York
UNESCO|Paris
World Health Organization|Geneva
International Labour Organization|Geneva
World Trade Organization|Geneva
International Monetary Fund|Washington, D.C.
UNICEF|New York
International Court of Justice|The Hague
FAO|Rome
SAARC Secretariat|Kathmandu
ASEAN Secretariat|Jakarta
International Olympic Committee|Lausanne
FIFA|Zurich
International Cricket Council|Dubai
Amnesty International|London
OPEC|Vienna
""")
table_topics('ga.organisations', GA, 'International Organisations', ORG_HQ, [
    ("The headquarters of {a} is in ___.", 'b', "{a}: {b}."),
])

INSTRUMENTS = rows("""
Ammeter|Electric current
Voltmeter|Potential difference
Barometer|Atmospheric pressure
Hygrometer|Relative humidity
Seismograph|Earthquake waves
Anemometer|Wind speed
Lactometer|Purity of milk
Hydrometer|Density of liquids
Odometer|Distance travelled by a vehicle
Sphygmomanometer|Blood pressure
Pyrometer|Very high temperatures
Altimeter|Altitude
Tachometer|Rotational speed
Ondometer|Frequency of electromagnetic waves
""")
table_topics('ga.instruments', GA, 'Scientific Instruments', INSTRUMENTS, [
    ("A {a} is used to measure ___.", 'b', "{a} measures {b}."),
    ("Which instrument measures {b}?", 'a', "{a} measures {b}."),
], difficulty='easy')

DAYS_ = rows("""
National Youth Day|12 January
Republic Day|26 January
National Science Day|28 February
International Women's Day|8 March
World Water Day|22 March
World Health Day|7 April
Earth Day|22 April
World Environment Day|5 June
International Yoga Day|21 June
National Sports Day (India)|29 August
Teachers' Day (India)|5 September
Hindi Diwas|14 September
Gandhi Jayanti|2 October
Constitution Day (India)|26 November
Human Rights Day|10 December
National Mathematics Day|22 December
""")
table_topics('ga.important_days', GA, 'Important Days', DAYS_, [
    ("{a} is observed on ___.", 'b', "{a}: {b}."),
    ("Which day is observed on {b}?", 'a', "{b}: {a}."),
])

COUNTRIES = rows("""
Japan|Tokyo|Yen
China|Beijing|Renminbi (Yuan)
Russia|Moscow|Rouble
United Kingdom|London|Pound sterling
France|Paris|Euro
Germany|Berlin|Euro
Australia|Canberra|Australian dollar
Canada|Ottawa|Canadian dollar
Brazil|Brasília|Real
Bangladesh|Dhaka|Taka
Nepal|Kathmandu|Nepalese rupee
Sri Lanka|Sri Jayawardenepura Kotte|Sri Lankan rupee
Pakistan|Islamabad|Pakistani rupee
Bhutan|Thimphu|Ngultrum
Myanmar|Naypyidaw|Kyat
Saudi Arabia|Riyadh|Riyal
South Africa|Pretoria (executive)|Rand
Turkey|Ankara|Lira
Indonesia|Jakarta|Rupiah
Afghanistan|Kabul|Afghani
""")
table_topics('ga.world', GA, 'World – Capitals & Currencies', [(c, cap) for c, cap, _ in COUNTRIES], [
    ("What is the capital of {a}?", 'b', "{b} is the capital of {a}."),
], difficulty='easy')
table_topics('ga.currencies', GA, 'World – Currencies', [(c, cur) for c, _, cur in COUNTRIES if cur != 'Euro'], [
    ("The currency of {a} is the ___.", 'b', "{a}: {b}."),
], difficulty='easy')

GA_TOPICS = ['ga.polity', 'ga.polity_articles', 'ga.history', 'ga.geography', 'ga.states', 'ga.rivers', 'ga.national_parks',
             'ga.culture', 'ga.economy', 'ga.science', 'ga.books', 'ga.inventions', 'ga.sports', 'ga.organisations',
             'ga.instruments', 'ga.important_days', 'ga.world', 'ga.currencies']
