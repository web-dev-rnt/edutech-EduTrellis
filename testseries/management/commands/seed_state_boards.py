import random

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from testseries.boards import STATE_BOARDS
from testseries.management.cbse_data import senior
from testseries.management.cbse_data.secondary import CLASSES as SECONDARY
from testseries.management.commands.seed_school_series import SUBJECTS, shuffled_options
from testseries.models import TestSeries, Test, Question, Subject
from video_courses.models import Category

BOARD_COLORS = ['#7c3aed', '#0891b2', '#16a34a', '#ea580c', '#db2777', '#4f46e5', '#ca8a04', '#0d9488']


def _pick(tests, per_subject, seed):
    """[(subject code, question)] taking `per_subject` questions from each test, varied per board."""
    rng = random.Random(seed)
    picked = []
    for code, _title, _desc, questions in tests:
        picked += [(code, q) for q in rng.sample(questions, per_subject)]
    return picked


class Command(BaseCommand):
    help = ("Create an 'Explore Exams' category plus Class 10 and Class 12 (Science) board-pattern mocks for each "
            "state board and NIOS, built from the NCERT-aligned question banks. Re-running replaces them.")

    def add_arguments(self, parser):
        parser.add_argument('boards', nargs='*', help="Board codes to seed, e.g. bseb mh (default: all).")

    @transaction.atomic
    def handle(self, *args, **options):
        boards = [b for b in STATE_BOARDS if not options['boards'] or b.code in options['boards']]
        if options['boards'] and len(boards) != len(options['boards']):
            raise CommandError(f"Unknown board codes. Choose from: {', '.join(b.code for b in STATE_BOARDS)}")

        subjects = {
            code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
            for code, (name, color, icon) in SUBJECTS.items()
        }
        # UP Board already has full class-wise series; it just needs its own category
        Category.objects.get_or_create(name='UP Board', defaults={
            'icon': 'school', 'icon_color': '#b45309',
            'description': "UPMSP High School (Class 10) and Intermediate (Class 12); Hindi-medium Parishadiya syllabus for Classes 1–8.",
        })

        class10 = SECONDARY[10]
        class12 = [senior.PHY_12, senior.CHE_12, senior.MAT_12, senior.BIO_12, senior.ENG_12]
        for i, board in enumerate(boards):
            Category.objects.get_or_create(name=board.category, defaults={
                'icon': 'school', 'icon_color': BOARD_COLORS[i % len(BOARD_COLORS)], 'description': board.note,
            })
            tests10 = class10 if board.hindi else [t for t in class10 if t[0] != 'HIN1']
            self._create_series(board, 10, '', _pick(tests10, 20 // len(tests10), f'{board.code}-10'), subjects)
            self._create_series(board, 12, 'science', _pick(class12, 4, f'{board.code}-12'), subjects)
        cache.delete('site-navbar-categories')

    def _create_series(self, board, grade, stream, questions, subjects):
        label = f"{board.label} Class {grade}{' Science' if stream else ''}"
        slug = f"{board.code}-board-class-{grade}{'-' + stream if stream else ''}-board-pattern-mock"
        subject_names = ", ".join(dict.fromkeys(subjects[code].name for code, _ in questions))
        syllabus = ("follows NCERT(-based) textbooks, so questions are drawn from the NCERT syllabus"
                    if board.ncert else
                    "has its own textbooks; questions cover the core topics common to the NCERT syllabus")

        TestSeries.objects.filter(slug=slug).delete()
        series = TestSeries.objects.create(
            title=f"{label} – Board Exam Pattern Mock",
            slug=slug,
            board=board.code,
            grade=grade,
            stream=stream,
            description=f"{board.note} This mock covers {subject_names}. The board {syllabus}.",
            difficulty='medium' if grade == 10 else 'hard',
            estimated_duration='25 minutes per mock',
            is_free=True,
            price=0,
            has_negative_marking=False,
            negative_marks=0,
            pass_percentage=33,
        )
        test = Test.objects.create(
            test_series=series,
            title=f"{label} Board Pattern Mock Test 1",
            description=f"Objective practice for the {label} board exam: {subject_names}.",
            duration_minutes=25,
            max_attempts=3,
            shuffle_questions=False,
        )
        for order, (code, (text, opts, answer, difficulty, explanation)) in enumerate(questions, start=1):
            options_map, answer = shuffled_options(text, opts, answer)
            Question.objects.create(
                test=test, subject=subjects[code], question_type='mcq_single', difficulty=difficulty,
                question_text=text, marks=1, negative_marks=0, options=options_map,
                correct_answer={'answer': answer}, explanation=explanation, order=order,
            )
        test.update_stats()
        series.update_stats()
        self.stdout.write(self.style.SUCCESS(f"{label}: {series.total_questions} questions."))
