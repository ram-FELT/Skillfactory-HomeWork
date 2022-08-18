from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    low = value.lower()
    CENSORED_WORDS = {'редиска'}
    for i in CENSORED_WORDS:
        if i.find(low):
            low = value.replace(i[1:5:], "*" * len(i))
    return f'{low}'
