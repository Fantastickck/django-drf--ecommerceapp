
from django import template
from catalog.models import *

register = template.Library()

@register.simple_tag()
def filter(feature):
    features = Feature.objects.filter(name=feature)
    return features
