# ==================== DJANGO CORE IMPORTS ====================
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.mail import get_connection, send_mail
from django.contrib.staticfiles import finders
from django.db import transaction
from django.db.models import Count, Sum, Prefetch, Q, Avg, F, Max, Min
from django.core.exceptions import PermissionDenied
from django.core import signing
from django.http import (
    JsonResponse,
    FileResponse,
    HttpResponse,
    Http404,
    HttpResponseBadRequest
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

# ==================== THIRD PARTY IMPORTS ====================
import razorpay

# ==================== LOCAL APP IMPORTS ====================
from .forms import (
    EmailLoginForm,
    SignupForm,
    ProfileEditForm,
    PasswordChangeSimpleForm,
    OTPVerificationForm
)

from .models import User, OTPVerification, UserCourseAccess, Payment, Notification as UserNotification

from .utils import has_smtp_configured, create_and_send_otp
from .search import search as site_search, ranked_ids
from .daily_quiz import (CATEGORY_KEYS as DAILY_QUIZ_CATEGORIES, build_quiz, homepage_context as daily_quiz_context,
                         record_attempt as record_daily_quiz, today_state as daily_quiz_today, user_stats as daily_quiz_stats)
from .security import (
    clear_otp_failures, is_rate_limited, otp_locked, record_otp_failure, reset_rate_limit,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from video_courses.models import VideoCourse, Category
from live_class.models import LiveClassCourse, LiveClassSession, LiveClassRecording
from testseries.models import TestSeries, Test, TestAttempt, StudentAnswer, Subject, Question, marks_num
from testseries.stats import apply_counts, subject_options
from testseries.boards import CATEGORY_BOARD_CODES, STATE_BOARDS
from testseries.exam_tools import EXAM_GROUPS
from django.core.paginator import Paginator

from elibrary.models import (
    ELibraryCourse,
    ELibraryPDF,
    ELibraryEnrollment,
    ELibraryDownload
)

from adminpanel.models import (
    ProductBundle,
    Coupon,
    UserCoupon,
    SMTPConfiguration,
    RazorpayConfiguration,
    Notification as AdminNotification,
    ContactSubmission,
)

# ==================== OTHER IMPORTS ====================
import json
import requests
from urllib.parse import quote, urlencode, urlparse
from .context_processors import safe_next_url
from . import tutor
import os
import secrets
import string
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


@require_GET
@cache_control(private=True, max_age=300)
def dropbox_file_redirect(request, token):
    """Resolve a signed storage URL outside the page-rendering request."""
    try:
        file_name = signing.loads(token, salt="dropbox-media", max_age=4 * 60 * 60)
    except signing.BadSignature:
        raise Http404("File link is invalid or expired")

    from video_courses.dropbox_storage import DropboxStorage

    target_url = DropboxStorage().temporary_url(file_name)
    if not target_url:
        raise Http404("File is temporarily unavailable")
    return redirect(target_url)

@require_GET
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def service_worker(request):
    """Serve the service worker from root URL"""
    sw_path = finders.find('serviceworker.js')
    
    try:
        if not sw_path:
            raise FileNotFoundError
        with open(sw_path, 'r', encoding='utf-8') as sw_file:
            sw_content = sw_file.read()
            response = HttpResponse(sw_content, content_type='application/javascript; charset=utf-8')
            response['Service-Worker-Allowed'] = '/'
            return response
    except FileNotFoundError:
        return HttpResponse('Service worker not found', status=404, content_type='text/plain')

@require_GET
@cache_control(max_age=3600)  # Cache for 1 hour
def manifest(request):
    """Generate and serve the manifest.json dynamically"""
    
    # Build absolute URLs for icons
    def build_icon_url(filename):
        return request.build_absolute_uri(settings.STATIC_URL + f'img/{filename}')

    from adminpanel.branding import brand
    from adminpanel.models import ThemeSettings
    theme_color = ThemeSettings.get_solo().primary_color
    site_brand = brand()

    manifest_data = {
        "name": f"{site_brand['full_name']} - Complete Learning Platform",
        "short_name": site_brand['name'],
        "description": f"Prepare smarter with {site_brand['name']}: live online classes, video courses, mock test series, previous year papers and e-books.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": theme_color,
        "orientation": "portrait-primary",
        "categories": ["education", "learning", "productivity"],
        "lang": "en-IN",
        "dir": "ltr",
        
        # Icons - required for PWA
        "icons": [
            {
                "src": build_icon_url("icon-192.png"),
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": build_icon_url("icon-512.png"),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        
        # Shortcuts - quick actions from app icon (Android)
        "shortcuts": [
            {
                "name": "Video Courses",
                "short_name": "Courses",
                "description": "Browse all video courses",
                "url": "/#video-courses",
                "icons": [
                    {
                        "src": build_icon_url("icon-192.png"),
                        "sizes": "192x192",
                        "type": "image/png"
                    }
                ]
            },
            {
                "name": "Live Classes",
                "short_name": "Live",
                "description": "Join live classes",
                "url": "/#live-classes",
                "icons": [
                    {
                        "src": build_icon_url("icon-192.png"),
                        "sizes": "192x192",
                        "type": "image/png"
                    }
                ]
            },
            {
                "name": "Test Series",
                "short_name": "Tests",
                "description": "Take practice tests",
                "url": "/#test-series",
                "icons": [
                    {
                        "src": build_icon_url("icon-192.png"),
                        "sizes": "192x192",
                        "type": "image/png"
                    }
                ]
            },
            {
                "name": "E-Library",
                "short_name": "Library",
                "description": "Access digital books",
                "url": "/#e-library",
                "icons": [
                    {
                        "src": build_icon_url("icon-192.png"),
                        "sizes": "192x192",
                        "type": "image/png"
                    }
                ]
            }
        ],
        
        # Related applications - set to false to prefer PWA
        "prefer_related_applications": False,
        
        # Additional features
        "iarc_rating_id": "",  # Add if you have IARC rating
        "gcm_sender_id": "",   # Add if using push notifications later
    }
    
    return JsonResponse(manifest_data, json_dumps_params={'indent': 2})

ROBOTS_DISALLOW = [
    '/admin/', '/api/', '/payment/', '/exam/', '/pdf/', '/dropbox-file/',
    '/my_purchases/', '/my_results/', '/my-library/', '/my-coupons/', '/profile/',
    '/notifications/', '/search/', '/login', '/signup_user', '/verify-otp/',
    '/resend-otp/', '/forgot-password/', '/verify-reset-otp/', '/reset-password/',
    '/offline/',
]

@require_GET
@cache_control(max_age=86400)
def robots_txt(request):
    """robots.txt pointing crawlers at the sitemap and away from private pages."""
    lines = ['User-agent: *', 'Allow: /']
    lines += [f'Disallow: {path}' for path in ROBOTS_DISALLOW]
    lines += ['', f'Sitemap: {settings.SITE_URL}/sitemap.xml', '']
    return HttpResponse('\n'.join(lines), content_type='text/plain')

@require_GET
def offline(request):
    """Offline fallback page"""
    return render(request, 'offline.html')


def extra_page_detail(request, slug):
    """Render an admin-managed static page (Privacy Policy, Disclaimer, Refund Policy, Contact Us, etc.)"""
    from adminpanel.models import ExtraPage
    from django.shortcuts import get_object_or_404
    page = get_object_or_404(ExtraPage, slug=slug, is_active=True)
    return render(request, 'extra_page_detail.html', {'page': page})


@require_POST
def contact_submit(request):
    """Handle the homepage 'Contact Us' lead form."""
    name = request.POST.get('name', '').strip()[:120]
    email = request.POST.get('email', '').strip()[:254]
    phone = request.POST.get('phone', '').strip()[:20]
    subject = request.POST.get('subject', '').strip()[:200]
    message_text = request.POST.get('message', '').strip()[:5000]

    if not name or not email or not message_text:
        messages.error(request, 'Please fill in your name, email and message.')
        return redirect(f"{reverse('home')}#contact-us")
    try:
        from django.core.validators import validate_email
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
        return redirect(f"{reverse('home')}#contact-us")
    if is_rate_limited(request, 'contact', limit=5, window=60 * 60):
        messages.error(request, 'You have sent several messages already. Please try again later.')
        return redirect(f"{reverse('home')}#contact-us")

    ContactSubmission.objects.create(
        name=name, email=email, phone=phone, subject=subject, message=message_text
    )
    messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
    return redirect(f"{reverse('home')}#contact-us")


#notifications views 
@login_required
def notifications_list(request):
    """Get user notifications with filtering - includes both user-specific and admin broadcast notifications"""
    # Get filter parameters
    filter_type = request.GET.get('type', 'all')
    show_read = request.GET.get('show_read', 'false') == 'true'
    
    # === USER-SPECIFIC NOTIFICATIONS ===
    notifications_query = request.user.notifications.all()
    
    # Apply filters
    if not show_read:
        notifications_query = notifications_query.filter(is_read=False)
    
    if filter_type != 'all':
        notifications_query = notifications_query.filter(notification_type=filter_type)
    
    # Exclude expired notifications
    notifications_query = notifications_query.exclude(
        expires_at__lt=timezone.now()
    )
    
    # Get user notifications
    user_notifications = list(notifications_query[:20])
    
    # === ADMIN BROADCAST NOTIFICATIONS ===
    # Get active admin notifications that are scheduled to show
    admin_notifications_qs = AdminNotification.objects.filter(
        is_active=True,
        scheduled_time__lte=timezone.now()
    )
    if not show_read:
        admin_notifications_qs = admin_notifications_qs.exclude(read_by=request.user)
    admin_notifications = list(admin_notifications_qs.order_by('-scheduled_time')[:10])

    # IDs this user has already read, so is_read can be reported per-user
    read_admin_ids = set(
        AdminNotification.objects.filter(
            is_active=True, scheduled_time__lte=timezone.now(), read_by=request.user
        ).values_list('id', flat=True)
    )

    # === CALCULATE UNREAD COUNT ===
    # Count user-specific unread notifications
    user_unread_count = request.user.notifications.filter(
        is_read=False
    ).exclude(
        expires_at__lt=timezone.now()
    ).count()

    # Count admin notifications this user hasn't read yet
    admin_unread_count = AdminNotification.objects.filter(
        is_active=True,
        scheduled_time__lte=timezone.now()
    ).exclude(read_by=request.user).count()

    # Total unread count (user notifications + admin notifications)
    total_unread_count = user_unread_count + admin_unread_count
    
    # Combine and format notifications
    notification_data = []
    
    # Add user-specific notifications
    for notification in user_notifications:
        notification_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'link': notification.link,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime('%b %d, %Y at %I:%M %p'),
            'type': notification.notification_type,
            'priority': notification.priority,
            'source': 'user',  # Mark as user-specific notification
            'is_admin': False
        })
    
    # Add admin broadcast notifications
    for notification in admin_notifications:
        notification_data.append({
            'id': f'admin_{notification.id}',
            'title': notification.title,
            'message': notification.body,
            'link': notification.link or '#',
            'is_read': notification.id in read_admin_ids,
            'created_at': notification.scheduled_time.strftime('%b %d, %Y at %I:%M %p'),
            'type': 'announcement',  # Set type as announcement
            'priority': 'high',
            'source': 'admin',  # Mark as admin notification
            'is_admin': True
        })
    
    # Sort combined notifications by creation date (newest first)
    notification_data.sort(
        key=lambda x: timezone.datetime.strptime(x['created_at'], '%b %d, %Y at %I:%M %p'),
        reverse=True
    )
    
    # Limit to 20 total notifications
    notification_data = notification_data[:20]
    
    return JsonResponse({
        'notifications': notification_data,
        'unread_count': total_unread_count,  # This now includes both user and admin notifications
        'user_unread_count': user_unread_count,
        'admin_unread_count': admin_unread_count,
        'total_count': len(notification_data)
    })

@login_required
def mark_notification_read(request, notification_id):
    """Mark a user-specific or admin broadcast notification as read"""
    if request.method == 'POST':
        try:
            if str(notification_id).startswith('admin_'):
                admin_id = str(notification_id).split('_', 1)[1]
                admin_notification = get_object_or_404(AdminNotification, id=admin_id)
                admin_notification.read_by.add(request.user)
            else:
                notification = get_object_or_404(
                    UserNotification,
                    id=notification_id,
                    user=request.user
                )
                notification.mark_as_read()

            # Recalculate total unread count
            user_unread = request.user.notifications.filter(
                is_read=False
            ).exclude(
                expires_at__lt=timezone.now()
            ).count()

            # Count admin notifications this user hasn't read yet
            admin_unread = AdminNotification.objects.filter(
                is_active=True,
                scheduled_time__lte=timezone.now()
            ).exclude(read_by=request.user).count()

            total_unread = user_unread + admin_unread

            return JsonResponse({
                'status': 'success',
                'unread_count': total_unread
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)

@login_required
def mark_all_notifications_read(request):
    """Mark all user-specific and currently visible admin broadcast notifications as read"""
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)

        active_admin_notifications = AdminNotification.objects.filter(
            is_active=True,
            scheduled_time__lte=timezone.now()
        ).exclude(read_by=request.user)
        for notification in active_admin_notifications:
            notification.read_by.add(request.user)

        return JsonResponse({
            'status': 'success',
            'unread_count': 0
        })
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request'
    }, status=400)

@login_required
def delete_notification(request, notification_id):
    """Delete a specific user notification"""
    if request.method == 'POST':
        try:
            # Check if it's an admin notification (can't delete)
            if str(notification_id).startswith('admin_'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Admin notifications cannot be deleted'
                }, status=400)
            
            notification = get_object_or_404(
                UserNotification, 
                id=notification_id, 
                user=request.user
            )
            notification.delete()

            # Recalculate total unread count
            user_unread = request.user.notifications.filter(
                is_read=False
            ).exclude(
                expires_at__lt=timezone.now()
            ).count()

            # Count admin notifications this user hasn't read yet
            admin_unread = AdminNotification.objects.filter(
                is_active=True,
                scheduled_time__lte=timezone.now()
            ).exclude(read_by=request.user).count()

            total_unread = user_unread + admin_unread

            return JsonResponse({
                'status': 'success',
                'unread_count': total_unread
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)

@login_required
def clear_all_notifications(request):
    """Clear all read user notifications"""
    if request.method == 'POST':
        request.user.notifications.filter(is_read=True).delete()

        # Recalculate total unread count
        user_unread = request.user.notifications.filter(
            is_read=False
        ).exclude(
            expires_at__lt=timezone.now()
        ).count()

        # Count admin notifications this user hasn't read yet
        admin_unread = AdminNotification.objects.filter(
            is_active=True,
            scheduled_time__lte=timezone.now()
        ).exclude(read_by=request.user).count()

        total_unread = user_unread + admin_unread
        
        return JsonResponse({
            'status': 'success',
            'unread_count': total_unread
        })
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request'
    }, status=400)

@login_required
def my_purchases(request):
    """
    Display all purchased products for the authenticated user.
    """
    user = request.user
    
    # Get all active course access records for the user
    course_access_records = UserCourseAccess.objects.filter(
        user=user,
        is_active=True
    ).select_related('payment').order_by('-access_granted_at')
    
    # Organize purchases by type
    purchases = {
        'video_courses': [],
        'live_classes': [],
        'test_series': [],
        'elibrary_courses': [],
        'bundles': []
    }
    
    # Collect IDs by type
    video_course_ids = []
    live_class_ids = []
    test_series_ids = []
    elibrary_ids = []
    bundle_ids = []
    
    for access in course_access_records:
        if access.course_type == 'video_course':
            video_course_ids.append(access.course_id)
        elif access.course_type == 'live_class':
            live_class_ids.append(access.course_id)
        elif access.course_type == 'test_series':
            test_series_ids.append(access.course_id)
        elif access.course_type == 'elibrary':
            elibrary_ids.append(access.course_id)
        elif access.course_type == 'bundle':
            bundle_ids.append(access.course_id)
    
    # Fetch actual course objects
    if video_course_ids:
        from video_courses.models import VideoCourse
        video_courses = VideoCourse.objects.filter(id__in=video_course_ids)
        # Create a mapping for quick lookup
        video_courses_dict = {vc.id: vc for vc in video_courses}
        
        for access_record in course_access_records:
            if access_record.course_type == 'video_course':
                course = video_courses_dict.get(access_record.course_id)
                if course:  # Only add if course exists
                    purchases['video_courses'].append({
                        'course': course,
                        'access_granted': access_record.access_granted_at,
                        'payment': access_record.payment,
                        'expires_at': access_record.expires_at,
                    })
    
    if live_class_ids:
        from live_class.models import LiveClassCourse
        live_classes = LiveClassCourse.objects.filter(id__in=live_class_ids)
        live_classes_dict = {lc.id: lc for lc in live_classes}
        
        for access_record in course_access_records:
            if access_record.course_type == 'live_class':
                course = live_classes_dict.get(access_record.course_id)
                if course:
                    purchases['live_classes'].append({
                        'course': course,
                        'access_granted': access_record.access_granted_at,
                        'payment': access_record.payment,
                        'expires_at': access_record.expires_at,
                    })
    
    if test_series_ids:
        test_series = TestSeries.objects.filter(id__in=test_series_ids)
        test_series_dict = {ts.id: ts for ts in test_series}
        
        for access_record in course_access_records:
            if access_record.course_type == 'test_series':
                course = test_series_dict.get(access_record.course_id)
                if course:
                    purchases['test_series'].append({
                        'course': course,
                        'access_granted': access_record.access_granted_at,
                        'payment': access_record.payment,
                        'expires_at': access_record.expires_at,
                    })
    
    if elibrary_ids:
        from elibrary.models import ELibraryCourse
        elibrary_courses = ELibraryCourse.objects.filter(id__in=elibrary_ids)
        elibrary_dict = {ec.id: ec for ec in elibrary_courses}
        
        for access_record in course_access_records:
            if access_record.course_type == 'elibrary':
                course = elibrary_dict.get(access_record.course_id)
                if course:
                    purchases['elibrary_courses'].append({
                        'course': course,
                        'access_granted': access_record.access_granted_at,
                        'payment': access_record.payment,
                        'expires_at': access_record.expires_at,
                    })
    
    if bundle_ids:
        bundles = ProductBundle.objects.filter(id__in=bundle_ids)
        bundles_dict = {b.id: b for b in bundles}
        
        for access_record in course_access_records:
            if access_record.course_type == 'bundle':
                bundle = bundles_dict.get(access_record.course_id)
                if bundle:
                    purchases['bundles'].append({
                        'course': bundle,
                        'access_granted': access_record.access_granted_at,
                        'payment': access_record.payment,
                        'expires_at': access_record.expires_at,
                    })
    
    # Calculate total spent
    total_spent = sum(
        access.payment.amount / 100 if access.payment else 0 
        for access in course_access_records
    )
    
    # Count total purchases
    total_purchases = len(course_access_records)
    
    context = {
        'purchases': purchases,
        'total_spent': total_spent,
        'total_purchases': total_purchases,
    }
    
    return render(request, 'my_purchases.html', context)


@login_required
def my_test_results(request):
    """
    Show every test attempt (submitted or in-progress) for the logged-in student,
    with their score/result for each one.
    """
    attempts = TestAttempt.objects.filter(
        user=request.user
    ).select_related('test', 'test__test_series').order_by('-created_at')

    submitted_attempts = attempts.filter(status='submitted')
    total_attempts = submitted_attempts.count()
    passed_count = submitted_attempts.filter(passed=True).count()
    average_percentage = submitted_attempts.aggregate(avg=Avg('percentage_score'))['avg'] or 0

    context = {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'passed_count': passed_count,
        'average_percentage': average_percentage,
        'quiz': daily_quiz_stats(request.user),
    }
    return render(request, 'my_results.html', context)


SCHOOL_BOARD_COLORS = {'cbse': '#2563eb', 'icse': '#7c3aed', 'up': '#ea580c', 'nios': '#0d9488'}
BOARD_SHORT_NAMES = {'cbse': 'CBSE', 'icse': 'ICSE', 'up': 'UP Board', **{b.code: b.category for b in STATE_BOARDS}}


def _apply_series_cover(series_list):
    """
    Give each series what its card cover shows when it has no thumbnail:
    an icon and colour (from its exam's category, or its board) plus kicker/title/subtitle text.
    """
    exam_style = {
        name: (icon or 'file-lines', color or '#667eea')
        for name, icon, color in Category.objects.filter(
            name__in={s.exam for s in series_list if s.exam}
        ).values_list('name', 'icon', 'icon_color')
    }
    stream_labels = dict(TestSeries.STREAM_CHOICES)
    for series in series_list:
        if series.board:
            series.icon = 'school'
            series.color = SCHOOL_BOARD_COLORS.get(series.board, '#0d9488')
            series.cover_kicker = BOARD_SHORT_NAMES.get(series.board, series.get_board_display())
            series.cover_title = f"Class {series.grade}" if series.grade else 'Board Exam'
            series.cover_sub = stream_labels.get(series.stream, '')
        elif series.exam:
            series.icon, series.color = exam_style.get(series.exam, ('file-lines', '#667eea'))
            series.cover_kicker = 'Exam Pattern Mock'
            series.cover_title = series.exam
            series.cover_sub = ''
        else:
            series.icon, series.color = 'file-lines', '#667eea'
            series.cover_kicker = 'Test Series'
            series.cover_title = series.title
            series.cover_sub = ''


def _series_cards(queryset, user):
    """Test series ready for the shared card: paid-test counts, demo flag, cover, price and purchase status."""
    series_list = apply_counts(list(queryset))
    purchased = set()
    if user.is_authenticated:
        purchased = set(
            UserCourseAccess.objects.filter(user=user, course_type='test_series', is_active=True)
            .values_list('course_id', flat=True)
        )
    _apply_series_cover(series_list)
    for series in series_list:
        series.is_purchased = series.id in purchased
        series.price_display = "Free" if series.is_free else f"₹{series.price:,.0f}"
    return series_list


def _test_series_directory(purchased_ids):
    """
    Every active test series grouped into tabs for the home page directory:
    CBSE/ICSE/UP Board by class, state boards as a board x class table, then exam groups.
    """
    series_list = apply_counts(list(
        TestSeries.objects.filter(is_active=True)
        .only('id', 'title', 'board', 'grade', 'stream', 'exam', 'is_free', 'price', 'difficulty')
        .order_by('grade', 'stream', 'title')
    ))
    if not series_list:
        return []

    _apply_series_cover(series_list)
    board_labels = dict(TestSeries.BOARD_CHOICES)
    for series in series_list:
        series.is_purchased = series.id in purchased_ids
        series.price_display = "Free" if series.is_free else f"₹{series.price:,.0f}"

    tabs = []

    # CBSE, ICSE, UP Board and NIOS: one row of class boxes per board.
    main_sections = []
    for code in SCHOOL_BOARD_COLORS:
        items = [s for s in series_list if s.board == code]
        if items:
            main_sections.append({
                'title': board_labels[code],
                'color': SCHOOL_BOARD_COLORS[code],
                'url': f"{reverse('all_test_series')}?board={code}",
                'items': items,
            })
    if main_sections:
        tabs.append({
            'key': 'school', 'label': 'School Boards', 'icon': 'school', 'layout': 'boards',
            'sections': main_sections, 'count': sum(len(s['items']) for s in main_sections),
        })

    # Every other board: one table row per board, one cell per class.
    state_rows = {}
    for series in series_list:
        if series.board and series.board not in SCHOOL_BOARD_COLORS:
            state_rows.setdefault(series.board, []).append(series)
    if state_rows:
        board_order = [code for code, _ in TestSeries.BOARD_CHOICES]
        rows = [
            {
                'title': board_labels.get(code, code),
                'url': f"{reverse('all_test_series')}?board={code}",
                'items': state_rows[code],
            }
            for code in sorted(state_rows, key=board_order.index)
        ]
        tabs.append({
            'key': 'state', 'label': 'State Boards', 'icon': 'book-open-reader', 'layout': 'table',
            'rows': rows, 'count': sum(len(r['items']) for r in rows),
        })

    # Competitive exams, in the order EXAM_GROUPS lists them.
    by_exam = {}
    for series in series_list:
        if not series.board and series.exam:
            by_exam.setdefault(series.exam, []).append(series)
    grouped = set()
    for key, label, icon, exams in EXAM_GROUPS:
        items = [s for exam in exams for s in by_exam.get(exam, [])]
        grouped.update(exams)
        if items:
            tabs.append({'key': key, 'label': label, 'icon': icon, 'layout': 'grid', 'items': items, 'count': len(items)})

    others = [
        s for s in series_list
        if not s.board and (not s.exam or s.exam not in grouped)
    ]
    if others:
        tabs.append({'key': 'more', 'label': 'More', 'icon': 'layer-group', 'layout': 'grid', 'items': others, 'count': len(others)})

    return tabs


def home(request):
    """
    Homepage view with AGGRESSIVE deduplication and purchase status.
    No prefetch_related or select_related on problematic models.
    """
    now = timezone.now()
    user = request.user

    # Fetch the category in the same query because cards display it.
    video_courses = list(
        VideoCourse.objects
        .select_related("category")
        .order_by('-created_at')[:10]
    )
    
    # Get user's purchased video courses if authenticated
    purchased_video_course_ids = set()
    if user.is_authenticated:
        purchased_video_course_ids = set(
            UserCourseAccess.objects
            .filter(
                user=user,
                course_type='video_course',
                is_active=True
            )
            .values_list('course_id', flat=True)
        )
    
    # Additional Python-level deduplication
    seen_vc_ids = set()
    unique_video_courses = []
    for vc in video_courses:
        if vc.id not in seen_vc_ids:
            seen_vc_ids.add(vc.id)
            vc.original_price_display = f"{vc.original_price:.2f}"
            vc.selling_price_display = f"{vc.selling_price:.2f}"
            # Check if user has purchased this course
            vc.is_purchased = vc.id in purchased_video_course_ids
            unique_video_courses.append(vc)
    
    video_courses = unique_video_courses

    upcoming_sessions_query = LiveClassSession.objects.filter(
        scheduled_datetime__gte=now
    ).order_by("scheduled_datetime")

    live_classes = list(
        LiveClassCourse.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            Prefetch(
                "sessions",
                queryset=upcoming_sessions_query,
                to_attr="upcoming_sessions_list",
            )
        )
        .order_by('-created_at')[:10]
    )
    
    # Get user's purchased live classes if authenticated
    purchased_live_class_ids = set()
    if user.is_authenticated:
        purchased_live_class_ids = set(
            UserCourseAccess.objects
            .filter(
                user=user,
                course_type='live_class',
                is_active=True
            )
            .values_list('course_id', flat=True)
        )
    
    # Additional Python-level deduplication + fetch sessions separately
    seen_lc_ids = set()
    unique_live_classes = []
    
    for course in live_classes:
        if course.id not in seen_lc_ids:
            seen_lc_ids.add(course.id)
            
            course.next_sessions = course.upcoming_sessions_list[:2]
            
            # Handle pricing display based on is_free field
            if course.is_free:
                course.original_price_display = "0.00"
                course.current_price_display = "FREE"
                course.price_display_text = "FREE"
                course.show_price_strike = False
            else:
                course.original_price_display = f"{course.original_price:.2f}"
                course.current_price_display = f"{course.current_price:.2f}"
                course.price_display_text = f"₹{course.current_price:.2f}"
                course.show_price_strike = course.original_price != course.current_price
            
            course.language_display = course.language
            # Check if user has purchased this course
            course.is_purchased = course.id in purchased_live_class_ids
            
            if course.about:
                course.about_short = (
                    course.about[:140] + '...' if len(course.about) > 140 else course.about
                )
            else:
                course.about_short = ""
            
            unique_live_classes.append(course)
    
    live_classes = unique_live_classes

    # ===== Test Series (Keep as is - working correctly) ===== 
    test_series = list(
        TestSeries.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                'tests',
                queryset=Test.objects
                .filter(is_active=True)
                .annotate(
                    question_count=Count('questions', distinct=True),
                    total_marks_sum=Sum('questions__marks')
                ),
                to_attr='active_tests_list'
            )
        )
        .order_by('-created_at')[:10]
    )
    
    # Get user's purchased test series if authenticated
    purchased_test_series_ids = set()
    if user.is_authenticated:
        purchased_test_series_ids = set(
            UserCourseAccess.objects
            .filter(
                user=user,
                course_type='test_series',
                is_active=True
            )
            .values_list('course_id', flat=True)
        )

    for series in test_series:
        # Demo tests repeat paid questions, so they count as free tests but not towards the totals.
        paid = [test for test in series.active_tests_list if not test.is_demo]
        series.total_tests = len(paid)
        series.total_questions = sum(test.question_count for test in paid)
        series.total_marks = marks_num(sum(test.total_marks_sum or 0 for test in paid))
        series.free_tests = (
            len(series.active_tests_list) if series.is_free
            else len(series.active_tests_list) - len(paid)
        )
        series.user_count = 0
        series.price_display = "FREE" if series.is_free else f"₹{series.price:,.0f}"
        # Check if user has purchased this test series
        series.is_purchased = series.id in purchased_test_series_ids
    _apply_series_cover(test_series)

        
    elibrary_courses = list(
        ELibraryCourse.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by('-created_at')[:10]
    )
    
    # Get user's purchased elibrary courses if authenticated
    purchased_elibrary_ids = set()
    if user.is_authenticated:
        purchased_elibrary_ids = set(
            UserCourseAccess.objects
            .filter(
                user=user,
                course_type='elibrary',
                is_active=True
            )
            .values_list('course_id', flat=True)
        )
    
    # Additional Python-level deduplication
    seen_el_ids = set()
    unique_elibrary = []
    
    for course in elibrary_courses:
        if course.id not in seen_el_ids:
            seen_el_ids.add(course.id)
            course.price_display = f"₹{course.current_price:.2f}"
            # Check if user has purchased this course
            course.is_purchased = course.id in purchased_elibrary_ids
            
            if hasattr(course, 'short_description') and course.short_description:
                course.short_desc = (
                    course.short_description[:100] + '...' 
                    if len(course.short_description) > 100 
                    else course.short_description
                )
            else:
                course.short_desc = ""
            
            unique_elibrary.append(course)
    
    elibrary_courses = unique_elibrary
    
    # ===== Product Bundles (WITH PURCHASE STATUS) ===== 
    product_bundles = list(
        ProductBundle.objects
        .filter(status='active')
        .prefetch_related(
            Prefetch('video_courses', to_attr='video_courses_list'),
            Prefetch('live_classes', to_attr='live_classes_list'),
            Prefetch('test_series', to_attr='test_series_list'),
            Prefetch('elibrary_courses', to_attr='elibrary_courses_list')
        )
        .order_by('display_order', '-created_at')[:6]
    )
    
    # Get user's purchased bundles if authenticated
    purchased_bundle_ids = set()
    if user.is_authenticated:
        purchased_bundle_ids = set(
            UserCourseAccess.objects
            .filter(
                user=user,
                course_type='bundle',
                is_active=True
            )
            .values_list('course_id', flat=True)
        )
    
    for bundle in product_bundles:
        bundle.discount_percent = bundle.discount_percentage
        bundle.savings = bundle.original_price - bundle.bundle_price
        # Check if user has purchased this bundle
        bundle.is_purchased = bundle.id in purchased_bundle_ids
        
        if hasattr(bundle, 'features') and bundle.features:
            features_list = [f.strip() for f in bundle.features.split('\n') if f.strip()]
            bundle.features_list = features_list[:3]
        else:
            bundle.features_list = []
            
        bundle.price_display = f"{bundle.bundle_price:.2f}"
        bundle.original_price_display = f"{bundle.original_price:.2f}"
    
    # Daily Quiz: a fresh set every day, generated from the test-series question engine.
    try:
        daily_quiz = daily_quiz_context(request.user)
    except Exception:  # never let the quiz take the homepage down
        logger.exception("Daily quiz could not be built")
        daily_quiz = None

    # ===== Build Context =====
    context = {
        'daily_quiz': daily_quiz,
        'live_classes': live_classes,
        'video_courses': video_courses,
        'test_series': test_series,
        'test_series_directory': _test_series_directory(purchased_test_series_ids),
        'featured_courses': elibrary_courses,
        'product_bundles': product_bundles,
        'now': now,
    }
    
    return render(request, 'base.html', context)


def _daily_quiz_login_required(request):
    return JsonResponse(
        {'error': 'login_required', 'login_url': _login_url_with_next('/#daily-quiz')},
        status=401,
    )


@require_GET
def daily_quiz_api(request, category):
    """Today's Daily Quiz for one category, as JSON for the homepage widget (logged-in students only)."""
    if category not in DAILY_QUIZ_CATEGORIES:
        raise Http404("Unknown quiz category")
    if not request.user.is_authenticated:
        return _daily_quiz_login_required(request)
    response = JsonResponse(build_quiz(timezone.localdate(), category))
    response['Cache-Control'] = 'private, max-age=600'
    return response


@require_POST
def daily_quiz_submit(request, category):
    """Score a finished Daily Quiz on the server and save it to the student's history."""
    if category not in DAILY_QUIZ_CATEGORIES:
        raise Http404("Unknown quiz category")
    if not request.user.is_authenticated:
        return _daily_quiz_login_required(request)
    if is_rate_limited(request, 'daily-quiz-submit', limit=200, window=60 * 60, extra_ident=request.user.pk):
        return JsonResponse({'error': 'Too many attempts. Please try again later.'}, status=429)
    try:
        picks = json.loads(request.body or b'{}').get('picks')
        attempt = record_daily_quiz(request.user, category, picks if isinstance(picks, list) else [])
    except (ValueError, AttributeError):
        return JsonResponse({'error': 'Invalid answers.'}, status=400)
    return JsonResponse({
        'score': attempt.latest_score,
        'first_score': attempt.score,
        'best': attempt.best_score,
        'total': attempt.total,
        'attempts': attempt.attempts,
        **daily_quiz_today(request.user),
    })


def product_bundle_detail(request, slug):
    """Display detailed view of a specific product bundle with purchase status"""
    try:
        bundle = get_object_or_404(
            ProductBundle.objects.prefetch_related(
                'video_courses',
                'live_classes',
                'test_series',
                'elibrary_courses',
                'category'
            ),
            slug=slug
            # Removed status='active' filter to debug
        )
        
        # DEBUG: Log bundle status
        logger.info(f"Bundle: {bundle.title}")
        logger.info(f"Status: {bundle.status}")
        logger.info(f"is_available: {bundle.is_available}")
        
        # DEBUG: Check why not available
        now = timezone.now().date()
        if bundle.start_date:
            logger.info(f"Start date: {bundle.start_date}, Today: {now}, Start in future: {now < bundle.start_date}")
        if bundle.end_date:
            logger.info(f"End date: {bundle.end_date}, Today: {now}, Ended: {now > bundle.end_date}")
        if bundle.max_enrollments:
            logger.info(f"Max enrollments: {bundle.max_enrollments}, Current: {bundle.current_enrollments}")
        
        # Increment view count
        bundle.total_views += 1
        bundle.save(update_fields=['total_views'])
        
        # Get all products in the bundle
        video_courses = bundle.video_courses.all()
        live_classes = bundle.live_classes.all()
        test_series_list = bundle.test_series.prefetch_related('tests__questions').all()
        elibrary_courses = bundle.elibrary_courses.all()
        
        # Calculate test series stats
        for series in test_series_list:
            active_tests = series.tests.filter(is_active=True)
            series.total_tests = active_tests.count()
            series.total_questions = sum(test.questions.count() for test in active_tests)
        
        # ===== DEFAULT CONTEXT =====
        context = {
            'bundle': bundle,
            'video_courses': video_courses,
            'live_classes': live_classes,
            'test_series_list': test_series_list,
            'elibrary_courses': elibrary_courses,
            'discount_percent': bundle.discount_percentage,
            'savings': bundle.savings_amount,
            'features_list': bundle.get_features_list(),
            'is_available': bundle.is_available,
            'price_display': f"₹{bundle.bundle_price:.2f}" if not bundle.is_free else "FREE",
            'original_price_display': f"₹{bundle.original_price:.2f}",
            # Purchase status
            'has_access': False,
            'is_purchased': False,
            'user_has_bundle': False,
            'access_expires_at': None,
        }
        
        # ===== CHECK USER PURCHASE STATUS =====
        if request.user.is_authenticated:
            try:
                # Check UserCourseAccess for bundle purchase
                access = UserCourseAccess.objects.get(
                    user=request.user,
                    course_id=bundle.id,
                    course_type='bundle'
                )
                
                # Check if access is still valid using the @property method
                if access.has_access:
                    context['has_access'] = True
                    context['is_purchased'] = True
                    context['user_has_bundle'] = True
                    context['access_expires_at'] = access.expires_at
                    
                    logger.info(f"User {request.user.id} has active access to bundle {bundle.id}")
                else:
                    # Access expired
                    context['has_access'] = False
                    context['is_purchased'] = False
                    context['user_has_bundle'] = False
                    
                    logger.info(f"User {request.user.id} access to bundle {bundle.id} has expired")
                    
            except UserCourseAccess.DoesNotExist:
                # User hasn't purchased this bundle
                context['has_access'] = False
                context['is_purchased'] = False
                context['user_has_bundle'] = False
                
                logger.info(f"User {request.user.id} has not purchased bundle {bundle.id}")
        
        return render(request, 'bundles/product_bundle_detail.html', context)
    
    except ProductBundle.DoesNotExist:
        raise Http404("Bundle not found")


def _has_test_series_access(user, series):
    """Free series, or a live purchase of the series itself or of a bundle that includes it."""
    if series.is_free:
        return True
    if not user.is_authenticated:
        return False
    live = UserCourseAccess.objects.filter(user=user, is_active=True).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
    )
    return live.filter(
        Q(course_type='test_series', course_id=series.pk)
        | Q(course_type='bundle', course_id__in=series.bundles.values('pk'))
    ).exists()


def test_series_detail(request, pk):
    """Test series page: pattern, syllabus coverage, every test with its marking scheme and the student's attempts."""
    test_series = get_object_or_404(TestSeries, pk=pk, is_active=True)
    _apply_series_cover([test_series])

    tests = list(
        test_series.tests.filter(is_active=True).annotate(
            q_count=Count('questions'),
            marks_sum=Sum('questions__marks'),
            max_penalty=Max('questions__negative_marks'),
            min_marks=Min('questions__marks'),
            max_marks=Max('questions__marks'),
            easy_count=Count('questions', filter=Q(questions__difficulty='easy')),
            medium_count=Count('questions', filter=Q(questions__difficulty='medium')),
            hard_count=Count('questions', filter=Q(questions__difficulty='hard')),
        )
    )

    # The free demo is listed first, then full mocks, subject tests and previous year papers; paid tests are numbered from 1.
    type_order = [key for key, _ in Test.PAPER_TYPES]
    tests.sort(key=lambda t: (not t.is_demo, type_order.index(t.paper_type) if t.paper_type in type_order else 0))
    has_access = _has_test_series_access(request.user, test_series)
    paid_tests = [t for t in tests if not t.is_demo]
    demo_ids = {t.id for t in tests if t.is_demo}

    # Questions and marks per subject, for each test's section list and the series' coverage table.
    section_rows = (
        Question.objects.filter(test__in=tests)
        .values('test_id', 'subject__name', 'subject__color', 'subject__icon')
        .annotate(questions=Count('id'), marks=Sum('marks'))
        .order_by('test_id', 'subject__name')
    )
    sections_by_test = {}
    coverage = {}
    for row in section_rows:
        name = row['subject__name'] or 'General'
        sections_by_test.setdefault(row['test_id'], []).append({'name': name, 'questions': row['questions']})
        if row['test_id'] in demo_ids:
            continue  # demo questions are copies of paid ones
        subject = coverage.setdefault(name, {
            'name': name, 'color': row['subject__color'] or '#6b7280', 'icon': row['subject__icon'],
            'questions': 0, 'marks': 0, 'tests': 0,
        })
        subject['questions'] += row['questions']
        # marks_num() may return a float (e.g. 199.5 for 1.33-mark questions), so add as floats, not float + Decimal.
        subject['marks'] = marks_num(float(subject['marks']) + float(row['marks'] or 0))
        subject['tests'] += 1

    attempts_by_test = {}
    if request.user.is_authenticated:
        for attempt in TestAttempt.objects.filter(user=request.user, test__in=tests, status='submitted').order_by('-submitted_at'):
            attempts_by_test.setdefault(attempt.test_id, []).append(attempt)

    for test in tests:
        test.question_count = test.q_count
        test.total_marks = marks_num(test.marks_sum)
        test.sections = sections_by_test.get(test.id, [])
        test.penalty = test.max_penalty if test_series.has_negative_marking and test.max_penalty else 0
        test.marks_range = (
            f"{marks_num(test.min_marks)}" if test.min_marks == test.max_marks else f"{marks_num(test.min_marks)}–{marks_num(test.max_marks)}"
        ) if test.question_count else ''
        test.unlocked = has_access or test.is_demo
        attempts = attempts_by_test.get(test.id, [])
        test.user_attempts = len(attempts)
        test.can_attempt = test.user_attempts < test.max_attempts
        test.last_attempt = attempts[0] if attempts else None
        best = max(attempts, key=lambda a: a.marks_obtained) if attempts else None
        test.best_score = best.marks_obtained if best else None
        test.best_percentage = best.percentage_score if best else None

    for number, test in enumerate(paid_tests, start=1):
        test.number = number

    total_questions = sum(t.question_count for t in paid_tests)
    total_marks = sum(t.total_marks for t in paid_tests)
    attempted_tests = sum(1 for t in tests if t.user_attempts)

    # The real exam's pattern is kept on its 'Explore Exams' category.
    exam_category = Category.objects.filter(name=test_series.exam).first() if test_series.exam else None

    related = TestSeries.objects.filter(is_active=True).exclude(pk=test_series.pk)
    if test_series.board:
        related = related.filter(board=test_series.board).order_by('grade', 'stream')
    elif test_series.exam:
        group = next((exams for _, _, _, exams in EXAM_GROUPS if test_series.exam in exams), [])
        related = related.filter(exam__in=group)
    else:
        related = related.order_by('-created_at')
    related = list(related[:6])
    _apply_series_cover(related)

    context = {
        'test_series': test_series,
        'tests': tests,
        'paid_tests': paid_tests,
        'demo_test': next((t for t in tests if t.is_demo), None),
        'paper_tabs': [
            (key, label, count) for key, label in Test.PAPER_TYPES
            if (count := sum(1 for t in paid_tests if t.paper_type == key))
        ],
        'subjects': sorted(coverage.values(), key=lambda s: -s['questions']),
        'total_questions': total_questions,
        'total_marks': total_marks,
        'total_minutes': sum(t.duration_minutes for t in paid_tests),
        'attempted_tests': attempted_tests,
        'progress_pct': round(attempted_tests * 100 / len(tests)) if tests else 0,
        'calculator_tests': [t for t in tests if t.calculator != 'none'],
        'max_penalty': max((t.penalty for t in tests), default=0),
        'exam_category': exam_category,
        'related_series': related,
        'is_purchased': has_access and not test_series.is_free,
        'can_take_tests': has_access,
        'price_display': "Free" if test_series.is_free else f"₹{test_series.price:,.0f}",
        'back_url': reverse('home'),
    }
    return render(request, 'test_series_detail.html', context)


@login_required
def start_test(request, test_id):
    """Start a new test attempt"""
    test = get_object_or_404(Test, id=test_id, is_active=True)
    
    # Check if test is available
    if not test.is_available:
        messages.error(request, 'This test is not currently available.')
        return redirect('front_exam_series_detail', pk=test.test_series.pk)

    if not test.is_demo and not _has_test_series_access(request.user, test.test_series):
        messages.warning(request, 'Buy this test series to unlock this test. You can try the free demo test first.')
        return redirect('front_exam_series_detail', pk=test.test_series.pk)
    
    # Check if user can attempt this test
    user_attempts = TestAttempt.objects.filter(
        user=request.user, 
        test=test,
        status='submitted'
    ).count()
    
    if user_attempts >= test.max_attempts:
        messages.error(request, f'You have already used all {test.max_attempts} attempts for this test.')
        return redirect('front_exam_series_detail', pk=test.test_series.pk)
    
    total_marks = test.questions.aggregate(Sum('marks'))['marks__sum'] or 0

    with transaction.atomic():
        # Lock the user row so two quick clicks can't both create an attempt.
        User.objects.select_for_update().filter(pk=request.user.pk).first()
        incomplete_attempt = TestAttempt.objects.filter(
            user=request.user,
            test=test,
            status__in=['started', 'in_progress']
        ).first()
        if incomplete_attempt:
            return redirect('front_exam_session', attempt_id=incomplete_attempt.id)

        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            attempt_number=user_attempts + 1,
            total_questions=test.questions.count(),
            total_marks=total_marks,
            status='in_progress'
        )
    
    messages.success(request, f'Test started! You have {test.duration_minutes} minutes to complete.')
    return redirect('front_exam_session', attempt_id=attempt.id)


@login_required
def take_test(request, attempt_id):
    """Take test interface"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    
    if attempt.status == 'submitted':
        return redirect('front_exam_result', attempt_id=attempt.id)
    
    # Check if time expired
    elapsed_time = timezone.now() - attempt.started_at
    duration_seconds = attempt.test.duration_minutes * 60
    
    if elapsed_time.total_seconds() >= duration_seconds:
        # Auto-submit if time is up
        return redirect('front_exam_submit', attempt_id=attempt.id)
    
    questions = attempt.test.questions.all().order_by('order')
    
    # Shuffle questions if enabled
    if attempt.test.shuffle_questions:
        questions = list(questions)
        import random
        random.seed(attempt.id.int)  # Use attempt ID as seed for consistency
        random.shuffle(questions)
    
    # Calculate remaining time
    time_remaining = duration_seconds - int(elapsed_time.total_seconds())

    # Sections follow the order subjects first appear in (as in the real paper)
    questions = list(questions.select_related('subject') if hasattr(questions, 'select_related') else questions)
    negative_marking = attempt.test.test_series.has_negative_marking
    sections = {}
    for number, question in enumerate(questions, start=1):
        question.number = number
        question.section = question.subject.name if question.subject else 'General'
        question.penalty = question.negative_marks if negative_marking and question.negative_marks else 0
        section = sections.setdefault(question.section, {'name': question.section, 'numbers': [], 'marks': 0})
        section['numbers'].append(number)
        section['marks'] = marks_num(float(section['marks']) + float(question.marks))

    context = {
        'attempt': attempt,
        'test': attempt.test,
        'series': attempt.test.test_series,
        'questions': questions,
        'sections': list(sections.values()),
        'total_marks': marks_num(sum(q.marks for q in questions)),
        'negative_marking': negative_marking and any(q.penalty for q in questions),
        'time_remaining': max(0, time_remaining),
    }
    return render(request, 'take_test.html', context)


EXAM_SUBMIT_GRACE_SECONDS = 120


def _clean_submitted_answer(question, value):
    """Drop anything that isn't a real option of this question (tampered forms count as unanswered)."""
    option_keys = {str(k).lower() for k in question.options} if isinstance(question.options, dict) else set()
    if isinstance(value, list):
        value = [str(v).strip()[:20] for v in value][:20]
        if option_keys:
            value = sorted({v for v in value if v.lower() in option_keys})
        return value
    value = str(value or '').strip()[:500]
    if question.question_type == 'mcq_single' and option_keys and value.lower() not in option_keys:
        return ''
    return value


def _same_number(given, expected, correct_answer):
    """Numerical answers match by value: '12', '12.0' and '12.00' are the same; an optional tolerance is honoured."""
    try:
        given_value = float(str(given).replace(',', '').replace('−', '-'))
        expected_value = float(str(expected).replace(',', '').replace('−', '-'))
    except ValueError:
        return False
    tolerance = 0.0
    if isinstance(correct_answer, dict):
        try:
            tolerance = float(correct_answer.get('tolerance') or 0)
        except (TypeError, ValueError):
            tolerance = 0.0
    return abs(given_value - expected_value) <= max(tolerance, 1e-9 + abs(expected_value) * 1e-9)


def _attempt_deadline(attempt):
    return attempt.started_at + timedelta(minutes=attempt.test.duration_minutes)


def _finalize_test_attempt(attempt, post_data):
    """Grade a test attempt from submitted answer data and persist the result.

    `post_data` only needs to support .get()/.getlist() (a QueryDict or plain dict).
    Used both for a normal form submission and for the timeout auto-submit path,
    where there is no answer data (everything counts as skipped).
    """
    # Calculate time spent
    time_spent = timezone.now() - attempt.started_at
    attempt.time_spent = time_spent
    attempt.submitted_at = timezone.now()

    # Initialize counters
    correct_answers = 0
    wrong_answers = 0
    attempted_questions = 0
    marks_obtained = 0.0
    subject_wise_score = {}

    # Get all questions for this test
    questions = attempt.test.questions.select_related('subject')
    StudentAnswer.objects.filter(attempt=attempt).delete()

    # Process each question
    for question in questions:
        answer_key = f'question_{question.id}'

        # Get student's answer from the submitted data
        if question.question_type == 'mcq_multiple':
            selected_answer = post_data.getlist(answer_key)
        else:
            selected_answer = post_data.get(answer_key, '')
        selected_answer = _clean_submitted_answer(question, selected_answer)

        # Check if answered
        is_answered = bool(selected_answer) and not (isinstance(selected_answer, list) and len(selected_answer) == 0)

        # Skip if not answered - create empty record
        if not is_answered:
            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer={},
                is_correct=False,
                marks_obtained=0,
                is_attempted=False
            )
            continue

        attempted_questions += 1

        # Normalize answers for comparison
        if isinstance(selected_answer, list):
            student_answer = sorted([ans.lower().strip() for ans in selected_answer])
        else:
            student_answer = selected_answer.lower().strip()

        # Get correct answer
        correct_answer = question.correct_answer

        # Check if answer is correct
        is_correct = False
        question_marks = 0.0

        if question.question_type == 'mcq_multiple':
            # For multiple choice, compare as sorted lists
            if isinstance(correct_answer, dict) and 'answers' in correct_answer:
                correct_list = sorted([ans.lower().strip() for ans in correct_answer['answers']])
            elif isinstance(correct_answer, list):
                correct_list = sorted([ans.lower().strip() for ans in correct_answer])
            else:
                correct_list = []

            is_correct = student_answer == correct_list

        elif question.question_type in ['mcq_single', 'true_false']:
            # For single choice
            if isinstance(correct_answer, dict) and 'answer' in correct_answer:
                correct_value = correct_answer['answer'].lower().strip()
            elif isinstance(correct_answer, str):
                correct_value = correct_answer.lower().strip()
            else:
                correct_value = ''

            is_correct = student_answer == correct_value

        elif question.question_type in ['fill_blank', 'numerical']:
            # For text/numerical answers
            if isinstance(correct_answer, dict) and 'answer' in correct_answer:
                correct_value = str(correct_answer['answer']).lower().strip()
            elif isinstance(correct_answer, str):
                correct_value = correct_answer.lower().strip()
            else:
                correct_value = ''

            is_correct = student_answer == correct_value
            if not is_correct and question.question_type == 'numerical':
                is_correct = _same_number(student_answer, correct_value, correct_answer)

        # Calculate marks
        if is_correct:
            correct_answers += 1
            question_marks = float(question.marks)
        else:
            wrong_answers += 1
            # Apply negative marking if enabled
            if attempt.test.test_series.has_negative_marking:
                question_marks = -float(question.negative_marks)

        marks_obtained += question_marks

        # Track subject-wise score
        if question.subject:
            subject_name = question.subject.name
            if subject_name not in subject_wise_score:
                subject_wise_score[subject_name] = {
                    'correct': 0,
                    'wrong': 0,
                    'marks': 0.0
                }

            if is_correct:
                subject_wise_score[subject_name]['correct'] += 1
            else:
                subject_wise_score[subject_name]['wrong'] += 1
            subject_wise_score[subject_name]['marks'] += question_marks

        # Save student answer with proper format
        StudentAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_answer={'answer': selected_answer} if not isinstance(selected_answer, list) else {'answers': selected_answer},
            is_correct=is_correct,
            marks_obtained=question_marks,
            is_attempted=True,
            answered_at=timezone.now()
        )

        # Update question analytics
        question.total_attempts += 1
        if is_correct:
            question.correct_attempts += 1
        question.save(update_fields=['total_attempts', 'correct_attempts'])

    # Calculate percentage
    percentage_score = 0
    if attempt.total_marks > 0:
        percentage_score = (marks_obtained / float(attempt.total_marks)) * 100

    # Update attempt with results
    attempt.status = 'submitted'
    attempt.attempted_questions = attempted_questions
    attempt.correct_answers = correct_answers
    attempt.wrong_answers = wrong_answers
    attempt.marks_obtained = marks_obtained
    attempt.percentage_score = max(0, percentage_score)
    attempt.subject_wise_score = subject_wise_score
    attempt.passed = attempt.percentage_score >= attempt.test.test_series.pass_percentage
    attempt.save()

    # Rank/percentile among all submitted attempts for this test
    attempt.calculate_rank()

    # Update test series analytics
    test_series = attempt.test.test_series
    test_series.total_attempts += 1

    # Recalculate average score
    all_attempts = TestAttempt.objects.filter(
        test__test_series=test_series,
        status='submitted'
    )
    if all_attempts.exists():
        avg_score = all_attempts.aggregate(avg=Sum('marks_obtained'))['avg'] or 0
        test_series.average_score = avg_score / all_attempts.count() if all_attempts.count() > 0 else 0

    test_series.save()
    return attempt


@login_required
def submit_test(request, attempt_id):
    """
    Submit and grade a test exactly once.
    The attempt is claimed with a conditional UPDATE inside a transaction, so double clicks,
    a second tab or a replayed request can never grade (or re-grade) the same attempt.
    Answers posted after the time limit (plus a short network grace) are ignored.
    """
    attempt = get_object_or_404(TestAttempt.objects.select_related('test', 'test__test_series'), id=attempt_id, user=request.user)

    if attempt.status == 'submitted':
        messages.info(request, 'This test has already been submitted.')
        return redirect('front_exam_result', attempt_id=attempt.id)

    from django.http import QueryDict
    late = timezone.now() > _attempt_deadline(attempt) + timedelta(seconds=EXAM_SUBMIT_GRACE_SECONDS)
    # A GET is the session view's timeout redirect: nothing was posted, everything counts as skipped.
    answers = request.POST if request.method == 'POST' and not late else QueryDict()

    with transaction.atomic():
        claimed = TestAttempt.objects.filter(
            pk=attempt.pk, user=request.user, status__in=['started', 'in_progress']
        ).update(status='submitted', submitted_at=timezone.now())
        if not claimed:
            messages.info(request, 'This test has already been submitted.')
            return redirect('front_exam_result', attempt_id=attempt.id)
        _finalize_test_attempt(attempt, answers)

    if request.method != 'POST':
        messages.warning(request, 'Time was up — your test was submitted automatically.')
    elif late:
        logger.warning("Late exam submission ignored: attempt=%s user=%s", attempt.pk, request.user.pk)
        messages.warning(request, 'Time was up before your answers arrived, so the test was submitted without them.')
    else:
        messages.success(request, 'Test submitted successfully!')
    return redirect('front_exam_result', attempt_id=attempt.id)



@login_required
def test_result(request, attempt_id):
    """Show test results"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    
    if attempt.status != 'submitted':
        messages.warning(request, 'Please submit the test first to see results.')
        return redirect('front_exam_session', attempt_id=attempt.id)
    
    test = attempt.test
    skipped_questions = attempt.total_questions - attempt.attempted_questions
    answers = list(
        StudentAnswer.objects.filter(attempt=attempt)
        .select_related('question', 'question__subject')
        .order_by('question__order', 'question__id')
    )

    # Section-wise breakdown and question strip
    sections = {}
    question_strip = []
    positive_marks = negative_marks = 0.0
    for number, answer in enumerate(answers, start=1):
        question = answer.question
        name = question.subject.name if question.subject else 'General'
        section = sections.setdefault(name, {
            'name': name, 'total': 0, 'correct': 0, 'wrong': 0, 'skipped': 0, 'marks': 0.0, 'max_marks': 0,
        })
        section['total'] += 1
        section['max_marks'] = marks_num(float(section['max_marks']) + float(question.marks))
        marks = float(answer.marks_obtained)
        section['marks'] += marks
        if not answer.is_attempted:
            status = 'skipped'
        elif answer.is_correct:
            status = 'correct'
            positive_marks += marks
        else:
            status = 'wrong'
            negative_marks += marks
        section[status] += 1
        question_strip.append({'number': number, 'status': status, 'section': name})
    for section in sections.values():
        attempted = section['correct'] + section['wrong']
        section['accuracy'] = round(section['correct'] * 100 / attempted) if attempted else 0
        section['score_pct'] = max(0, round(section['marks'] * 100 / section['max_marks'])) if section['max_marks'] else 0
    section_list = sorted(sections.values(), key=lambda s: s['score_pct'])

    # Time
    seconds = int(attempt.time_spent.total_seconds()) if attempt.time_spent else 0
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    time_taken = f"{hours}h {minutes:02d}m {secs:02d}s" if hours else f"{minutes}m {secs:02d}s"
    duration_seconds = test.duration_minutes * 60

    # How others did on this test
    submitted = TestAttempt.objects.filter(test=test, status='submitted')
    stats = submitted.aggregate(avg=Avg('marks_obtained'), top=Max('marks_obtained'))
    previous_attempts = (
        TestAttempt.objects.filter(test=test, user=request.user, status='submitted')
        .exclude(pk=attempt.pk).order_by('-submitted_at')[:5]
    )

    attempted = attempt.attempted_questions
    pass_percentage = test.test_series.pass_percentage
    context = {
        'attempt': attempt,
        'test': test,
        'series': test.test_series,
        'skipped_questions': skipped_questions,
        'accuracy': round(attempt.correct_answers * 100 / attempted) if attempted else 0,
        'time_taken': time_taken,
        'time_used_pct': min(100, round(seconds * 100 / duration_seconds)) if duration_seconds else 0,
        'avg_time_per_question': round(seconds / attempt.total_questions) if attempt.total_questions else 0,
        'positive_marks': positive_marks,
        'negative_marks': abs(negative_marks),
        'score_pct': max(0, min(100, float(attempt.percentage_score))),
        'pass_percentage': pass_percentage,
        'pass_marks': round(float(attempt.total_marks) * pass_percentage / 100, 2),
        'sections': sorted(sections.values(), key=lambda s: list(sections).index(s['name'])),
        'weakest_section': section_list[0] if len(section_list) > 1 else None,
        'strongest_section': section_list[-1] if len(section_list) > 1 else None,
        'question_strip': question_strip,
        'average_marks': stats['avg'] or 0,
        'top_marks': stats['top'] or 0,
        'total_takers': submitted.count(),
        'previous_attempts': previous_attempts,
        'attempts_left': max(0, test.max_attempts - submitted.filter(user=request.user).count()),
    }
    return render(request, 'test_result.html', context)

@login_required
def review_answers(request, attempt_id):
    """Review test answers with correct solutions"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    
    # Check if review is allowed
    if not attempt.test.allow_review:
        messages.error(request, 'Answer review is not available for this test.')
        return redirect('front_exam_result', attempt_id=attempt.id)
    
    if attempt.status != 'submitted':
        messages.warning(request, 'Please submit the test first to review answers.')
        return redirect('front_exam_session', attempt_id=attempt.id)
    
    # Get all student answers with related question data
    student_answers = StudentAnswer.objects.filter(
        attempt=attempt
    ).select_related(
        'question', 
        'question__subject'
    ).order_by('question__order')
    
    # Prepare answers with additional context
    answers_with_context = []
    for student_answer in student_answers:
        question = student_answer.question
        
        # Format correct answer display with full option text
        correct_answer_display = "No correct answer set"
        if question.correct_answer and isinstance(question.correct_answer, dict):
            if question.question_type in ['mcq_single', 'true_false']:
                if 'answer' in question.correct_answer and question.correct_answer['answer']:
                    answer_key = str(question.correct_answer['answer']).lower()
                    if question.options and answer_key in question.options:
                        # Show both key and option text
                        correct_answer_display = f"{answer_key.upper()}. {question.options[answer_key]}"
                    else:
                        correct_answer_display = f"{answer_key.upper()}. (Option text missing)"
            
            elif question.question_type == 'mcq_multiple':
                if 'answers' in question.correct_answer and question.correct_answer['answers']:
                    answer_keys = question.correct_answer['answers']
                    if question.options:
                        # Show all correct options with text
                        option_displays = []
                        for key in answer_keys:
                            key_lower = str(key).lower()
                            if key_lower in question.options:
                                option_displays.append(f"{key_lower.upper()}. {question.options[key_lower]}")
                            else:
                                option_displays.append(f"{key_lower.upper()}. (Option text missing)")
                        correct_answer_display = ', '.join(option_displays)
                    else:
                        correct_answer_display = ', '.join([str(key).upper() for key in answer_keys])
            
            elif question.question_type in ['fill_blank', 'numerical']:
                correct_answer_display = str(question.correct_answer.get('answer', 'N/A'))
        
        # Format student answer display with full option text - THIS IS THE KEY FIX
        student_answer_display = "Not Attempted"
        if student_answer.is_attempted and student_answer.selected_answer:
            if isinstance(student_answer.selected_answer, dict):
                # Single answer (MCQ single, True/False, Fill blank, Numerical)
                if 'answer' in student_answer.selected_answer and student_answer.selected_answer['answer']:
                    answer_value = student_answer.selected_answer['answer']
                    
                    if question.question_type in ['mcq_single', 'true_false']:
                        # For MCQ, show key + option text
                        answer_key = str(answer_value).lower()
                        
                        # Check if options exist and the key is in options
                        if question.options and isinstance(question.options, dict):
                            if answer_key in question.options:
                                student_answer_display = f"{answer_key.upper()}. {question.options[answer_key]}"
                            else:
                                student_answer_display = f"{answer_key.upper()}. (Option text not found)"
                        else:
                            student_answer_display = f"{answer_key.upper()}. (No options available)"
                    
                    elif question.question_type in ['fill_blank', 'numerical']:
                        # For text/numerical, just show the answer
                        student_answer_display = str(answer_value)
                
                # Multiple answers (MCQ multiple)
                elif 'answers' in student_answer.selected_answer and student_answer.selected_answer['answers']:
                    answer_keys = student_answer.selected_answer['answers']
                    
                    if question.options and isinstance(question.options, dict):
                        # Show all selected options with text
                        option_displays = []
                        for key in answer_keys:
                            key_lower = str(key).lower()
                            if key_lower in question.options:
                                option_displays.append(f"{key_lower.upper()}. {question.options[key_lower]}")
                            else:
                                option_displays.append(f"{key_lower.upper()}. (Option text not found)")
                        student_answer_display = ', '.join(option_displays)
                    else:
                        student_answer_display = ', '.join([str(key).upper() for key in answer_keys])
        
        answers_with_context.append({
            'student_answer': student_answer,
            'question': question,
            'correct_answer_display': correct_answer_display,
            'student_answer_display': student_answer_display,
        })
    
    # Calculate skipped questions
    skipped_questions = attempt.total_questions - attempt.attempted_questions
    
    # Subject-wise analysis
    subject_analysis = []
    if attempt.subject_wise_score:
        for subject_name, scores in attempt.subject_wise_score.items():
            subject_analysis.append({
                'name': subject_name,
                'correct': scores.get('correct', 0),
                'wrong': scores.get('wrong', 0),
                'marks': scores.get('marks', 0),
            })
    
    context = {
        'attempt': attempt,
        'test': attempt.test,
        'answers_with_context': answers_with_context,
        'skipped_questions': skipped_questions,
        'subject_analysis': subject_analysis,
    }
    
    # Mark as reviewed
    if not attempt.is_reviewed:
        attempt.is_reviewed = True
        attempt.save(update_fields=['is_reviewed'])
    
    return render(request, 'review_answers.html', context)







def live_class_detail(request, pk):
    """
    Public view for displaying live class details with purchase status check.
    Shows "Already Enrolled" if user has purchased the course.
    """
    try:
        now = timezone.now()
        
        # Get the live class with related sessions
        course = LiveClassCourse.objects.prefetch_related('sessions').get(
            pk=pk, 
            is_active=True
        )
        
        # Format price displays
        if course.is_free:
            course.original_price_display = "0.00"
            course.current_price_display = "FREE"
        else:
            course.original_price_display = f"₹{course.original_price:.2f}"
            course.current_price_display = f"₹{course.current_price:.2f}"
        
        # Get next sessions
        # Every session with its room state (upcoming / open / ended) and how many recordings students can watch.
        from live_class.access import room_state
        ready = dict(
            LiveClassRecording.objects.filter(session__course=course, status='ready', is_published=True)
            .values('session').annotate(n=Count('id')).values_list('session', 'n')
        )
        all_sessions = list(course.sessions.all().order_by('scheduled_datetime'))
        for s in all_sessions:
            s.room_state = room_state(s, now)
            s.recordings_ready = ready.get(s.pk, 0)

        # Upcoming = not ended yet, so a class that is live right now is listed (with a Join button).
        course.next_sessions = [s for s in all_sessions if s.room_state != 'ended'][:10]

        # Calculate total sessions and free sessions
        total_sessions = len(all_sessions)
        free_sessions = sum(1 for s in all_sessions if s.is_free)
        
        # ===== DEFAULT CONTEXT =====
        context = {
            'course': course,
            'next_sessions': course.next_sessions,
            'all_sessions': all_sessions,
            'total_sessions': total_sessions,
            'free_sessions': free_sessions,
            'now': now,
            'is_purchased': False,  # Default: user hasn't purchased
        }
        
        # ===== CHECK PURCHASE STATUS FOR AUTHENTICATED USERS =====
        if request.user.is_authenticated:
            try:
                # Check if user has access to this course
                access = UserCourseAccess.objects.get(
                    user=request.user,
                    course_id=pk,
                    course_type='live_class'
                )
                
                # Check if access is active (if is_active field exists)
                if hasattr(access, 'is_active'):
                    if access.is_active:
                        context['is_purchased'] = True
                else:
                    # If no is_active field, just having the record means purchased
                    context['is_purchased'] = True
                    
            except UserCourseAccess.DoesNotExist:
                # User hasn't purchased this course
                context['is_purchased'] = False
        
        return render(request, 'live_class_detail.html', context)
    
    except LiveClassCourse.DoesNotExist:
        raise Http404("Live class not found")




def video_course_detail(request, pk):
    """
    Public view for displaying video course details with purchase status check
    """
    try:
        # Optimized query with prefetch_related
        course = VideoCourse.objects.prefetch_related(
            'videos', 
            'learn_points', 
            'includes'
        ).get(pk=pk)
        
        # Format price displays
        course.original_price_display = f"{course.original_price:.2f}"
        course.selling_price_display = f"{course.selling_price:.2f}"
        
        # Get related videos with duration formatting
        videos = course.videos.all()
        for video in videos:
            # Convert seconds to MM:SS format
            if video.duration_seconds and video.duration_seconds > 0:
                minutes = video.duration_seconds // 60
                seconds = video.duration_seconds % 60
                video.duration_display = f"{minutes}:{seconds:02d}"
            else:
                video.duration_display = "--:--"
        
        # Get learn points and includes
        learn_points = course.learn_points.all()
        includes = course.includes.all()
        
        # ===== DEFAULT CONTEXT =====
        context = {
            'course': course,
            'videos': videos,
            'learn_points': learn_points,
            'includes': includes,
            'has_access': False,
            'is_purchased': False,
            'access_expires_at': None,
        }
        
        # ===== CHECK USER PURCHASE STATUS =====
        if request.user.is_authenticated:
            try:
                # Get user's course access
                access = UserCourseAccess.objects.get(
                    user=request.user,
                    course_id=pk,
                    course_type='video_course'
                )
                
                # Check if access is still valid using the @property method
                if access.has_access:
                    context['has_access'] = True
                    context['is_purchased'] = True
                    context['access_expires_at'] = access.expires_at
                else:
                    # Access expired
                    context['has_access'] = False
                    context['is_purchased'] = False
                    
            except UserCourseAccess.DoesNotExist:
                # User hasn't purchased this course
                context['has_access'] = False
                context['is_purchased'] = False
        
        return render(request, 'video_course_detail.html', context)
    
    except VideoCourse.DoesNotExist:
        raise Http404("Course not found")


def loginuser(request):
    """Render the login page (static)."""
    return render(request, "login.html")


# base/views.py (add these imports and views)


def _requested_next(request):
    """Validated same-site ``next`` from the POST body or query string (or None)."""
    return safe_next_url(request, request.POST.get('next') or request.GET.get('next'))


def _login_url_with_next(next_url):
    """URL of the login page that returns the user to ``next_url`` afterwards."""
    url = reverse('login')
    return f"{url}?{urlencode({'next': next_url})}" if next_url else url


def login_view(request):
    """Handle user login with 'remember me'. Rate limited per IP and per account."""
    if request.user.is_authenticated:
        return redirect(_requested_next(request) or 'home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()[:254]
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'login.html', status=400)

        if is_rate_limited(request, 'login', limit=10, window=15 * 60, extra_ident=email):
            messages.error(request, 'Too many login attempts. Please wait 15 minutes and try again.')
            return render(request, 'login.html', status=429)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # authenticate() already refuses inactive users, so this is an active account.
            login(request, user)
            reset_rate_limit('login:acct', email)

            # Remember Me functionality
            if remember:
                request.session.set_expiry(2592000)  # 30 days
            else:
                request.session.set_expiry(0)  # until browser closes

            messages.success(request, f'Welcome back, {user.get_full_name_or_email()}!')

            # Back to the page the user came from (validated to prevent open-redirects)
            return redirect(_requested_next(request) or 'home')

        inactive = User.objects.filter(email__iexact=email, is_active=False).exists()
        if inactive:
            messages.error(request, 'This account is not active yet. Please verify your email or contact support.')
        else:
            # Same message for "no such account" and "wrong password" so emails can't be probed.
            messages.error(request, 'Incorrect email or password. Please try again.')

    return render(request, 'login.html')



RESET_SENT_MESSAGE = 'If an account exists for this email, a 6-digit code has been sent to it. Please check your inbox.'


@require_http_methods(["POST"])
def forgot_password_request(request):
    """
    Email a password-reset OTP. The pending reset is bound to this browser session,
    and the reply is the same whether or not the email has an account.
    """
    email = request.POST.get('email', '').strip().lower()[:254]
    if not email:
        return JsonResponse({'success': False, 'message': 'Email is required'}, status=400)

    if is_rate_limited(request, 'pw-reset-request', limit=5, window=60 * 60, extra_ident=email):
        return JsonResponse({
            'success': False,
            'message': 'Too many reset requests. Please wait an hour and try again.',
        }, status=429)

    smtp_config = SMTPConfiguration.objects.filter(is_active=True).first()
    if not smtp_config or smtp_config.test_status != 'success':
        return JsonResponse({
            'success': False,
            'message': 'Password reset by email is not available right now. Please contact support.'
        })

    user = User.objects.filter(email__iexact=email, is_active=True).first()
    request.session['reset_pending_user_id'] = user.id if user else None
    request.session.pop('reset_verified', None)
    request.session.pop('reset_user_id', None)
    if not user:
        return JsonResponse({'success': True, 'message': RESET_SENT_MESSAGE})

    otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
    OTPVerification.objects.filter(user=user, verification_type='password_reset', is_used=False).delete()
    clear_otp_failures(user.id, 'password_reset')
    otp_instance = OTPVerification.objects.create(
        user=user,
        otp_code=otp_code,
        verification_type='password_reset',
        expires_at=timezone.now() + timezone.timedelta(minutes=10)
    )

    from adminpanel.branding import brand_name
    site_name = brand_name()
    email_message = f"""
Hello {user.first_name or user.email},

You have requested to reset your {site_name} password.

Your OTP code is: {otp_code}

This OTP is valid for 10 minutes. Never share it with anyone.

If you did not request this password reset, please ignore this email.

Best regards,
{site_name} Support
    """.strip()

    try:
        connection = get_connection(
            backend=smtp_config.email_backend,
            host=smtp_config.email_host,
            port=smtp_config.email_port,
            username=smtp_config.email_host_user,
            password=smtp_config.email_host_password,
            use_tls=smtp_config.email_use_tls,
            use_ssl=smtp_config.email_use_ssl,
        )
        sent = send_mail(
            subject=f'Your {site_name} password reset code',
            message=email_message,
            from_email=smtp_config.default_from_email,
            recipient_list=[user.email],
            fail_silently=False,
            connection=connection
        )
    except Exception:
        logger.exception("Password reset email failed for user %s", user.id)
        sent = 0

    if sent != 1:
        otp_instance.delete()
        return JsonResponse({'success': False, 'message': 'We could not send the email. Please try again later.'})
    return JsonResponse({'success': True, 'message': RESET_SENT_MESSAGE})


@require_http_methods(["POST"])
def verify_reset_otp(request):
    """Verify the reset OTP for the account this session asked to reset (5 wrong codes burn it)."""
    otp_code = (request.POST.get('otp_code') or request.POST.get('otpcode') or '').strip()
    user_id = request.session.get('reset_pending_user_id')

    if not otp_code:
        return JsonResponse({'success': False, 'message': 'Please enter the 6-digit code.'}, status=400)
    if 'reset_pending_user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'Session expired. Please request a new code.'})
    if is_rate_limited(request, 'pw-reset-verify', limit=10, window=15 * 60):
        return JsonResponse({'success': False, 'message': 'Too many attempts. Please wait 15 minutes.'}, status=429)

    invalid = JsonResponse({'success': False, 'message': 'Invalid or expired code. Please try again.'})
    if not user_id:
        return invalid  # no account for that email; answer exactly like a wrong code
    if otp_locked(user_id, 'password_reset'):
        return JsonResponse({'success': False, 'message': 'Too many wrong codes. Please request a new code.'})

    otp = OTPVerification.objects.filter(
        user_id=user_id, otp_code=otp_code, verification_type='password_reset', is_used=False
    ).first()
    if not (otp and otp.is_valid()):
        record_otp_failure(user_id, 'password_reset')
        return invalid

    otp.is_used = True
    otp.save(update_fields=['is_used'])
    clear_otp_failures(user_id, 'password_reset')
    request.session.cycle_key()
    request.session['reset_user_id'] = user_id
    request.session['reset_verified'] = True
    request.session['reset_verified_at'] = timezone.now().timestamp()
    request.session.pop('reset_pending_user_id', None)
    return JsonResponse({'success': True, 'message': 'Code verified. Please create a new password.'})


@require_http_methods(["POST"])
def reset_password(request):
    """Set a new password after the OTP was verified in this session (valid for 10 minutes)."""
    user_id = request.session.get('reset_user_id')
    verified_at = request.session.get('reset_verified_at', 0)
    if not request.session.get('reset_verified') or not user_id or timezone.now().timestamp() - verified_at > 600:
        return JsonResponse({'success': False, 'message': 'Session expired. Please start the password reset again.'})

    new_password = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')
    if not new_password or not confirm_password:
        return JsonResponse({'success': False, 'message': 'Please fill in all password fields.'})
    if new_password != confirm_password:
        return JsonResponse({'success': False, 'message': 'Passwords do not match.'})

    user = User.objects.filter(id=user_id, is_active=True).first()
    if not user:
        return JsonResponse({'success': False, 'message': 'Session expired. Please start the password reset again.'})
    try:
        validate_password(new_password, user=user)
    except ValidationError as exc:
        return JsonResponse({'success': False, 'message': ' '.join(exc.messages)})

    user.set_password(new_password)
    user.save(update_fields=['password'])
    for key in ('reset_user_id', 'reset_verified', 'reset_verified_at'):
        request.session.pop(key, None)
    logger.info("Password reset completed for user %s", user.id)
    return JsonResponse({
        'success': True,
        'message': 'Password reset successfully. You can now login with your new password.'
    })


def logout_view(request):
    """Handle user logout"""
    referer = request.META.get('HTTP_REFERER', '')
    next_url = None
    if referer and safe_next_url(request, referer):
        parsed = urlparse(referer)
        next_url = parsed.path + (f"?{parsed.query}" if parsed.query else '')
        if next_url == '/' or next_url.startswith(reverse('logout_user')):
            next_url = None
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(_login_url_with_next(next_url))


def is_mobile_request(request):
    """Fast mobile detection."""
    ua = request.META.get("HTTP_USER_AGENT", "").lower()
    mobile_keywords = ["mobile", "android", "iphone", "ipad", "blackberry", "windows phone"]
    return any(keyword in ua for keyword in mobile_keywords)

@csrf_protect
def signup_view(request):
    """
    ULTRA-FAST signup:
    - MOBILE: 3s SMTP timeout → instant if fails
    - DESKTOP: 10s SMTP timeout
    - NO SMTP: <500ms direct login
    - ANY ERROR: Clean redirect to login
    """
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)

        if is_rate_limited(request, 'signup', limit=5, window=60 * 60):
            messages.error(request, "Too many sign-up attempts from your network. Please try again in an hour.")
            return render(request, "signup.html", {"form": form, "smtp_configured": has_smtp_configured()}, status=429)

        if form.is_valid():
            next_url = _requested_next(request)
            is_mobile = is_mobile_request(request)
            smtp_configured = has_smtp_configured()
            
            logger.debug("Mobile=%s, SMTP=%s", is_mobile, smtp_configured)

            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    
                    # PATH 1: No SMTP → INSTANT LOGIN
                    if not smtp_configured:
                        user.is_active = True
                        # Comment if no is_verified:
                        # user.is_verified = True
                        user.save()
                        messages.success(
                            request,
                            "Account created successfully. Please log in."
                        )
                        return redirect(_login_url_with_next(next_url))
                    
                    # PATH 2: MOBILE + SMTP → FAST OTP (3s timeout)
                    if is_mobile:
                        user.is_active = False
                        # Comment if no is_verified:
                        # user.is_verified = False
                        user.save()
                        
                        otp, message = create_and_send_otp(user, is_mobile=True)
                        
                        if otp:
                            request.session["pending_user_id"] = user.id
                            request.session["post_auth_next"] = next_url
                            messages.success(
                                request,
                                "Account created! Check email for OTP (3s delivery)."
                            )
                            return redirect("verify_otp")
                        else:
                            # Fast fallback
                            user.is_active = True
                            user.save()
                            messages.info(
                                request,
                                "We could not send the verification email, so your account was activated. Please log in."
                            )
                            return redirect(_login_url_with_next(next_url))
                    
                    # PATH 3: DESKTOP + SMTP → Full OTP (10s timeout)
                    user.is_active = False
                    # Comment if no is_verified:
                    # user.is_verified = False
                    user.save()
                    
                    otp, message = create_and_send_otp(user, is_mobile=False)
                    
                    if otp:
                        request.session["pending_user_id"] = user.id
                        request.session["post_auth_next"] = next_url
                        messages.success(
                            request,
                            "Account created! Check your email for verification code."
                        )
                        return redirect("verify_otp")
                    else:
                        user.delete()
                        logger.warning("Signup OTP email failed: %s", message)
                        messages.error(
                            request,
                            "We could not send the verification email. Please try signing up again later."
                        )
                        return redirect(_login_url_with_next(next_url))

            except Exception as e:
                logger.exception("Signup error - fallback to login")
                messages.error(
                    request,
                    "Something went wrong. You can log in directly."
                )
                return redirect(_login_url_with_next(next_url))

        # Invalid form
        messages.error(request, "Please fix the form errors below.")
    else:
        form = SignupForm()

    context = {
        "form": form,
        "smtp_configured": has_smtp_configured(),
    }
    return render(request, "signup.html", context)


def verify_otp_view(request):
    """Handle OTP verification for new users."""
    user_id = request.session.get('pending_user_id')
    if not user_id:
        messages.error(request, 'No pending verification found.')
        return redirect('signup')

    user = get_object_or_404(User, id=user_id, is_active=False)

    if request.method == 'POST':
        form = OTPVerificationForm(user=user, data=request.POST)
        if otp_locked(user.id, 'email'):
            messages.error(request, 'Too many wrong codes. Please request a new OTP.')
            form = OTPVerificationForm(user=user)
        elif form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            try:
                otp = OTPVerification.objects.get(
                    user=user,
                    otp_code=otp_code,
                    verification_type='email',
                    is_used=False
                )
                if otp.is_valid():
                    otp.is_used = True
                    otp.save()
                    clear_otp_failures(user.id, 'email')

                    user.is_active = True
                    user.is_verified = True
                    user.save()

                    login(request, user)
                    request.session.pop('pending_user_id', None)
                    next_url = safe_next_url(request, request.session.pop('post_auth_next', None))

                    messages.success(request, 'Email verified successfully! Welcome.')
                    return redirect(next_url or 'home')
                else:
                    messages.error(request, 'OTP has expired. Please request a new one.')
            except OTPVerification.DoesNotExist:
                failures = record_otp_failure(user.id, 'email')
                messages.error(request, 'Invalid OTP code.' if failures < 5 else 'Too many wrong codes. Please request a new OTP.')
    else:
        form = OTPVerificationForm(user=user)

    context = {'form': form, 'user': user, 'can_resend': True}
    return render(request, 'verify_otp.html', context)


@require_http_methods(["POST"])
def resend_otp_view(request):
    """Resend OTP via AJAX."""
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'No pending verification found.'})

    try:
        user = User.objects.get(id=user_id, is_active=False)

        last_otp = OTPVerification.objects.filter(
            user=user,
            verification_type='email'
        ).order_by('-created_at').first()

        if last_otp and (timezone.now() - last_otp.created_at).seconds < 60:
            return JsonResponse({
                'success': False,
                'message': 'Please wait at least 1 minute before requesting a new OTP.'
            })

        if is_rate_limited(request, 'otp-resend', limit=5, window=60 * 60, extra_ident=user.id):
            return JsonResponse({'success': False, 'message': 'Too many OTP requests. Please try again later.'}, status=429)

        otp, message = create_and_send_otp(user)
        if otp:
            clear_otp_failures(user.id, 'email')
            return JsonResponse({'success': True, 'message': 'New OTP sent to your email!'})
        logger.warning("Resend OTP failed for user %s: %s", user.id, message)
        return JsonResponse({'success': False, 'message': 'Could not send the OTP. Please try again later.'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid user.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred.'})


# Profile Management
@login_required
def profile_edit(request):
    """Edit user profile (details + picture)."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form, 'quiz': daily_quiz_stats(request.user, recent=0)})


@login_required
@require_http_methods(["POST"])
def change_password(request):
    """Change user password (AJAX)."""
    form = PasswordChangeSimpleForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    old_pw = form.cleaned_data['old_password']
    new_pw = form.cleaned_data['new_password1']
    user = request.user

    if is_rate_limited(request, 'change-password', limit=10, window=15 * 60, extra_ident=user.pk):
        return JsonResponse({'success': False, 'message': 'Too many attempts. Please wait 15 minutes.'}, status=429)
    if not user.check_password(old_pw):
        return JsonResponse({'success': False, 'message': 'Current password is incorrect.'}, status=400)
    try:
        validate_password(new_pw, user=user)
    except ValidationError as exc:
        return JsonResponse({'success': False, 'message': ' '.join(exc.messages)}, status=400)

    user.set_password(new_pw)
    user.save()
    update_session_auth_hash(request, user)
    return JsonResponse({'success': True, 'message': 'Password updated successfully.'})

# Coupons
@login_required
def apply_coupon(request):
    """Apply and save a coupon for the authenticated user."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    if is_rate_limited(request, 'coupon', limit=15, window=15 * 60, extra_ident=request.user.pk):
        return JsonResponse({'success': False, 'message': 'Too many coupon attempts. Please wait a few minutes.'}, status=429)

    try:
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code', '').strip().upper()
        if not coupon_code:
            return JsonResponse({'success': False, 'message': 'Please enter a coupon code'})

        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code'})

        if not coupon.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'This coupon has expired or is no longer valid'
            })

        user_coupon, created = UserCoupon.objects.get_or_create(
            user=request.user,
            coupon=coupon,
            defaults={'assigned_at': timezone.now()}
        )

        if not created:
            return JsonResponse({
                'success': False,
                'message': 'You have already saved this coupon'
            })

        return JsonResponse({
            'success': True,
            'message': f'Coupon {coupon_code} saved successfully! You can now use it for discounts.'
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid data format'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})


@login_required
def my_coupons(request):
    """Retrieve and return user's saved coupons."""
    try:
        user_coupons = UserCoupon.objects.filter(
            user=request.user, is_used=False
        ).select_related('coupon')

        coupons_data = []
        current_time = timezone.now()

        for user_coupon in user_coupons:
            coupon = user_coupon.coupon
            is_expired = (
                current_time > coupon.valid_to or
                coupon.used_count >= coupon.usage_limit
            )
            coupons_data.append({
                'code': coupon.code,
                'description': coupon.description or '',
                'discount_display': coupon.get_discount_display(),
                'valid_to': coupon.valid_to.strftime('%d %b %Y'),
                'minimum_amount': float(coupon.minimum_amount),
                'usage_limit': coupon.usage_limit,
                'used_count': coupon.used_count,
                'is_expired': is_expired
            })

        return JsonResponse({'success': True, 'coupons': coupons_data})
    except Exception:
        return JsonResponse({'success': False, 'message': 'Error loading coupons'})

@require_GET
def search_suggestions(request):
    """
    AJAX endpoint for live search suggestions across categories, test series, courses,
    e-books and bundles. Typo-tolerant; see base/search.py.
    """
    query = request.GET.get('q', '').strip()[:100]
    if len(query) < 2:
        return JsonResponse({'suggestions': [], 'corrected': None, 'popular': POPULAR_SEARCHES})

    found = site_search(query, limit=8)
    suggestions = [
        {key: item.get(key) for key in ('type', 'name', 'url', 'price', 'thumbnail', 'category')}
        for item in found['results']
    ]
    return JsonResponse({
        'suggestions': suggestions,
        'corrected': found['corrected'],
        'popular': POPULAR_SEARCHES if not suggestions else [],
    })


SEARCH_RESULT_LIMIT = 60
POPULAR_SEARCHES = ['JEE Main', 'NEET UG', 'SSC CGL', 'CBSE Class 10', 'UPSC', 'Banking', 'Olympiad', 'Class 12 Science']



def search_results(request):
    """
    Full search results page
    """
    query = request.GET.get('q', '').strip()
    
    context = {
        'query': query,
        'categories': [],
        'video_courses': [],
        'live_courses': [],
        'test_series': [],
        'elibrary_courses': [],
        'product_bundles': [],
        'total_results': 0,
        'popular_searches': POPULAR_SEARCHES,
    }
    
    if query:
        found = site_search(query)
        context['corrected'] = found['corrected']
        ids = {}
        for item in found['results']:
            ids.setdefault(item['type'], []).append(item['pk'])

        def in_rank_order(queryset, kind, limit=None):
            wanted = ids.get(kind, [])[:limit]
            rows = queryset.in_bulk(wanted)
            return [rows[pk] for pk in wanted if pk in rows]

        categories = in_rank_order(Category.objects.all(), 'Category')
        video_courses = in_rank_order(VideoCourse.objects.select_related('category'), 'Video Course')
        live_courses = in_rank_order(LiveClassCourse.objects.select_related('category'), 'Live Class')
        elibrary_courses = in_rank_order(ELibraryCourse.objects.select_related('category'), 'E-Library')

        series_ids = ids.get('Test Series', [])
        test_series_total = len(series_ids)
        position = {pk: i for i, pk in enumerate(series_ids)}
        test_series = sorted(
            _series_cards(TestSeries.objects.filter(pk__in=series_ids[:SEARCH_RESULT_LIMIT]), request.user),
            key=lambda series: position[series.pk],
        )

        product_bundles = in_rank_order(
            ProductBundle.objects.select_related('category').prefetch_related(
                'video_courses', 'live_classes', 'test_series', 'elibrary_courses'
            ),
            'Bundle',
        )

        # Add calculated fields to bundles
        bundle_list = []
        for bundle in product_bundles:
            total_courses = (
                bundle.video_courses.count() +
                bundle.live_classes.count() +
                bundle.test_series.count() +
                bundle.elibrary_courses.count()
            )
            
            discount_percent = 0
            if bundle.original_price > 0:
                discount_percent = ((bundle.original_price - bundle.bundle_price) / bundle.original_price) * 100
            
            bundle.total_courses = total_courses
            bundle.discount_percent = discount_percent
            bundle_list.append(bundle)
        
        context['categories'] = categories
        context['video_courses'] = video_courses
        context['live_courses'] = live_courses
        context['test_series'] = test_series
        context['elibrary_courses'] = elibrary_courses
        context['product_bundles'] = bundle_list
        context['category_count'] = len(categories)
        context['video_course_count'] = len(video_courses)
        context['live_course_count'] = len(live_courses)
        context['test_series_count'] = test_series_total
        context['test_series_more'] = test_series_total > len(test_series)
        context['test_series_url'] = f"{reverse('all_test_series')}?q={quote(query)}"
        context['elibrary_course_count'] = len(elibrary_courses)
        context['total_results'] = (
            len(categories) +
            len(video_courses) +
            len(live_courses) +
            test_series_total +
            len(elibrary_courses) +
            len(bundle_list)
        )
    
    return render(request, 'search_results.html', context)



TEST_SERIES_SORTS = {
    'newest': ('Newest first', ['-created_at']),
    'popular': ('Most attempted', ['-total_attempts', '-created_at']),
    'class': ('Class (low to high)', ['grade', 'board', 'stream', 'title']),
    'price_low': ('Price: low to high', ['price', 'title']),
    'price_high': ('Price: high to low', ['-price', 'title']),
    'title': ('Name (A–Z)', ['title']),
}


def all_test_series(request):
    """Browse every active test series with search, board/class/stream/subject/level/price filters and sorting."""
    params = request.GET
    query = params.get('q', '').strip()
    exam = params.get('exam', '')
    board = params.get('board', '')
    grade = params.get('grade', '')
    stream = params.get('stream', '')
    subject = params.get('subject', '')
    difficulty = params.get('difficulty', '')
    price = params.get('price', '')
    paper = params.get('paper', '') if params.get('paper') in ('subject', 'pyp') else ''
    sort = params.get('sort', 'newest') if params.get('sort') in TEST_SERIES_SORTS else 'newest'

    series_qs = TestSeries.objects.filter(is_active=True)
    if query:
        series_qs = series_qs.filter(pk__in=ranked_ids(query, 'Test Series'))
    if exam:
        series_qs = series_qs.filter(exam=exam)
    if board in dict(TestSeries.BOARD_CHOICES):
        series_qs = series_qs.filter(board=board)
    if grade.isdigit():
        series_qs = series_qs.filter(grade=int(grade))
    if stream in dict(TestSeries.STREAM_CHOICES):
        series_qs = series_qs.filter(stream=stream)
    if subject:
        series_qs = series_qs.filter(
            pk__in=Question.objects.filter(test__is_active=True, subject__code=subject).values('test__test_series')
        )
    if difficulty in dict(TestSeries.DIFFICULTY_CHOICES):
        series_qs = series_qs.filter(difficulty=difficulty)
    if price == 'free':
        series_qs = series_qs.filter(is_free=True)
    elif price == 'paid':
        series_qs = series_qs.filter(is_free=False)
    if paper:
        series_qs = series_qs.filter(
            pk__in=Test.objects.filter(is_active=True, is_demo=False, paper_type=paper).values('test_series')
        )

    series_qs = series_qs.order_by(*TEST_SERIES_SORTS[sort][1])

    page_obj = Paginator(series_qs, 12).get_page(params.get('page'))
    page_obj.object_list = apply_counts(list(page_obj.object_list))

    purchased_ids = set()
    if request.user.is_authenticated:
        purchased_ids = set(
            UserCourseAccess.objects
            .filter(user=request.user, course_type='test_series', is_active=True)
            .values_list('course_id', flat=True)
        )
    for series in page_obj:
        series.price_display = "FREE" if series.is_free else f"₹{series.price:.2f}"
        series.is_purchased = series.id in purchased_ids

    active_filters = []
    labels = {
        'exam': exam or None,
        'board': dict(TestSeries.BOARD_CHOICES).get(board),
        'grade': f"Class {grade}" if grade.isdigit() else None,
        'stream': dict(TestSeries.STREAM_CHOICES).get(stream),
        'subject': Subject.objects.filter(code=subject).values_list('name', flat=True).first() if subject else None,
        'difficulty': dict(TestSeries.DIFFICULTY_CHOICES).get(difficulty),
        'price': {'free': 'Free', 'paid': 'Paid'}.get(price),
        'paper': {'subject': 'Has subject tests', 'pyp': 'Has previous year papers'}.get(paper),
        'q': f'"{query}"' if query else None,
    }
    for key, label in labels.items():
        if label:
            remaining = params.copy()
            remaining.pop(key, None)
            remaining.pop('page', None)
            active_filters.append({'label': label, 'remove_url': f"?{remaining.urlencode()}"})

    pagination_params = params.copy()
    pagination_params.pop('page', None)

    active_series = TestSeries.objects.filter(is_active=True)
    board_counts = dict(active_series.exclude(board='').values_list('board').annotate(n=Count('id')))
    context = {
        'page_obj': page_obj,
        'total_count': page_obj.paginator.count,
        'query': query,
        'selected': {
            'exam': exam, 'board': board, 'grade': grade, 'stream': stream, 'subject': subject,
            'difficulty': difficulty, 'price': price, 'paper': paper, 'sort': sort,
        },
        'board_options': [
            (value, label, board_counts[value])
            for value, label in TestSeries.BOARD_CHOICES
            if board_counts.get(value)
        ],
        'exam_options': list(
            active_series.exclude(exam='').values_list('exam').annotate(n=Count('id')).order_by('exam')
        ),
        'grade_options': sorted(set(active_series.exclude(grade__isnull=True).values_list('grade', flat=True))),
        'stream_options': TestSeries.STREAM_CHOICES,
        'subject_options': subject_options(),
        'difficulty_options': TestSeries.DIFFICULTY_CHOICES,
        'sort_options': [(key, label) for key, (label, _) in TEST_SERIES_SORTS.items()],
        'active_filters': active_filters,
        'pagination_query': pagination_params.urlencode(),
    }
    return render(request, 'all_test_series.html', context)


#category display

def category_detail(request, slug):
    """
    Display all courses (Video, Live Class, Test Series, E-Library) 
    under a specific category
    """
    category = get_object_or_404(Category, slug=slug)
    
    # Get all courses under this category
    video_courses = list(VideoCourse.objects.filter(
        category=category
    ).order_by('-created_at'))
    
    live_courses = list(LiveClassCourse.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at'))
    
    elibrary_courses = list(ELibraryCourse.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at'))

    # Test series are linked by exam name (e.g. 'SSC CGL'); board categories show that board's class-wise series
    board_codes = CATEGORY_BOARD_CODES.get(category.name)
    test_series_filter = Q(board__in=board_codes) if board_codes else Q(exam=category.name)
    test_series = _series_cards(
        TestSeries.objects.filter(test_series_filter, is_active=True).order_by('grade', 'stream', '-created_at'),
        request.user,
    )
    if board_codes:
        test_series_url = reverse('all_test_series') + (f"?board={board_codes[0]}" if len(board_codes) == 1 else '')
    else:
        test_series_url = reverse('all_test_series') + f"?exam={quote(category.name)}"

    # Count total courses
    total_courses = (
        len(video_courses) +
        len(live_courses) +
        len(test_series) +
        len(elibrary_courses)
    )
    
    context = {
        'category': category,
        'video_courses': video_courses,
        'live_courses': live_courses,
        'elibrary_courses': elibrary_courses,
        'test_series': test_series,
        'test_series_url': test_series_url,
        'test_total': sum(series.active_test_count for series in test_series),
        'question_total': sum(series.active_question_count for series in test_series),
        'demo_series_total': sum(1 for series in test_series if series.demo_count and not series.is_free),
        'total_courses': total_courses,
        'video_course_count': len(video_courses),
        'live_course_count': len(live_courses),
        'test_series_count': len(test_series),
        'elibrary_course_count': len(elibrary_courses),
    }
    return render(request, 'category_detail.html', context)

#Elibrary
def elibrary_home(request):
    """Display all e-library courses with filtering"""
    
    # Get featured and popular courses
    featured_courses = ELibraryCourse.objects.filter(
        is_active=True, 
        is_featured=True
    ).order_by('-created_at')[:8]
    
    # Get bestsellers
    bestseller_courses = ELibraryCourse.objects.filter(
        is_active=True,
        is_bestseller=True
    ).order_by('-enrollment_count')[:8]
    
    # Get all active courses
    all_courses = ELibraryCourse.objects.filter(
        is_active=True
    ).order_by('-created_at')
    
    context = {
        'featured_courses': featured_courses,
        'bestseller_courses': bestseller_courses,
        'all_courses': all_courses,
    }
    return render(request, 'elibrary/library.html', context)


def elibrary_course_detail(request, pk):
    """Display detailed information about a specific e-library course"""
    
    course = get_object_or_404(ELibraryCourse, pk=pk, is_active=True)
    
    # Check if user has purchased/has access to the course
    is_purchased = course.is_free
    access_expires_at = None
    
    if request.user.is_authenticated:
        # Check UserCourseAccess
        access = UserCourseAccess.objects.filter(
            user=request.user,
            course_id=course.id,
            course_type='elibrary',
            is_active=True
        ).first()
        
        if access and access.has_access:
            is_purchased = True
            access_expires_at = access.expires_at
    
    # Get PDFs organized by chapter
    pdfs = list(
        course.pdfs.filter(is_active=True).order_by('chapter_number', 'order')
    )
    
    # Get preview PDFs (free access)
    preview_pdfs = [pdf for pdf in pdfs if pdf.is_preview]
    
    # Organize PDFs by chapter
    chapters = {}
    for pdf in pdfs:
        if pdf.chapter_number not in chapters:
            chapters[pdf.chapter_number] = []
        chapters[pdf.chapter_number].append(pdf)
    
    context = {
        'course': course,
        'is_purchased': is_purchased,
        'access_expires_at': access_expires_at,
        'pdfs': pdfs,
        'preview_pdfs': preview_pdfs,
        'preview_pdf_count': len(preview_pdfs),
        'chapters': chapters,
        'total_chapters': len(chapters),
    }
    return render(request, 'elibrary/course_detail.html', context)



@login_required
def elibrary_view_pdf(request, pdf_id):
    """Stream a PDF after verifying preview, free-course, or purchase access."""
    pdf = get_object_or_404(
        ELibraryPDF.objects.select_related("course"),
        pk=pdf_id,
        is_active=True,
    )
    if not _user_can_access_elibrary_pdf(request.user, pdf):
        raise PermissionDenied("Purchase this course to view this PDF.")
    return _serve_elibrary_pdf(request, pdf, as_attachment=False)


@login_required
def elibrary_download_pdf(request, pdf_id):
    """Download a PDF after verifying course access."""
    pdf = get_object_or_404(
        ELibraryPDF.objects.select_related("course"),
        pk=pdf_id,
        is_active=True,
    )
    if not _user_can_access_elibrary_pdf(request.user, pdf):
        raise PermissionDenied("Purchase this course to download this PDF.")
    return _serve_elibrary_pdf(request, pdf, as_attachment=True)


def _user_can_access_elibrary_pdf(user, pdf):
    if pdf.is_preview or pdf.course.is_free:
        return True

    now = timezone.now()
    has_course_access = UserCourseAccess.objects.filter(
        user=user,
        course_id=pdf.course_id,
        course_type="elibrary",
        is_active=True,
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now)).exists()

    if has_course_access:
        return True

    return ELibraryEnrollment.objects.filter(
        user=user,
        course_id=pdf.course_id,
        payment_status="completed",
    ).exists()


def _serve_elibrary_pdf(request, pdf, *, as_attachment):
    try:
        pdf_file = pdf.file.open("rb")
    except Exception as exc:
        logger.error("Unable to open e-library PDF %s: %s", pdf.pk, exc)
        return HttpResponse(
            "This PDF is temporarily unavailable.",
            status=503,
            content_type="text/plain",
        )

    ELibraryDownload.objects.create(
        user=request.user,
        pdf=pdf,
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    ELibraryPDF.objects.filter(pk=pdf.pk).update(
        download_count=F("download_count") + 1
    )
    return FileResponse(
        pdf_file,
        content_type="application/pdf",
        as_attachment=as_attachment,
        filename=f"{pdf.title}.pdf",
    )


@login_required
def my_elibrary(request):
    """E-books the user can open: direct enrollments plus active purchases (including via bundles)."""
    now = timezone.now()
    access_ids = set(
        UserCourseAccess.objects.filter(user=request.user, course_type='elibrary', is_active=True)
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now))
        .values_list('course_id', flat=True)
    )
    enrolled_ids = set(
        ELibraryEnrollment.objects.filter(user=request.user, payment_status='completed').values_list('course_id', flat=True)
    )
    courses = (
        ELibraryCourse.objects.filter(pk__in=access_ids | enrolled_ids, is_active=True)
        .select_related('category')
        .order_by('title')
    )
    return render(request, 'elibrary/my_library.html', {'courses': courses})


def elibrary_category(request, category_slug):
    """Filter courses by category"""
    
    from video_courses.models import Category
    category = get_object_or_404(Category, slug=category_slug)
    
    courses = ELibraryCourse.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at')
    
    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'elibrary/category.html', context)




#Payment views

logger = logging.getLogger(__name__)

def get_razorpay_client():
    """Build a client from the active admin configuration or environment fallback."""
    config = RazorpayConfiguration.objects.filter(is_active=True).first()
    if config:
        key_id = config.key_id
        key_secret = config.key_secret
    else:
        key_id = settings.RAZORPAY_KEY_ID
        key_secret = settings.RAZORPAY_KEY_SECRET

    if not key_id or not key_secret:
        raise ValueError('Razorpay credentials are not configured.')

    return razorpay.Client(auth=(key_id, key_secret)), key_id

# ===== COURSE MODEL MAPPING =====
COURSE_MODELS = {
    'video_course': VideoCourse,
    'live_class': LiveClassCourse,
    'test_series': TestSeries,
    'elibrary': ELibraryCourse,
    'bundle': ProductBundle,
}


def get_course_model(course_type):
    """Get the model class for a course type"""
    return COURSE_MODELS.get(course_type)


def get_course_name(course, course_type):
    """
    Extract name from course based on type.
    Different models use different field names for the course name.
    """
    if course_type == 'video_course':
        return course.name if hasattr(course, 'name') else course.title
    elif course_type == 'live_class':
        return course.name
    elif course_type == 'test_series':
        return course.title
    elif course_type == 'elibrary':
        return course.title
    elif course_type == 'bundle':
        return course.title
    
    return str(course)


def get_course_price(course, course_type):
    """
    Extract price from course based on type.
    Returns tuple: (price, is_free)
    """
    # Check if course has is_free attribute
    is_free = getattr(course, 'is_free', False)
    
    if is_free:
        return 0, True
    
    # Different models use different price field names
    if course_type == 'video_course':
        return course.selling_price, False
    elif course_type == 'live_class':
        return course.current_price, False
    elif course_type == 'test_series':
        return course.price, False
    elif course_type == 'elibrary':
        return course.current_price, False
    elif course_type == 'bundle':
        return course.bundle_price, False
    
    return 0, False


def get_validity_days(course, course_type):
    """Get validity days for different course types"""
    if course_type == 'bundle':
        return course.validity_days
    # Add validity for other course types if needed
    return 365  # Default 1 year


def calculate_expiry_date(validity_days):
    """Calculate expiry date from validity days"""
    return timezone.now() + timedelta(days=validity_days)


# ===== PAYMENT ORDER CREATION =====

@login_required
def create_payment_order(request, course_type, course_id):
    """
    Create Razorpay order for course purchase.
    Works with video_course, live_class, test_series, elibrary, and bundle.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        # Validate course type
        course_model = get_course_model(course_type)
        if not course_model:
            return JsonResponse({
                'success': False, 
                'error': f'Invalid course type: {course_type}'
            }, status=400)
        
        # Get course details
        course = get_object_or_404(course_model, id=course_id)
        
        # Get course name
        course_name = get_course_name(course, course_type)
        
        # Get price and free status
        price, is_free = get_course_price(course, course_type)
        
        # Handle free courses/bundles - create access directly without payment
        if is_free:
            logger.info(f"Free enrollment: {course_type} - {course.id} by user {request.user.id}")
            
            # Get validity days and calculate expiry
            validity_days = get_validity_days(course, course_type)
            expires_at = calculate_expiry_date(validity_days)
            
            # Grant access immediately for free courses
            access, created = UserCourseAccess.objects.get_or_create(
                user=request.user,
                course_id=course.id,
                course_type=course_type,
                defaults={
                    'access_granted_at': timezone.now(),
                    'expires_at': expires_at,
                    'is_active': True
                }
            )
            
            if not created and not access.is_active:
                access.is_active = True
                access.access_granted_at = timezone.now()
                access.expires_at = expires_at
                access.save()
            
            # Handle specific course type enrollments for free items
            if course_type == 'elibrary':
                enrollment, _ = ELibraryEnrollment.objects.get_or_create(
                    user=request.user,
                    course=course,
                    defaults={
                        'payment_status': 'completed',
                        'amount_paid': 0
                    }
                )
                if not created:
                    enrollment.payment_status = 'completed'
                    enrollment.save()
            
            # Update bundle stats for free bundles
            elif course_type == 'bundle':
                course.current_enrollments += 1
                course.total_purchases += 1
                course.save(update_fields=['current_enrollments', 'total_purchases'])
            
            return JsonResponse({
                'success': True,
                'is_free': True,
                'message': f'Free {course_type.replace("_", " ")} access granted!',
                'course_name': course_name,
                'course_type': course_type,
                'course_id': course.id
            })
        
        # Calculate amount in paise (multiply by 100)
        amount_paise = int(float(price) * 100)
        
        if amount_paise <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid amount'}, status=400)
        
        # Create Razorpay order
        try:
            razorpay_client, razorpay_key_id = get_razorpay_client()
            order_data = {
                'amount': amount_paise,
                'currency': 'INR',
                'payment_capture': '1',  # Auto-capture
                'receipt': f'order_{course_type}_{course_id}_{request.user.id}_{int(timezone.now().timestamp())}'
            }
            
            razorpay_order = razorpay_client.order.create(order_data)
            razorpay_order_id = razorpay_order['id']
            
            logger.info(f"Razorpay order created: {razorpay_order_id} for {course_type} - {course_id}")
            
        except Exception as e:
            logger.error(f"Razorpay order creation failed: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': f'Order creation failed: {str(e)}'
            }, status=400)
        
        # Save payment record in DB
        try:
            payment = Payment.objects.create(
                user=request.user,
                razorpay_order_id=razorpay_order_id,
                course_type=course_type,
                course_id=course_id,
                course_name=course_name,
                amount=amount_paise,
                currency='INR',
                status='Pending'
            )
            logger.info(f"Payment record created: {payment.id} for order {razorpay_order_id}")
            
        except Exception as e:
            logger.error(f"Payment record creation failed: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': f'Database error: {str(e)}'
            }, status=400)
        
        # Get user phone if available
        user_phone = ''
        if hasattr(request.user, 'profile') and hasattr(request.user.profile, 'phone'):
            user_phone = request.user.profile.phone
        
        # Return checkout data
        return JsonResponse({
            'success': True,
            'is_free': False,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': razorpay_key_id,
            'amount': amount_paise,
            'currency': 'INR',
            'course_name': course_name,
            'course_type': course_type,
            'course_id': course.id,
            'user_name': request.user.get_full_name() or request.user.email,
            'user_email': request.user.email,
            'user_phone': user_phone
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in create_payment_order: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ===== PAYMENT VERIFICATION =====

@csrf_exempt
def payment_handler(request):
    """
    Handle Razorpay payment callback for all course types including bundles.
    Verifies payment signature and grants course access.
    Returns JSON response.
    """
    if request.method != "POST":
        return JsonResponse({
            'success': False, 
            'error': 'Invalid request',
            'type': 'error'
        }, status=400)
    
    try:
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        
        if not all([payment_id, order_id, signature]):
            return JsonResponse({
                'success': False,
                'error': 'Missing payment information',
                'type': 'error'
            }, status=400)
        
        # Fetch payment record
        try:
            payment = Payment.objects.get(razorpay_order_id=order_id)
        except Payment.DoesNotExist:
            logger.error(f"Payment record not found for order: {order_id}")
            return JsonResponse({
                'success': False,
                'error': 'Payment record not found',
                'type': 'error'
            }, status=404)
        
        # Verify signature
        try:
            razorpay_client, _ = get_razorpay_client()
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment signature verified: {payment_id}")
            
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"Payment signature verification failed: {str(e)}")
            payment.status = 'Failed'
            payment.save()
            
            return JsonResponse({
                'success': False,
                'error': 'Payment verification failed',
                'type': 'error'
            }, status=400)
        
        # Update payment status
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = 'Success'
        payment.save()
        
        logger.info(f"Payment status updated to Success: {payment_id}")
        
        # Get course to determine validity days and calculate expiry
        course_model = get_course_model(payment.course_type)
        if course_model:
            try:
                course = course_model.objects.get(id=payment.course_id)
                validity_days = get_validity_days(course, payment.course_type)
                expires_at = calculate_expiry_date(validity_days)
            except:
                validity_days = 365  # Default
                expires_at = calculate_expiry_date(validity_days)
        else:
            validity_days = 365  # Default
            expires_at = calculate_expiry_date(validity_days)
        
        # Grant course access - FIXED: Removed validity_days, use expires_at
        access, created = UserCourseAccess.objects.get_or_create(
            user=payment.user,
            course_id=payment.course_id,
            course_type=payment.course_type,
            defaults={
                'access_granted_at': timezone.now(),
                'expires_at': expires_at,
                'is_active': True
            }
        )
        
        if created:
            logger.info(f"Course access created for user {payment.user.id}: {payment.course_type} - {payment.course_id}")
        else:
            # If access already exists, make sure it's active
            if not access.is_active:
                access.is_active = True
                access.access_granted_at = timezone.now()
                access.expires_at = expires_at
                access.save()
                logger.info(f"Course access reactivated for user {payment.user.id}: {payment.course_type} - {payment.course_id}")
        
        # Handle specific course type enrollments after payment
        if payment.course_type == 'elibrary':
            try:
                course = ELibraryCourse.objects.get(id=payment.course_id)
                enrollment, enroll_created = ELibraryEnrollment.objects.get_or_create(
                    user=payment.user,
                    course=course,
                    defaults={
                        'payment_status': 'completed',
                        'amount_paid': payment.amount / 100,
                        'payment_id': payment_id
                    }
                )
                
                if not enroll_created:
                    enrollment.payment_status = 'completed'
                    enrollment.amount_paid = payment.amount / 100
                    enrollment.payment_id = payment_id
                    enrollment.save()
                
                # Update enrollment count
                course.enrollment_count += 1
                course.save()
                
                logger.info(f"eLibrary enrollment created for user {payment.user.id}: {course.title}")
            except Exception as e:
                logger.error(f"Failed to create eLibrary enrollment: {str(e)}")
        
        # Handle bundle purchase - update stats
        elif payment.course_type == 'bundle':
            try:
                bundle = ProductBundle.objects.get(id=payment.course_id)
                
                # Update bundle stats
                bundle.current_enrollments += 1
                bundle.total_purchases += 1
                bundle.save(update_fields=['current_enrollments', 'total_purchases'])
                
                logger.info(f"Bundle purchase recorded for user {payment.user.id}: {bundle.title}")
            except Exception as e:
                logger.error(f"Failed to update Bundle stats: {str(e)}")
        
        # Return JSON response
        return JsonResponse({
            'success': True,
            'type': 'success',
            'message': f'Payment successful! Access granted to {payment.course_name}',
            'payment_id': payment_id,
            'order_id': order_id,
            'course_name': payment.course_name,
            'course_type': payment.course_type,
            'course_id': payment.course_id,
            'amount': float(payment.amount / 100),
            'user': payment.user.get_full_name() or payment.user.email
        })
        
    except Exception as e:
        logger.error(f"Payment handler error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e),
            'type': 'error'
        }, status=500)


# ===== TUTOR (AI TEACHER CHAT) =====

TUTOR_HISTORY_LIMIT = 12        # messages sent upstream per request
TUTOR_MESSAGE_LIMIT = 2000      # characters per student message
TUTOR_HOURLY_LIMIT = {'user': 60, 'guest': 15}


def _tutor_rate_limited(request):
    """Count this request against an hourly allowance per user (or per IP for guests)."""
    if request.user.is_authenticated:
        key, limit = f"tutor-rate:u{request.user.pk}", TUTOR_HOURLY_LIMIT['user']
    else:
        key, limit = f"tutor-rate:ip{tutor.client_ip(request)}", TUTOR_HOURLY_LIMIT['guest']
    cache.add(key, 0, timeout=3600)
    try:
        count = cache.incr(key)
    except ValueError:  # expired between add and incr
        cache.set(key, 1, timeout=3600)
        count = 1
    return count > limit


@require_POST
def tutor_chat(request):
    """Relay a chat with Tutor to the AI provider (key stays on the server) and log the question."""
    try:
        payload = json.loads(request.body or b'{}')
    except ValueError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    messages_in = payload.get('messages')
    if not isinstance(messages_in, list) or not messages_in:
        return JsonResponse({'error': 'Send at least one message.'}, status=400)
    page = str(payload.get('page') or '')[:300]

    history = []
    for item in messages_in[-TUTOR_HISTORY_LIMIT:]:
        if not isinstance(item, dict):
            continue
        role = item.get('role')
        content = str(item.get('content', '')).strip()[:TUTOR_MESSAGE_LIMIT]
        if role in ('user', 'assistant') and content:
            history.append({'role': role, 'content': content})
    # The conversation sent upstream must start with the student and end with their new question.
    while history and history[0]['role'] != 'user':
        history.pop(0)
    if not history or history[-1]['role'] != 'user':
        return JsonResponse({'error': 'Send a question for Tutor.'}, status=400)
    question = history[-1]['content']

    config = tutor.load_settings()
    if not config.is_enabled or not config.effective_key:
        tutor.log_query(request, question, page, 'disabled')
        return JsonResponse({'error': 'Tutor is not available right now. Please try again later.'}, status=503)

    if _tutor_rate_limited(request):
        tutor.log_query(request, question, page, 'rate_limited')
        return JsonResponse(
            {'error': 'You have sent a lot of questions this hour. Please take a short break and try again.'},
            status=429,
        )

    if request.user.is_authenticated and request.user.first_name:
        history[-1] = {
            'role': 'user',
            'content': f"[The student's name is {request.user.first_name}.]\n{question}",
        }

    reply, usage, error, latency = tutor.timed_ask(config, history)
    if not reply:
        tutor.log_query(request, question, page, 'error', error=error, latency_ms=latency, model=config.model_name)
        message = ('Tutor is taking too long to answer. Please ask again.' if error == 'timeout'
                   else 'Tutor could not answer that. Please try again.')
        if request.user.is_authenticated and request.user.is_staff:
            message += f" (Admin only: {error or 'no reply'}. Check the key under Tutor AI.)"
        return JsonResponse({'error': message}, status=504 if error == 'timeout' else 502)

    tutor.log_query(request, question, page, 'ok', reply=reply, latency_ms=latency, usage=usage,
                    model=config.model_name)
    return JsonResponse({'reply': reply, 'suggestions': tutor.suggest_series(question)})


# ===== ERROR PAGES =====
# Self-contained templates (no navbar/DB tags) so they still render when the database is the problem.

ERROR_PAGES = {
    403: ('Access denied', "You don't have permission to open this page. If you bought this course, make sure you're logged in with the same account."),
    404: ('Page not found', "We couldn't find that page. It may have been moved, or the link may be mistyped."),
    429: ('Too many requests', "You're going a little fast. Please wait a few minutes and try again."),
    500: ('Something went wrong', "An unexpected error occurred on our side. Our team has been notified — please try again shortly."),
}


def _error_page(request, status):
    title, message = ERROR_PAGES[status]
    from adminpanel.branding import brand
    html = loader.render_to_string('errors/error.html', {'status': status, 'title': title, 'message': message, 'brand': brand()})
    return HttpResponse(html, status=status)


def error_403(request, exception=None):
    return _error_page(request, 403)


def error_404(request, exception=None):
    return _error_page(request, 404)


def error_500(request):
    return _error_page(request, 500)
