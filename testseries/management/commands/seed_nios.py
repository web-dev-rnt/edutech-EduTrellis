from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import transaction

from testseries.management import nios_seed
from testseries.models import Question, Subject, Test, TestSeries
from video_courses.models import Category


class Command(BaseCommand):
    help = (
        "Create the NIOS Secondary (Class 10) and Senior Secondary (Class 12) test series with NIOS course-wise "
        "subject tests, combination mocks, a rules test and a free demo. Never deletes anything; re-running only "
        "adds missing tests."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        added = nios_seed.seed(TestSeries, Test, Question, Subject, Category, log=self.stdout.write)
        cache.delete('site-navbar-categories')
        self.stdout.write(self.style.SUCCESS(f"NIOS: added {added} tests."))
