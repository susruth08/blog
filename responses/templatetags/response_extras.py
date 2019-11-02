from django import template
register = template.Library()

@register.filter(name='likes_count')
def likes_count(res):
    return res.filter(liked=True,disliked=False).count()

@register.filter(name='dislikes_count')
def dislikes_count(res):
    return res.filter(liked=False,disliked=True).count()
