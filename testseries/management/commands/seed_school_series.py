import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from testseries.management.cbse_data import BOARDS
from testseries.models import TestSeries, Test, Question, Subject

# Codes match seed_cbse_class1 so subjects are shared across boards and classes.
SUBJECTS = {
    'ENG1': ('English', '#3B82F6', 'book'),
    'HIN1': ('Hindi', '#F97316', 'language'),
    'MAT1': ('Mathematics', '#10B981', 'calculator'),
    'EVS1': ('EVS', '#22C55E', 'leaf'),
    'GK1': ('General Knowledge', '#8B5CF6', 'globe'),
    'SCI1': ('Science', '#06B6D4', 'flask'),
    'SST1': ('Social Science', '#EAB308', 'landmark'),
    'SAN1': ('Sanskrit', '#D97706', 'om'),
    'HCV1': ('History & Civics', '#B45309', 'landmark'),
    'GEO1': ('Geography', '#0EA5E9', 'earth-asia'),
    'PHY1': ('Physics', '#6366F1', 'atom'),
    'CHE1': ('Chemistry', '#14B8A6', 'vial'),
    'BIO1': ('Biology', '#16A34A', 'dna'),
    'ACC1': ('Accountancy', '#0F766E', 'book-open'),
    'BST1': ('Business Studies', '#9333EA', 'briefcase'),
    'ECO1': ('Economics', '#CA8A04', 'chart-line'),
    'HIS1': ('History', '#A16207', 'scroll'),
    'POL1': ('Political Science', '#DC2626', 'scale-balanced'),
    # Competitive exam sections (seed_exam_series)
    'RSN1': ('Reasoning', '#EC4899', 'brain'),
    'QNT1': ('Quantitative Aptitude', '#0891B2', 'square-root-variable'),
    'GA1': ('General Awareness', '#7C3AED', 'newspaper'),
    'DI1': ('Data Interpretation', '#0284C7', 'chart-pie'),
    'LGL1': ('Legal Reasoning', '#B91C1C', 'gavel'),
    'LAW1': ('Business Laws', '#991B1B', 'file-contract'),
    'CDP1': ('Child Development & Pedagogy', '#DB2777', 'children'),
    'TCH1': ('Teaching & Research Aptitude', '#4F46E5', 'chalkboard-user'),
    'CMP1': ('ICT & Computers', '#475569', 'laptop'),
    'CSE1': ('Computer Science', '#334155', 'microchip'),
    'MED1': ('Medicine', '#E11D48', 'stethoscope'),
    'CIV1': ('Civil Engineering', '#78716C', 'helmet-safety'),
    'DSG1': ('Design & Visual Aptitude', '#F43F5E', 'pen-ruler'),
    'DM1': ('Decision Making', '#0D9488', 'scale-unbalanced'),
    'NUR1': ('Nursing', '#EC4899', 'user-nurse'),
    'DEN1': ('Dentistry', '#06B6D4', 'tooth'),
    'TAX1': ('Taxation', '#65A30D', 'receipt'),
    'ARD1': ('Agriculture & Rural Development', '#15803D', 'tractor'),
    'PHA1': ('Pharmacy', '#7C3AED', 'prescription-bottle-medical'),
    'HSP1': ('Hospitality & Service Aptitude', '#B45309', 'hotel'),
}


def shuffled_options(text, opts, answer):
    """Shuffle options (same order on every run) so the correct letter isn't predictable."""
    correct = opts['abcd'.index(answer)]
    order = list(opts)
    random.Random(text).shuffle(order)
    return dict(zip('abcd', order)), 'abcd'[order.index(correct)]


def _settings_for(grade):
    """(difficulty, minutes per test, pass %) by stage."""
    if grade <= 5:
        return 'easy', 20, 40
    if grade <= 8:
        return 'medium', 25, 40
    return 'hard', 30, 33


BOARD_CODES = {'CBSE': 'cbse', 'ICSE': 'icse', 'UP Board': 'up'}


def _series_specs(board, config, grades):
    """Yield (title, slug, grade, stream, label, tests) for every series of a board."""
    for grade, tests in sorted(config['classes'].items()):
        if not grades or grade in grades:
            slug = (f'cbse-class-{grade}' if board == 'CBSE' else f'{slugify(board)}-class-{grade}')
            yield f"{board} Class {grade} – Subject-wise Test Series", f'{slug}-subject-wise-test-series', grade, '', f"{board} Class {grade}", tests
    for grade, streams in sorted(config['streams'].items()):
        if not grades or grade in grades:
            name = config['senior_name']
            for stream, tests in streams.items():
                label = f"{name} Class {grade} {stream}"
                yield f"{label} – Subject-wise Test Series", f'{slugify(label)}-subject-wise-test-series', grade, stream.lower(), label, tests


class Command(BaseCommand):
    help = "Create board-wise subject test series (CBSE 2-12, ICSE/ISC 1-12, UP Board 1-12). Re-running replaces them."

    def add_arguments(self, parser):
        parser.add_argument('classes', nargs='*', type=int, help="Classes to seed (default: all).")
        parser.add_argument('--board', action='append', choices=list(BOARDS), help="Board(s) to seed (default: all).")

    @transaction.atomic
    def handle(self, *args, **options):
        subjects = {}
        for code, (name, color, icon) in SUBJECTS.items():
            subjects[code], _ = Subject.objects.get_or_create(
                code=code, defaults={'name': name, 'color': color, 'icon': icon}
            )

        grades = set(options['classes'])
        for board in options['board'] or list(BOARDS):
            for title, slug, grade, stream, label, tests in _series_specs(board, BOARDS[board], grades):
                missing = {t[0] for t in tests} - subjects.keys()
                if missing:
                    raise CommandError(f"{label}: unknown subject codes {missing}")
                self._create_series(title, slug, BOARD_CODES[board], grade, stream, label, tests, subjects)

    def _create_series(self, title, slug, board, grade, stream, label, tests, subjects):
        difficulty, minutes, pass_pct = _settings_for(grade)
        subject_names = ", ".join(dict.fromkeys(subjects[t[0]].name for t in tests))

        TestSeries.objects.filter(slug=slug).delete()
        series = TestSeries.objects.create(
            title=title,
            slug=slug,
            board=board,
            grade=grade,
            stream=stream,
            description=(
                f"Subject-wise practice tests for {label} covering {subject_names}. "
                f"Each test has 10 multiple-choice questions with explanations."
            ),
            difficulty=difficulty,
            estimated_duration=f'{minutes} minutes per test',
            is_free=True,
            price=0,
            has_negative_marking=False,
            negative_marks=0,
            pass_percentage=pass_pct,
        )

        for code, test_title, description, questions in tests:
            test = Test.objects.create(
                test_series=series,
                title=test_title,
                description=description,
                duration_minutes=minutes,
                max_attempts=3,
            )
            for order, (text, opts, answer, q_difficulty, explanation) in enumerate(questions, start=1):
                options_map, answer = shuffled_options(text, opts, answer)
                Question.objects.create(
                    test=test,
                    subject=subjects[code],
                    question_type='mcq_single',
                    difficulty=q_difficulty,
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
        self.stdout.write(self.style.SUCCESS(f'{label}: {series.total_tests} tests, {series.total_questions} questions.'))
