from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def abs_url(context, str, *args, **kwargs):
    # Could add except for KeyError, if rendering the template
    # without a request available.
    # return context['request'].build_absolute_uri(
    #     reverse(view_name, args=args, kwargs=kwargs)
    # )
    return context['request'].build_absolute_uri(
        reverse(str, args=args, kwargs=kwargs)
    )
