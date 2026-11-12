from django.db import migrations
from django.utils.text import slugify


TOPIC_WISE = 'Topic Wise Tests'
FULL_MOCKS = 'Full Length Mock Tests'

PRIMARY = ['English', 'Hindi', 'Mathematics', 'EVS']
MIDDLE = ['English', 'Hindi', 'Mathematics', 'Science', 'Social Science']
SENIOR = ['English', 'Physics', 'Chemistry', 'Mathematics', 'Biology']


def subjects_for(level_name):
    """Subjects under 'Topic Wise Tests' for a class, by its (seeded) name suffix."""
    suffix = level_name.rsplit('Class ', 1)[-1] if 'Class ' in level_name else ''
    if suffix in ('XI', 'XII'):
        return SENIOR
    if suffix in ('VI', 'VII', 'VIII', 'IX', 'X'):
        return MIDDLE
    return PRIMARY  # Nursery, LKG, UKG, Class I-V


def seed(apps, schema_editor):
    Category = apps.get_model('video_courses', 'Category')
    Sub = apps.get_model('testseries', 'TestSeriesSubCategory')
    TestSeries = apps.get_model('testseries', 'TestSeries')

    def child(category, parent, name, order):
        node = Sub.objects.filter(category=category, parent=parent, name=name).first()
        if node:
            return node
        base = slugify(f'{parent.slug} {name}')[:110]
        slug, n = base, 2
        while Sub.objects.filter(category=category, slug=slug).exists():
            slug, n = f'{base}-{n}', n + 1
        return Sub.objects.create(category=category, parent=parent, name=name, slug=slug, order=order)

    for board in Category.objects.filter(slug__in=['cbse', 'icse', 'state-board']):
        for level in Sub.objects.filter(category=board, parent__isnull=True):
            topic_wise = child(board, level, TOPIC_WISE, 1)
            mocks = child(board, level, FULL_MOCKS, 2)
            for order, subject in enumerate(subjects_for(level.name), start=1):
                child(board, topic_wise, f'{subject} Tests', order)

            # The existing class practice papers mix subjects, so they are full mock tests
            TestSeries.objects.filter(subcategory=level).update(subcategory=mocks)


class Migration(migrations.Migration):

    dependencies = [
        ('testseries', '0007_subcategory_parent'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
