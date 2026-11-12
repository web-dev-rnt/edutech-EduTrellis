from .models import Category
from django.core.cache import cache

from testseries.boards import STATE_BOARDS
from testseries.exam_tools import EXAM_GROUPS

SCHOOL_BOARD_CATEGORIES = ['CBSE', 'ICSE', 'UP Board', 'NIOS', 'State Board']


def _group_categories(categories):
    """Explore Exams menu sections: school boards, state boards, each exam group, then everything else."""
    by_name = {category.name: category for category in categories}
    used = set()
    groups = []

    def add(key, label, icon, names):
        items = [by_name[name] for name in names if name in by_name and name not in used]
        used.update(category.name for category in items)
        if items:
            groups.append({'key': key, 'label': label, 'icon': icon, 'categories': items})

    add('school', 'School Boards', 'school', SCHOOL_BOARD_CATEGORIES)
    add('state', 'State Boards', 'map-location-dot', [board.category for board in STATE_BOARDS])
    for key, label, icon, exams in EXAM_GROUPS:
        add(key, label, icon, exams)
    add('more', 'More', 'layer-group', [category.name for category in categories])
    return groups


def categories_context(request):
    """Context processor to make categories available in all templates"""
    cached = cache.get("site-navbar-categories")
    if not isinstance(cached, dict):
        categories = list(Category.objects.all())
        cached = {'categories': categories, 'groups': _group_categories(categories)}
        cache.set("site-navbar-categories", cached, 300)

    return {
        'navbar_categories': cached['categories'],
        'navbar_category_groups': cached['groups'],
    }
