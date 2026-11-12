"""Switch on the on-screen calculator for existing tests of exams that provide one (frozen copy of the mapping).

Only tests still set to 'none' are changed, so a calculator an admin chose for a test by hand is kept.
"""
from django.db import migrations

EXAM_CALCULATORS = {
    'GATE': 'scientific', 'GATE EE': 'scientific', 'GATE ME': 'scientific', 'GATE CE': 'scientific',
    'GATE EC': 'scientific', 'GATE DA': 'scientific', 'IIT JAM': 'scientific',
    'CAT': 'basic', 'CA Foundation': 'basic', 'CA Foundation Economics': 'basic', 'CA Intermediate': 'basic',
    'CMA Foundation': 'basic', 'TCS NQT': 'basic',
}


def set_exam_calculators(apps, schema_editor):
    Test = apps.get_model('testseries', 'Test')
    for exam, calculator in EXAM_CALCULATORS.items():
        Test.objects.filter(test_series__exam=exam, calculator='none').update(calculator=calculator)


class Migration(migrations.Migration):

    dependencies = [
        ('testseries', '0018_more_state_boards'),
    ]

    operations = [
        migrations.RunPython(set_exam_calculators, migrations.RunPython.noop),
    ]
