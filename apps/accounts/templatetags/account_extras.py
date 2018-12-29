from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def add_class(field, css_class):
    css_class = field.css_classes(css_class)
    return field.as_widget(attrs={'class':css_class})

@register.filter
def li_to_br(text_with_li):
    return '<br>'.join(map(strip_tags, text_with_li.split('</li><li>')))
