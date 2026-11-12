from django.core.management.base import BaseCommand
from django.db import transaction

from testseries.models import TestSeries, Test, Question, Subject
from testseries.management.commands.seed_school_series import shuffled_options

SERIES_TITLE = "CBSE Class 1 – Subject-wise Test Series"
OLD_TITLES = ["CBSE Class 1 – Subject-wise Test Series (Lucknow)"]

SUBJECTS = {
    'ENG1': ('English', '#3B82F6', 'book'),
    'HIN1': ('Hindi', '#F97316', 'language'),
    'MAT1': ('Mathematics', '#10B981', 'calculator'),
    'EVS1': ('EVS', '#22C55E', 'leaf'),
    'GK1': ('General Knowledge', '#8B5CF6', 'globe'),
    'RSN1': ('Reasoning', '#EC4899', 'brain'),
}

# (subject code, test title, description, [(question, [a, b, c, d], answer, difficulty, explanation)])
TESTS = [
    ('ENG1', 'English Test 1 – Alphabet & Vowels', 'Capital and small letters, vowels and letter order.', [
        ("Which letter comes after 'C'?", ['B', 'D', 'E', 'F'], 'b', 'easy', "The order is A, B, C, D."),
        ("Which of these is a vowel?", ['B', 'K', 'E', 'M'], 'c', 'easy', "The vowels are A, E, I, O, U."),
        ("How many letters are there in the English alphabet?", ['24', '25', '26', '28'], 'c', 'easy', "There are 26 letters from A to Z."),
        ("What is the small letter of 'G'?", ['q', 'g', 'j', 'p'], 'b', 'easy', "Capital G is written as g in small letters."),
        ("Which letter comes between 'L' and 'N'?", ['K', 'O', 'M', 'P'], 'c', 'easy', "L, M, N."),
        ("How many vowels are there in English?", ['3', '4', '5', '6'], 'c', 'easy', "A, E, I, O, U are five vowels."),
        ("Which is the last letter of the alphabet?", ['X', 'Y', 'W', 'Z'], 'd', 'easy', "Z is the last letter."),
        ("Which word starts with a vowel?", ['Apple', 'Ball', 'Cat', 'Dog'], 'a', 'medium', "Apple starts with A, which is a vowel."),
        ("Which letter comes before 'S'?", ['T', 'R', 'Q', 'U'], 'b', 'medium', "R comes just before S."),
        ("Fill in the missing letter: P, Q, __, S", ['T', 'O', 'R', 'U'], 'c', 'medium', "P, Q, R, S."),
    ]),
    ('ENG1', 'English Test 2 – Words & Grammar', 'Opposites, a/an, naming words and simple spellings.', [
        ("What is the opposite of 'big'?", ['Tall', 'Small', 'Fat', 'Long'], 'b', 'easy', "Big and small are opposites."),
        ("Choose the correct word: ___ apple", ['a', 'an', 'the two', 'some a'], 'b', 'easy', "We use 'an' before a vowel sound."),
        ("Choose the correct word: ___ cat", ['an', 'a', 'two', 'many a'], 'b', 'easy', "We use 'a' before a consonant sound."),
        ("What is the opposite of 'hot'?", ['Warm', 'Cold', 'Wet', 'Dry'], 'b', 'easy', "Hot and cold are opposites."),
        ("Which is the correct spelling?", ['Bal', 'Ball', 'Baal', 'Bol'], 'b', 'easy', "B-A-L-L spells ball."),
        ("Which of these is a naming word (noun)?", ['Run', 'Happy', 'Table', 'Quickly'], 'c', 'medium', "Table is the name of a thing."),
        ("What is the plural of 'pen'?", ['Pens', 'Penes', 'Pen', 'Penns'], 'a', 'medium', "Add -s: pens."),
        ("What is the opposite of 'day'?", ['Morning', 'Evening', 'Night', 'Noon'], 'c', 'easy', "Day and night are opposites."),
        ("Which word rhymes with 'cat'?", ['Cup', 'Hat', 'Cot', 'Car'], 'b', 'medium', "Cat and hat both end with -at."),
        ("Which is the correct spelling?", ['Skool', 'Scool', 'School', 'Schol'], 'c', 'medium', "S-C-H-O-O-L spells school."),
    ]),
    ('HIN1', 'हिंदी टेस्ट 1 – स्वर और व्यंजन', 'स्वर, व्यंजन और वर्णमाला का क्रम।', [
        ("'अ' के बाद कौन सा स्वर आता है?", ['इ', 'आ', 'उ', 'ए'], 'b', 'easy', "अ, आ, इ, ई ..."),
        ("इनमें से कौन सा स्वर है?", ['क', 'ख', 'इ', 'ग'], 'c', 'easy', "इ एक स्वर है।"),
        ("'क' के बाद कौन सा व्यंजन आता है?", ['ग', 'ख', 'घ', 'च'], 'b', 'easy', "क, ख, ग, घ ..."),
        ("'च' वर्ग का पहला अक्षर कौन सा है?", ['ज', 'छ', 'च', 'झ'], 'c', 'easy', "च, छ, ज, झ।"),
        ("'आम' शब्द किस अक्षर से शुरू होता है?", ['अ', 'आ', 'इ', 'म'], 'b', 'easy', "आम = आ + म।"),
        ("इनमें से कौन सा व्यंजन है?", ['उ', 'ए', 'ओ', 'प'], 'd', 'easy', "प एक व्यंजन है।"),
        ("'ग' और 'ङ' के बीच कौन सा अक्षर आता है?", ['घ', 'ख', 'च', 'क'], 'a', 'medium', "क, ख, ग, घ, ङ।"),
        ("'कमल' शब्द में कितने अक्षर हैं?", ['2', '3', '4', '5'], 'b', 'medium', "क + म + ल = 3 अक्षर।"),
        ("'त' के बाद कौन सा अक्षर आता है?", ['द', 'थ', 'ध', 'न'], 'b', 'medium', "त, थ, द, ध, न।"),
        ("हिंदी वर्णमाला का पहला अक्षर कौन सा है?", ['क', 'आ', 'अ', 'इ'], 'c', 'easy', "वर्णमाला 'अ' से शुरू होती है।"),
    ]),
    ('HIN1', 'हिंदी टेस्ट 2 – शब्द और चित्र', 'सरल शब्द, फल-जानवरों के नाम और विलोम शब्द।', [
        ("'बिल्ली' कौन सी आवाज़ निकालती है?", ['भौं-भौं', 'म्याऊँ', 'काँव-काँव', 'मैं-मैं'], 'b', 'easy', "बिल्ली म्याऊँ करती है।"),
        ("इनमें से कौन सा फल है?", ['आलू', 'केला', 'प्याज़', 'गाजर'], 'b', 'easy', "केला एक फल है।"),
        ("'बड़ा' का उल्टा (विलोम) क्या है?", ['मोटा', 'लंबा', 'छोटा', 'ऊँचा'], 'c', 'easy', "बड़ा – छोटा।"),
        ("'दिन' का विलोम शब्द क्या है?", ['सुबह', 'रात', 'शाम', 'दोपहर'], 'b', 'easy', "दिन – रात।"),
        ("आसमान का रंग कैसा होता है?", ['हरा', 'लाल', 'नीला', 'पीला'], 'c', 'easy', "आसमान नीला दिखता है।"),
        ("'गाय' हमें क्या देती है?", ['अंडा', 'दूध', 'ऊन', 'शहद'], 'b', 'easy', "गाय हमें दूध देती है।"),
        ("'ठंडा' का विलोम शब्द क्या है?", ['गरम', 'गीला', 'सूखा', 'मीठा'], 'a', 'medium', "ठंडा – गरम।"),
        ("इनमें से कौन सा जानवर है?", ['आम', 'शेर', 'कमल', 'पेड़'], 'b', 'easy', "शेर एक जानवर है।"),
        ("'घर' शब्द किस अक्षर से शुरू होता है?", ['ग', 'घ', 'र', 'क'], 'b', 'medium', "घर = घ + र।"),
        ("सही शब्द चुनिए: पानी में रहने वाला जीव", ['मछली', 'तोता', 'बकरी', 'घोड़ा'], 'a', 'medium', "मछली पानी में रहती है।"),
    ]),
    ('MAT1', 'Maths Test 1 – Numbers & Counting', 'Counting, number order, before/after and comparing numbers.', [
        ("What comes after 9?", ['8', '10', '11', '19'], 'b', 'easy', "9, 10."),
        ("What comes before 20?", ['21', '18', '19', '10'], 'c', 'easy', "19 comes just before 20."),
        ("Which number is the biggest?", ['12', '21', '19', '15'], 'b', 'easy', "21 is the biggest."),
        ("Which number is the smallest?", ['7', '3', '9', '5'], 'b', 'easy', "3 is the smallest."),
        ("What number comes between 14 and 16?", ['13', '15', '17', '12'], 'b', 'easy', "14, 15, 16."),
        ("How many fingers are there on one hand?", ['4', '5', '6', '10'], 'b', 'easy', "One hand has 5 fingers."),
        ("Which number is written as 'thirty'?", ['13', '30', '33', '3'], 'b', 'medium', "Thirty = 30."),
        ("How many tens are there in 40?", ['4', '40', '0', '14'], 'a', 'medium', "40 = 4 tens."),
        ("Fill in the blank: 2, 4, 6, __, 10", ['7', '9', '8', '12'], 'c', 'medium', "Counting by 2s: 8."),
        ("Which sign is correct? 8 __ 5", ['<', '>', '=', '+'], 'b', 'medium', "8 is greater than 5, so 8 > 5."),
    ]),
    ('MAT1', 'Maths Test 2 – Addition & Subtraction', 'Adding and taking away numbers up to 20.', [
        ("3 + 2 = ?", ['4', '5', '6', '1'], 'b', 'easy', "3 + 2 = 5."),
        ("7 - 3 = ?", ['3', '5', '4', '10'], 'c', 'easy', "7 - 3 = 4."),
        ("5 + 5 = ?", ['10', '55', '9', '11'], 'a', 'easy', "5 + 5 = 10."),
        ("9 - 9 = ?", ['9', '1', '18', '0'], 'd', 'easy', "Any number minus itself is 0."),
        ("6 + 0 = ?", ['0', '6', '60', '7'], 'b', 'easy', "Adding 0 does not change a number."),
        ("8 + 4 = ?", ['11', '12', '13', '14'], 'b', 'medium', "8 + 4 = 12."),
        ("15 - 5 = ?", ['5', '20', '10', '15'], 'c', 'medium', "15 - 5 = 10."),
        ("Riya has 4 apples. She gets 3 more. How many apples does she have now?", ['6', '7', '1', '8'], 'b', 'medium', "4 + 3 = 7."),
        ("There are 10 birds. 6 fly away. How many are left?", ['4', '16', '6', '3'], 'a', 'medium', "10 - 6 = 4."),
        ("9 + 6 = ?", ['14', '16', '15', '13'], 'c', 'hard', "9 + 6 = 15."),
    ]),
    ('MAT1', 'Maths Test 3 – Shapes, Time & Money', 'Basic shapes, days of the week, clock and Indian coins.', [
        ("How many sides does a triangle have?", ['2', '3', '4', '5'], 'b', 'easy', "A triangle has 3 sides."),
        ("Which shape is round like a ball's outline?", ['Square', 'Triangle', 'Circle', 'Rectangle'], 'c', 'easy', "A circle is round."),
        ("How many sides does a square have?", ['3', '5', '4', '6'], 'c', 'easy', "A square has 4 equal sides."),
        ("How many days are there in a week?", ['5', '6', '7', '10'], 'c', 'easy', "Monday to Sunday is 7 days."),
        ("Which day comes after Monday?", ['Sunday', 'Tuesday', 'Wednesday', 'Friday'], 'b', 'easy', "Monday, Tuesday."),
        ("What is the money used in India called?", ['Dollar', 'Rupee', 'Pound', 'Yen'], 'b', 'easy', "India uses the Rupee (₹)."),
        ("A clock has how many hands (usually)?", ['1', '2', '4', '5'], 'b', 'medium', "An hour hand and a minute hand."),
        ("₹2 + ₹5 = ?", ['₹3', '₹7', '₹10', '₹25'], 'b', 'medium', "2 + 5 = 7 rupees."),
        ("Which day comes before Sunday?", ['Monday', 'Friday', 'Saturday', 'Thursday'], 'c', 'medium', "Saturday, Sunday."),
        ("Which of these has no corners?", ['Square', 'Circle', 'Triangle', 'Rectangle'], 'b', 'medium', "A circle has no corners."),
    ]),
    ('EVS1', 'EVS Test 1 – My Body & Family', 'Parts of the body, sense organs, healthy habits and family.', [
        ("We see with our ___.", ['Ears', 'Eyes', 'Nose', 'Hands'], 'b', 'easy', "Eyes help us see."),
        ("We hear with our ___.", ['Ears', 'Tongue', 'Eyes', 'Legs'], 'a', 'easy', "Ears help us hear."),
        ("We smell with our ___.", ['Mouth', 'Skin', 'Nose', 'Eyes'], 'c', 'easy', "The nose helps us smell."),
        ("How many legs do we have?", ['1', '2', '3', '4'], 'b', 'easy', "We have two legs."),
        ("We should brush our teeth ___.", ['Once a week', 'Never', 'Twice a day', 'Once a month'], 'c', 'easy', "Brush in the morning and at night."),
        ("Your father's mother is your ___.", ['Aunt', 'Sister', 'Grandmother', 'Cousin'], 'c', 'medium', "Father's mother is grandmother (Dadi)."),
        ("We should wash our hands ___ eating.", ['After only', 'Before', 'Never', 'Instead of'], 'b', 'easy', "Always wash hands before eating."),
        ("Which part of the body helps us taste food?", ['Tongue', 'Nose', 'Ear', 'Hair'], 'a', 'medium', "The tongue tastes food."),
        ("How many sense organs do we have?", ['3', '4', '5', '6'], 'c', 'medium', "Eyes, ears, nose, tongue and skin."),
        ("Which food is healthy?", ['Chips', 'Fruits', 'Candy', 'Cold drink'], 'b', 'easy', "Fruits keep us healthy."),
    ]),
    ('EVS1', 'EVS Test 2 – Plants, Animals & Surroundings', 'Plants, animals, their homes, water and weather.', [
        ("Which part of a plant is under the soil?", ['Leaf', 'Flower', 'Root', 'Fruit'], 'c', 'easy', "Roots grow under the soil."),
        ("A dog lives in a ___.", ['Nest', 'Kennel', 'Stable', 'Hive'], 'b', 'easy', "A dog's house is a kennel."),
        ("A bird lives in a ___.", ['Nest', 'Den', 'Burrow', 'Shed'], 'a', 'easy', "Birds live in nests."),
        ("Which animal gives us milk?", ['Lion', 'Cow', 'Tiger', 'Snake'], 'b', 'easy', "The cow gives us milk."),
        ("What colour are most leaves?", ['Blue', 'Green', 'Black', 'White'], 'b', 'easy', "Most leaves are green."),
        ("Which of these is a wild animal?", ['Cat', 'Dog', 'Tiger', 'Cow'], 'c', 'easy', "Tigers live in forests."),
        ("Bees make ___.", ['Milk', 'Honey', 'Silk', 'Wool'], 'b', 'medium', "Bees make honey."),
        ("We get rain from ___.", ['Clouds', 'Trees', 'Stars', 'Mountains'], 'a', 'medium', "Rain falls from clouds."),
        ("Which season is the hottest?", ['Winter', 'Rainy', 'Summer', 'Spring'], 'c', 'medium', "Summer is the hottest season."),
        ("Which animal lives in water?", ['Fish', 'Goat', 'Horse', 'Parrot'], 'a', 'easy', "Fish live in water."),
    ]),
    ('GK1', 'GK Test 1 – India, Our Country', 'Our country, its capital, famous places and national symbols.', [
        ("What is the capital of India?", ['Mumbai', 'New Delhi', 'Chennai', 'Kolkata'], 'b', 'easy', "New Delhi is the capital of India."),
        ("Who is called the 'Father of the Nation' in India?", ['Jawaharlal Nehru', 'Mahatma Gandhi', 'Bhagat Singh', 'Subhas Chandra Bose'], 'b', 'easy', "Mahatma Gandhi is called the Father of the Nation."),
        ("Which is the longest river in India?", ['Yamuna', 'Godavari', 'Ganga', 'Narmada'], 'c', 'medium', "The Ganga is the longest river in India."),
        ("What is the national animal of India?", ['Lion', 'Elephant', 'Tiger', 'Peacock'], 'c', 'easy', "The tiger is India's national animal."),
        ("What is the national bird of India?", ['Parrot', 'Peacock', 'Crow', 'Pigeon'], 'b', 'easy', "The peacock is India's national bird."),
        ("How many colours are there in the Indian flag (excluding the wheel)?", ['2', '3', '4', '5'], 'b', 'easy', "Saffron, white and green."),
        ("In which city is the Taj Mahal?", ['Delhi', 'Agra', 'Jaipur', 'Mumbai'], 'b', 'medium', "The Taj Mahal is in Agra."),
        ("How many spokes are there in the Ashoka Chakra on our flag?", ['12', '20', '24', '30'], 'c', 'hard', "The Ashoka Chakra has 24 spokes."),
        ("What is the national flower of India?", ['Rose', 'Sunflower', 'Lotus', 'Lily'], 'c', 'easy', "The lotus is India's national flower."),
        ("What is the national fruit of India?", ['Apple', 'Banana', 'Mango', 'Orange'], 'c', 'easy', "The mango is India's national fruit."),
    ]),
    # ---- Premium practice tests: a step up, with word problems, reading and reasoning ----
    ('ENG1', 'English Test 3 – Reading & Sentences', 'Read short sentences, pick the right word and spot mistakes.', [
        ("Read: 'Tom has a red ball. He plays with it in the park.' What colour is Tom's ball?", ['Blue', 'Red', 'Green', 'Yellow'], 'b', 'easy', "The sentence says Tom has a red ball."),
        ("Read: 'Tom has a red ball. He plays with it in the park.' Where does Tom play?", ['At school', 'At home', 'In the park', 'On the road'], 'c', 'medium', "He plays with it in the park."),
        ("Choose the correct word: The sun ___ in the east.", ['rise', 'rises', 'rising', 'rose up'], 'b', 'medium', "For one thing (the sun) we say 'rises'."),
        ("Which sentence begins correctly?", ['my name is Ria.', 'My name is Ria.', 'mY name is Ria.', 'my Name is Ria.'], 'b', 'medium', "A sentence starts with a capital letter."),
        ("Which mark comes at the end of a telling sentence?", ['?', '!', '.', ','], 'c', 'easy', "A telling sentence ends with a full stop."),
        ("Which mark comes at the end of 'What is your name'?", ['.', '?', ',', '!'], 'b', 'medium', "An asking sentence ends with a question mark."),
        ("Choose the correct word: I ___ a girl.", ['is', 'are', 'am', 'be'], 'c', 'medium', "We say 'I am'."),
        ("Choose the correct word: They ___ playing.", ['is', 'am', 'are', 'was a'], 'c', 'hard', "With 'they' we use 'are'."),
        ("Put the words in order: 'is / This / pen / my'", ['My pen is this.', 'This is my pen.', 'Is this pen my.', 'Pen my is this.'], 'b', 'hard', "This is my pen."),
        ("Which word is a doing word (verb)?", ['Chair', 'Jump', 'Green', 'Book'], 'b', 'medium', "Jump is an action we do."),
    ]),
    ('ENG1', 'English Test 4 – Vocabulary Challenge', 'Opposites, one-many, animal sounds and young ones.', [
        ("What is the plural of 'box'?", ['Boxs', 'Boxes', 'Boxies', 'Boxen'], 'b', 'hard', "Words ending in -x take -es: boxes."),
        ("What is the plural of 'child'?", ['Childs', 'Childes', 'Children', 'Childrens'], 'c', 'hard', "One child, many children."),
        ("What is the opposite of 'happy'?", ['Glad', 'Sad', 'Funny', 'Kind'], 'b', 'easy', "Happy and sad are opposites."),
        ("What is the opposite of 'open'?", ['Close', 'Push', 'Pull', 'Start'], 'a', 'easy', "Open and close are opposites."),
        ("A young one of a dog is called a ___.", ['Kitten', 'Calf', 'Puppy', 'Cub'], 'c', 'medium', "A baby dog is a puppy."),
        ("A young one of a cat is called a ___.", ['Kitten', 'Puppy', 'Lamb', 'Chick'], 'a', 'medium', "A baby cat is a kitten."),
        ("Which animal 'roars'?", ['Cow', 'Lion', 'Duck', 'Sheep'], 'b', 'easy', "A lion roars."),
        ("Which animal 'quacks'?", ['Duck', 'Dog', 'Horse', 'Cat'], 'a', 'easy', "A duck quacks."),
        ("Which word is the odd one out?", ['Red', 'Blue', 'Mango', 'Green'], 'c', 'medium', "Mango is a fruit; the others are colours."),
        ("Which word means 'very big'?", ['Tiny', 'Huge', 'Thin', 'Short'], 'b', 'hard', "Huge means very big."),
    ]),
    ('HIN1', 'हिंदी टेस्ट 3 – मात्राएँ', 'आ, इ, ई, उ, ऊ की मात्रा वाले शब्द पहचानें।', [
        ("'आ' की मात्रा वाला शब्द कौन सा है?", ['कमल', 'नाक', 'घर', 'जल'], 'b', 'medium', "नाक = न + ा + क।"),
        ("'इ' की मात्रा वाला शब्द कौन सा है?", ['किताब', 'मोर', 'पानी', 'गाय'], 'a', 'medium', "कि में छोटी इ की मात्रा है।"),
        ("'ई' की मात्रा वाला शब्द कौन सा है?", ['दिन', 'नदी', 'फल', 'बस'], 'b', 'medium', "नदी में 'दी' पर बड़ी ई की मात्रा है।"),
        ("'उ' की मात्रा वाला शब्द कौन सा है?", ['गुलाब', 'सेब', 'आम', 'पेड़'], 'a', 'medium', "गु में छोटे उ की मात्रा है।"),
        ("'ऊ' की मात्रा वाला शब्द कौन सा है?", ['फूल', 'घर', 'मछली', 'तोता'], 'a', 'medium', "फू में बड़े ऊ की मात्रा है।"),
        ("बिना मात्रा वाला शब्द कौन सा है?", ['माला', 'कलम', 'चिड़िया', 'भालू'], 'b', 'easy', "कलम में कोई मात्रा नहीं है।"),
        ("'क' + 'ा' + 'ल' + 'ा' से कौन सा शब्द बनता है?", ['कला', 'काला', 'कील', 'कुल'], 'b', 'hard', "का + ला = काला।"),
        ("सही शब्द चुनिए:", ['पानि', 'पानी', 'पनी', 'पाणि'], 'b', 'hard', "सही वर्तनी 'पानी' है।"),
        ("'ए' की मात्रा वाला शब्द कौन सा है?", ['सेब', 'आम', 'कमल', 'नल'], 'a', 'medium', "से में 'ए' की मात्रा है।"),
        ("'ओ' की मात्रा वाला शब्द कौन सा है?", ['मोर', 'बतख', 'हिरन', 'शेर'], 'a', 'medium', "मो में 'ओ' की मात्रा है।"),
    ]),
    ('HIN1', 'हिंदी टेस्ट 4 – गिनती, रंग और दिन', 'हिंदी में गिनती, रंग, सप्ताह के दिन और एक-अनेक।', [
        ("'पाँच' को अंकों में कैसे लिखते हैं?", ['4', '5', '6', '7'], 'b', 'easy', "पाँच = 5।"),
        ("'10' को हिंदी में क्या कहते हैं?", ['आठ', 'नौ', 'दस', 'सात'], 'c', 'easy', "10 = दस।"),
        ("'तीन' के बाद कौन सी संख्या आती है?", ['दो', 'चार', 'पाँच', 'छह'], 'b', 'easy', "तीन, चार।"),
        ("तोते का रंग कैसा होता है?", ['लाल', 'काला', 'हरा', 'सफ़ेद'], 'c', 'easy', "तोता हरा होता है।"),
        ("सप्ताह में कितने दिन होते हैं?", ['पाँच', 'छह', 'सात', 'आठ'], 'c', 'easy', "सप्ताह में सात दिन होते हैं।"),
        ("सोमवार के बाद कौन सा दिन आता है?", ['रविवार', 'मंगलवार', 'बुधवार', 'शुक्रवार'], 'b', 'medium', "सोमवार, मंगलवार।"),
        ("रविवार से पहले कौन सा दिन आता है?", ['शनिवार', 'सोमवार', 'गुरुवार', 'बुधवार'], 'a', 'medium', "शनिवार, रविवार।"),
        ("'लड़का' का बहुवचन क्या है?", ['लड़की', 'लड़के', 'लड़कों', 'लड़कि'], 'b', 'hard', "एक लड़का – कई लड़के।"),
        ("'केला' का बहुवचन क्या है?", ['केले', 'केलों', 'केली', 'केलाएँ'], 'a', 'hard', "एक केला – कई केले।"),
        ("दूध का रंग कैसा होता है?", ['पीला', 'सफ़ेद', 'नीला', 'भूरा'], 'b', 'easy', "दूध सफ़ेद होता है।"),
    ]),
    ('MAT1', 'Maths Test 4 – Patterns & Place Value', 'Tens and ones, number patterns and skip counting.', [
        ("How many tens and ones are in 34?", ['4 tens 3 ones', '3 tens 4 ones', '34 tens', '3 ones 4 ones'], 'b', 'medium', "34 = 3 tens and 4 ones."),
        ("Which number has 5 tens and 2 ones?", ['25', '52', '502', '7'], 'b', 'medium', "5 tens = 50, plus 2 = 52."),
        ("What comes next: 5, 10, 15, 20, __?", ['21', '22', '25', '30'], 'c', 'medium', "Counting by 5s: 25."),
        ("What comes next: 10, 20, 30, __?", ['31', '40', '35', '50'], 'b', 'easy', "Counting by 10s: 40."),
        ("What comes next: ▲ ● ▲ ● ▲ __?", ['▲', '●', '■', '★'], 'b', 'easy', "The pattern repeats triangle, circle."),
        ("What is the number name of 45?", ['Forty-four', 'Fifty-four', 'Forty-five', 'Fourteen'], 'c', 'medium', "45 is forty-five."),
        ("Which is the biggest 2-digit number?", ['10', '90', '99', '100'], 'c', 'hard', "99 is the biggest number with two digits."),
        ("Which is the smallest 2-digit number?", ['1', '10', '11', '9'], 'b', 'hard', "10 is the smallest number with two digits."),
        ("Arrange in order from smallest: 27, 72, 17", ['72, 27, 17', '17, 27, 72', '27, 17, 72', '17, 72, 27'], 'b', 'hard', "17 < 27 < 72."),
        ("What comes next: 20, 18, 16, 14, __?", ['13', '12', '10', '15'], 'b', 'hard', "Counting back by 2s: 12."),
    ]),
    ('MAT1', 'Maths Test 5 – Word Problems & Measurement', 'Real-life sums, longer/shorter, heavier/lighter.', [
        ("Aman has 8 toffees. He gives 3 to his sister. How many does he have left?", ['5', '11', '4', '3'], 'a', 'medium', "8 - 3 = 5."),
        ("There are 6 red balloons and 7 blue balloons. How many balloons in all?", ['12', '13', '14', '1'], 'b', 'medium', "6 + 7 = 13."),
        ("A pencil costs ₹5. What do 2 pencils cost?", ['₹7', '₹10', '₹3', '₹52'], 'b', 'hard', "₹5 + ₹5 = ₹10."),
        ("Which is heavier?", ['A feather', 'A leaf', 'An elephant', 'A paper'], 'c', 'easy', "An elephant is the heaviest."),
        ("Which is longer?", ['A pencil', 'A train', 'An eraser', 'A spoon'], 'b', 'easy', "A train is the longest."),
        ("A bus has 20 children. 10 get off. How many are still on the bus?", ['30', '10', '20', '0'], 'b', 'medium', "20 - 10 = 10."),
        ("Neha read 4 pages on Monday and 5 pages on Tuesday. How many pages did she read?", ['8', '9', '10', '1'], 'b', 'medium', "4 + 5 = 9."),
        ("There are 3 cars. Each car has 4 wheels. How many wheels in all?", ['7', '10', '12', '16'], 'c', 'hard', "4 + 4 + 4 = 12."),
        ("Which do we use to measure how long something is?", ['Clock', 'Ruler (scale)', 'Weighing balance', 'Thermometer'], 'b', 'medium', "A ruler measures length."),
        ("Ravi is 7 years old. His brother is 3 years older. How old is his brother?", ['4', '10', '9', '11'], 'b', 'hard', "7 + 3 = 10."),
    ]),
    ('EVS1', 'EVS Test 3 – Safety, Transport & Festivals', 'Road safety, means of transport, helpers and festivals of India.', [
        ("At a traffic light, which colour means 'Stop'?", ['Green', 'Yellow', 'Red', 'Blue'], 'c', 'easy', "Red means stop."),
        ("Which colour of the traffic light means 'Go'?", ['Red', 'Green', 'Yellow', 'Orange'], 'b', 'easy', "Green means go."),
        ("Where should we cross the road?", ['Anywhere', 'At the zebra crossing', 'Between cars', 'Running fast'], 'b', 'medium', "Always cross at the zebra crossing."),
        ("Which of these moves on water?", ['Bus', 'Ship', 'Train', 'Aeroplane'], 'b', 'easy', "A ship moves on water."),
        ("Which of these flies in the sky?", ['Car', 'Boat', 'Aeroplane', 'Cycle'], 'c', 'easy', "An aeroplane flies."),
        ("Who treats us when we are sick?", ['Farmer', 'Doctor', 'Tailor', 'Cobbler'], 'b', 'easy', "A doctor treats sick people."),
        ("Who grows food for us?", ['Farmer', 'Postman', 'Pilot', 'Barber'], 'a', 'medium', "A farmer grows crops."),
        ("Diwali is called the festival of ___.", ['Colours', 'Lights', 'Kites', 'Flowers'], 'b', 'medium', "We light diyas on Diwali."),
        ("Holi is called the festival of ___.", ['Lights', 'Colours', 'Lamps', 'Sweets only'], 'b', 'medium', "We play with colours on Holi."),
        ("If you touch something very hot by mistake, you should ___.", ['Keep touching it', 'Tell an adult and cool it under water', 'Hide it', 'Ignore it'], 'b', 'hard', "Tell an adult and put the burn under cool running water."),
    ]),
    ('GK1', 'GK Test 2 – The World Around Us', 'Sun, moon, planets, colours, sports and inventions.', [
        ("Which gives us light during the day?", ['Moon', 'Sun', 'Stars', 'Clouds'], 'b', 'easy', "The Sun gives us light in the day."),
        ("On which planet do we live?", ['Mars', 'Earth', 'Moon', 'Sun'], 'b', 'easy', "We live on planet Earth."),
        ("How many colours are there in a rainbow?", ['5', '6', '7', '8'], 'c', 'medium', "A rainbow has 7 colours."),
        ("Which game is played with a bat and ball?", ['Football', 'Cricket', 'Chess', 'Swimming'], 'b', 'easy', "Cricket uses a bat and ball."),
        ("Which is the biggest animal on land?", ['Lion', 'Giraffe', 'Elephant', 'Horse'], 'c', 'medium', "The elephant is the biggest land animal."),
        ("Which is the tallest animal?", ['Elephant', 'Giraffe', 'Camel', 'Horse'], 'b', 'medium', "The giraffe is the tallest animal."),
        ("Which animal is called the 'Ship of the Desert'?", ['Horse', 'Camel', 'Elephant', 'Donkey'], 'b', 'hard', "The camel can travel long in the desert."),
        ("How many months are there in a year?", ['10', '11', '12', '13'], 'c', 'medium', "A year has 12 months."),
        ("Which is the first month of the year?", ['March', 'December', 'January', 'June'], 'c', 'easy', "January is the first month."),
        ("What do we call a person who flies an aeroplane?", ['Driver', 'Pilot', 'Sailor', 'Captain of bus'], 'b', 'hard', "A pilot flies an aeroplane."),
    ]),
    ('RSN1', 'Reasoning Test 1 – Logical Thinking', 'Odd one out, patterns, comparisons and simple puzzles.', [
        ("Find the odd one out:", ['Apple', 'Banana', 'Carrot', 'Mango'], 'c', 'easy', "Carrot is a vegetable; the rest are fruits."),
        ("Find the odd one out:", ['Cow', 'Dog', 'Parrot', 'Goat'], 'c', 'medium', "A parrot is a bird; the rest are animals with four legs."),
        ("Find the odd one out:", ['Car', 'Bus', 'Truck', 'Boat'], 'd', 'medium', "A boat moves on water; the rest move on roads."),
        ("What comes next: A, C, E, G, __?", ['H', 'I', 'J', 'F'], 'b', 'hard', "Skip one letter each time: I."),
        ("What comes next: 1, 3, 5, 7, __?", ['8', '9', '10', '11'], 'b', 'medium', "Add 2 each time: 9."),
        ("Shoe is to foot as glove is to ___.", ['Head', 'Hand', 'Leg', 'Neck'], 'b', 'hard', "We wear gloves on our hands."),
        ("Riya is taller than Sam. Sam is taller than Tia. Who is the shortest?", ['Riya', 'Sam', 'Tia', 'All same'], 'c', 'hard', "Riya > Sam > Tia, so Tia is the shortest."),
        ("Which number is missing? 2, 4, __, 8", ['5', '6', '7', '3'], 'b', 'easy', "Counting by 2s: 6."),
        ("If today is Monday, what day was yesterday?", ['Tuesday', 'Sunday', 'Saturday', 'Wednesday'], 'b', 'medium', "The day before Monday is Sunday."),
        ("Bird is to nest as bee is to ___.", ['Hive', 'Den', 'Kennel', 'Stable'], 'a', 'hard', "Bees live in a hive."),
    ]),
]


class Command(BaseCommand):
    help = "Create the CBSE Class 1 subject-wise test series (19 tests). Safe to re-run: it replaces the series."

    @transaction.atomic
    def handle(self, *args, **options):
        subjects = {}
        for code, (name, color, icon) in SUBJECTS.items():
            subjects[code], _ = Subject.objects.get_or_create(
                code=code, defaults={'name': name, 'color': color, 'icon': icon}
            )

        TestSeries.objects.filter(title__in=[SERIES_TITLE, *OLD_TITLES]).delete()
        series = TestSeries.objects.create(
            title=SERIES_TITLE,
            slug='cbse-class-1-subject-wise-test-series',
            board='cbse',
            grade=1,
            description=(
                "Subject-wise practice tests for CBSE Class 1 students, covering English, Hindi, Mathematics, "
                "EVS, General Knowledge and Reasoning. Includes premium practice tests with reading, word "
                "problems and logical thinking. Each test has 10 multiple-choice questions with explanations."
            ),
            difficulty='easy',
            estimated_duration='15 minutes per test',
            is_free=True,
            price=0,
            has_negative_marking=False,
            negative_marks=0,
            pass_percentage=40,
        )

        for code, title, description, questions in TESTS:
            test = Test.objects.create(
                test_series=series,
                title=title,
                description=description,
                duration_minutes=15,
                max_attempts=3,
            )
            for order, (text, opts, answer, difficulty, explanation) in enumerate(questions, start=1):
                options_map, answer = shuffled_options(text, opts, answer)
                Question.objects.create(
                    test=test,
                    subject=subjects[code],
                    question_type='mcq_single',
                    difficulty=difficulty,
                    question_text=text,
                    marks=1,
                    negative_marks=0,
                    options=options_map,
                    correct_answer={'answer': answer},
                    explanation=explanation,
                    order=order,
                )
            test.update_stats()

        series.update_stats()
        self.stdout.write(self.style.SUCCESS(
            f'Created "{series.title}" with {series.total_tests} tests and {series.total_questions} questions.'
        ))
