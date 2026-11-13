from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, RegexValidator
from django.utils import timezone
from django.core.mail import get_connection, send_mail
from django.core.exceptions import ValidationError
from django.core.cache import cache
import string
import random
import os
import smtplib


def hex_to_rgb_str(hex_color, fallback=(37, 99, 235)):
    """Convert a '#rrggbb' (or '#rgb') string to an 'r, g, b' triplet for CSS custom properties."""
    hex_color = (hex_color or '').lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    try:
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}"
    except ValueError:
        return f"{fallback[0]}, {fallback[1]}, {fallback[2]}"


def _contrast(rgb_a, rgb_b):
    """WCAG contrast ratio between two (r, g, b) colors."""
    def luminance(rgb):
        r, g, b = (c / 255 for c in rgb)
        r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    hi, lo = sorted((luminance(rgb_a), luminance(rgb_b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


#notifications models

def default_backup_folder():
    from .branding import default_backup_folder as folder
    return folder()

class Notification(models.Model):
    title = models.CharField(max_length=200, help_text="Notification title")
    body = models.TextField(help_text="Notification message/content")
    link = models.URLField(max_length=500, blank=True, null=True, help_text="Optional link (leave empty if not needed)")
    scheduled_time = models.DateTimeField(help_text="When to show this notification")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='read_admin_notifications',
        help_text="Users who have marked this broadcast notification as read"
    )

    class Meta:
        ordering = ['-scheduled_time', '-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return self.title
    
    @property
    def is_scheduled(self):
        """Check if notification is scheduled for future"""
        return self.scheduled_time > timezone.now()
    



class DeveloperPopup(models.Model):
    """Model to manage the developer info popup displayed on first page load"""
    
    # Profile Information
    profile_image = models.ImageField(
        upload_to='developer/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Developer profile image. Recommended: 300x300px, max 1MB"
    )
    greeting_text = models.CharField(
        max_length=100,
        default="Greetings! I'm",
        help_text="Greeting message before developer name"
    )
    developer_name = models.CharField(
        max_length=200,
        help_text="Full name of the developer"
    )
    tagline = models.TextField(
        max_length=500,
        help_text="Brief description/tagline about the developer (max 500 characters)"
    )
    
    # Message Section
    message_title = models.CharField(
        max_length=200,
        default="I design professional websites!",
        help_text="Bold message title"
    )
    message_body = models.TextField(
        help_text="Main message body text"
    )
    
    # Contact Information
    email = models.EmailField(
        help_text="Developer email address"
    )
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    whatsapp_number = models.CharField(
        validators=[phone_validator],
        max_length=17,
        help_text="WhatsApp number with country code (e.g., 917905817391)"
    )
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        help_text="Full LinkedIn profile URL"
    )
    linkedin_display_text = models.CharField(
        max_length=200,
        default="Rudra Narayan Tiwari",
        help_text="Text to display for LinkedIn link"
    )
    
    # Footer Message
    footer_message = models.CharField(
        max_length=300,
        default="🚀 Looking forward to working with all of you!",
        help_text="Footer message displayed at bottom of popup"
    )
    
    # Display Settings
    is_active = models.BooleanField(
        default=True,
        help_text="Show/hide the popup on website"
    )
    delay_seconds = models.PositiveIntegerField(
        default=1,
        help_text="Delay in seconds before showing popup (default: 1 second)"
    )
    show_once_per_session = models.BooleanField(
        default=True,
        help_text="Show popup only once per browser session"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Developer Popup"
        verbose_name_plural = "Developer Popup Settings"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Developer Popup - {self.developer_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active popup exists
        if self.is_active:
            DeveloperPopup.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)





class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    )
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    usage_limit = models.PositiveIntegerField(default=1, help_text="Maximum number of times this coupon can be used")
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey('base.User', on_delete=models.CASCADE, related_name='created_coupons')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"

    def get_discount_display(self):
        if self.discount_type == 'percentage':
            return f"{self.discount_value}% off"
        return f"₹{self.discount_value} off"

    def is_valid(self):
        now = timezone.now()
        return (
            self.status == 'active'
            and self.valid_from <= now <= self.valid_to
            and self.used_count < self.usage_limit
        )

    def can_be_used(self, order_amount):
        return self.is_valid() and order_amount >= self.minimum_amount

    def calculate_discount(self, order_amount):
        if not self.can_be_used(order_amount):
            return 0
        if self.discount_type == 'percentage':
            discount = (order_amount * self.discount_value) / 100
            if self.maximum_discount and discount > self.maximum_discount:
                discount = self.maximum_discount
        else:
            discount = self.discount_value
        return min(discount, order_amount)

    def use_coupon(self):
        self.used_count += 1
        self.save(update_fields=['used_count'])

    @staticmethod
    def generate_coupon_code(length=8):
        letters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usage_history')
    user = models.ForeignKey('base.User', on_delete=models.CASCADE, null=True, blank=True, related_name='coupon_usages')
    order_id = models.CharField(max_length=100, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-used_at']

    def __str__(self):
        return f"{self.coupon.code} used on {self.used_at.date()}"


class UserCoupon(models.Model):
    user = models.ForeignKey('base.User', on_delete=models.CASCADE, related_name='user_coupons')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='user_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'coupon')
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.user.email} - {self.coupon.code}"


def banner_upload_path(instance, filename):
    return f'banners/{filename}'


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=banner_upload_path, help_text="Recommended size: 1920x800px")
    mobile_image = models.ImageField(
        upload_to=banner_upload_path,
        blank=True,
        null=True,
        help_text="Optional mobile-only banner. Recommended size: 750x400px. Falls back to the desktop image if left blank."
    )
    alt_text = models.CharField(max_length=200, help_text="Alternative text for accessibility")
    link_url = models.URLField(blank=True, help_text="Optional link when banner is clicked")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image files (from Dropbox or local disk) when the banner is deleted
        for image in (self.image, self.mobile_image):
            if image:
                try:
                    image.storage.delete(image.name)
                except Exception:
                    pass
        super().delete(*args, **kwargs)


def stat_icon_upload_path(instance, filename):
    """Custom upload path for stat card icons"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create new filename using the label
    filename = f"stat_icon_{instance.label.lower().replace(' ', '_')}.{ext}"
    return os.path.join('stat_icons/', filename)

class StatCard(models.Model):
    ICON_TYPE_CHOICES = [
        ('font_awesome', 'Font Awesome Icon'),
        ('image', 'Custom Image'),
    ]
    
    icon_type = models.CharField(
        max_length=20, 
        choices=ICON_TYPE_CHOICES, 
        default='font_awesome',
        help_text="Choose between Font Awesome icon or custom image"
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Font Awesome icon name (e.g., users, graduation-cap)"
    )
    icon_image = models.ImageField(
        upload_to=stat_icon_upload_path,
        blank=True,
        null=True,
        help_text="Upload custom icon image (.png, .jpg, .svg)"
    )
    icon_color = models.CharField(
        max_length=7,
        default='#007bff',
        help_text="Hex color code for Font Awesome icons (e.g., #007bff)"
    )
    number = models.CharField(
        max_length=50, 
        help_text="Statistic number (e.g., 4 Crore+)"
    )
    label = models.CharField(
        max_length=100, 
        help_text="Label text (e.g., Users)"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(
        default=0, 
        help_text="Display order (lower numbers first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        if self.icon_type == 'font_awesome':
            return f"FA:{self.icon} {self.number} {self.label}"
        else:
            return f"IMG:{self.icon_image.name if self.icon_image else 'No Image'} {self.number} {self.label}"

    @property
    def icon_color_rgb(self):
        """icon_color as an 'r, g, b' triplet, for use in the card's --stat-accent custom property."""
        return hex_to_rgb_str(self.icon_color or '#007bff')

    def get_icon_display(self):
        """Return appropriate icon display based on type"""
        if self.icon_type == 'font_awesome' and self.icon:
            return f'<i class="fas fa-{self.icon}" style="color: {self.icon_color};"></i>'
        elif self.icon_type == 'image' and self.icon_image:
            return f'<img src="{self.icon_image.url}" alt="{self.label}" style="width: 32px; height: 32px; object-fit: contain;">'
        else:
            return '<i class="fas fa-question-circle" style="color: #6c757d;"></i>'

    def clean(self):
        """Validate that appropriate icon is provided based on type"""
        from django.core.exceptions import ValidationError
        
        if self.icon_type == 'font_awesome' and not self.icon:
            raise ValidationError({'icon': 'Font Awesome icon name is required when icon type is Font Awesome.'})
        elif self.icon_type == 'image' and not self.icon_image:
            raise ValidationError({'icon_image': 'Icon image is required when icon type is Custom Image.'})


class CTASection(models.Model):
    title = models.CharField(max_length=200, help_text="Main CTA text")
    description = models.CharField(
        max_length=300, blank=True, help_text="Brief description or tagline for the call-to-action"
    )
    button_text = models.CharField(max_length=100, help_text="Button text")
    button_link = models.URLField(blank=True, help_text="Optional button link")
    button_color = models.CharField(
        max_length=7, default='#D7263D', help_text="Hex color code for the CTA button (e.g., #D4AF37)"
    )
    background_image = models.ImageField(
        upload_to='cta/', blank=True, null=True, help_text="Optional background image (recommended 1920x600px)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CTA Section"
        verbose_name_plural = "CTA Sections"

    def __str__(self):
        return self.title

    @property
    def button_color_rgb(self):
        """button_color as an 'r, g, b' triplet, for use in the button's shadow/hover styling."""
        return hex_to_rgb_str(self.button_color or '#D7263D', fallback=(215, 38, 61))

    @property
    def button_text_color(self):
        """Ink or white, whichever reads better on button_color."""
        rgb = tuple(int(c) for c in self.button_color_rgb.split(', '))
        return '#14141b' if _contrast(rgb, (20, 20, 27)) >= _contrast(rgb, (255, 255, 255)) else '#ffffff'


class AboutUsSection(models.Model):
    company_name = models.CharField(max_length=200, default="Edutrellis")
    heading = models.CharField(max_length=200, default="About Edutrellis")
    description = models.TextField(default="Online test series and mock tests for competitive and board exams. 10,000+ students trained.")
    logo = models.ImageField(upload_to='about/', blank=True, help_text="Company logo image")

    # Contact Information
    address = models.TextField(default="P-109, Prembagh, Shahpur, Chinhat, Lucknow, Uttar Pradesh 226028")
    email = models.EmailField(default="support@edutrellis.in")
    phone = models.CharField(max_length=50, default="+91 91941 30645")
    phone_hours = models.CharField(max_length=100, default="(Mon to Fri, 10 AM to 7 PM)")

    # Social Media Links
    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    telegram_url = models.URLField(blank=True, default="")

    # Map
    map_embed_url = models.TextField(
        blank=True,
        default="https://www.google.com/maps?q=P-109+Prembagh+Shahpur+Chinhat+Lucknow+Uttar+Pradesh+226028&output=embed",
        help_text="Google Maps embed URL"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Us Section"
        verbose_name_plural = "About Us Sections"

    def __str__(self):
        return f"About Us - {self.company_name}"


class WhyChooseUsItem(models.Model):
    icon_class = models.CharField(max_length=100, default="fa fa-user-circle", help_text="FontAwesome icon class")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title


class ServiceItem(models.Model):
    icon_class = models.CharField(max_length=100, default="fa fa-video-camera", help_text="FontAwesome icon class")
    service_name = models.CharField(max_length=200)
    service_description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.service_name


class ThemeSettings(models.Model):
    """Site-wide brand name and color. The name is used in page titles, emails, SEO and the admin panel."""
    site_name = models.CharField(
        max_length=60,
        default='Edutrellis',
        help_text="Short brand name shown in page titles, emails, the admin panel and search results."
    )
    site_full_name = models.CharField(
        max_length=120,
        default='Edutrellis',
        help_text="Full or legal name, used in the homepage title, search results and structured data."
    )
    primary_color = models.CharField(
        max_length=7,
        default='#D7263D',
        help_text="Main brand color used for buttons, links, and hover states across the site."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand & Theme Settings"
        verbose_name_plural = "Brand & Theme Settings"

    def __str__(self):
        return f"{self.site_name} ({self.primary_color})"

    @property
    def primary_color_rgb(self):
        return hex_to_rgb_str(self.primary_color, fallback=(215, 38, 61))

    @property
    def primary_color_dark(self):
        """A ~18% darker shade of primary_color, for hover/active states."""
        hex_color = (self.primary_color or '#D7263D').lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        try:
            r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            r, g, b = (215, 38, 61)
        r, g, b = (max(0, round(c * 0.82)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _rgb(self):
        return tuple(int(c) for c in self.primary_color_rgb.split(', '))

    @property
    def primary_color_text(self):
        """primary_color darkened until it reads as text on white (WCAG AA, 4.5:1)."""
        rgb = self._rgb()
        while _contrast(rgb, (255, 255, 255)) < 4.5:
            rgb = tuple(round(c * 0.94) for c in rgb)
        return '#%02x%02x%02x' % rgb

    @property
    def primary_color_on(self):
        """Text color for content placed on a primary_color background."""
        ink = (20, 20, 27)
        return '#14141b' if _contrast(self._rgb(), ink) >= _contrast(self._rgb(), (255, 255, 255)) else '#ffffff'

    def save(self, *args, **kwargs):
        if not self.pk and ThemeSettings.objects.exists():
            raise ValueError('Only one ThemeSettings instance allowed')
        super().save(*args, **kwargs)
        cache.delete("site-theme-settings-v2")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("site-theme-settings-v2")

    @classmethod
    def get_solo(cls):
        theme = cache.get("site-theme-settings-v2")
        if theme is None:
            theme, _ = cls.objects.get_or_create(pk=1)
            cache.set("site-theme-settings-v2", theme, 3600)
        return theme


class AuthPageSettings(models.Model):
    """Side images shown on the login and signup pages."""
    login_image = models.ImageField(
        upload_to='auth_pages/',
        blank=True,
        null=True,
        help_text="Side image for the login page. Recommended size: 1000x1200px. Falls back to the default image if left blank."
    )
    signup_image = models.ImageField(
        upload_to='auth_pages/',
        blank=True,
        null=True,
        help_text="Side image for the signup page. Recommended size: 1000x1200px. Falls back to the default image if left blank."
    )
    login_image_mobile = models.ImageField(
        upload_to='auth_pages/',
        blank=True,
        null=True,
        help_text="Optional wide image shown above the login form on phones and tablets. Recommended size: 1200x480px."
    )
    signup_image_mobile = models.ImageField(
        upload_to='auth_pages/',
        blank=True,
        null=True,
        help_text="Optional wide image shown above the signup form on phones and tablets. Recommended size: 1200x480px."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Login/Signup Page Settings"
        verbose_name_plural = "Login/Signup Page Settings"

    def __str__(self):
        return "Login/Signup Page Settings"

    def save(self, *args, **kwargs):
        if not self.pk and AuthPageSettings.objects.exists():
            raise ValueError('Only one AuthPageSettings instance allowed')
        super().save(*args, **kwargs)
        cache.delete("site-auth-page-settings-v1")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("site-auth-page-settings-v1")

    @classmethod
    def get_solo(cls):
        settings_obj = cache.get("site-auth-page-settings-v1")
        if settings_obj is None:
            settings_obj, _ = cls.objects.get_or_create(pk=1)
            cache.set("site-auth-page-settings-v1", settings_obj, 3600)
        return settings_obj


class NavbarSettings(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('call', 'Phone Call'),
    ]
    
    logo = models.ImageField(upload_to='navbar/', blank=True, null=True, help_text="Website logo")
    favicon = models.ImageField(upload_to='navbar/favicon/', blank=True, null=True, help_text="Website favicon (16x16 or 32x32 px)")
    logo_height = models.PositiveSmallIntegerField(
        default=34, validators=[MinValueValidator(16), MaxValueValidator(96)],
        help_text="Logo height on desktop, in pixels (16-96). Smaller laptop screens scale it down automatically.")
    logo_height_mobile = models.PositiveSmallIntegerField(
        default=26, validators=[MinValueValidator(16), MaxValueValidator(64)],
        help_text="Logo height on phones, in pixels (16-64).")
    contact_number = models.CharField(max_length=20, default="91941 30645", help_text="Contact phone number")
    contact_hours = models.CharField(max_length=50, default="(Mon-Fri, 10 AM-7 PM)", help_text="Contact hours")
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPE_CHOICES, default='whatsapp', help_text="Contact method type")
    search_placeholder = models.CharField(max_length=100, default="Search courses", help_text="Search box placeholder text")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Navbar Settings"
        verbose_name_plural = "Navbar Settings"

    def __str__(self):
        return "Navbar Settings"
    
    def get_contact_url(self):
        """Generate WhatsApp or Call URL based on contact_type"""
        # Remove any non-numeric characters from phone number
        clean_number = ''.join(filter(str.isdigit, self.contact_number))
        
        if self.contact_type == 'whatsapp':
            # WhatsApp Click-to-Chat format
            return f"https://wa.me/91{clean_number}?text=Hello%2C%20I%20would%20like%20to%20know%20more%20about%20your%20courses"
        else:
            # Phone Call format
            return f"tel:+91{clean_number}"
    
    def get_contact_icon(self):
        """Return appropriate Font Awesome icon class"""
        return 'fab fa-whatsapp' if self.contact_type == 'whatsapp' else 'fa fa-phone'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and NavbarSettings.objects.exists():
            raise ValueError('Only one NavbarSettings instance allowed')
        super().save(*args, **kwargs)
        cache.delete("site-navbar-settings-v3")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("site-navbar-settings-v3")



class FooterSettings(models.Model):
    logo = models.ImageField(upload_to='footer/', blank=True, null=True, help_text="Footer logo image")
    email = models.EmailField(default="support@edutrellis.in", help_text="Contact email")
    copyright_text = models.CharField(max_length=200, default="Copyright © 2026 Edutrellis. All rights reserved.")

    google_play_url = models.URLField(blank=True, default="https://play.google.com/store/apps", help_text="Google Play Store URL")
    app_store_url = models.URLField(blank=True, default="https://apps.apple.com/app", help_text="Apple App Store URL")

    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    telegram_url = models.URLField(blank=True, default="")

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"

    def __str__(self):
        return "Footer Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and FooterSettings.objects.exists():
            raise ValueError('Only one FooterSettings instance allowed')
        super().save(*args, **kwargs)
        cache.delete("site-footer-settings-v3")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("site-footer-settings-v3")


class FooterLink(models.Model):
    SECTION_CHOICES = [
        ('about', 'About'),
        ('help', 'Help'),
        ('student', 'Student'),
        ('business', 'Business'),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES, help_text="Footer section")
    title = models.CharField(max_length=100, help_text="Link title")
    url = models.CharField(max_length=200, help_text="Link URL (use # for placeholder)")
    order = models.IntegerField(default=0, help_text="Display order within section")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['section', 'order', 'title']
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return f"{self.get_section_display()} - {self.title}"


class FooterLegalLink(models.Model):
    title = models.CharField(max_length=100, help_text="Legal link title")
    url = models.CharField(max_length=200, help_text="Legal link URL")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Footer Legal Link"
        verbose_name_plural = "Footer Legal Links"

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    """Leads captured from the homepage 'Contact Us' form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at:%Y-%m-%d}"


class ExtraPage(models.Model):
    """Admin-editable static pages (Privacy Policy, Disclaimer, Refund Policy, Contact Us, etc.)."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, help_text="Used in the page URL, e.g. privacy-policy")
    content = models.TextField(help_text="Page content. Basic HTML tags are allowed.")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Extra Page"
        verbose_name_plural = "Extra Pages"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('extra_page_detail', args=[self.slug])


class SMTPConfiguration(models.Model):
    BACKEND_CHOICES = [
        ('django.core.mail.backends.smtp.EmailBackend', 'SMTP Backend'),
        ('django.core.mail.backends.console.EmailBackend', 'Console Backend (Development)'),
    ]

    name = models.CharField(max_length=100, default="Default SMTP")
    email_backend = models.CharField(max_length=200, choices=BACKEND_CHOICES, default='django.core.mail.backends.smtp.EmailBackend')
    email_host = models.CharField(max_length=200, default='smtp.gmail.com', help_text="SMTP server hostname")
    email_port = models.IntegerField(default=587, help_text="SMTP server port (587 for TLS, 465 for SSL)")
    email_use_tls = models.BooleanField(default=True, help_text="Use TLS encryption")
    email_use_ssl = models.BooleanField(default=False, help_text="Use SSL encryption")
    email_host_user = models.EmailField(help_text="Email address for authentication")
    email_host_password = models.CharField(max_length=200, help_text="Email password or app password")
    default_from_email = models.EmailField(help_text="Default sender email address")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_tested = models.DateTimeField(null=True, blank=True)
    test_status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ], default='pending')

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name = "SMTP Configuration"
        verbose_name_plural = "SMTP Configurations"

    def __str__(self):
        return f"{self.name} ({self.email_host_user})"

    def clean(self):
        if self.email_use_tls and self.email_use_ssl:
            raise ValidationError("Cannot use both TLS and SSL simultaneously")

        if self.is_active:
            # Ensure only one active configuration
            if SMTPConfiguration.objects.filter(is_active=True).exclude(pk=self.pk).exists():
                raise ValidationError("Only one SMTP configuration can be active at a time")

    def test_connection(self):
        """Test the SMTP connection and return result"""
        try:
            connection = get_connection(
                backend=self.email_backend,
                host=self.email_host,
                port=self.email_port,
                username=self.email_host_user,
                password=self.email_host_password,
                use_tls=self.email_use_tls,
                use_ssl=self.email_use_ssl,
            )

            # Test with a simple email
            result = send_mail(
                subject='SMTP Configuration Test',
                message='This is a test email to verify SMTP configuration.',
                from_email=self.email_host_user,
                recipient_list=[self.email_host_user],
                fail_silently=False,
                connection=connection
            )

            if result == 1:
                self.test_status = 'success'
                self.last_tested = timezone.now()
                self.save(update_fields=['test_status', 'last_tested'])
                return True, "SMTP configuration test successful!"
            else:
                self.test_status = 'failed'
                self.save(update_fields=['test_status'])
                return False, "Email sending failed"

        except smtplib.SMTPAuthenticationError:
            self.test_status = 'failed'
            self.save(update_fields=['test_status'])
            return False, "Authentication failed. Check your email and password."
        except smtplib.SMTPConnectError:
            self.test_status = 'failed'
            self.save(update_fields=['test_status'])
            return False, "Could not connect to SMTP server. Check host and port."
        except Exception as e:
            self.test_status = 'failed'
            self.save(update_fields=['test_status'])
            return False, f"Error: {str(e)}"


class RazorpayConfiguration(models.Model):
    """Razorpay API credentials managed from the custom admin panel."""

    name = models.CharField(max_length=100, default="Default Razorpay")
    key_id = models.CharField(max_length=100, help_text="Razorpay Key ID (for example, rzp_test_...)")
    key_secret = models.CharField(max_length=200, help_text="Razorpay Key Secret")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_active', '-updated_at']
        verbose_name = "Razorpay Configuration"
        verbose_name_plural = "Razorpay Configurations"

    def __str__(self):
        return f"{self.name} ({self.key_id})"

    @property
    def masked_secret(self):
        if not self.key_secret:
            return ""
        visible = self.key_secret[-4:] if len(self.key_secret) > 4 else ""
        return f"{'*' * 8}{visible}"


class DropboxConfiguration(models.Model):
    """Dropbox backup credentials managed by a super administrator."""

    name = models.CharField(max_length=100, default="Primary Dropbox")
    app_key = models.CharField(max_length=100)
    app_secret = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=500)
    backup_folder = models.CharField(max_length=255, default=default_backup_folder)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "-updated_at"]
        verbose_name = "Dropbox Configuration"
        verbose_name_plural = "Dropbox Configurations"

    def __str__(self):
        return f"{self.name} ({self.masked_app_key})"

    @staticmethod
    def _masked(value, visible=4):
        if not value:
            return "Not set"
        return f"{'•' * 8}{value[-visible:]}" if len(value) > visible else "•" * len(value)

    @property
    def masked_app_key(self):
        return self._masked(self.app_key)

    @property
    def masked_app_secret(self):
        return self._masked(self.app_secret)

    @property
    def masked_refresh_token(self):
        return self._masked(self.refresh_token, visible=6)




# bundles/models.py
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from video_courses.models import VideoCourse, Category
from live_class.models import LiveClassCourse
from testseries.models import TestSeries
from elibrary.models import ELibraryCourse
from base.models import User
import uuid


class ProductBundle(models.Model):
    """Main bundle model that groups multiple products together"""
    
    BUNDLE_TYPE_CHOICES = [
        ('mixed', 'Mixed Bundle'),
        ('video_only', 'Video Courses Only'),
        ('live_only', 'Live Classes Only'),
        ('test_only', 'Test Series Only'),
        ('elibrary_only', 'E-Library Only'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    description = models.TextField(help_text="Detailed description of the bundle")
    short_description = models.CharField(max_length=300, blank=True, help_text="Brief description for cards")
    
    # Bundle Type
    bundle_type = models.CharField(max_length=20, choices=BUNDLE_TYPE_CHOICES, default='mixed')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='bundles')
    
    # Media
    thumbnail = models.ImageField(upload_to='bundles/thumbnails/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='bundles/banners/', blank=True, null=True)
    
    # Pricing
    is_free = models.BooleanField(default=False, help_text="Check if this bundle is completely free")
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total original price of all included products",
        default=0
    )
    bundle_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Special bundle price (should be less than original)",
        default=0
    )
    currency = models.CharField(max_length=8, default="INR")
    
    # Products in Bundle
    video_courses = models.ManyToManyField(
        VideoCourse, 
        blank=True, 
        related_name='bundles',
        help_text="Select video courses to include"
    )
    live_classes = models.ManyToManyField(
        LiveClassCourse, 
        blank=True, 
        related_name='bundles',
        help_text="Select live class courses to include"
    )
    test_series = models.ManyToManyField(
        TestSeries, 
        blank=True, 
        related_name='bundles',
        help_text="Select test series to include"
    )
    elibrary_courses = models.ManyToManyField(
        ELibraryCourse, 
        blank=True, 
        related_name='bundles',
        help_text="Select e-library courses to include"
    )
    
    # Features & Benefits
    features = models.TextField(
        blank=True,
        help_text="One feature per line, will be displayed as bullet points"
    )
    
    # Validity
    validity_days = models.PositiveIntegerField(
        default=365,
        help_text="Number of days the bundle is valid after purchase"
    )
    start_date = models.DateField(blank=True, null=True, help_text="Bundle availability start date")
    end_date = models.DateField(blank=True, null=True, help_text="Bundle availability end date")
    
    # Status & Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_bestseller = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0, help_text="Lower number = higher priority")
    
    # Limits
    max_enrollments = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Maximum number of students who can purchase (leave empty for unlimited)"
    )
    current_enrollments = models.PositiveIntegerField(default=0)
    
    # Analytics
    total_views = models.PositiveIntegerField(default=0)
    total_purchases = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_bundles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Product Bundle'
        verbose_name_plural = 'Product Bundles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:270]
        
        # If bundle is free, set prices to 0
        if self.is_free:
            self.original_price = 0
            self.bundle_price = 0
            
        super().save(*args, **kwargs)
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.is_free:
            return 100
        if self.original_price > 0:
            discount = ((self.original_price - self.bundle_price) / self.original_price) * 100
            return round(discount, 0)
        return 0
    
    @property
    def total_products(self):
        """Count total products in bundle"""
        return (
            self.video_courses.count() + 
            self.live_classes.count() + 
            self.test_series.count() + 
            self.elibrary_courses.count()
        )
    
    @property
    def is_available(self):
        """Check if bundle is currently available for purchase"""
        from django.utils import timezone
        now = timezone.now().date()
        
        if self.status != 'active':
            return False
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        if self.max_enrollments and self.current_enrollments >= self.max_enrollments:
            return False
        
        return True
    
    @property
    def savings_amount(self):
        """Calculate total savings"""
        if self.is_free:
            return self.calculate_original_price()
        return self.original_price - self.bundle_price
    
    @property
    def current_price(self):
        """Return current price (0 if free, bundle_price otherwise)"""
        return 0 if self.is_free else self.bundle_price
    
    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []
    
    def calculate_original_price(self):
        """Auto-calculate original price based on included products"""
        total = 0
        
        # Video courses
        for course in self.video_courses.all():
            total += course.selling_price
        
        # Live classes
        for live_class in self.live_classes.all():
            total += live_class.current_price
        
        # Test series
        for test in self.test_series.all():
            if not test.is_free:
                total += test.price
        
        # E-Library courses
        for elibrary in self.elibrary_courses.all():
            total += elibrary.current_price
        
        return total
    



class AdminAuditLog(models.Model):
    """Who changed what in the management area, plus staff logins and failed logins."""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('login_failed', 'Failed login'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    user_email = models.CharField(max_length=254, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='other', db_index=True)
    method = models.CharField(max_length=8, blank=True)
    path = models.CharField(max_length=500, blank=True)
    view_name = models.CharField(max_length=120, blank=True)
    object_id = models.CharField(max_length=64, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Audit log entry"
        verbose_name_plural = "Audit log"

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.user_email or 'anonymous'} {self.action} {self.path}"


# ===================== TUTOR (AI TEACHER) =====================

NVIDIA_CHAT_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_TUTOR_MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b"


class TutorSettings(models.Model):
    """Single row: the AI provider key and behaviour of the Tutor chat widget, editable in the admin panel."""

    is_enabled = models.BooleanField(default=True, help_text="Turn the Tutor chat on or off for the whole site.")
    api_url = models.URLField(default=NVIDIA_CHAT_URL, help_text="OpenAI-compatible chat completions endpoint.")
    api_key = models.CharField(max_length=300, blank=True, help_text="Provider API key (NVIDIA keys start with nvapi-).")
    model_name = models.CharField(max_length=150, default=DEFAULT_TUTOR_MODEL)
    max_tokens = models.PositiveIntegerField(default=1200, validators=[MinValueValidator(100)])
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.6)
    enable_thinking = models.BooleanField(
        default=False, help_text="Let the model reason before answering. Slower, but better for hard maths.")
    auto_greet = models.BooleanField(
        default=True, help_text="Pop up a prompt asking visitors what they want to study, once per visit.")
    greeting = models.CharField(max_length=200, default="What are you preparing for today?")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    CACHE_KEY = 'tutor-settings'

    class Meta:
        verbose_name = "Tutor settings"
        verbose_name_plural = "Tutor settings"

    def __str__(self):
        return f"Tutor settings ({self.model_name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(self.CACHE_KEY)

    @classmethod
    def load(cls):
        """The settings row (created on first use), cached for a minute."""
        obj = cache.get(cls.CACHE_KEY)
        if obj is None:
            obj = cls.objects.first() or cls.objects.create()
            cache.set(cls.CACHE_KEY, obj, 60)
        return obj

    @property
    def effective_key(self):
        """The admin-panel key, or the TUTOR_API_KEY environment variable as a fallback."""
        return self.api_key or getattr(settings, 'TUTOR_API_KEY', '')

    @property
    def masked_key(self):
        key = self.effective_key
        if not key:
            return ''
        return f"{key[:6]}{'•' * 10}{key[-4:]}" if len(key) > 12 else '•' * len(key)


class TutorQuery(models.Model):
    """One question asked to Tutor: who asked, what, from which page, and how it went."""

    STATUS_CHOICES = [
        ('ok', 'Answered'),
        ('error', 'Error'),
        ('rate_limited', 'Rate limited'),
        ('disabled', 'Tutor off'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='tutor_queries')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page = models.CharField(max_length=300, blank=True)
    question = models.TextField()
    reply = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ok', db_index=True)
    error = models.CharField(max_length=300, blank=True)
    latency_ms = models.PositiveIntegerField(default=0)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    model_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tutor question"
        verbose_name_plural = "Tutor questions"

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.question[:60]}"
