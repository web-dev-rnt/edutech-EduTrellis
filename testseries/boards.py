"""School boards used by test series (TestSeries.board) and their 'Explore Exams' categories."""
from collections import namedtuple

Board = namedtuple('Board', 'code category label ncert hindi note')

# State boards and NIOS. `ncert`: the board prescribes NCERT(-based) textbooks for Classes 9-12.
# `hindi`: Hindi is a commonly taken language, so the Class 10 mock includes it.
STATE_BOARDS = [
    Board('bseb', 'Bihar Board', 'Bihar Board (BSEB)', True, True,
          "BSEB Matric (Class 10) and Intermediate (Class 12). About half of each paper is objective (MCQ) on an OMR sheet."),
    Board('mh', 'Maharashtra Board', 'Maharashtra Board (MSBSHSE)', False, True,
          "MSBSHSE SSC (Class 10) and HSC (Class 12) on Balbharati textbooks; 35% is the pass mark."),
    Board('mp', 'MP Board', 'MP Board (MPBSE)', True, True,
          "MPBSE High School (Class 10) and Higher Secondary (Class 12), following NCERT textbooks."),
    Board('rj', 'Rajasthan Board', 'Rajasthan Board (RBSE)', True, True,
          "RBSE Secondary (Class 10) and Senior Secondary (Class 12), largely NCERT-based in science and maths."),
    Board('gj', 'Gujarat Board', 'Gujarat Board (GSEB)', True, False,
          "GSEB SSC (Class 10) and HSC (Class 12); NCERT-based textbooks in science and maths."),
    Board('wb', 'West Bengal Board', 'West Bengal Board (WBBSE/WBCHSE)', False, False,
          "WBBSE Madhyamik (Class 10) and WBCHSE Higher Secondary (Class 12), on the state syllabus."),
    Board('tn', 'Tamil Nadu Board', 'Tamil Nadu Board (TNDGE)', False, False,
          "Tamil Nadu SSLC (Class 10) and HSC (Classes 11–12) on the Samacheer Kalvi syllabus; 35 out of 100 to pass."),
    Board('ka', 'Karnataka Board', 'Karnataka Board (KSEAB)', False, False,
          "KSEAB SSLC (Class 10) and II PUC (Class 12); 35% is the pass mark."),
    Board('kl', 'Kerala Board', 'Kerala Board (KBPE/DHSE)', False, False,
          "Kerala SSLC (Class 10) and Higher Secondary (Plus Two) on SCERT textbooks, with grade-based results."),
    Board('ap', 'Andhra Pradesh Board', 'Andhra Pradesh Board (BSEAP/BIEAP)', False, False,
          "BSEAP SSC (Class 10) and BIEAP Intermediate (Classes 11–12)."),
    Board('ts', 'Telangana Board', 'Telangana Board (BSE TS/TGBIE)', False, False,
          "BSE Telangana SSC (Class 10) and Board of Intermediate Education (Classes 11–12)."),
    Board('pb', 'Punjab Board', 'Punjab Board (PSEB)', False, True,
          "PSEB Matric (Class 10) and Senior Secondary (Class 12)."),
    Board('hr', 'Haryana Board', 'Haryana Board (BSEH)', True, True,
          "BSEH Secondary (Class 10) and Senior Secondary (Class 12), following NCERT textbooks."),
    Board('jh', 'Jharkhand Board', 'Jharkhand Board (JAC)', True, True,
          "JAC Matric (Class 10) and Intermediate (Class 12), following NCERT textbooks."),
    Board('uk', 'Uttarakhand Board', 'Uttarakhand Board (UBSE)', True, True,
          "UBSE High School (Class 10) and Intermediate (Class 12), following NCERT textbooks."),
    Board('cg', 'Chhattisgarh Board', 'Chhattisgarh Board (CGBSE)', True, True,
          "CGBSE High School (Class 10) and Higher Secondary (Class 12)."),
    Board('od', 'Odisha Board', 'Odisha Board (BSE/CHSE)', False, False,
          "BSE Odisha HSC (Class 10) and CHSE Odisha (Class 12)."),
    Board('as', 'Assam Board', 'Assam Board (ASSEB)', False, False,
          "Assam State School Education Board, formerly SEBA (Class 10) and AHSEC (Class 12)."),
    Board('hp', 'Himachal Board', 'Himachal Board (HPBOSE)', True, True,
          "HPBOSE Matric (Class 10) and Senior Secondary (Class 12), following NCERT textbooks."),
    Board('jk', 'J&K Board', 'J&K Board (JKBOSE)', True, False,
          "JKBOSE Class 10 and Class 12, following NCERT textbooks."),
    Board('ga', 'Goa Board', 'Goa Board (GBSHSE)', False, False,
          "Goa Board of Secondary and Higher Secondary Education: SSC (Class 10) and HSSC (Class 12)."),
    Board('mn', 'Manipur Board', 'Manipur Board (BOSEM/COHSEM)', False, False,
          "BOSEM HSLC (Class 10) and COHSEM Higher Secondary (Class 12)."),
    Board('ml', 'Meghalaya Board', 'Meghalaya Board (MBOSE)', False, False,
          "Meghalaya Board of School Education: SSLC (Class 10) and HSSLC (Class 12)."),
    Board('mz', 'Mizoram Board', 'Mizoram Board (MBSE)', False, False,
          "Mizoram Board of School Education: HSLC (Class 10) and HSSLC (Class 12)."),
    Board('nl', 'Nagaland Board', 'Nagaland Board (NBSE)', False, False,
          "Nagaland Board of School Education: HSLC (Class 10) and HSSLC (Class 12)."),
    Board('tr', 'Tripura Board', 'Tripura Board (TBSE)', True, False,
          "Tripura Board of Secondary Education: Madhyamik (Class 10) and Higher Secondary (Class 12), on NCERT-based textbooks."),
    Board('nios', 'NIOS', 'NIOS (Open Schooling)', False, True,
          "National Institute of Open Schooling: Secondary (Class 10) and Senior Secondary (Class 12) with flexible on-demand and public exams."),
]

BOARD_CHOICES = (
    [('cbse', 'CBSE'), ('icse', 'ICSE / ISC'), ('up', 'UP Board (UPMSP)')]
    + [(b.code, b.label) for b in STATE_BOARDS]
    + [('other', 'Other')]
)

# NIOS is a national open-schooling board, listed with the school boards rather than the state boards.
STATE_BOARD_CODES = ['up'] + [b.code for b in STATE_BOARDS if b.code != 'nios']

# 'Explore Exams' category name -> board codes whose series it lists
CATEGORY_BOARD_CODES = {
    'CBSE': ['cbse'],
    'ICSE': ['icse'],
    'UP Board': ['up'],
    'State Board': STATE_BOARD_CODES,
    **{b.category: [b.code] for b in STATE_BOARDS},
}
