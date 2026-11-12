from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from testseries.exam_tools import EXAM_CALCULATORS
from testseries.management.cbse_data.pyq_pattern import PAPERS
from testseries.management.commands.seed_school_series import SUBJECTS, shuffled_options
from testseries.models import TestSeries, Test, Question, Subject

TITLE = 'Previous Year Pattern Paper 1'


class Command(BaseCommand):
    help = (
        "Add a previous-year-pattern paper (topics past papers ask repeatedly, in the real marking scheme) to the "
        "CBSE 10/12, JEE Main, NEET UG, SSC CGL and UPSC series. Never deletes anything; re-running skips papers "
        "that already exist."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        subjects = {
            code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
            for code, (name, color, icon) in SUBJECTS.items()
        }
        added = 0
        for paper in PAPERS:
            series = TestSeries.objects.filter(is_active=True, **paper['series']).order_by('pk').first()
            if not series:
                self.stdout.write(self.style.WARNING(f"  skipped {paper['name']}: no matching series"))
                continue
            if series.tests.filter(title=TITLE).exists():
                continue

            section_names = ", ".join(dict.fromkeys(name for _, name, *_ in paper['sections']))
            test = Test.objects.create(
                test_series=series,
                title=TITLE,
                description=(
                    f"Questions on topics that past {paper['name']} papers ask again and again, with the real "
                    f"marking scheme ({section_names}). Original practice questions, not an official question paper."
                ),
                duration_minutes=paper['minutes'],
                max_attempts=3,
                shuffle_questions=False,
                calculator=EXAM_CALCULATORS.get(series.exam, 'none'),
                paper_type='pyp',
            )
            order = 0
            for code, section, marks, negative, questions in paper['sections']:
                penalty = Decimal(str(negative)) if series.has_negative_marking else 0
                for text, opts, answer, difficulty, explanation in questions:
                    order += 1
                    options_map, answer = shuffled_options(text, opts, answer)
                    Question.objects.create(
                        test=test, subject=subjects[code], question_type='mcq_single', difficulty=difficulty,
                        question_text=text, marks=marks, negative_marks=penalty, options=options_map,
                        correct_answer={'answer': answer}, explanation=f"[{section}] {explanation}", order=order,
                    )
            test.update_stats()
            series.update_stats()
            added += 1
            self.stdout.write(f"  + {series.title}: {test.total_questions} questions, {paper['minutes']} min")
        self.stdout.write(self.style.SUCCESS(f"Added {added} previous-year-pattern papers."))
