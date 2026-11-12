"""English language: vocabulary, idioms, one-word substitution, spelling and grammar (SSC, Banking, CDS, CLAT, CUET)."""
from .core import generator, mcq, register

S = 'ENG1'

# word | synonym | antonym
VOCAB = """
abundant|plentiful|scarce
accelerate|hasten|decelerate
accurate|precise|inaccurate
adamant|unyielding|flexible
admonish|reprimand|praise
affluent|wealthy|poor
aggravate|worsen|alleviate
amiable|friendly|hostile
ample|sufficient|meagre
ancient|old|modern
animosity|hostility|friendship
apathy|indifference|enthusiasm
arrogant|haughty|humble
audacious|bold|timid
austere|severe|lavish
authentic|genuine|fake
benevolent|kind|malevolent
brevity|conciseness|verbosity
candid|frank|evasive
capable|competent|incompetent
cautious|careful|reckless
cease|stop|continue
coarse|rough|smooth
commence|begin|conclude
compassion|sympathy|cruelty
comprehensive|thorough|partial
conceal|hide|reveal
condemn|denounce|praise
confident|assured|diffident
conspicuous|noticeable|inconspicuous
contempt|scorn|respect
copious|abundant|sparse
courteous|polite|rude
credible|believable|implausible
cunning|crafty|naive
curtail|reduce|extend
deceit|fraud|honesty
deficient|lacking|adequate
dejected|depressed|elated
deliberate|intentional|accidental
diligent|industrious|lazy
diminish|decrease|increase
discord|disagreement|harmony
docile|submissive|unruly
dwindle|shrink|grow
eminent|distinguished|obscure
enormous|huge|tiny
ephemeral|transient|permanent
eradicate|eliminate|establish
exonerate|acquit|convict
expand|enlarge|contract
fallacy|misconception|truth
feeble|weak|strong
fertile|fruitful|barren
fickle|changeable|constant
flexible|pliable|rigid
frugal|thrifty|extravagant
futile|useless|fruitful
generous|liberal|stingy
gloomy|dismal|cheerful
gregarious|sociable|reserved
hamper|hinder|facilitate
harsh|severe|gentle
hostile|unfriendly|amicable
immense|vast|minute
impartial|unbiased|biased
impede|obstruct|assist
inevitable|unavoidable|avoidable
infamous|notorious|reputable
innocent|blameless|guilty
jovial|cheerful|morose
lethargic|sluggish|energetic
lucid|clear|obscure
meticulous|painstaking|careless
miserly|stingy|generous
modest|humble|boastful
mundane|ordinary|extraordinary
negligent|careless|careful
notorious|infamous|reputable
novice|beginner|expert
obedient|dutiful|defiant
obscure|vague|clear
obsolete|outdated|current
obstinate|stubborn|amenable
optimistic|hopeful|pessimistic
opulent|luxurious|squalid
ostentatious|showy|modest
pacify|calm|provoke
paucity|scarcity|abundance
peculiar|strange|ordinary
perilous|dangerous|safe
perpetual|everlasting|temporary
placid|calm|agitated
prohibit|forbid|permit
prolific|productive|unproductive
prosperity|affluence|adversity
prudent|wise|foolish
quell|suppress|incite
reluctant|unwilling|eager
remote|distant|near
renowned|famous|unknown
reticent|reserved|talkative
robust|sturdy|frail
scanty|meagre|plentiful
serene|tranquil|turbulent
shrewd|astute|simple
sincere|genuine|insincere
slander|defamation|praise
solitary|lonely|sociable
spurious|fake|genuine
stagnant|still|flowing
sterile|barren|fertile
tedious|boring|interesting
tranquil|peaceful|noisy
transparent|clear|opaque
trivial|petty|significant
ubiquitous|omnipresent|rare
vacant|empty|occupied
valiant|brave|cowardly
vanity|conceit|modesty
venerate|revere|despise
verbose|wordy|concise
vigilant|watchful|careless
vindictive|revengeful|forgiving
voluntary|optional|compulsory
wane|decline|wax
wary|cautious|unwary
zeal|enthusiasm|apathy
zenith|peak|nadir
"""
VOCAB = [tuple(line.split('|')) for line in VOCAB.strip().splitlines()]

# Words close in meaning (or exact opposites) are never offered as each other's distractors, so a question
# can't end up with two defensible answers.
FAMILIES = [
    'abundant plentiful copious ample abundance sufficient adequate scarce sparse meagre scanty scarcity paucity lacking deficient',
    'calm placid serene tranquil peaceful pacify quell suppress agitated turbulent noisy provoke incite',
    'famous renowned eminent distinguished reputable notorious infamous unknown',
    'clear lucid transparent obscure vague opaque',
    'careful cautious wary vigilant watchful meticulous painstaking careless negligent reckless unwary',
    'generous liberal benevolent kind malevolent miserly stingy frugal thrifty extravagant lavish austere severe harsh gentle luxurious opulent squalid',
    'humble modest arrogant haughty boastful vanity conceit modesty ostentatious showy',
    'brave valiant bold audacious cowardly timid confident assured diffident',
    'lazy diligent industrious lethargic sluggish energetic',
    'increase decrease diminish dwindle expand contract enlarge grow shrink reduce curtail extend wane wax decline accelerate hasten decelerate',
    'friendly hostile amiable amicable unfriendly animosity hostility friendship gregarious sociable solitary lonely reserved reticent talkative courteous polite rude',
    'jovial cheerful morose gloomy dismal dejected depressed elated optimistic hopeful pessimistic',
    'fertile fruitful barren sterile futile useless prolific productive unproductive',
    'genuine authentic fake spurious sincere insincere credible believable implausible honesty deceit fraud',
    'permanent perpetual everlasting temporary ephemeral transient',
    'praise condemn denounce admonish reprimand slander defamation venerate revere despise contempt scorn respect',
    'begin commence conclude cease stop continue',
    'hide conceal reveal',
    'strong feeble weak robust sturdy frail capable competent incompetent',
    'huge enormous immense vast tiny minute',
    'prohibit forbid permit voluntary optional compulsory',
    'hamper hinder impede obstruct facilitate assist',
    'ordinary mundane extraordinary peculiar strange',
    'flexible pliable rigid adamant unyielding obstinate stubborn amenable docile submissive unruly obedient dutiful defiant',
    'old ancient modern obsolete outdated current',
    'wise prudent foolish shrewd astute simple cunning crafty naive',
    'innocent blameless guilty exonerate acquit convict',
    'reluctant unwilling eager zeal enthusiasm apathy indifference',
    'tedious boring interesting trivial petty significant',
    'vacant empty occupied remote distant near',
    'harmony discord disagreement',
    'deliberate intentional accidental inevitable unavoidable avoidable',
    'impartial unbiased biased',
    'brevity conciseness verbosity verbose wordy concise',
    'coarse rough smooth',
    'perilous dangerous safe',
    'prosperity affluence adversity affluent wealthy poor',
    'zenith peak nadir',
]


def _clusters():
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for row in VOCAB:
        for w in row[1:]:
            union(row[0], w)
    for fam in FAMILIES:
        words = fam.split()
        for w in words[1:]:
            union(words[0], w)
    return {w: find(w) for row in VOCAB for w in row}


CLUSTER = _clusters()


@generator('english.synonym', S, 'Synonyms')
def synonym(rng):
    w, syn, ant = rng.choice(VOCAB)
    others = [s for x, s, a in VOCAB if CLUSTER[s] != CLUSTER[w]] + [a for x, s, a in VOCAB if CLUSTER[a] != CLUSTER[w]]
    rng.shuffle(others)
    d = rng.choice(['easy', 'medium', 'medium', 'hard'])
    return mcq(rng, f"Choose the word most similar in meaning to '{w.upper()}'.", syn.title(), [ant.title()] + [o.title() for o in others[:4]],
               d, f"{w.title()} means {syn}; its opposite is {ant}.")


@generator('english.antonym', S, 'Antonyms')
def antonym(rng):
    w, syn, ant = rng.choice(VOCAB)
    others = [a for x, s, a in VOCAB if CLUSTER[a] != CLUSTER[w]] + [s for x, s, a in VOCAB if CLUSTER[s] != CLUSTER[w]]
    rng.shuffle(others)
    d = rng.choice(['easy', 'medium', 'medium', 'hard'])
    return mcq(rng, f"Choose the word opposite in meaning to '{w.upper()}'.", ant.title(), [syn.title()] + [o.title() for o in others[:4]],
               d, f"{w.title()} means {syn}; the opposite is {ant}.")


IDIOMS = """
A piece of cake|Very easy
Beat around the bush|Avoid the main point
Bite the bullet|Face a difficult situation bravely
Break the ice|Start a conversation in an awkward situation
Burn the midnight oil|Work or study late into the night
Call a spade a spade|Speak frankly
Cry over spilt milk|Regret what cannot be undone
Cut corners|Do something poorly to save time or money
Hit the nail on the head|Describe exactly what is causing a situation
In hot water|In trouble
Let the cat out of the bag|Reveal a secret
Once in a blue moon|Very rarely
Over the moon|Extremely happy
Spill the beans|Disclose a secret
Under the weather|Feeling unwell
A blessing in disguise|Something good that seemed bad at first
At the eleventh hour|At the last moment
Bury the hatchet|Make peace
By hook or by crook|By any means, fair or unfair
Hold one's horses|Wait and be patient
A white elephant|A costly but useless possession
Add fuel to the fire|Make a bad situation worse
Bark up the wrong tree|Accuse or pursue the wrong person or thing
Turn a deaf ear|Ignore a request
To smell a rat|To suspect something wrong
To be all ears|To listen very attentively
Throw in the towel|Admit defeat
Keep one's fingers crossed|Hope for a good result
A bolt from the blue|A sudden, unexpected event
Blow one's own trumpet|Praise oneself
Get cold feet|Become nervous and back out
Pull someone's leg|Tease or joke with someone
See eye to eye|Agree fully
Take with a pinch of salt|Not believe completely
Through thick and thin|In all circumstances, good or bad
Make both ends meet|Live within one's income
A wild goose chase|A hopeless search
Apple of one's eye|Someone very dear
At sixes and sevens|In a state of confusion
Hand in glove|Working closely together, often secretly
"""
IDIOMS = [tuple(line.split('|')) for line in IDIOMS.strip().splitlines()]


@generator('english.idioms', S, 'Idioms & Phrases')
def idioms(rng):
    idiom, meaning = rng.choice(IDIOMS)
    others = [m for i, m in IDIOMS if m != meaning]
    rng.shuffle(others)
    return mcq(rng, f"Choose the correct meaning of the idiom: '{idiom}'", meaning, others, 'medium', f"'{idiom}' means: {meaning.lower()}.")


ONE_WORD = """
A person who cannot read or write|Illiterate
One who believes in God|Theist
One who does not believe in God|Atheist
A speech delivered without preparation|Extempore
A person who loves mankind|Philanthropist
A person who hates mankind|Misanthrope
A place where bees are kept|Apiary
A place where birds are kept|Aviary
The study of birds|Ornithology
The study of insects|Entomology
A cure for all diseases|Panacea
A life history written by oneself|Autobiography
A government by the people|Democracy
Rule by a few people|Oligarchy
That which cannot be read|Illegible
That which cannot be seen|Invisible
That which cannot be avoided|Inevitable
That which cannot be corrected|Incorrigible
One who walks in sleep|Somnambulist
A person who eats too much|Glutton
One who is present everywhere|Omnipresent
One who knows everything|Omniscient
Fear of water|Hydrophobia
Fear of heights|Acrophobia
A word opposite in meaning|Antonym
A remedy for poison|Antidote
A medical examination of a dead body|Autopsy
One who leaves his country to settle in another|Emigrant
One who comes into a country to settle|Immigrant
A list of books|Bibliography
Killing of a king|Regicide
A child born after the death of the father|Posthumous
Lasting for a very short time|Ephemeral
A person who is unable to pay debts|Insolvent
One who is fond of fighting|Bellicose
A period of ten years|Decade
A period of a thousand years|Millennium
One who speaks many languages|Polyglot
An animal that eats only plants|Herbivore
A place where dead bodies are kept|Mortuary
Words written on a tomb|Epitaph
A collection of poems|Anthology
One who does not eat meat|Vegetarian
Incapable of being wounded or harmed|Invulnerable
Something no longer in use|Obsolete
"""
ONE_WORD = [tuple(line.split('|')) for line in ONE_WORD.strip().splitlines()]


@generator('english.one_word', S, 'One Word Substitution')
def one_word(rng):
    definition, word = rng.choice(ONE_WORD)
    others = [w for d, w in ONE_WORD if w != word]
    rng.shuffle(others)
    return mcq(rng, f"Choose the one word for: '{definition}'", word, others, 'medium', f"{word}: {definition.lower()}.")


SPELLINGS = """
Accommodate|Accomodate|Acommodate|Accommadate
Necessary|Neccessary|Necesary|Neccesary
Occasion|Occassion|Ocassion|Ocasion
Embarrass|Embarass|Embaress|Emberrass
Separate|Seperate|Separete|Seprate
Definitely|Definately|Definitly|Defenitely
Receive|Recieve|Receeve|Recive
Privilege|Priviledge|Privelege|Privilage
Committee|Commitee|Comittee|Commitie
Conscientious|Consciencious|Conscientous|Concientious
Millennium|Millenium|Milennium|Millenniun
Rhythm|Rythm|Rhythem|Rhytm
Questionnaire|Questionaire|Questionnare|Quesionnaire
Entrepreneur|Entreprenuer|Enterpreneur|Entrepeneur
Guarantee|Garantee|Guarentee|Gaurantee
Maintenance|Maintainance|Maintenence|Maintanance
Bureaucracy|Beaurocracy|Bureacracy|Burocracy
Lieutenant|Leiutenant|Lieutenent|Liutenant
Mischievous|Mischievious|Mischevous|Mischivous
Pronunciation|Pronounciation|Pronunciasion|Pronuntiation
Recommend|Reccommend|Recomend|Reccomend
Surveillance|Survellance|Surveilance|Survaillance
Achievement|Acheivement|Achievment|Achievemant
Exaggerate|Exagerate|Exaggarate|Exxagerate
Hierarchy|Heirarchy|Hierarcy|Hierachy
"""
SPELLINGS = [line.split('|') for line in SPELLINGS.strip().splitlines()]


@generator('english.spelling', S, 'Spelling')
def spelling(rng):
    right, *wrong = rng.choice(SPELLINGS)
    return mcq(rng, "Choose the correctly spelt word.", right, wrong, 'medium', f"The correct spelling is '{right}'.")


GRAMMAR = [
    ("She is fond ___ music.", ['of', 'in', 'at', 'for'], 'easy', "'Fond of' is the fixed preposition."),
    ("He has been living here ___ 2015.", ['since', 'for', 'from', 'by'], 'easy', "'Since' with a point of time."),
    ("He has been ill ___ three days.", ['for', 'since', 'from', 'by'], 'easy', "'For' with a period of time."),
    ("The train arrived ___ the station on time.", ['at', 'in', 'on', 'to'], 'easy', "'Arrive at' a station."),
    ("She was angry ___ her brother.", ['with', 'on', 'at', 'to'], 'medium', "Angry with a person, angry at a thing."),
    ("I prefer tea ___ coffee.", ['to', 'than', 'over', 'from'], 'medium', "'Prefer A to B'."),
    ("The book is divided ___ five chapters.", ['into', 'in', 'among', 'between'], 'medium', "'Divided into' parts."),
    ("He insisted ___ paying the bill.", ['on', 'for', 'at', 'to'], 'medium', "'Insist on'."),
    ("Neither the teacher nor the students ___ present.", ['were', 'was', 'is', 'has been'], 'hard', "With neither…nor the verb agrees with the nearer subject (students)."),
    ("Each of the boys ___ a prize.", ['was given', 'were given', 'have been given', 'are given'], 'medium', "'Each' takes a singular verb."),
    ("If I ___ a bird, I would fly.", ['were', 'was', 'am', 'had been'], 'medium', "Subjunctive 'were' in unreal conditions."),
    ("He is one of the best players who ___ ever played for India.", ['have', 'has', 'had', 'is'], 'hard', "'Who' refers to 'players' (plural)."),
    ("Scarcely had he left ___ it began to rain.", ['when', 'than', 'then', 'that'], 'hard', "'Scarcely … when'."),
    ("No sooner had the bell rung ___ the students rushed out.", ['than', 'when', 'then', 'as'], 'hard', "'No sooner … than'."),
    ("The news ___ very encouraging.", ['is', 'are', 'were', 'have been'], 'easy', "'News' is singular."),
    ("Mathematics ___ my favourite subject.", ['is', 'are', 'were', 'have been'], 'easy', "Subject names ending in -s are singular."),
    ("I have ___ honest friend.", ['an', 'a', 'the', 'no article'], 'easy', "'Honest' begins with a vowel sound."),
    ("She is ___ European.", ['a', 'an', 'the', 'no article'], 'medium', "'European' begins with a 'yu' (consonant) sound."),
    ("The Ganga is ___ holiest river of India.", ['the', 'a', 'an', 'no article'], 'easy', "Superlatives take 'the'."),
    ("He is senior ___ me by two years.", ['to', 'than', 'from', 'over'], 'medium', "Latin comparatives (senior, junior, superior) take 'to'."),
    ("The police ___ arrested the thief.", ['have', 'has', 'is', 'was'], 'medium', "'Police' is always plural."),
    ("Ten kilometres ___ a long distance to walk.", ['is', 'are', 'were', 'have been'], 'hard', "A distance taken as one amount is singular."),
    ("She sings ___ than her sister.", ['better', 'best', 'good', 'well'], 'easy', "Comparative of 'well'."),
    ("By next year, she ___ her degree.", ['will have completed', 'will complete', 'completes', 'has completed'], 'hard', "Future perfect for an action finished before a future time."),
]
register('english.grammar', S, 'Grammar – Fill in the Blanks', rows=GRAMMAR)

ERRORS = [
    ("Spot the error: He did not knew (A) / the answer (B) / to this question. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'medium', "'did not know' – after 'did' use the base form."),
    ("Spot the error: One of my friend (A) / has gone (B) / to Delhi. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'easy', "'One of my friends' – plural noun after 'one of'."),
    ("Spot the error: The furnitures (A) / in this room (B) / are very costly. (C) / No error (D)", ['A', 'C', 'B', 'D'], 'medium', "'Furniture' is uncountable; also 'is very costly'. The first error is in A."),
    ("Spot the error: She is (A) / more cleverer (B) / than her sister. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "Double comparative: say 'cleverer' or 'more clever'."),
    ("Spot the error: I am (A) / knowing him (B) / for many years. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Know' is a stative verb: 'I have known him for many years'."),
    ("Spot the error: Each of the students (A) / have submitted (B) / the assignment. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Each of' takes a singular verb: 'has submitted'."),
    ("Spot the error: He is (A) / an university (B) / professor. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'easy', "'A university' – 'u' sounds like 'yu'."),
    ("Spot the error: The sceneries (A) / of Kashmir (B) / are beautiful. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'medium', "'Scenery' is uncountable: 'The scenery … is'."),
    ("Spot the error: Unless you (A) / do not work hard, (B) / you will fail. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Unless' is already negative; drop 'do not'."),
    ("Spot the error: The committee (A) / have submitted (B) / its report. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'hard', "Acting as one body ('its report'), the committee takes 'has'."),
    ("Spot the error: She returned back (A) / from London (B) / last week. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'easy', "'Returned back' is redundant."),
    ("Spot the error: We discussed about (A) / the problem (B) / for hours. (C) / No error (D)", ['A', 'B', 'C', 'D'], 'medium', "'Discuss' takes no preposition."),
    ("Spot the error: He has (A) / gone to abroad (B) / for studies. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Abroad' is an adverb: 'gone abroad'."),
    ("Spot the error: The cattle (A) / is grazing (B) / in the field. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'medium', "'Cattle' is plural: 'are grazing'."),
    ("Spot the error: I look forward (A) / to meet you (B) / next week. (C) / No error (D)", ['B', 'A', 'C', 'D'], 'hard', "'Look forward to' + -ing: 'to meeting you'."),
]
register('english.error_spotting', S, 'Error Spotting', rows=ERRORS)

VOICE_NARRATION = [
    ("Change into passive voice: 'Rahul is writing a letter.'", ['A letter is being written by Rahul.', 'A letter is written by Rahul.', 'A letter was being written by Rahul.', 'A letter has been written by Rahul.'], 'easy', "Present continuous passive: is being + V3."),
    ("Change into passive voice: 'They have completed the work.'", ['The work has been completed by them.', 'The work had been completed by them.', 'The work is completed by them.', 'The work was completed by them.'], 'easy', "Present perfect passive: has been + V3."),
    ("Change into passive voice: 'Who wrote this book?'", ['By whom was this book written?', 'Who was this book written?', 'By whom this book was written?', 'This book was written by whom?'], 'medium', "Wh-questions: By whom + was + object + V3?"),
    ("Change into passive voice: 'Open the door.'", ['Let the door be opened.', 'The door is opened.', 'The door should open.', 'Let the door open.'], 'medium', "Imperative passive: Let + object + be + V3."),
    ("Change into passive voice: 'She will sing a song.'", ['A song will be sung by her.', 'A song would be sung by her.', 'A song will sung by her.', 'A song shall sing by her.'], 'easy', "Future passive: will be + V3."),
    ("Change into passive voice: 'The police caught the thief.'", ['The thief was caught by the police.', 'The thief is caught by the police.', 'The thief had been caught by the police.', 'The thief has been caught by the police.'], 'easy', "Simple past passive: was + V3."),
    ("Change into indirect speech: He said, 'I am tired.'", ['He said that he was tired.', 'He said that I am tired.', 'He said that he is tired.', 'He told that he was tired.'], 'easy', "Present becomes past; 'I' becomes 'he'."),
    ("Change into indirect speech: She said to me, 'Please help me.'", ['She requested me to help her.', 'She said me to help her.', 'She told me that please help her.', 'She requested me that help her.'], 'medium', "Requests: requested + object + to-infinitive."),
    ("Change into indirect speech: He said, 'I will come tomorrow.'", ['He said that he would come the next day.', 'He said that he will come tomorrow.', 'He said that he would come tomorrow.', 'He says that he would come the next day.'], 'medium', "will → would, tomorrow → the next day."),
    ("Change into indirect speech: The teacher said, 'The Earth revolves around the Sun.'", ['The teacher said that the Earth revolves around the Sun.', 'The teacher said that the Earth revolved around the Sun.', 'The teacher said that the Earth had revolved around the Sun.', 'The teacher told that the Earth revolves around the Sun.'], 'hard', "Universal truths keep the present tense."),
    ("Change into indirect speech: He asked me, 'Where do you live?'", ['He asked me where I lived.', 'He asked me where do I live.', 'He asked me where did I live.', 'He asked me that where I lived.'], 'medium', "Questions become statements; present → past."),
]
register('english.voice_narration', S, 'Active-Passive & Narration', rows=VOICE_NARRATION)

SENTENCE_IMPROVEMENT = [
    ("Improve the underlined part: 'He is senior than me.'", ['senior to me', 'more senior than me', 'senior from me', 'No improvement'], 'medium', "'Senior to'."),
    ("Improve the underlined part: 'I am used to get up early.'", ['used to getting up', 'use to get up', 'using to get up', 'No improvement'], 'hard', "'Be used to' + -ing."),
    ("Improve the underlined part: 'He told that he was busy.'", ['said that', 'told to me that', 'spoke that', 'No improvement'], 'medium', "'Told' needs an object; use 'said that'."),
    ("Improve the underlined part: 'Hardly had I reached the station than the train left.'", ['when the train left', 'then the train left', 'as the train left', 'No improvement'], 'hard', "'Hardly … when'."),
    ("Improve the underlined part: 'The man who I met yesterday is a doctor.'", ['whom I met', 'which I met', 'whose I met', 'No improvement'], 'medium', "Object of 'met' → 'whom' (formal)."),
    ("Improve the underlined part: 'She is the more intelligent of the two sisters.'", ['No improvement', 'most intelligent', 'intelligent', 'much intelligent'], 'hard', "Comparing two: 'the more intelligent' is correct."),
    ("Improve the underlined part: 'I have seen him yesterday.'", ['saw him yesterday', 'had seen him yesterday', 'have saw him yesterday', 'No improvement'], 'medium', "A past time word takes the simple past."),
    ("Improve the underlined part: 'Let us discuss about the plan.'", ['discuss the plan', 'discuss on the plan', 'discussing about the plan', 'No improvement'], 'easy', "'Discuss' takes no preposition."),
]
register('english.sentence_improvement', S, 'Sentence Improvement', rows=SENTENCE_IMPROVEMENT)

PASSAGES = [
    ("Read the passage and answer.\n\nThe banyan tree, India's national tree, sends down aerial roots that grow into new trunks. "
     "A single tree can spread over several acres, which is why it is often seen as a symbol of immortality and shelter.\n\n"
     "Why is the banyan seen as a symbol of immortality?",
     ['Its aerial roots keep forming new trunks so it spreads and lives on', 'It is India\'s national tree', 'It grows only in temples', 'It never sheds its leaves'],
     'medium', "The passage links its spreading, self-renewing trunks to immortality."),
    ("Read the passage and answer.\n\nRegular exercise improves the heart's efficiency, lowers blood pressure and helps control weight. "
     "Experts recommend at least 150 minutes of moderate activity every week, such as brisk walking.\n\n"
     "According to the passage, how much moderate activity is recommended weekly?",
     ['At least 150 minutes', 'Exactly 60 minutes', 'At least 300 minutes daily', 'No fixed amount'],
     'easy', "Stated directly."),
    ("Read the passage and answer.\n\nThe printing press, developed by Johannes Gutenberg around 1440, made books cheaper and faster to produce. "
     "As books spread, literacy rose and ideas travelled across Europe as never before.\n\n"
     "What was the main effect of the printing press described in the passage?",
     ['It spread books, literacy and ideas widely', 'It made books more expensive', 'It ended the use of paper', 'It was used only by kings'],
     'easy', "Cheaper books → higher literacy and spread of ideas."),
    ("Read the passage and answer.\n\nMangroves grow where rivers meet the sea. Their tangled roots trap sediment, protect coasts from storm "
     "surges and provide nurseries for fish. The Sundarbans in India and Bangladesh is the largest mangrove forest in the world.\n\n"
     "Which of the following is NOT mentioned as a benefit of mangroves?",
     ['Producing timber for export', 'Protecting coasts from storm surges', 'Trapping sediment', 'Providing nurseries for fish'],
     'medium', "Timber export is not mentioned."),
    ("Read the passage and answer.\n\nUnlike a sprint, a marathon rewards patience. Runners who start too fast often tire early, while those "
     "who keep a steady pace finish stronger. Many coaches say success in long projects works the same way.\n\n"
     "The author compares long projects to a marathon in order to stress the value of ___.",
     ['steady, patient effort', 'starting very fast', 'running every day', 'winning sprints'],
     'medium', "The point is steady pacing over time."),
]
register('english.comprehension', S, 'Reading Comprehension', rows=PASSAGES)
