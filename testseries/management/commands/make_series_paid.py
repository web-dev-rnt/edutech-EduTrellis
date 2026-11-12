import math
from decimal import Decimal
from itertools import zip_longest

from django.core.management.base import BaseCommand
from django.db import transaction

from testseries.models import TestSeries, Test, Question

DEMO_QUESTIONS = 10
DEMO_TITLE = 'Free Demo Test'

# Postgraduate, professional and officer-grade exams carry the higher price.
PREMIUM_EXAMS = {
    'JEE Advanced', 'GATE', 'NEET PG', 'NEET MDS', 'UPSC Civil Services', 'UPSC ESE', 'UPSC CMS',
    'CAT', 'CA Intermediate', 'CSIR NET', 'RBI Grade B', 'SEBI Grade A', 'NABARD Grade A', 'Judicial Services',
}

# Copied from a source question onto its demo copy.
QUESTION_FIELDS = [
    'subject', 'question_type', 'difficulty', 'question_text', 'question_image', 'marks', 'negative_marks',
    'options', 'correct_answer', 'explanation', 'solution_image', 'solution_video_url',
]


def default_price(series):
    """Price for a series that has none: by class for school boards, by level for exams."""
    if series.board:
        if not series.grade:
            return Decimal('99')
        if series.grade <= 5:
            return Decimal('49')
        if series.grade <= 8:
            return Decimal('79')
        if series.grade <= 10:
            return Decimal('99')
        return Decimal('149')
    if series.exam:
        return Decimal('299') if series.exam in PREMIUM_EXAMS else Decimal('199')
    return Decimal('99')


def demo_sample(questions, limit):
    """Up to `limit` questions taken in turn from each subject, so the demo shows every section."""
    by_subject = {}
    for question in questions:
        by_subject.setdefault(question.subject_id, []).append(question)
    picked = [q for round_ in zip_longest(*by_subject.values()) for q in round_ if q is not None][:limit]
    # Present them in paper order: section by section.
    subject_order = list(by_subject)
    return sorted(picked, key=lambda q: (subject_order.index(q.subject_id), q.order, q.pk))


class Command(BaseCommand):
    help = (
        "Make every free test series paid (prices by class or exam level, existing prices kept) "
        "and give each series a free demo test sampled from its questions. Safe to re-run."
    )

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would change without saving.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        priced = demos = 0
        with transaction.atomic():
            for series in TestSeries.objects.order_by('pk'):
                if series.is_free or not series.price:
                    series.is_free = False
                    if not series.price:
                        series.price = default_price(series)
                    series.save(update_fields=['is_free', 'price'])
                    priced += 1
                    self.stdout.write(f"  paid  Rs.{series.price:>4}  {series.title}")

                if self._create_demo(series):
                    demos += 1

            if dry_run:
                transaction.set_rollback(True)

        prefix = 'Would make' if dry_run else 'Made'
        self.stdout.write(self.style.SUCCESS(f"{prefix} {priced} series paid and add {demos} demo tests."))

    def _create_demo(self, series):
        if series.tests.filter(is_demo=True).exists():
            return False
        source_tests = list(series.tests.filter(is_active=True, is_demo=False).order_by('created_at'))
        questions = list(
            Question.objects.filter(test__in=source_tests).order_by('test__created_at', 'order', 'pk')
        )
        if not questions:
            return False

        sample = demo_sample(questions, DEMO_QUESTIONS)
        base = source_tests[0]
        base_count = base.questions.count() or len(sample)
        minutes = max(5, math.ceil(base.duration_minutes * len(sample) / base_count))

        demo = Test.objects.create(
            test_series=series,
            title=DEMO_TITLE,
            description=(
                f"Try {len(sample)} sample questions from this series in the real exam interface, "
                "free and without buying the series."
            ),
            duration_minutes=minutes,
            max_attempts=3,
            shuffle_questions=False,
            show_result_immediately=True,
            allow_review=True,
            calculator=base.calculator,
            is_demo=True,
        )
        Question.objects.bulk_create([
            Question(test=demo, order=number, **{field: getattr(q, field) for field in QUESTION_FIELDS})
            for number, q in enumerate(sample, start=1)
        ])
        demo.update_stats()
        series.update_stats()
        self.stdout.write(f"  demo  {len(sample):>2} Qs {minutes:>3} min  {series.title}")
        return True
