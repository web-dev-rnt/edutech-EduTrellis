"""Folds every question from the earlier hand-written seed files into the topic pools, so nothing already uploaded is lost.

Pools created:
  exam.<exam slug>.<subject code>        questions written for that exam (e.g. exam.jee-main.PHY1)
  school.<board>.<grade>.<subject code>  board/class questions (board: cbse, icse, up)
  school.any.<grade>.<subject code>      the same questions merged across boards (state boards draw from these)
  pool.<subject code>                    every competitive-exam question of that subject
"""
from django.utils.text import slugify

from .core import TOPICS, register

LABELS = {}


def _add(key, code, label, rows):
    if rows:
        register(key, code, label, rows=rows)


def load():
    if 'pool.QNT1' in TOPICS:  # already loaded
        return
    from testseries.management.cbse_data import BOARDS
    from testseries.management.cbse_data.exams import EXAMS
    from testseries.management.cbse_data.pyq_pattern import PAPERS
    from testseries.management.commands.seed_cbse_class1 import TESTS as CLASS1
    from testseries.management.commands.seed_school_series import SUBJECTS

    def name(code):
        return SUBJECTS.get(code, (code,))[0]

    for spec in EXAMS:
        for code, section, _marks, _neg, questions in spec['sections']:
            _add(f"exam.{slugify(spec['exam'])}.{code}", code, f"{spec['exam']} – {section}", questions)
            _add(f"pool.{code}", code, name(code), questions)

    board_codes = {'CBSE': 'cbse', 'ICSE': 'icse', 'UP Board': 'up'}
    for board, config in BOARDS.items():
        b = board_codes[board]
        for grade, tests in config['classes'].items():
            for code, _title, _desc, questions in tests:
                _add(f"school.{b}.{grade}.{code}", code, name(code), questions)
                _add(f"school.any.{grade}.{code}", code, name(code), questions)
        for grade, streams in config['streams'].items():
            for _stream, tests in streams.items():
                for code, _title, _desc, questions in tests:
                    if f"school.{b}.{grade}.{code}" in TOPICS and questions[0] in (TOPICS[f"school.{b}.{grade}.{code}"].rows or []):
                        continue  # shared between streams
                    _add(f"school.{b}.{grade}.{code}", code, name(code), questions)
                    _add(f"school.any.{grade}.{code}", code, name(code), questions)
    for code, _title, _desc, questions in CLASS1:
        _add(f"school.cbse.1.{code}", code, name(code), questions)
        _add(f"school.any.1.{code}", code, name(code), questions)

    for paper in PAPERS:
        sel = paper['series']
        for code, section, _m, _n, questions in paper['sections']:
            if 'exam' in sel:
                _add(f"exam.{slugify(sel['exam'])}.{code}", code, section, questions)
                _add(f"pool.{code}", code, name(code), questions)
            else:
                grade = sel.get('grade')
                _add(f"school.{sel.get('board', 'cbse')}.{grade}.{code}", code, name(code), questions)
                _add(f"school.any.{grade}.{code}", code, name(code), questions)

    # Duplicate rows (the same question used for two boards) would only waste draws.
    for key, topic in TOPICS.items():
        if topic.rows and (key.startswith('school.') or key.startswith('pool.') or key.startswith('exam.')):
            seen, unique = set(), []
            for row in topic.rows:
                k = row[0].strip().lower()
                if k not in seen:
                    seen.add(k)
                    unique.append(row)
            topic.rows = unique


def exam_key(exam, code):
    key = f"exam.{slugify(exam)}.{code}"
    return key if key in TOPICS else None
