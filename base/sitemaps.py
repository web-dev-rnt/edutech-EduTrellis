from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from adminpanel.models import ExtraPage, ProductBundle
from elibrary.models import ELibraryCourse
from live_class.models import LiveClassCourse
from testseries.models import TestSeries
from video_courses.models import Category, VideoCourse


class CanonicalSitemap(Sitemap):
    """Emit URLs on settings.SITE_URL whatever host the sitemap is fetched from."""

    protocol = settings.SITE_URL.split("://", 1)[0]

    def get_domain(self, site=None):
        return settings.SITE_URL.split("://", 1)[1]


class StaticViewSitemap(CanonicalSitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ["home", "all_test_series"]

    def location(self, item):
        return reverse(item)


class VideoCourseSitemap(CanonicalSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return VideoCourse.objects.only("pk", "updated_at")

    def location(self, obj):
        return reverse("video_course_detail", args=[obj.pk])

    def lastmod(self, obj):
        return obj.updated_at


class LiveClassSitemap(CanonicalSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return LiveClassCourse.objects.filter(is_active=True).only("pk")

    def location(self, obj):
        return reverse("live_class_detail", args=[obj.pk])


class TestSeriesSitemap(CanonicalSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return TestSeries.objects.filter(is_active=True).only("pk", "updated_at")

    def location(self, obj):
        return reverse("front_exam_series_detail", args=[obj.pk])

    def lastmod(self, obj):
        return obj.updated_at


class ELibrarySitemap(CanonicalSitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ELibraryCourse.objects.filter(is_active=True).only("pk", "updated_at")

    def location(self, obj):
        return reverse("course_detail", args=[obj.pk])

    def lastmod(self, obj):
        return obj.updated_at


class BundleSitemap(CanonicalSitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ProductBundle.objects.filter(status="active").only("slug")

    def location(self, obj):
        return reverse("product_bundle_detail", args=[obj.slug])


class CategorySitemap(CanonicalSitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Category.objects.exclude(slug="").only("slug", "updated_at")

    def location(self, obj):
        return reverse("category_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class ExtraPageSitemap(CanonicalSitemap):
    priority = 0.3
    changefreq = "monthly"

    def items(self):
        return ExtraPage.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "video-courses": VideoCourseSitemap,
    "live-classes": LiveClassSitemap,
    "test-series": TestSeriesSitemap,
    "e-library": ELibrarySitemap,
    "bundles": BundleSitemap,
    "categories": CategorySitemap,
    "pages": ExtraPageSitemap,
}
