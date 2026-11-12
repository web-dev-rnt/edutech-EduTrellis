import re

from django.db import migrations
from django.utils.text import slugify


# (group name, font awesome icon, category slugs listed under it)
GROUPS = [
    ('School Level - All India', 'school', ['cbse', 'icse', 'state-board']),
    ('Engineering Entrance', 'cogs', ['jee-main', 'jee-advanced', 'bitsat', 'viteee', 'gate', 'polytechnic-entrance']),
    ('Medical Entrance', 'stethoscope', ['neet-ug', 'neet-pg', 'aiims']),
    ('Civil Services', 'landmark', ['upsc-civil-services', 'state-psc']),
    ('Banking & Insurance', 'university', ['ibps-po', 'ibps-clerk', 'sbi-po', 'rbi-grade-b', 'lic-aao']),
    ('SSC Exams', 'file-alt', ['ssc-cgl', 'ssc-chsl', 'ssc-gd', 'ssc-mts']),
    ('Railway Exams', 'train', ['rrb-ntpc', 'rrb-group-d', 'rrb-je']),
    ('Defence Exams', 'shield-alt', [
        'nda', 'cds', 'afcat', 'indian-army-gd', 'indian-navy-agniveer',
        'indian-air-force', 'capf-assistant-commandant',
    ]),
    ('Police Exams', 'user-shield', ['state-police-constable', 'sub-inspector-si']),
    ('Teaching Exams', 'chalkboard-teacher', ['ctet', 'ugc-net']),
    ('Law, MBA & Other Entrances', 'balance-scale', ['clat', 'cat', 'mat', 'ca-foundation']),
]

# Boards that get a class-wise breakdown (Nursery -> Class XII)
SCHOOL_BOARD_SLUGS = ['cbse', 'icse', 'state-board']
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
LEVELS = ['Nursery', 'Lower Kindergarten - LKG', 'Upper Kindergarten - UKG'] + [f'Class {r}' for r in ROMAN]


def seed(apps, schema_editor):
    Category = apps.get_model('video_courses', 'Category')
    TestSeriesGroup = apps.get_model('testseries', 'TestSeriesGroup')
    TestSeriesSubCategory = apps.get_model('testseries', 'TestSeriesSubCategory')
    TestSeries = apps.get_model('testseries', 'TestSeries')

    for order, (name, icon, category_slugs) in enumerate(GROUPS, start=1):
        group, _ = TestSeriesGroup.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name)[:140], 'icon': icon, 'order': order},
        )
        group.categories.add(*Category.objects.filter(slug__in=category_slugs))

    for board in Category.objects.filter(slug__in=SCHOOL_BOARD_SLUGS):
        for order, level in enumerate(LEVELS, start=1):
            name = f'{board.name} {level}'
            TestSeriesSubCategory.objects.get_or_create(
                category=board, name=name,
                defaults={'slug': slugify(name)[:120], 'order': order},
            )

        # File existing "... Class 7 ..." series under the matching class
        for series in TestSeries.objects.filter(category=board, subcategory__isnull=True):
            match = re.search(r'\bClass\s+(\d{1,2})\b', series.title, re.IGNORECASE)
            if not match or not 1 <= int(match.group(1)) <= 12:
                continue
            sub = TestSeriesSubCategory.objects.filter(
                category=board, name=f'{board.name} Class {ROMAN[int(match.group(1)) - 1]}'
            ).first()
            if sub:
                series.subcategory = sub
                series.save(update_fields=['subcategory'])


class Migration(migrations.Migration):

    dependencies = [
        ('testseries', '0005_testseriesgroup_subcategory_order'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
