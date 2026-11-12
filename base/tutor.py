"""Tutor, the AI teacher chat: provider call, test-series suggestions and request logging.

The provider is any OpenAI-compatible chat completions API (NVIDIA by default). The key, model and options
come from adminpanel.TutorSettings, which admins edit in the management area.
"""
import logging
import re
import time

import requests
from django.db.models import Q
from django.urls import reverse

from adminpanel.models import TutorQuery, TutorSettings
from testseries.models import TestSeries

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are Tutor, the AI teacher on {brand}, an Indian learning platform whose main product is "
    "online test series: exam-pattern mock tests with instant results and solutions for school boards (CBSE, "
    "ICSE, UP Board, NIOS and state boards) and competitive exams (JEE, NEET, SSC, banking, railways, defence, "
    "UPSC and more).\n"
    "How to answer:\n"
    "- Teach patiently, step by step, in simple language with short examples. Keep replies brief unless the "
    "student asks for detail.\n"
    "- Use Markdown: short paragraphs, bullet or numbered lists, **bold** for key terms. Write maths in plain "
    "text (for example 2x + 5 = 17, x² , √2, 3/4); do not use LaTeX.\n"
    "- If the student writes in Hindi or Hinglish, reply in the same way.\n"
    "- When the student asks what to study, which test to take or how to prepare, give a short plan and "
    "suggest practising with the site's test series (all series: /test-series/). Matching series are shown to "
    "the student automatically under your reply, so do not invent series names, prices or links.\n"
    "- Never mention any other product, company or AI model name. If asked who made you, say you are Tutor "
    "from {brand}.\n"
    "- Politely decline requests unrelated to studies, careers or exams."
)

def system_prompt():
    from adminpanel.branding import brand_name
    return SYSTEM_PROMPT.replace('{brand}', brand_name())


THINK_RE = re.compile(r'<think>.*?</think>\s*', re.S)

# Words that say nothing about which series the student wants.
STOPWORDS = set("""
a an the and or of in on to for with by from at is are am be was were it this that these those i me my we you your
he she they them our us what which who whom how why when where can could should would will shall do does did done
please help want need give make show tell explain solve step steps simply simple about some any all more most best
good list find suggest recommend start started get got prepare preparing preparation study studying learn learning
test tests series mock mocks practice practise paper papers exam exams question questions quiz online free demo
plan day days month months year years hindi english today now new top topic chapter chapters subject subjects mcq mcqs
""".split())


def client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    ip = forwarded.split(',')[0].strip() or request.META.get('REMOTE_ADDR', '')
    return ip or None


def ask_provider(config, history):
    """Send the chat to the provider. Returns (reply, usage dict, error message)."""
    payload = {
        'model': config.model_name,
        'messages': [{'role': 'system', 'content': system_prompt()}] + history,
        'max_tokens': config.max_tokens,
        'temperature': float(config.temperature),
        'top_p': 0.95,
        'stream': False,
        'chat_template_kwargs': {'enable_thinking': bool(config.enable_thinking)},
    }
    try:
        response = requests.post(
            config.api_url,
            json=payload,
            headers={'Authorization': f'Bearer {config.effective_key}', 'Accept': 'application/json'},
            timeout=90,
        )
    except requests.Timeout:
        return None, {}, 'timeout'
    except requests.RequestException as exc:
        logger.warning("Tutor provider request failed: %s", exc)
        return None, {}, 'network error'

    try:
        data = response.json()
    except ValueError:
        data = {}
    if not response.ok:
        detail = data.get('detail') or data.get('error') or data.get('title') or response.text[:200]
        if isinstance(detail, dict):
            detail = detail.get('message', str(detail))
        logger.error("Tutor provider HTTP %s: %s", response.status_code, detail)
        return None, {}, f"HTTP {response.status_code}: {detail}"[:300]

    try:
        content = data['choices'][0]['message'].get('content') or ''
    except (KeyError, IndexError, TypeError, AttributeError):
        content = data.get('reply') or ''  # older relay format
    reply = THINK_RE.sub('', content).strip()
    if not reply:
        return None, data.get('usage') or {}, 'empty reply'
    return reply, data.get('usage') or {}, ''


def suggest_series(text, limit=3):
    """Up to `limit` active test series whose titles best match the student's words."""
    lowered = text.lower()
    words = [w for w in re.findall(r'[a-z]+', lowered) if len(w) >= 3 and w not in STOPWORDS]
    phrases = [f"class {n}" for n in re.findall(r'class\s*(\d{1,2})\b', lowered)]
    terms = list(dict.fromkeys(phrases + words))[:8]
    if not terms:
        return []

    query = Q()
    for term in terms:
        query |= Q(title__icontains=term) | Q(exam__iexact=term)
    candidates = (
        TestSeries.objects.filter(query, is_active=True)
        .only('id', 'title', 'is_free', 'price', 'total_tests', 'exam')[:300]
    )
    scored = []
    for series in candidates:
        title = series.title.lower()
        score = sum(2 if ' ' in term else 1 for term in terms if term in title or term == (series.exam or '').lower())
        if score:
            scored.append((score, series.total_tests, series))
    if not scored:
        return []
    best = max(s for s, _, _ in scored)
    # Keep only strong matches so a single common word doesn't pull in unrelated series.
    floor = best if best >= 2 else 1
    scored = [item for item in scored if item[0] >= floor]
    scored.sort(key=lambda item: (-item[0], -item[1]))
    return [
        {
            'title': series.title,
            'url': reverse('front_exam_series_detail', args=[series.pk]),
            'tests': series.total_tests,
            'price': 'Free' if series.is_free or not series.price else f"₹{series.price:,.0f}",
        }
        for _, _, series in scored[:limit]
    ]


def log_query(request, question, page, status, reply='', error='', latency_ms=0, usage=None, model=''):
    usage = usage or {}
    try:
        TutorQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip_address=client_ip(request),
            page=(page or '')[:300],
            question=question[:4000],
            reply=reply[:8000],
            status=status,
            error=error[:300],
            latency_ms=latency_ms,
            prompt_tokens=usage.get('prompt_tokens') or 0,
            completion_tokens=usage.get('completion_tokens') or 0,
            model_name=model[:150],
        )
    except Exception:  # logging must never break the chat
        logger.exception("Could not log Tutor query")


def timed_ask(config, history):
    started = time.monotonic()
    reply, usage, error = ask_provider(config, history)
    return reply, usage, error, int((time.monotonic() - started) * 1000)


def load_settings():
    return TutorSettings.load()
