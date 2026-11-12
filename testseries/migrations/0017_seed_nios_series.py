from django.db import migrations


def seed_nios(apps, schema_editor):
    from testseries.management import nios_seed

    nios_seed.seed(
        apps.get_model('testseries', 'TestSeries'),
        apps.get_model('testseries', 'Test'),
        apps.get_model('testseries', 'Question'),
        apps.get_model('testseries', 'Subject'),
        apps.get_model('video_courses', 'Category'),
        log=lambda message: None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('testseries', '0016_alter_question_marks_alter_test_paper_type'),
        ('video_courses', '0005_alter_coursevideo_file'),
    ]

    operations = [
        migrations.RunPython(seed_nios, migrations.RunPython.noop),
    ]
