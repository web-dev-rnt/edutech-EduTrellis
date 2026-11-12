"""
Typo-tolerant site search.

The catalogue is small (a few hundred courses/series/categories), so every searchable
item is kept in a cached in-memory index and ranked in Python. That lets us:
  * normalise input  - "class1 1st", "std 1", "Class I", "first class" all mean class 1
  * correct typos    - "mathmatics olympaid" -> "mathematics olympiad"
  * match numbers exactly - "class 1" never matches Class 10/11/12
  * rank by where the words appear (title beats category beats description)
"""
import difflib
import math
import re

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

INDEX_CACHE_KEY = "site-search-index-v2"
INDEX_TIMEOUT = 60 * 30

STOPWORDS = {"the", "a", "an", "of", "for", "and", "in", "to", "with", "on", "online", "me", "my", "i"}
ORDINAL_SUFFIXES = {"st", "nd", "rd", "th"}
SYNONYMS = {
    "std": "class", "standard": "class", "grade": "class", "cls": "class", "clas": "class", "classes": "class",
    "kaksha": "class", "maths": "math", "mathematics": "math", "sci": "science", "eng": "english",
    "bio": "biology", "chem": "chemistry", "phy": "physics", "gk": "general", "olympiyad": "olympiad",
    "tests": "test", "mocks": "mock", "papers": "paper", "pyq": "previous", "pyqs": "previous",
    "ebook": "ebook", "ebooks": "ebook", "notes": "notes", "navodaya": "jnvst",
}
NUMBER_WORDS = {
    "one": "1", "first": "1", "two": "2", "second": "2", "three": "3", "third": "3", "four": "4", "fourth": "4",
    "five": "5", "fifth": "5", "six": "6", "sixth": "6", "seven": "7", "seventh": "7", "eight": "8",
    "eighth": "8", "nine": "9", "ninth": "9", "ten": "10", "tenth": "10", "eleven": "11", "eleventh": "11",
    "twelve": "12", "twelfth": "12",
}
ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7", "viii": "8",
         "ix": "9", "x": "10", "xi": "11", "xii": "12"}

ALIAS_WORDS = sorted(set(SYNONYMS) | set(NUMBER_WORDS))

TITLE_WEIGHT, TAG_WEIGHT, TEXT_WEIGHT = 3.0, 1.5, 0.5
TYPE_ORDER = {"Category": 0, "Test Series": 1, "Video Course": 2, "Live Class": 3, "E-Library": 4, "Bundle": 5}


def tokenize(text):
    """Lower-case, split letters from digits, map synonyms/ordinals/roman numerals, drop stopwords."""
    text = re.sub(r"[^a-z0-9]+", " ", str(text or "").lower())
    text = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", text)
    raw = text.split()
    tokens = []
    for i, word in enumerate(raw):
        prev = tokens[-1] if tokens else ""
        if word in ORDINAL_SUFFIXES and i and raw[i - 1].isdigit():
            continue  # "1st" -> "1"
        if word in ROMAN and prev == "class":
            word = ROMAN[word]  # "class xii" -> "class 12"
        word = NUMBER_WORDS.get(word, word)
        word = SYNONYMS.get(word, word)
        if word in STOPWORDS:
            continue
        tokens.append(word)
    return tokens


def _unique(tokens):
    seen, out = set(), []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


# ── index ───────────────────────────────────────────────────────────────────

def _file_url(field):
    try:
        return field.url if field else None
    except ValueError:
        return None


def _build_index():
    from adminpanel.models import ProductBundle
    from elibrary.models import ELibraryCourse
    from live_class.models import LiveClassCourse
    from testseries.models import TestSeries
    from testseries.exam_tools import EXAM_GROUPS
    from video_courses.models import Category, VideoCourse

    # "banking", "railway", "defence"... -> every exam in that Explore Exams group.
    group_tags = {}
    for slug, label, _icon, exams in EXAM_GROUPS:
        for exam in exams:
            group_tags[exam.lower()] = f"{label} {slug.replace('-', ' ')}"

    items = []

    def add(kind, pk, name, url, tags="", text="", **extra):
        items.append({
            "type": kind, "pk": pk, "name": name, "url": url,
            "title_tokens": set(tokenize(name)),
            "tag_tokens": set(tokenize(tags)),
            "text_tokens": set(tokenize(str(text or "")[:400])),
            **extra,
        })

    for c in Category.objects.only("pk", "name", "slug", "description"):
        if c.slug:
            add("Category", c.pk, c.name, f"/category/{c.slug}/", f"exam category {group_tags.get(c.name.lower(), '')}", c.description,
                price="", thumbnail=None, category="Exam Category")

    boards = dict(TestSeries.BOARD_CHOICES)
    for s in TestSeries.objects.filter(is_active=True).only(
        "pk", "title", "description", "exam", "board", "grade", "stream", "is_free", "price", "thumbnail"
    ):
        tags = " ".join(filter(None, [
            s.exam, group_tags.get((s.exam or "").lower(), ""), boards.get(s.board, ""),
            f"class {s.grade}" if s.grade else "", s.stream, "test series mock",
        ]))
        add("Test Series", s.pk, s.title, f"/exam-series/{s.pk}/", tags, s.description,
            price="Free" if s.is_free else f"₹{s.price:,.0f}", thumbnail=_file_url(s.thumbnail),
            category=s.exam or boards.get(s.board, "") or "Test Series")

    for v in VideoCourse.objects.select_related("category").only(
        "pk", "name", "description", "selling_price", "is_free", "thumbnail", "category__name"
    ):
        cat = v.category.name if v.category else ""
        add("Video Course", v.pk, v.name, f"/course/{v.pk}/", f"{cat} video course", v.description,
            price="Free" if v.is_free else f"₹{v.selling_price:,.0f}", thumbnail=_file_url(v.thumbnail),
            category=cat or "Video Course")

    for lc in LiveClassCourse.objects.filter(is_active=True).select_related("category"):
        cat = lc.category.name if lc.category else ""
        add("Live Class", lc.pk, lc.name, f"/live-class/{lc.pk}/", f"{cat} live class {lc.language}", lc.about,
            price="Free" if lc.is_free else f"₹{lc.current_price:,.0f}", thumbnail=_file_url(lc.banner_image_desktop),
            category=cat or "Live Class")

    for e in ELibraryCourse.objects.filter(is_active=True).select_related("category"):
        cat = e.category.name if e.category else ""
        add("E-Library", e.pk, e.title, f"/ebook/{e.pk}/", f"{cat} ebook notes pdf library",
            f"{e.short_description or ''} {e.description or ''}",
            price="Free" if e.is_free else f"₹{e.current_price:,.0f}", thumbnail=_file_url(e.cover_image),
            category=cat or "E-Library")

    for b in ProductBundle.objects.filter(status="active").select_related("category"):
        cat = b.category.name if b.category else ""
        add("Bundle", b.pk, b.title, f"/bundle/{b.slug}/", f"{cat} bundle combo package",
            f"{b.short_description or ''} {b.description or ''}",
            price="Free" if b.is_free else f"₹{b.bundle_price:,.0f}", thumbnail=_file_url(b.thumbnail),
            category=cat or "Bundle")

    vocab = set()
    for item in items:
        vocab |= item["title_tokens"] | item["tag_tokens"]
    return {"items": items, "vocab": sorted(t for t in vocab if not t.isdigit())}


def get_index():
    index = cache.get(INDEX_CACHE_KEY)
    if index is None:
        index = _build_index()
        cache.set(INDEX_CACHE_KEY, index, INDEX_TIMEOUT)
    return index


def clear_index(**kwargs):
    cache.delete(INDEX_CACHE_KEY)


def connect_signals():
    from adminpanel.models import ProductBundle
    from elibrary.models import ELibraryCourse
    from live_class.models import LiveClassCourse
    from testseries.models import TestSeries
    from video_courses.models import Category, VideoCourse

    for model in (Category, TestSeries, VideoCourse, LiveClassCourse, ELibraryCourse, ProductBundle):
        post_save.connect(clear_index, sender=model, dispatch_uid=f"search-index-{model.__name__}-save")
        post_delete.connect(clear_index, sender=model, dispatch_uid=f"search-index-{model.__name__}-delete")


# ── querying ────────────────────────────────────────────────────────────────

def _correct(token, vocab, vocab_set):
    """Return (token to search with, whether it was changed)."""
    if token.isdigit() or token in vocab_set:
        return token, False
    if any(v.startswith(token) for v in vocab) and len(token) >= 2:
        return token, False  # user is still typing ("chemi")
    cutoff = 0.7 if len(token) >= 5 else 0.75
    match = difflib.get_close_matches(token, vocab + ALIAS_WORDS, n=1, cutoff=cutoff)
    if not match:
        return token, False
    fixed = match[0]
    return NUMBER_WORDS.get(fixed, SYNONYMS.get(fixed, fixed)), True


def _token_score(token, tokens):
    if token in tokens:
        return 1.0
    if token.isdigit():
        return 0.0
    if len(token) >= 2 and any(t.startswith(token) for t in tokens):
        return 0.8
    return 0.0


def search(query, types=None, limit=None):
    """
    Rank indexed items for a free-text query.
    Returns {"results": [item, ...], "corrected": "did-you-mean text" or None}.
    """
    index = get_index()
    vocab = index["vocab"]
    vocab_set = set(vocab)
    raw = _unique(tokenize(query))
    if not raw:
        return {"results": [], "corrected": None}

    tokens, changed = [], False
    for t in raw:
        fixed, was_changed = _correct(t, vocab, vocab_set)
        tokens.append(fixed)
        changed |= was_changed
    tokens = _unique(tokens)
    phrase = " ".join(tokens)

    scored = []
    for item in index["items"]:
        if types and item["type"] not in types:
            continue
        total, matched = 0.0, 0
        for t in tokens:
            best = max(
                _token_score(t, item["title_tokens"]) * TITLE_WEIGHT,
                _token_score(t, item["tag_tokens"]) * TAG_WEIGHT,
                # Numbers ("class 1") only count in titles/tags; descriptions mention "1 hour" etc.
                0.0 if t.isdigit() else _token_score(t, item["text_tokens"]) * TEXT_WEIGHT,
            )
            if best:
                matched += 1
                total += best
        if not matched:
            continue
        title = " ".join(tokenize(item["name"]))
        if phrase and phrase in title:
            total += 2.0  # the words appear together, in order, in the title
        if item["title_tokens"] and set(tokens) >= item["title_tokens"]:
            total += 1.0  # query names the item exactly
        scored.append((matched, total, item))

    needed = len(tokens)
    results = [s for s in scored if s[0] == needed]
    if not results and needed > 1:
        # Nothing matches every word: fall back to items matching most of them.
        needed = max(1, math.ceil(needed * 0.6))
        results = [s for s in scored if s[0] >= needed]

    results.sort(key=lambda s: (-s[0], -s[1], TYPE_ORDER.get(s[2]["type"], 9), s[2]["name"]))
    items = [s[2] for s in results]
    if limit:
        items = items[:limit]
    return {"results": items, "corrected": phrase if changed and items else None}


def ranked_ids(query, kind):
    """Primary keys of one content type, best match first."""
    return [item["pk"] for item in search(query, types={kind})["results"]]
