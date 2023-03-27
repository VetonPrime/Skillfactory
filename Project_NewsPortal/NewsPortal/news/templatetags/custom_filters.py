from django import template
from ..models import CONTENTS

register = template.Library()


@register.filter()
def censor(value):
    bad_words = [
        'редиска',
        'дурак'
    ]

    for word in bad_words:
        if word in value.lower():
            end_world = ''.join(['*' for _ in word[1:-1]]) + word[-1]
            value = value.replace(word, word[0] + end_world)
            value = value.replace(word.title(), word[0].title() + end_world)

    return value


@register.filter()
def content_new(value):
    for i, j in CONTENTS:
        if i == value:
            return j
