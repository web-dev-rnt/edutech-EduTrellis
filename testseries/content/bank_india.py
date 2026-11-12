"""India GK for state PSC, SSC, railway, banking, police and teaching exams: static facts only (nothing that goes
out of date), as fact tables (each row yields questions both ways) plus hand-written questions.

Also legal GK (Acts and their years) and computer awareness (abbreviations, shortcuts) for bank and clerical exams.
"""
from .core import register, table_topics

GA, LGL, CMP = 'GA1', 'LGL1', 'CMP1'


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


# ------------------------------------------------------------------ States: monuments, festivals, lakes, languages
MONUMENTS = rows("""
Konark Sun Temple|Odisha
Jagannath Temple, Puri|Odisha
Lingaraj Temple|Odisha
Khajuraho Group of Monuments|Madhya Pradesh
Sanchi Stupa|Madhya Pradesh
Group of Monuments at Hampi|Karnataka
Gol Gumbaz|Karnataka
Ajanta Caves|Maharashtra
Ellora Caves|Maharashtra
Gateway of India|Maharashtra
Brihadeeswarar Temple, Thanjavur|Tamil Nadu
Meenakshi Temple, Madurai|Tamil Nadu
Shore Temple, Mahabalipuram|Tamil Nadu
Golden Temple (Harmandir Sahib)|Punjab
Hawa Mahal|Rajasthan
Chittorgarh Fort|Rajasthan
Victoria Memorial|West Bengal
Charminar|Telangana
Qutub Minar|Delhi
Red Fort|Delhi
Taj Mahal|Uttar Pradesh
Fatehpur Sikri|Uttar Pradesh
Rani ki Vav|Gujarat
Sun Temple, Modhera|Gujarat
Somnath Temple|Gujarat
Mahabodhi Temple, Bodh Gaya|Bihar
Kamakhya Temple|Assam
Kedarnath Temple|Uttarakhand
Basilica of Bom Jesus|Goa
Rumtek Monastery|Sikkim
Tawang Monastery|Arunachal Pradesh
Ujjayanta Palace|Tripura
Kangla Fort|Manipur
Padmanabhaswamy Temple|Kerala
Hemis Monastery|Ladakh
Rock Garden|Chandigarh
""")
table_topics('ga.monuments', GA, 'Monuments & Heritage Sites', MONUMENTS, [
    ("{a} is located in ___.", 'b', "{a} is in {b}."),
    ("Which of these monuments is in {b}?", 'a', "{a} is in {b}."),
])

FESTIVALS = rows("""
Onam|Kerala
Thrissur Pooram|Kerala
Pongal|Tamil Nadu
Bihu|Assam
Hornbill Festival|Nagaland
Chhath Puja|Bihar
Lohri|Punjab
Pushkar Fair|Rajasthan
Ganesh Chaturthi (grandest public celebration)|Maharashtra
Rann Utsav|Gujarat
Hampi Utsav|Karnataka
Wangala|Meghalaya
Chapchar Kut|Mizoram
Sangai Festival|Manipur
Hemis Festival|Ladakh
Hareli|Chhattisgarh
Nuakhai|Odisha
Sohrai|Jharkhand
Bathukamma|Telangana
Kullu Dussehra|Himachal Pradesh
Shigmo|Goa
Torgya|Arunachal Pradesh
Kharchi Puja|Tripura
""")
table_topics('ga.festivals', GA, 'Fairs & Festivals', FESTIVALS, [
    ("'{a}' is a famous festival of ___.", 'b', "{a} is celebrated in {b}."),
    ("Which festival is associated with {b}?", 'a', "{a} is celebrated in {b}."),
])

LAKES = rows("""
Dal Lake|Jammu and Kashmir
Wular Lake|Jammu and Kashmir
Chilika Lake|Odisha
Loktak Lake|Manipur
Vembanad Lake|Kerala
Pangong Tso|Ladakh
Sambhar Lake|Rajasthan
Hussain Sagar|Telangana
Kolleru Lake|Andhra Pradesh
Upper Lake (Bhojtal)|Madhya Pradesh
Nainital (Naini Lake)|Uttarakhand
Tsomgo (Changu) Lake|Sikkim
Rudrasagar Lake|Tripura
Umiam Lake|Meghalaya
Renuka Lake|Himachal Pradesh
Sukhna Lake|Chandigarh
Lonar Lake|Maharashtra
""")
table_topics('ga.lakes', GA, 'Lakes of India', LAKES, [
    ("{a} is located in ___.", 'b', "{a} is in {b}."),
    ("Which lake is in {b}?", 'a', "{a} is in {b}."),
])

LANGUAGES = rows("""
Karnataka|Kannada
Kerala|Malayalam
Tamil Nadu|Tamil
Andhra Pradesh|Telugu
Telangana|Telugu
Maharashtra|Marathi
Gujarat|Gujarati
Punjab|Punjabi
West Bengal|Bengali
Odisha|Odia
Assam|Assamese
Goa|Konkani
Manipur|Manipuri (Meitei)
Mizoram|Mizo
Nagaland|English
""")
table_topics('ga.state_languages', GA, 'States & Official Languages', LANGUAGES, [
    ("The official language of {a} is ___.", 'b', "{b} is the official language of {a}."),
    ("{b} is the official language of which state?", 'a', "{b} is the official language of {a}."),
], difficulty='easy')

# ------------------------------------------------------------------ Modern history
FREEDOM_EVENTS = rows("""
Battle of Plassey|1757
Battle of Buxar|1764
Revolt of 1857 (First War of Independence)|1857
Founding of the Indian National Congress|1885
Partition of Bengal|1905
Founding of the All-India Muslim League|1906
Surat Split of the Congress|1907
Morley–Minto Reforms|1909
Lucknow Pact|1916
Champaran Satyagraha|1917
Jallianwala Bagh massacre|1919
Non-Cooperation Movement launched|1920
Chauri Chaura incident|1922
Arrival of the Simon Commission in India|1928
Dandi March (Salt Satyagraha)|1930
Gandhi–Irwin Pact|1931
Poona Pact|1932
Government of India Act|1935
Quit India Movement|1942
Cabinet Mission to India|1946
First Battle of Panipat|1526
Second Battle of Panipat|1556
Third Battle of Panipat|1761
Battle of Haldighati|1576
Battle of Talikota|1565
Second Battle of Tarain|1192
""")
table_topics('ga.freedom_events', GA, 'Modern History – Events & Years', FREEDOM_EVENTS, [
    ("In which year did the {a} take place?", 'b', "{a}: {b}."),
    ("Which of these took place in {b}?", 'a', "{a}: {b}."),
])

TITLES = rows("""
Iron Man of India|Sardar Vallabhbhai Patel
Frontier Gandhi|Khan Abdul Ghaffar Khan
Netaji|Subhas Chandra Bose
Lokmanya|Bal Gangadhar Tilak
Deshbandhu|Chittaranjan Das
Gurudev|Rabindranath Tagore
Nightingale of India|Sarojini Naidu
Missile Man of India|Dr A. P. J. Abdul Kalam
Mahamana|Madan Mohan Malaviya
Punjab Kesari|Lala Lajpat Rai
Grand Old Man of India|Dadabhai Naoroji
Shaheed-e-Azam|Bhagat Singh
Loknayak|Jayaprakash Narayan
Father of the Indian Constitution|Dr B. R. Ambedkar
Andhra Kesari|Tanguturi Prakasam
Father of the Green Revolution in India|M. S. Swaminathan
Father of the White Revolution|Verghese Kurien
Father of the Indian Space Programme|Vikram Sarabhai
Father of Indian Nuclear Programme|Homi J. Bhabha
Bapu|Mahatma Gandhi
""")
table_topics('ga.titles', GA, 'Famous Personalities & Titles', TITLES, [
    ("Who is known as '{a}'?", 'b', "{b} is known as '{a}'."),
    ("{b} is popularly known as ___.", 'a', "{b} is known as '{a}'."),
], difficulty='easy')

FOUNDERS = rows("""
Brahmo Samaj|Raja Ram Mohan Roy
Arya Samaj|Swami Dayananda Saraswati
Ramakrishna Mission|Swami Vivekananda
Satyashodhak Samaj|Jyotirao Phule
Servants of India Society|Gopal Krishna Gokhale
Indian National Congress|A. O. Hume
Ghadar Party|Lala Har Dayal
Forward Bloc|Subhas Chandra Bose
Aligarh Movement|Sir Syed Ahmad Khan
Self-Respect Movement|E. V. Ramasamy (Periyar)
Young Bengal Movement|Henry Louis Vivian Derozio
Visva-Bharati University|Rabindranath Tagore
Banaras Hindu University|Madan Mohan Malaviya
Khudai Khidmatgar|Khan Abdul Ghaffar Khan
Indian Association|Surendranath Banerjee
Bhoodan Movement|Vinoba Bhave
Narmada Bachao Andolan|Medha Patkar
""")
table_topics('ga.founders', GA, 'Founders – Organisations & Movements', FOUNDERS, [
    ("Who founded the {a}?", 'b', "The {a} was founded by {b}."),
    ("{b} founded the ___.", 'a', "The {a} was founded by {b}."),
])

FIRSTS = rows("""
First President of India|Dr Rajendra Prasad
First Prime Minister of India|Jawaharlal Nehru
First Vice President of India|Dr S. Radhakrishnan
First woman Prime Minister of India|Indira Gandhi
First woman President of India|Pratibha Patil
First Indian Governor-General of India|C. Rajagopalachari
First Governor-General of independent India|Lord Mountbatten
First Chief Justice of India|H. J. Kania
First Chief Election Commissioner of India|Sukumar Sen
First Speaker of the Lok Sabha|G. V. Mavalankar
First woman Speaker of the Lok Sabha|Meira Kumar
First woman Governor of an Indian state|Sarojini Naidu
First woman Chief Minister of an Indian state|Sucheta Kriplani
First Indian in space|Rakesh Sharma
First Indian-born woman in space|Kalpana Chawla
First Indian Nobel laureate|Rabindranath Tagore
First Indian woman to climb Mount Everest|Bachendri Pal
First woman IPS officer|Kiran Bedi
First Indian woman to win an Olympic medal|Karnam Malleswari
First Indian to join the ICS|Satyendranath Tagore
""")
table_topics('ga.firsts', GA, 'Firsts in India', FIRSTS, [
    ("Who was the {a}?", 'b', "{b} – {a}."),
])

# ------------------------------------------------------------------ Polity
SCHEDULES = rows("""
First Schedule|Names of States and Union Territories
Second Schedule|Salaries and allowances of the President, Governors, judges, etc.
Third Schedule|Forms of oaths and affirmations
Fourth Schedule|Allocation of seats in the Rajya Sabha
Fifth Schedule|Administration of Scheduled Areas and Scheduled Tribes
Sixth Schedule|Tribal areas of Assam, Meghalaya, Tripura and Mizoram
Seventh Schedule|Union, State and Concurrent Lists
Eighth Schedule|Languages recognised by the Constitution
Ninth Schedule|Laws protected from judicial review (added by the 1st Amendment)
Tenth Schedule|Anti-defection law
Eleventh Schedule|Powers of Panchayats (29 subjects)
Twelfth Schedule|Powers of Municipalities (18 subjects)
""")
table_topics('ga.schedules', GA, 'Polity – Schedules of the Constitution', SCHEDULES, [
    ("The {a} of the Constitution deals with ___.", 'b', "{a}: {b}."),
    ("Which Schedule of the Constitution deals with: {b}?", 'a', "{a}: {b}."),
])

AMENDMENTS = rows("""
1st Amendment (1951)|Added the Ninth Schedule
7th Amendment (1956)|Reorganisation of states on linguistic lines
52nd Amendment (1985)|Anti-defection law (Tenth Schedule)
69th Amendment (1991)|Special status for Delhi as the National Capital Territory
86th Amendment (2002)|Right to Education (Article 21A)
91st Amendment (2003)|Size of the Council of Ministers limited to 15% of the House
97th Amendment (2011)|Constitutional status for cooperative societies
103rd Amendment (2019)|10% reservation for economically weaker sections
104th Amendment (2020)|Ended nomination of Anglo-Indians to the Lok Sabha
105th Amendment (2021)|Restored the power of states to identify backward classes
106th Amendment (2023)|One-third reservation for women in the Lok Sabha and state assemblies
""")
table_topics('ga.amendments', GA, 'Polity – Constitutional Amendments', AMENDMENTS, [
    ("The {a} is related to ___.", 'b', "{a}: {b}."),
    ("Which amendment provided for: {b}?", 'a', "{a}: {b}."),
], difficulty='hard')

POLITY_MORE = [
    ("How many Schedules does the Constitution of India have at present?", ['12', '8', '10', '14'], 'easy', "Originally 8; now 12."),
    ("How many languages are listed in the Eighth Schedule?", ['22', '18', '24', '14'], 'easy', "22 languages after the 92nd Amendment (2003)."),
    ("The minimum age to become a member of the Lok Sabha is ___.", ['25 years', '30 years', '21 years', '35 years'], 'easy', "Article 84."),
    ("The minimum age to become a member of the Rajya Sabha is ___.", ['30 years', '25 years', '35 years', '21 years'], 'easy', "Article 84."),
    ("The minimum age to become President of India is ___.", ['35 years', '30 years', '25 years', '40 years'], 'easy', "Article 58."),
    ("The President of India is elected by ___.", ['An electoral college of elected MPs and MLAs', 'Direct vote of citizens', 'Lok Sabha only', 'Rajya Sabha only'], 'medium', "Article 54."),
    ("Who administers the oath of office to the President of India?", ['The Chief Justice of India', 'The Vice President', 'The Speaker', 'The Prime Minister'], 'medium', "Article 60."),
    ("The Vice President of India is the ex-officio Chairman of the ___.", ['Rajya Sabha', 'Lok Sabha', 'NITI Aayog', 'Planning Commission'], 'easy', "Article 64."),
    ("A Money Bill can be introduced only in the ___.", ['Lok Sabha', 'Rajya Sabha', 'Either House', 'Joint sitting'], 'medium', "Article 109."),
    ("The Rajya Sabha can delay a Money Bill for at most ___.", ['14 days', '30 days', '6 months', '3 months'], 'medium', "It must return it within 14 days."),
    ("A joint sitting of both Houses of Parliament is presided over by the ___.", ['Speaker of the Lok Sabha', 'President', 'Vice President', 'Prime Minister'], 'medium', "Article 108 and 118."),
    ("The Rajya Sabha is a permanent body; ___ of its members retire every two years.", ['One-third', 'One-half', 'One-fourth', 'Two-thirds'], 'easy', "Article 83."),
    ("Judges of the Supreme Court retire at the age of ___.", ['65 years', '62 years', '60 years', '70 years'], 'easy', "Article 124."),
    ("Judges of a High Court retire at the age of ___.", ['62 years', '65 years', '60 years', '58 years'], 'easy', "Article 217."),
    ("The writ issued to produce a detained person before the court is ___.", ['Habeas corpus', 'Mandamus', 'Certiorari', 'Quo warranto'], 'easy', "'To have the body'."),
    ("The writ commanding a public official to perform a duty is ___.", ['Mandamus', 'Habeas corpus', 'Prohibition', 'Quo warranto'], 'medium', "'We command'."),
    ("The writ that asks 'by what authority' a person holds a public office is ___.", ['Quo warranto', 'Certiorari', 'Mandamus', 'Prohibition'], 'medium', "Quo warranto."),
    ("Panchayati Raj was first introduced in India in ___.", ['Nagaur, Rajasthan (1959)', 'Anand, Gujarat (1960)', 'Lucknow, UP (1952)', 'Patna, Bihar (1957)'], 'medium', "Inaugurated by Nehru on 2 October 1959."),
    ("The Balwant Rai Mehta Committee is associated with ___.", ['Panchayati Raj', 'Centre–state relations', 'Banking reforms', 'Official languages'], 'medium', "Recommended three-tier Panchayati Raj (1957)."),
    ("The Sarkaria Commission examined ___.", ['Centre–state relations', 'Electoral reforms', 'Police reforms', 'Tax reforms'], 'medium', "Set up in 1983."),
    ("Which Article deals with the Comptroller and Auditor General of India?", ['Article 148', 'Article 76', 'Article 280', 'Article 324'], 'medium', "Article 148."),
    ("Which body conducts elections to the Lok Sabha and state assemblies?", ['Election Commission of India', 'State Election Commission', 'Parliament', 'Supreme Court'], 'easy', "Article 324."),
    ("Elections to Panchayats are conducted by the ___.", ['State Election Commission', 'Election Commission of India', 'District Collector', 'Governor'], 'medium', "Article 243K."),
    ("The Constitution of India was adopted with ___ Articles originally.", ['395', '448', '370', '420'], 'medium', "395 Articles, 22 Parts, 8 Schedules."),
]
register('ga.polity', GA, 'Indian Polity', rows=POLITY_MORE)

# ------------------------------------------------------------------ Geography & history extras
GEOGRAPHY_MORE = [
    ("The Tropic of Cancer does NOT pass through which state?", ['Odisha', 'Jharkhand', 'Mizoram', 'Tripura'], 'hard', "It passes through Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura and Mizoram."),
    ("The highest peak in India is ___.", ['Kangchenjunga', 'Nanda Devi', 'K2', 'Anamudi'], 'easy', "Kangchenjunga (8,586 m) in Sikkim."),
    ("The highest peak of the Western Ghats is ___.", ['Anamudi', 'Doddabetta', 'Mahendragiri', 'Kalsubai'], 'medium', "Anamudi (2,695 m) in Kerala."),
    ("The oldest mountain range in India is the ___.", ['Aravalli', 'Himalaya', 'Vindhya', 'Satpura'], 'easy', "Aravallis are among the world's oldest fold mountains."),
    ("The largest state of India by area is ___.", ['Rajasthan', 'Madhya Pradesh', 'Maharashtra', 'Uttar Pradesh'], 'easy', "Rajasthan."),
    ("The smallest state of India by area is ___.", ['Goa', 'Sikkim', 'Tripura', 'Mizoram'], 'easy', "Goa."),
    ("Which state has the longest coastline in India?", ['Gujarat', 'Andhra Pradesh', 'Tamil Nadu', 'Maharashtra'], 'medium', "Gujarat."),
    ("The Palk Strait separates India from ___.", ['Sri Lanka', 'Maldives', 'Myanmar', 'Bangladesh'], 'easy', "Between Tamil Nadu and Sri Lanka."),
    ("The Duncan Passage lies between ___.", ['South Andaman and Little Andaman', 'Little Andaman and Car Nicobar', 'India and Sri Lanka', 'Lakshadweep and Maldives'], 'hard', "In the Andaman Islands."),
    ("The 'Ten Degree Channel' separates ___.", ['Andaman Islands and Nicobar Islands', 'Lakshadweep and Maldives', 'India and Sri Lanka', 'Great and Little Nicobar'], 'medium', "Ten Degree Channel."),
    ("India's only active volcano is on ___.", ['Barren Island', 'Narcondam Island', 'Havelock Island', 'Minicoy'], 'medium', "Barren Island, Andaman Sea."),
    ("Black soil (regur) is best suited for growing ___.", ['Cotton', 'Tea', 'Rice', 'Jute'], 'easy', "Moisture-retentive soil of the Deccan."),
    ("The Indira Gandhi Canal irrigates mainly ___.", ['Rajasthan', 'Punjab', 'Haryana', 'Gujarat'], 'easy', "Draws water from the Sutlej–Beas (Harike barrage)."),
    ("Bhakra Nangal Dam is built on the river ___.", ['Sutlej', 'Beas', 'Ravi', 'Chenab'], 'easy', "Himachal Pradesh–Punjab."),
    ("Hirakud Dam is built on the river ___.", ['Mahanadi', 'Godavari', 'Krishna', 'Damodar'], 'easy', "Odisha."),
    ("Sardar Sarovar Dam is on the river ___.", ['Narmada', 'Tapti', 'Mahi', 'Sabarmati'], 'easy', "Gujarat."),
    ("Tehri Dam is built on the river ___.", ['Bhagirathi', 'Alaknanda', 'Yamuna', 'Ganga at Haridwar'], 'medium', "Uttarakhand."),
    ("Which river is known as the 'Sorrow of Bihar'?", ['Kosi', 'Gandak', 'Son', 'Ghaghara'], 'easy', "Frequent floods and course changes."),
    ("Which river is known as the 'Sorrow of Bengal'?", ['Damodar', 'Hooghly', 'Teesta', 'Subarnarekha'], 'easy', "Damodar."),
    ("The Godavari is also called the ___.", ['Dakshin Ganga', 'Vridha Ganga only', 'Lifeline of Gujarat', 'Red River'], 'easy', "Largest peninsular river."),
    ("Majuli, one of the largest river islands in the world, is in ___.", ['Assam', 'West Bengal', 'Bihar', 'Odisha'], 'easy', "On the Brahmaputra."),
    ("Which state is the largest producer of tea in India?", ['Assam', 'West Bengal', 'Kerala', 'Tamil Nadu'], 'easy', "Assam."),
    ("The Siachen Glacier lies in the ___ range.", ['Karakoram', 'Zanskar', 'Pir Panjal', 'Shivalik'], 'medium', "Karakoram."),
    ("Which pass connects Srinagar and Leh?", ['Zoji La', 'Nathu La', 'Shipki La', 'Rohtang'], 'medium', "Zoji La."),
    ("Nathu La pass connects Sikkim with ___.", ['Tibet (China)', 'Nepal', 'Bhutan', 'Myanmar'], 'medium', "Nathu La."),
]
register('ga.geography', GA, 'Geography', rows=GEOGRAPHY_MORE)

HISTORY_MORE = [
    ("The Harappan site of Lothal, known for its dockyard, is in ___.", ['Gujarat', 'Rajasthan', 'Punjab', 'Haryana'], 'easy', "Lothal, Gujarat."),
    ("The Great Bath was found at ___.", ['Mohenjo-daro', 'Harappa', 'Kalibangan', 'Lothal'], 'easy', "Mohenjo-daro."),
    ("Gautama Buddha attained enlightenment at ___.", ['Bodh Gaya', 'Sarnath', 'Kushinagar', 'Lumbini'], 'easy', "Under the Bodhi tree."),
    ("Buddha delivered his first sermon at ___.", ['Sarnath', 'Bodh Gaya', 'Rajgir', 'Vaishali'], 'easy', "Dharmachakra Pravartana."),
    ("The 24th Tirthankara of Jainism was ___.", ['Mahavira', 'Rishabhanatha', 'Parshvanatha', 'Neminatha'], 'easy', "Vardhamana Mahavira."),
    ("The founder of the Maurya Empire was ___.", ['Chandragupta Maurya', 'Ashoka', 'Bindusara', 'Bimbisara'], 'easy', "c. 322 BCE."),
    ("Ashoka embraced Buddhism after the ___.", ['Kalinga War', 'Battle of Hydaspes', 'Battle of Tarain', 'Kurukshetra war'], 'easy', "c. 261 BCE."),
    ("The 'Arthashastra' was written by ___.", ['Kautilya', 'Kalidasa', 'Banabhatta', 'Megasthenes'], 'easy', "Chanakya (Kautilya)."),
    ("'Indica' was written by ___.", ['Megasthenes', 'Fa-Hien', 'Hiuen Tsang', 'Al-Biruni'], 'medium', "Greek envoy at Chandragupta's court."),
    ("The Gupta ruler known as the 'Napoleon of India' is ___.", ['Samudragupta', 'Chandragupta II', 'Skandagupta', 'Kumaragupta'], 'medium', "As per V. A. Smith."),
    ("The Chinese pilgrim who visited India during Harshavardhana's reign was ___.", ['Hiuen Tsang', 'Fa-Hien', 'I-Tsing', 'Megasthenes'], 'medium', "Xuanzang."),
    ("The founder of the Delhi Sultanate's Slave dynasty was ___.", ['Qutb-ud-din Aibak', 'Iltutmish', 'Balban', 'Razia Sultan'], 'easy', "1206."),
    ("Who introduced the market reforms in the Delhi Sultanate?", ['Alauddin Khalji', 'Muhammad bin Tughlaq', 'Firoz Shah Tughlaq', 'Balban'], 'medium', "Alauddin Khalji."),
    ("Who shifted the capital from Delhi to Daulatabad?", ['Muhammad bin Tughlaq', 'Alauddin Khalji', 'Iltutmish', 'Sikandar Lodi'], 'easy', "Muhammad bin Tughlaq."),
    ("The founder of the Mughal Empire in India was ___.", ['Babur', 'Humayun', 'Akbar', 'Sher Shah Suri'], 'easy', "First Battle of Panipat, 1526."),
    ("Din-i-Ilahi was started by ___.", ['Akbar', 'Jahangir', 'Shah Jahan', 'Aurangzeb'], 'easy', "1582."),
    ("The Grand Trunk Road was rebuilt and extended by ___.", ['Sher Shah Suri', 'Akbar', 'Ashoka', 'Shah Jahan'], 'medium', "Sadak-e-Azam."),
    ("Shivaji was crowned Chhatrapati in 1674 at ___.", ['Raigad', 'Pune', 'Satara', 'Sinhagad'], 'medium', "Raigad fort."),
    ("The Doctrine of Lapse was introduced by ___.", ['Lord Dalhousie', 'Lord Wellesley', 'Lord Cornwallis', 'Lord Curzon'], 'easy', "Annexed Satara, Jhansi, Nagpur."),
    ("The Subsidiary Alliance system was introduced by ___.", ['Lord Wellesley', 'Lord Dalhousie', 'Warren Hastings', 'Lord Hastings'], 'medium', "1798."),
    ("The Permanent Settlement of Bengal (1793) was introduced by ___.", ['Lord Cornwallis', 'Lord Wellesley', 'Warren Hastings', 'Lord Bentinck'], 'medium', "Cornwallis."),
    ("Sati was abolished in 1829 by ___.", ['Lord William Bentinck', 'Lord Dalhousie', 'Lord Canning', 'Lord Ripon'], 'easy', "With Raja Ram Mohan Roy's support."),
    ("The first session of the Indian National Congress was held at ___.", ['Bombay', 'Calcutta', 'Madras', 'Lahore'], 'easy', "1885, presided by W. C. Bonnerjee."),
    ("The Congress declared 'Purna Swaraj' as its goal at the ___ session.", ['Lahore (1929)', 'Lucknow (1916)', 'Karachi (1931)', 'Haripura (1938)'], 'medium', "Presided by Jawaharlal Nehru."),
    ("The slogan 'Do or Die' was given during the ___.", ['Quit India Movement', 'Non-Cooperation Movement', 'Civil Disobedience Movement', 'Swadeshi Movement'], 'easy', "Gandhi, August 1942."),
    ("Who gave the slogan 'Swaraj is my birthright and I shall have it'?", ['Bal Gangadhar Tilak', 'Lala Lajpat Rai', 'Gopal Krishna Gokhale', 'Bipin Chandra Pal'], 'easy', "Tilak."),
    ("Who gave the slogan 'Jai Hind'?", ['Subhas Chandra Bose', 'Mahatma Gandhi', 'Bhagat Singh', 'Jawaharlal Nehru'], 'medium', "Popularised by Netaji and the INA."),
    ("Who composed 'Vande Mataram'?", ['Bankim Chandra Chattopadhyay', 'Rabindranath Tagore', 'Muhammad Iqbal', 'Sarojini Naidu'], 'easy', "In the novel Anandamath."),
    ("Who wrote 'Saare Jahan Se Achha'?", ['Muhammad Iqbal', 'Rabindranath Tagore', 'Bankim Chandra Chattopadhyay', 'Ram Prasad Bismil'], 'easy', "Muhammad Iqbal."),
    ("The Indian National Army (Azad Hind Fauj) was first organised by ___.", ['Mohan Singh', 'Subhas Chandra Bose', 'Rash Behari Bose', 'Shah Nawaz Khan'], 'hard', "Captain Mohan Singh in 1942; later led by Netaji."),
]
register('ga.history', GA, 'History', rows=HISTORY_MORE)

ECONOMY_MORE = [
    ("The Reserve Bank of India was established in ___.", ['1935', '1949', '1947', '1969'], 'easy', "Under the RBI Act, 1934; nationalised in 1949."),
    ("The RBI was nationalised in ___.", ['1949', '1935', '1969', '1955'], 'medium', "1 January 1949."),
    ("Fourteen major commercial banks were nationalised in ___.", ['1969', '1980', '1955', '1991'], 'easy', "19 July 1969."),
    ("The State Bank of India was formed in 1955 from the ___.", ['Imperial Bank of India', 'Bank of Calcutta', 'Presidency Bank of Madras', 'Allahabad Bank'], 'medium', "Imperial Bank of India."),
    ("NABARD was established in ___.", ['1982', '1975', '1990', '1969'], 'medium', "Apex bank for agriculture and rural development."),
    ("SEBI got statutory powers in ___.", ['1992', '1988', '1995', '2000'], 'medium', "Set up in 1988; statutory body under the SEBI Act, 1992."),
    ("SIDBI primarily finances ___.", ['Micro, small and medium enterprises', 'Agriculture', 'Exports only', 'Housing'], 'easy', "Set up in 1990."),
    ("Regional Rural Banks were first set up in ___.", ['1975', '1969', '1982', '1991'], 'medium', "On 2 October 1975."),
    ("GST was rolled out in India on ___.", ['1 July 2017', '1 April 2017', '8 November 2016', '1 January 2018'], 'easy', "Under the 101st Amendment."),
    ("NITI Aayog replaced the Planning Commission on ___.", ['1 January 2015', '15 August 2014', '26 January 2015', '1 April 2015'], 'medium', "1 January 2015."),
    ("The Indian rupee symbol (₹) was designed by ___.", ['D. Udaya Kumar', 'Raghuram Rajan', 'Satyajit Ray', 'Urjit Patel'], 'medium', "Adopted in 2010."),
    ("Who chairs the GST Council?", ['The Union Finance Minister', 'The Prime Minister', 'The RBI Governor', 'The President'], 'easy', "Article 279A."),
    ("Who chairs the Monetary Policy Committee?", ['The RBI Governor', 'The Finance Minister', 'The Chief Economic Adviser', 'The Prime Minister'], 'easy', "Six-member MPC."),
    ("Repo rate is the rate at which ___.", ['RBI lends to banks', 'Banks lend to the RBI', 'Banks lend to customers', 'Government borrows abroad'], 'easy', "Short-term lending against securities."),
    ("Cash Reserve Ratio (CRR) is kept by banks with the ___.", ['RBI', 'Government of India', 'SEBI', 'Their own branches'], 'easy', "As cash balance with the RBI."),
    ("SLR is maintained in the form of ___.", ['Cash, gold and approved securities', 'Only cash with RBI', 'Foreign currency', 'Shares of companies'], 'medium', "Statutory Liquidity Ratio."),
    ("Which agency releases GDP estimates in India?", ['National Statistics Office (NSO)', 'RBI', 'NITI Aayog', 'Finance Commission'], 'medium', "Under MoSPI."),
    ("The Finance Commission is constituted every ___.", ['5 years', '3 years', '10 years', '2 years'], 'easy', "Article 280."),
    ("The 'Pradhan Mantri Jan Dhan Yojana' is related to ___.", ['Financial inclusion through bank accounts', 'Housing', 'Crop insurance', 'Skill training'], 'easy', "Launched in 2014."),
    ("UPI was developed by ___.", ['National Payments Corporation of India', 'RBI', 'SBI', 'NITI Aayog'], 'easy', "NPCI, launched 2016."),
    ("Which tax is a direct tax?", ['Income tax', 'GST', 'Customs duty', 'Excise duty'], 'easy', "Borne by the person on whom it is levied."),
    ("Inflation in India is targeted by the RBI at ___.", ['4% with a band of ±2%', '6% fixed', '2% with ±1%', '5% with ±3%'], 'medium', "Flexible inflation targeting since 2016."),
    ("The headquarters of the RBI is in ___.", ['Mumbai', 'New Delhi', 'Kolkata', 'Chennai'], 'easy', "Moved from Calcutta to Bombay in 1937."),
    ("The 'Kisan Credit Card' scheme was introduced in ___.", ['1998', '2005', '1991', '2014'], 'hard', "Based on the R. V. Gupta Committee."),
    ("The term 'stagflation' means ___.", ['High inflation with stagnant growth', 'Falling prices with growth', 'Rapid growth', 'Zero inflation'], 'medium', "Inflation + unemployment + slow growth."),
]
register('ga.economy', GA, 'Indian Economy & Banking', rows=ECONOMY_MORE)

# ------------------------------------------------------------------ Legal GK
ACTS = rows("""
Indian Contract Act|1872
Indian Evidence Act|1872
Indian Penal Code|1860
Transfer of Property Act|1882
Negotiable Instruments Act|1881
Code of Civil Procedure|1908
Sale of Goods Act|1930
Indian Partnership Act|1932
Hindu Marriage Act|1955
Hindu Succession Act|1956
Special Marriage Act|1954
Dowry Prohibition Act|1961
Advocates Act|1961
Limitation Act|1963
Specific Relief Act|1963
Wildlife (Protection) Act|1972
Forest (Conservation) Act|1980
Environment (Protection) Act|1986
Legal Services Authorities Act|1987
SC/ST (Prevention of Atrocities) Act|1989
Protection of Human Rights Act|1993
Arbitration and Conciliation Act|1996
Information Technology Act|2000
Right to Information Act|2005
Protection of Women from Domestic Violence Act|2005
Right of Children to Free and Compulsory Education Act|2009
POCSO Act|2012
Companies Act|2013
Juvenile Justice (Care and Protection of Children) Act|2015
Consumer Protection Act|2019
""")
table_topics('law.acts', LGL, 'Legal GK – Acts & Years', ACTS, [
    ("The {a} was enacted in ___.", 'b', "{a}, {b}."),
    ("Which of these laws was enacted in {b}?", 'a', "{a}, {b}."),
])

register('law.legal_gk', LGL, 'Legal GK', rows=[
    ("The Bharatiya Nyaya Sanhita, 2023 replaced the ___.", ['Indian Penal Code, 1860', 'Code of Criminal Procedure, 1973', 'Indian Evidence Act, 1872', 'Code of Civil Procedure, 1908'], 'easy', "In force from 1 July 2024."),
    ("The Bharatiya Nagarik Suraksha Sanhita, 2023 replaced the ___.", ['Code of Criminal Procedure, 1973', 'Indian Penal Code, 1860', 'Indian Evidence Act, 1872', 'Limitation Act, 1963'], 'easy', "In force from 1 July 2024."),
    ("The Bharatiya Sakshya Adhiniyam, 2023 replaced the ___.", ['Indian Evidence Act, 1872', 'Indian Penal Code, 1860', 'Code of Criminal Procedure, 1973', 'Indian Contract Act, 1872'], 'easy', "In force from 1 July 2024."),
    ("Which court has original jurisdiction in disputes between the Centre and a state?", ['Supreme Court', 'High Court', 'District Court', 'Tribunal'], 'easy', "Article 131."),
    ("Public Interest Litigation in India was pioneered by ___.", ['Justice P. N. Bhagwati and Justice V. R. Krishna Iyer', 'Justice H. J. Kania', 'Justice Y. V. Chandrachud alone', 'Justice M. C. Mahajan'], 'medium', "In the late 1970s and early 1980s."),
    ("Lok Adalats get statutory status under the ___.", ['Legal Services Authorities Act, 1987', 'Code of Civil Procedure, 1908', 'Arbitration Act, 1996', 'Constitution (42nd Amendment)'], 'medium', "Their awards are final and binding."),
    ("A contract with a minor in India is ___.", ['Void ab initio', 'Voidable at the option of the minor', 'Valid', 'Illegal and punishable'], 'medium', "Mohori Bibee v. Dharmodas Ghose (1903)."),
    ("'Consideration' in a contract means ___.", ['Something in return (quid pro quo)', 'Kindness', 'The written document', 'The court fee'], 'easy', "Section 2(d), Indian Contract Act."),
    ("An agreement without free consent caused by coercion is ___.", ['Voidable', 'Void', 'Valid', 'Illegal'], 'medium', "Section 19, Indian Contract Act."),
    ("The National Green Tribunal was set up in ___.", ['2010', '2005', '1986', '2015'], 'medium', "Under the NGT Act, 2010."),
    ("The Right to Information Act gives a reply time of ___ in normal cases.", ['30 days', '15 days', '60 days', '7 days'], 'easy', "48 hours if life or liberty is involved."),
    ("The Bar Council of India is a statutory body under the ___.", ['Advocates Act, 1961', 'Legal Services Authorities Act, 1987', 'Constitution, Article 32', 'Bar Act, 1926'], 'medium', "It also conducts the AIBE."),
    ("The doctrine of 'Basic Structure' was laid down in ___.", ['Kesavananda Bharati v. State of Kerala (1973)', 'Golaknath v. State of Punjab (1967)', 'Minerva Mills v. Union of India (1980)', 'Maneka Gandhi v. Union of India (1978)'], 'medium', "13-judge bench."),
    ("'Tort' is best described as ___.", ['A civil wrong other than breach of contract', 'A criminal offence', 'A breach of trust only', 'A type of contract'], 'easy', "Remedy: unliquidated damages."),
    ("Strict liability in tort originated in ___.", ['Rylands v. Fletcher', 'Donoghue v. Stevenson', 'Ashby v. White', 'Carlill v. Carbolic Smoke Ball Co.'], 'medium', "1868, English case."),
])

# ------------------------------------------------------------------ Computer awareness
ABBREVIATIONS = rows("""
CPU|Central Processing Unit
RAM|Random Access Memory
ROM|Read Only Memory
ALU|Arithmetic Logic Unit
BIOS|Basic Input/Output System
GUI|Graphical User Interface
URL|Uniform Resource Locator
HTTP|HyperText Transfer Protocol
HTML|HyperText Markup Language
LAN|Local Area Network
WAN|Wide Area Network
ISP|Internet Service Provider
DNS|Domain Name System
USB|Universal Serial Bus
PDF|Portable Document Format
SMTP|Simple Mail Transfer Protocol
FTP|File Transfer Protocol
VPN|Virtual Private Network
OCR|Optical Character Recognition
MICR|Magnetic Ink Character Recognition
UPS|Uninterruptible Power Supply
ASCII|American Standard Code for Information Interchange
WWW|World Wide Web
IP|Internet Protocol
SSD|Solid State Drive
OTP|One-Time Password
""")
table_topics('cs.abbreviations', CMP, 'Computer Abbreviations', ABBREVIATIONS, [
    ("In computers, '{a}' stands for ___.", 'b', "{a} = {b}."),
    ("What is the abbreviation for '{b}'?", 'a', "{a} = {b}."),
], difficulty='easy')

SHORTCUTS = rows("""
Ctrl + C|Copy
Ctrl + V|Paste
Ctrl + X|Cut
Ctrl + Z|Undo
Ctrl + Y|Redo
Ctrl + S|Save
Ctrl + P|Print
Ctrl + A|Select all
Ctrl + F|Find
Ctrl + B|Bold
Ctrl + I|Italic
Ctrl + U|Underline
Alt + F4|Close the active window
F5|Refresh (or start a slide show in PowerPoint)
Ctrl + N|New document or window
""")
table_topics('cs.shortcuts', CMP, 'Keyboard Shortcuts', SHORTCUTS, [
    ("In Windows / MS Office, the shortcut {a} is used to ___.", 'b', "{a}: {b}."),
    ("Which shortcut is used to '{b}'?", 'a', "{a}: {b}."),
], difficulty='easy')

register('cs.awareness', CMP, 'Computer Awareness', rows=[
    ("1 byte is equal to ___ bits.", ['8', '4', '16', '10'], 'easy', "1 byte = 8 bits."),
    ("1 kilobyte (KB) is equal to ___ bytes (binary convention).", ['1,024', '1,000', '512', '2,048'], 'easy', "2¹⁰ bytes."),
    ("Who is called the 'Father of the Computer'?", ['Charles Babbage', 'Alan Turing', 'John von Neumann', 'Bill Gates'], 'easy', "Designed the Analytical Engine."),
    ("First-generation computers used ___.", ['Vacuum tubes', 'Transistors', 'Integrated circuits', 'Microprocessors'], 'easy', "1940s–50s."),
    ("Second-generation computers used ___.", ['Transistors', 'Vacuum tubes', 'Integrated circuits', 'VLSI chips'], 'easy', "Late 1950s–60s."),
    ("Third-generation computers used ___.", ['Integrated circuits', 'Transistors', 'Vacuum tubes', 'Artificial intelligence'], 'easy', "1960s–70s."),
    ("Which memory loses its contents when power is switched off?", ['RAM', 'ROM', 'Hard disk', 'Flash drive'], 'easy', "RAM is volatile."),
    ("The brain of the computer is the ___.", ['CPU', 'Monitor', 'Keyboard', 'Hard disk'], 'easy', "Central Processing Unit."),
    ("Which of these is an input device?", ['Scanner', 'Printer', 'Monitor', 'Speaker'], 'easy', "Scanner."),
    ("Which of these is an output device?", ['Plotter', 'Mouse', 'Keyboard', 'Joystick'], 'easy', "Plotter."),
    ("Which of these is system software?", ['Operating system', 'MS Word', 'Photoshop', 'Tally'], 'easy', "Manages the hardware."),
    ("Linux is an example of ___.", ['Open-source operating system', 'Web browser', 'Spreadsheet', 'Antivirus'], 'easy', "Open source."),
    ("In MS Excel, a cell reference like $A$1 is ___.", ['Absolute reference', 'Relative reference', 'Mixed reference', 'Circular reference'], 'medium', "Both row and column fixed."),
    ("In MS Excel, columns are identified by ___.", ['Letters', 'Numbers', 'Symbols', 'Colours'], 'easy', "Rows by numbers."),
    ("Which device connects a computer to the internet over telephone or cable lines?", ['Modem', 'Monitor', 'Printer', 'Plotter'], 'easy', "Modulator–demodulator."),
    ("A computer virus is a ___.", ['Malicious program', 'Hardware fault', 'Type of RAM', 'Dust particle'], 'easy', "Malware."),
    ("Phishing means ___.", ['Tricking users into revealing personal data', 'Speeding up a computer', 'Backing up files', 'Compressing data'], 'easy', "Fraudulent messages/sites."),
    ("Which protocol is used to send e-mail?", ['SMTP', 'FTP', 'HTTP', 'DHCP'], 'medium', "Simple Mail Transfer Protocol."),
    ("The binary equivalent of decimal 10 is ___.", ['1010', '1100', '1001', '1110'], 'easy', "8 + 2."),
    ("Which key is used to start a new paragraph in a word processor?", ['Enter', 'Shift', 'Tab', 'Esc'], 'easy', "Enter key."),
    ("Which of these is a web browser?", ['Google Chrome', 'MS Excel', 'Windows', 'Oracle'], 'easy', "Chrome."),
    ("The extension '.xlsx' is used by ___.", ['MS Excel', 'MS Word', 'MS PowerPoint', 'Notepad'], 'easy', "Excel workbook."),
    ("The extension '.pptx' is used by ___.", ['MS PowerPoint', 'MS Excel', 'MS Access', 'MS Word'], 'easy', "PowerPoint presentation."),
    ("Which storage device has no moving parts?", ['Solid State Drive', 'Hard Disk Drive', 'Floppy disk drive', 'CD-ROM drive'], 'easy', "Flash memory."),
    ("A 'firewall' is used to ___.", ['Block unauthorised network access', 'Cool the CPU', 'Store passwords', 'Increase RAM'], 'easy', "Network security."),
])
