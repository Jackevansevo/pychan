from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter(name='addClass')
def addClass(value, newClass):
    try:
        current_classes = value.field.widget.attrs["class"]
        new_classes = current_classes + " " + newClass
        value.field.widget.attrs["class"] = mark_safe(new_classes)
    except KeyError:
        value.field.widget.attrs["class"] = newClass
    return value
