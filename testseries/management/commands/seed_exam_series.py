from decimal import Decimal

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from testseries.management.cbse_data.exams import EXAMS
from testseries.management.commands.seed_school_series import SUBJECTS, shuffled_options
from testseries.exam_tools import EXAM_CALCULATORS
from testseries.models import TestSeries, Test, Question, Subject
from video_courses.models import Category


class Command(BaseCommand):
    help = "Create a pattern mock test series for each competitive exam (SSC, Banking, JEE, NEET, UPSC…). Re-running replaces them."

    def add_arguments(self, parser):
        parser.add_argument('exams', nargs='*', help='Exam names to seed, e.g. "SSC CGL" (default: all).')

    @transaction.atomic
    def handle(self, *args, **options):
        wanted = set(options['exams'])
        unknown = wanted - {e['exam'] for e in EXAMS}
        if unknown:
            raise CommandError(f"Unknown exams: {', '.join(sorted(unknown))}")

        subjects = {
            code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
            for code, (name, color, icon) in SUBJECTS.items()
        }
        for spec in EXAMS:
            if wanted and spec['exam'] not in wanted:
                continue
            self._ensure_category(spec)
            self._create_series(spec, subjects)
        cache.delete('site-navbar-categories')

    def _ensure_category(self, spec):
        """Create the exam's 'Explore Exams' category if missing; fill in a blank description with the pattern."""
        category, created = Category.objects.get_or_create(
            name=spec['exam'],
            defaults={
                'icon': spec.get('icon', 'graduation-cap'),
                'icon_color': spec.get('color', '#667eea'),
                'description': spec['pattern'],
            },
        )
        if created:
            self.stdout.write(f"  + category '{category.name}'")
        elif not category.description:
            category.description = spec['pattern']
            category.save(update_fields=['description'])

    def _create_series(self, spec, subjects):
        exam = spec['exam']
        sections = spec['sections']
        for code, section, *_ in sections:
            if code not in subjects:
                raise CommandError(f"{exam} / {section}: unknown subject code {code}")

        negatives = [Decimal(str(neg)) for *_, neg, _ in sections if neg]
        slug = f'{slugify(exam)}-pattern-mock-test-series'
        TestSeries.objects.filter(slug=slug).delete()
        series = TestSeries.objects.create(
            title=f"{exam} – Pattern Mock Test Series",
            slug=slug,
            exam=exam,
            description=(
                f"Mock test for {exam} following the official exam pattern: sections, marking scheme and "
                f"time per question match the real paper. {spec['pattern']}"
            ),
            difficulty=spec['difficulty'],
            estimated_duration=f"{spec['minutes']} minutes per mock",
            is_free=True,
            price=0,
            has_negative_marking=bool(negatives),
            negative_marks=max(negatives) if negatives else 0,
            pass_percentage=33,
        )

        section_names = ", ".join(dict.fromkeys(section for _, section, *_ in sections))
        test = Test.objects.create(
            test_series=series,
            title=f"{exam} Pattern Mock Test 1",
            description=f"Sections: {section_names}. {spec['pattern']}",
            duration_minutes=spec['minutes'],
            max_attempts=3,
            shuffle_questions=False,  # keep questions grouped by section, as in the real paper
            calculator=EXAM_CALCULATORS.get(exam, 'none'),
        )
        order = 0
        for code, section, marks, negative, questions in sections:
            for text, opts, answer, difficulty, explanation in questions:
                order += 1
                options_map, answer = shuffled_options(text, opts, answer)
                Question.objects.create(
                    test=test,
                    subject=subjects[code],
                    question_type='mcq_single',
                    difficulty=difficulty,
                    question_text=text,
                    marks=marks,
                    negative_marks=negative,
                    options=options_map,
                    correct_answer={'answer': answer},
                    explanation=f"[{section}] {explanation}",
                    order=order,
                )
        test.update_stats()
        series.update_stats()
        self.stdout.write(self.style.SUCCESS(
            f"{exam}: {series.total_questions} questions, {series.total_marks} marks, {spec['minutes']} min."
        ))
