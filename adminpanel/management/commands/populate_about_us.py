# adminpanel/management/commands/populate_about_us.py
from django.core.management.base import BaseCommand
from adminpanel.models import AboutUsSection, WhyChooseUsItem, ServiceItem

class Command(BaseCommand):
    help = 'Populate default About Us data'
    
    def handle(self, *args, **options):
        # Create default About Us section
        about_us, created = AboutUsSection.objects.get_or_create(
            defaults={
                'company_name': 'Edutrellis',
                'heading': 'About Edutrellis',
                'description': '''Edutrellis is an online test series platform that has trained 10,000+ students for competitive and board exams.
Our exam-pattern mock tests, previous year papers, instant results and detailed solutions help students build speed, accuracy and confidence before the real exam.''',
                'address': 'P-109, Prembagh, Shahpur, Chinhat, Lucknow, Uttar Pradesh 226028',
                'email': 'support@edutrellis.in',
                'phone': '+91 91941 30645',
                'phone_hours': '(Mon to Fri, 10 AM to 7 PM)',
                'facebook_url': '',
                'twitter_url': '',
                'linkedin_url': '',
                'instagram_url': '',
                'telegram_url': '',
                'map_embed_url': 'https://www.google.com/maps?q=P-109+Prembagh+Shahpur+Chinhat+Lucknow+Uttar+Pradesh+226028&output=embed',
            }
        )
        
        # Create default Why Choose Us items
        why_choose_items = [
            {
                'icon_class': 'fa fa-user-circle',
                'title': '10,000+ students trained',
                'description': '<b>10,000+ students trained</b> for competitive and board exams',
                'order': 1
            },
            {
                'icon_class': 'fa fa-magic',
                'title': 'Proven exam results',
                'description': '<b>Proven exam results:</b> Thousands of toppers every year',
                'order': 2
            },
            {
                'icon_class': 'fa fa-thumbs-up',
                'title': 'Shortest path to selection',
                'description': '<b>Shortest path to selection</b> – with analytics & improvements',
                'order': 3
            },
            {
                'icon_class': 'fa fa-star',
                'title': 'Highest-rated platform',
                'description': '<b>Highest-rated platform/app</b> among students',
                'order': 4
            },
            {
                'icon_class': 'fa fa-shield',
                'title': '100% safe & ad-free',
                'description': '<b>100% safe & ad-free</b> learning environment',
                'order': 5
            },
        ]
        
        for item_data in why_choose_items:
            WhyChooseUsItem.objects.get_or_create(
                title=item_data['title'],
                defaults=item_data
            )
        
        # Create default Service items
        service_items = [
            {
                'icon_class': 'fa fa-video-camera',
                'service_name': 'Live & Interactive Classes',
                'service_description': 'Learn from top educators in real-time with two-way doubt resolution and personal mentoring.',
                'order': 1
            },
            {
                'icon_class': 'fa fa-file-text',
                'service_name': 'Extensive Test Series',
                'service_description': 'Mock exams, practice sets, PYQs, and AI-powered analytics for targeted competitive exam prep.',
                'order': 2
            },
            {
                'icon_class': 'fa fa-book',
                'service_name': 'E-Books & E-Library',
                'service_description': 'Downloadable, exam-focused e-books, summaries, and revision notes—anywhere, anytime.',
                'order': 3
            },
            {
                'icon_class': 'fa fa-bar-chart',
                'service_name': 'Personalized Analytics',
                'service_description': 'Smart progress reports, benchmarking, and improvement suggestions unique to every learner.',
                'order': 4
            },
            {
                'icon_class': 'fa fa-mobile',
                'service_name': 'Anytime, Anywhere Access',
                'service_description': 'Mobile apps and web for seamless learning across all your devices.',
                'order': 5
            },
        ]
        
        for item_data in service_items:
            ServiceItem.objects.get_or_create(
                service_name=item_data['service_name'],
                defaults=item_data
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated About Us data')
        )
