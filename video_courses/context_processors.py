from django.core.cache import cache

from testseries.boards import STATE_BOARDS
from testseries.exam_tools import EXAM_GROUPS

from .models import Category

SCHOOL_BOARD_CATEGORIES = ['CBSE', 'ICSE', 'UP Board', 'NIOS', 'State Board']
CACHE_KEY = "site-navbar-categories"        # full menu; build_test_content clears both keys after adding exams
TABS_CACHE_KEY = "site-navbar-category-tabs"  # just the tabs, read on every page
CACHE_SECONDS = 300


def clear_menu_cache():
    cache.delete_many([CACHE_KEY, TABS_CACHE_KEY])


def _group_categories(categories):
    """Explore Exams menu: school boards, state boards, each exam category (split into its sub-categories), then the rest.

    Each group: {'key', 'label', 'icon', 'count', 'subs': [{'label', 'categories': [{'name', 'slug', 'icon', 'color', 'rgb'}]}]}.
    """
    from testseries.content.catalog import placement

    by_name = {category.name: category for category in categories}
    used = set()
    groups = []

    def add(key, label, icon, names, sub_of=None):
        items = [by_name[name] for name in names if name in by_name and name not in used]
        used.update(category.name for category in items)
        if not items:
            return
        subs = {}
        for category in items:
            subs.setdefault(sub_of(category) if sub_of else label, []).append({
                'name': category.name, 'slug': category.slug, 'icon': category.icon or 'graduation-cap',
                'color': category.icon_color, 'rgb': category.icon_color_rgb,
            })
        groups.append({'key': key, 'label': label, 'icon': icon, 'count': len(items),
                       'subs': [{'label': sub, 'categories': members} for sub, members in subs.items()]})

    add('school', 'School Boards', 'school', SCHOOL_BOARD_CATEGORIES)
    add('state', 'State Boards', 'map-location-dot', [board.category for board in STATE_BOARDS])
    for key, label, icon, exams in EXAM_GROUPS:
        add(key, label, icon, exams, sub_of=lambda category: category.sub_category or placement(category.name)[1])
    add('more', 'More', 'layer-group', [category.name for category in categories])
    return groups


def category_groups():
    """The whole menu (used by the exam_menu view when the menu is opened)."""
    groups = cache.get(CACHE_KEY)
    if not isinstance(groups, list):
        categories = list(Category.objects.only('id', 'name', 'slug', 'icon', 'icon_color', 'sub_category').exclude(slug=''))
        groups = _group_categories(categories)
        cache.set(CACHE_KEY, groups, CACHE_SECONDS)
    return groups


def category_tabs():
    tabs = cache.get(TABS_CACHE_KEY)
    if not isinstance(tabs, list):
        tabs = [{k: g[k] for k in ('key', 'label', 'icon', 'count')} for g in category_groups()]
        cache.set(TABS_CACHE_KEY, tabs, CACHE_SECONDS)
    return tabs


def categories_context(request):
    """Explore Exams menu tabs for every page; the exam links load when the menu is first opened (exam_menu view)."""
    return {'navbar_category_groups': category_tabs()}
