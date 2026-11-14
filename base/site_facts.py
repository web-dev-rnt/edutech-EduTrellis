"""Plain facts about the site for search engines and AI assistants.

One source for the home page FAQ (and its FAQPage structured data) and /llms.txt, so what people read,
what Google indexes and what ChatGPT/Claude/Perplexity/Gemini summarise always agree. Numbers are live.
"""
from urllib.parse import quote

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse

from adminpanel.branding import brand
from adminpanel.context_processors import (
    PARENT_NAME, PARENT_SITES, PARENT_URL, SITE_ADDRESS, SITE_CEO_EMAIL, SITE_EMAIL, SITE_PHONE_DISPLAY,
    SITE_STUDENTS_TRAINED, SITE_SUPPORT_HOURS,
)

# Well-known exams, listed by name when the site has a series for them (checked against the database).
MAJOR_EXAMS = [
    "SSC CGL", "SSC CHSL", "SSC MTS", "SSC GD", "SBI PO", "SBI Clerk", "IBPS PO", "IBPS Clerk", "RRB NTPC",
    "RRB Group D", "UPSC CSE", "JEE Main", "JEE Advanced", "NEET UG", "CUET UG", "NDA", "CDS", "CTET", "UPTET",
    "UP Police Constable",
]
FACTS_CACHE_KEY = "site-facts-v1"


def _indian(n):
    from adminpanel.templatetags.banner_tags import _indian_number

    return _indian_number(n)


def site_domain():
    return settings.SITE_URL.split("://", 1)[-1].rstrip("/")


def numbers():
    """Live catalogue numbers (cached with the home page stats)."""
    from adminpanel.templatetags.banner_tags import _test_series_stats

    values = {key: stat["value"] for key, stat in zip(("series", "tests", "questions", "exams"), _test_series_stats())}
    return {key: _indian(value) for key, value in values.items()}


def exams_covered():
    """(major exams that have a series, boards with series) — names only, cached for an hour."""
    data = cache.get(FACTS_CACHE_KEY)
    if data is None:
        from testseries.models import TestSeries

        active = TestSeries.objects.filter(is_active=True)
        have = set(active.filter(exam__in=MAJOR_EXAMS).values_list("exam", flat=True))
        exams = [name for name in MAJOR_EXAMS if name in have]
        board_names = dict(TestSeries._meta.get_field("board").choices)
        boards = [(code, board_names.get(code, code.upper()))
                  for code in active.exclude(board="").values_list("board", flat=True).distinct().order_by("board")]
        data = (exams, boards)
        cache.set(FACTS_CACHE_KEY, data, 3600)
    return data


def faq():
    """[(question, answer)] shown on the home page and in /llms.txt (plain text answers)."""
    site_brand = brand()
    name, full_name = site_brand["name"], site_brand["full_name"]
    n = numbers()
    exams, boards = exams_covered()
    exam_examples = ", ".join(exams[:10]) if exams else "SSC, Banking, Railways, JEE and NEET"
    board_examples = ", ".join(label for _, label in boards[:6]) if boards else "CBSE, ICSE and state boards"
    family = ", ".join(site[0] for site in PARENT_SITES[1:])
    return [
        (f"What is {full_name}?",
         f"{full_name} ({site_domain()}) is the official online test series website of {PARENT_NAME} "
         f"({PARENT_URL.split('://')[1].rstrip('/')}), based in Lucknow, Uttar Pradesh. It offers exam-pattern mock tests, "
         f"previous year papers with step-by-step solutions, instant results and an all-India rank. "
         f"{SITE_STUDENTS_TRAINED} students have trained with {name}."),
        (f"Which exams does {name} have test series for?",
         f"{n.get('series', 'Hundreds of')} test series with {n.get('tests', 'thousands of')} mock and practice tests and "
         f"{n.get('questions', 'lakhs of')} questions with solutions, covering {n.get('exams', 'over a thousand')} exams and "
         f"boards. These include {exam_examples}, and school boards such as {board_examples}."),
        ("Can I try a test for free?",
         "Yes. Every test series includes a free demo test, and the home page has a free daily quiz. "
         "No payment is needed to start practising."),
        ("How are results and ranks shown?",
         "As soon as you submit a test you see your score, accuracy, step-by-step solutions for every question and "
         "your all-India rank among everyone who took the same test. All attempts are saved under My Results."),
        (f"Can I use {name} on my phone?",
         f"Yes. The website works on every phone, tablet and computer, and you can install it as an app from your "
         f"browser with the Install App button for quicker access."),
        (f"How do I contact {name}?",
         f"Call or WhatsApp {SITE_PHONE_DISPLAY} ({SITE_SUPPORT_HOURS}), email {SITE_EMAIL}, or write to the CEO at "
         f"{SITE_CEO_EMAIL}. Address: {SITE_ADDRESS}."),
        (f"Who runs {full_name}?",
         f"{full_name} is run by {PARENT_NAME} ({PARENT_URL}), a Lucknow company that also runs {family}."),
    ]


def faq_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{settings.SITE_URL}/#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq()
        ],
    }


def llms_txt():
    """The /llms.txt file (https://llmstxt.org): a Markdown summary of the site for AI assistants."""
    from adminpanel.models import ExtraPage

    site_brand = brand()
    name, full_name = site_brand["name"], site_brand["full_name"]
    url = settings.SITE_URL.rstrip("/")
    n = numbers()
    exams, boards = exams_covered()
    series_url = url + reverse("all_test_series")
    lines = [
        f"# {full_name}",
        "",
        f"> {full_name} ({url}/) is the official online test series website of {PARENT_NAME} ({PARENT_URL}), "
        f"Lucknow, India: exam-pattern mock tests, previous year papers with step-by-step solutions, instant results "
        f"and all-India rank for competitive and board exams. {SITE_STUDENTS_TRAINED} students trained.",
        "",
        "## About",
        f"- Name: {full_name} (also written {name} Exams, {name} Online Test Series)",
        f"- Website: {url}/",
        f"- Part of: {PARENT_NAME}, {PARENT_URL} (Lucknow, Uttar Pradesh, India)",
        f"- What it offers: online test series and mock tests, previous year papers (PYQs), sectional and full-length "
        f"tests, instant results, step-by-step solutions, all-India rank, a free daily quiz and a free demo test in every series",
        f"- Catalogue: {n.get('series')} test series, {n.get('tests')} mock and practice tests, {n.get('questions')} "
        f"questions with solutions, {n.get('exams')} exams and boards",
        f"- Students trained: {SITE_STUDENTS_TRAINED}",
        f"- Phone / WhatsApp: {SITE_PHONE_DISPLAY} ({SITE_SUPPORT_HOURS})",
        f"- Support email: {SITE_EMAIL}",
        f"- CEO email: {SITE_CEO_EMAIL}",
        f"- Address: {SITE_ADDRESS}",
        "",
        "## Main pages",
        f"- [Home]({url}/): test series highlights, free daily quiz, about {name} and contact details",
        f"- [All test series]({series_url}): browse and filter every test series by exam, board, class, subject and price",
    ]
    if exams:
        lines += ["", "## Popular exams"]
        lines += [f"- [{exam} test series]({series_url}?exam={quote(exam)})" for exam in exams]
    if boards:
        lines += ["", "## School boards"]
        lines += [f"- [{label} test series]({series_url}?board={code})" for code, label in boards]
    pages = list(ExtraPage.objects.filter(is_active=True).order_by("title").values_list("title", "slug"))
    if pages:
        lines += ["", "## Policies and information"]
        lines += [f"- [{title}]({url}{reverse('extra_page_detail', args=[slug])})" for title, slug in pages]
    lines += ["", f"## Other {PARENT_NAME} websites"]
    lines += [f"- [{site_name}]({site_url}): {note}" for site_name, site_url, _, note in PARENT_SITES]
    lines += ["", "## Frequently asked questions"]
    for question, answer in faq():
        lines += [f"### {question}", answer, ""]
    return "\n".join(lines).rstrip() + "\n"
