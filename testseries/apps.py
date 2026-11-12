from django.apps import AppConfig


class TestseriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testseries'

    def ready(self):
        from testseries.stats import connect_signals
        connect_signals()
