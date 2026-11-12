"""Per-series test and question counts for listing pages, computed in one query and cached.

Counting through tests -> questions with a JOIN for every listed series gets slow once there are 1.5 lakh questions,
so listings read these cached numbers instead. Any change to a test or question clears the cache.
"""
from django.core.cache import cache
from django.db.models import Count
from django.db.models.signals import post_delete, post_save

CACHE_KEY = 'series-counts-v1'
SUBJECTS_KEY = 'series-subject-options-v1'


def series_counts():
    """{series id: {'tests': paid tests, 'questions': paid questions, 'demos': demo tests}}."""
    counts = cache.get(CACHE_KEY)
    if counts is None:
        from testseries.models import Question, Test
        counts = {}
        for row in Test.objects.filter(is_active=True).values('test_series', 'is_demo').annotate(n=Count('id')).order_by():
            entry = counts.setdefault(row['test_series'], {'tests': 0, 'questions': 0, 'demos': 0})
            entry['demos' if row['is_demo'] else 'tests'] += row['n']
        for row in (Question.objects.filter(test__is_active=True, test__is_demo=False)
                    .values('test__test_series').annotate(n=Count('id')).order_by()):
            counts.setdefault(row['test__test_series'], {'tests': 0, 'questions': 0, 'demos': 0})['questions'] = row['n']
        cache.set(CACHE_KEY, counts, 60 * 30)
    return counts


def apply_counts(series_list):
    counts = series_counts()
    for series in series_list:
        entry = counts.get(series.pk, {})
        series.active_test_count = entry.get('tests', 0)
        series.active_question_count = entry.get('questions', 0)
        series.demo_count = entry.get('demos', 0)
    return series_list


def subject_options():
    """Subjects that appear in at least one active series, for the catalogue filter."""
    options = cache.get(SUBJECTS_KEY)
    if options is None:
        from testseries.models import Question, Subject
        ids = (Question.objects.filter(test__is_active=True, test__test_series__is_active=True)
               .values_list('subject_id', flat=True).distinct().order_by())
        options = list(Subject.objects.filter(pk__in=list(ids)).order_by('name'))
        cache.set(SUBJECTS_KEY, options, 60 * 30)
    return options


def clear(*args, **kwargs):
    cache.delete_many([CACHE_KEY, SUBJECTS_KEY])


def connect_signals():
    from testseries.models import Question, Test, TestSeries
    for model in (Question, Test, TestSeries):
        post_save.connect(clear, sender=model, dispatch_uid=f"series-counts-{model.__name__}-save")
        post_delete.connect(clear, sender=model, dispatch_uid=f"series-counts-{model.__name__}-delete")
