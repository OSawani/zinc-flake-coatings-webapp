from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
import re

register = template.Library()

@register.filter(name='strip_html')
def strip_html(text):
    return strip_tags(text)


@register.filter(name='highlight')
def highlight(text, query):
    if not query:
        return text
    text = strip_tags(text)  # Strip HTML tags first
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    # Replace matches with <mark> tags
    highlighted_text = pattern.sub(
        lambda match: '<mark>{}</mark>'.format(match.group()), text)
    return mark_safe(highlighted_text)


@register.filter(name='contextual_highlight')
def contextual_highlight(text, query, context_length=100):
    if not query:
        return text

    text = strip_tags(text)  # Strip HTML tags first
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    matches = list(pattern.finditer(text))

    if not matches:
        return text

    snippets = []
    for match in matches:
        start = match.start()
        end = match.end()

        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)

        snippet = text[context_start:start] + '<mark>' + text[
                                                         start:end] + '</mark>' + text[
                                                                                  end:context_end]

        if context_start > 0:
            snippet = '...' + snippet
        if context_end < len(text):
            snippet = snippet + '...'

        snippets.append(snippet)

    return mark_safe(' '.join(snippets))
