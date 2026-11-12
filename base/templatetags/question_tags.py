import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

FENCE = re.compile(r"```[a-zA-Z]*\n(.*?)\n?```", re.S)


@register.filter
def question_html(text):
    """Question text as safe HTML: escaped, line breaks kept, and ```code``` blocks shown as monospace with indentation."""
    text = str(text or '')
    parts, last = [], 0
    for match in FENCE.finditer(text):
        parts.append(escape(text[last:match.start()]).strip('\n').replace('\n', '<br>'))
        parts.append(f'<pre class="q-code">{escape(match.group(1))}</pre>')
        last = match.end()
    parts.append(escape(text[last:]).strip('\n').replace('\n', '<br>'))
    return mark_safe(''.join(p for p in parts if p))
