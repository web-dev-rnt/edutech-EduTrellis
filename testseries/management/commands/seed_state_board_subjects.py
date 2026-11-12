import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from testseries.boards import STATE_BOARDS
from testseries.management.cbse_data.secondary import CLASSES as SECONDARY
from testseries.management.cbse_data.senior import STREAMS
from testseries.management.commands.seed_school_series import SUBJECTS, shuffled_options
from testseries.models import TestSeries, Test, Question, Subject


class Command(BaseCommand):
    help = (
        "Add subject-wise tests to every state board's Class 10 and Class 12 Science series, and create Class 12 "
        "Commerce and Arts series (board-pattern mock + subject tests). Never deletes anything, so purchases "
        "and attempts are kept; re-running only fills in what is missing. Run make_series_paid afterwards."
    )

    def add_arguments(self, parser):
        parser.add_argument('boards', nargs='*', help="Board codes, e.g. bseb mh (default: all).")

    @transaction.atomic
    def handle(self, *args, **options):
        boards = [b for b in STATE_BOARDS if not options['boards'] or b.code in options['boards']]
        if options['boards'] and len(boards) != len(options['boards']):
            raise CommandError(f"Unknown board codes. Choose from: {', '.join(b.code for b in STATE_BOARDS)}")

        self.subjects = {
            code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
            for code, (name, color, icon) in SUBJECTS.items()
        }
        added_tests = added_series = 0
        for board in boards:
            class10 = [t for t in SECONDARY[10] if board.hindi or t[0] != 'HIN1']
            plan = [(10, '', class10)] + [
                (12, stream.lower(), banks) for stream, banks in STREAMS[12].items()
            ]
            for grade, stream, banks in plan:
                series, created = self._series(board, grade, stream, banks)
                added_series += created
                for bank in banks:
                    added_tests += self._subject_test(series, board, grade, bank)
        self.stdout.write(self.style.SUCCESS(f"Added {added_series} series and {added_tests} subject tests."))

    def _series(self, board, grade, stream, banks):
        """The board's existing series for this class/stream, or a new one with a mixed board-pattern mock."""
        slug = f"{board.code}-board-class-{grade}{'-' + stream if stream else ''}-board-pattern-mock"
        series = TestSeries.objects.filter(slug=slug).first()
        if series:
            return series, False

        label = f"{board.label} Class {grade}{' ' + stream.title() if stream else ''}"
        names = ", ".join(self.subjects[bank[0]].name for bank in banks)
        series = TestSeries.objects.create(
            title=f"{label} – Board Exam Pattern Mock",
            slug=slug, board=board.code, grade=grade, stream=stream,
            description=(
                f"{board.note} This series covers {names} with a full board-pattern mock and a test for each "
                "subject. Questions follow the NCERT syllabus that the board's textbooks are based on."
            ),
            difficulty='hard', estimated_duration='25 minutes per mock',
            is_free=True, price=0, has_negative_marking=False, negative_marks=0, pass_percentage=33,
        )
        rng = random.Random(f'{board.code}-{grade}-{stream}')
        mixed = [(bank[0], q) for bank in banks for q in rng.sample(bank[3], 4)]
        test = Test.objects.create(
            test_series=series, title=f"{label} Board Pattern Mock Test 1",
            description=f"Objective practice for the {label} board exam: {names}.",
            duration_minutes=25, max_attempts=3, shuffle_questions=False, paper_type='mock',
        )
        self._add_questions(test, mixed)
        self.stdout.write(f"  + series {series.title}")
        return series, True

    def _subject_test(self, series, board, grade, bank):
        code, _title, desc, questions = bank
        subject = self.subjects[code]
        title = f"{subject.name} – Subject Test"
        if series.tests.filter(title=title).exists():
            return 0
        test = Test.objects.create(
            test_series=series, title=title,
            description=f"Class {grade} {subject.name} for the {board.category} board: {desc}",
            duration_minutes=15, max_attempts=3, shuffle_questions=False, paper_type='subject',
        )
        self._add_questions(test, [(code, q) for q in questions])
        return 1

    def _add_questions(self, test, items):
        for order, (code, (text, opts, answer, difficulty, explanation)) in enumerate(items, start=1):
            options_map, answer = shuffled_options(text, opts, answer)
            Question.objects.create(
                test=test, subject=self.subjects[code], question_type='mcq_single', difficulty=difficulty,
                question_text=text, marks=1, negative_marks=0, options=options_map,
                correct_answer={'answer': answer}, explanation=explanation, order=order,
            )
        test.update_stats()
        test.test_series.update_stats()
