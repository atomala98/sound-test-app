from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)