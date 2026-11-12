from django import template
from adminpanel.models import *

register = template.Library()

@register.inclusion_tag('components/banner_slider.html')
def render_banner_slider():
    banners = Banner.objects.filter(is_active=True)
    return {'banners': banners}


def _test_series_stats():
    """Live test-series numbers for the home page, cached for 10 minutes."""
    from django.core.cache import cache
    from django.urls import reverse
    from testseries.models import Question, Test, TestSeries

    stats = cache.get('home-test-series-stats')
    if stats is None:
        series = TestSeries.objects.filter(is_active=True)
        tests = Test.objects.filter(is_active=True, test_series__is_active=True, is_demo=False)
        exams = set(series.exclude(exam='').values_list('exam', flat=True).distinct())
        boards = set(series.exclude(board='').values_list('board', flat=True).distinct())
        stats = {
            'series': series.count(),
            'tests': tests.count(),
            'questions': Question.objects.filter(test__in=tests).count(),
            'exams': len(exams) + len(boards),
        }
        cache.set('home-test-series-stats', stats, 600)

    url = reverse('all_test_series')
    return [
        {'value': stats['series'], 'label': 'Test Series', 'icon': 'layer-group', 'color': '37, 99, 235', 'url': url},
        {'value': stats['tests'], 'label': 'Mock & Practice Tests', 'icon': 'file-pen', 'color': '234, 88, 12', 'url': url},
        {'value': stats['questions'], 'label': 'Questions with Solutions', 'icon': 'circle-question', 'color': '22, 163, 74', 'url': url},
        {'value': stats['exams'], 'label': 'Exams & Boards', 'icon': 'graduation-cap', 'color': '124, 58, 237', 'url': url},
    ]


def _indian_number(value):
    """12345678 -> '1,23,45,678' (Indian digit grouping, matching the counter animation)."""
    digits = str(int(value))
    if len(digits) <= 3:
        return digits
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return ','.join(([head] if head else []) + groups) + ',' + tail


@register.inclusion_tag('components/stats_section.html')
def render_stats_section():
    from django.urls import reverse
    stats = [dict(s, display=_indian_number(s['value'])) for s in _test_series_stats() if s['value']]
    return {'test_stats': stats, 'test_series_url': reverse('all_test_series')}

@register.inclusion_tag('components/cta_section.html')
def render_cta_section():
    cta_sections = CTASection.objects.filter(is_active=True)
    return {'cta_sections': cta_sections}

@register.inclusion_tag('components/about_us_section.html')
def render_about_us_section():
    about_us = AboutUsSection.objects.filter(is_active=True).first()
    why_choose_items = WhyChooseUsItem.objects.filter(is_active=True)
    service_items = ServiceItem.objects.filter(is_active=True)
    
    return {
        'about_us': about_us,
        'why_choose_items': why_choose_items,
        'service_items': service_items,
    }

@register.inclusion_tag('components/contact_section.html')
def render_contact_section():
    return {}


@register.inclusion_tag('components/footer_section.html', takes_context=True)
def render_footer_section(context):
    footer_settings = context.get('footer_settings')
    footer_links = context.get('footer_links', [])
    footer_legal_links = context.get('footer_legal_links', [])
    
    # Define footer sections for template
    footer_sections = [
        ('about', 'About'),
        ('help', 'Help'),
        ('student', 'Student'),
        ('business', 'Business'),
    ]
    
    return {
        'footer_settings': footer_settings,
        'footer_links': footer_links,
        'footer_legal_links': footer_legal_links,
        'footer_sections': footer_sections,
        'site_contact': context.get('site_contact', {}),
    }
