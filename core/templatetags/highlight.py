from django import template
import re

register = template.Library()


@register.filter(name='highlight')
def highlight(text, query):
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda match: '<mark>{}</mark>'.format(match.group()),
                       text)


@register.filter(name='contextual_highlight')
def contextual_highlight(text, query, context_length=100):
    if not query:
        return text

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    matches = pattern.finditer(text)

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

    return ' '.join(snippets)
