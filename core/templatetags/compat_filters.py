"""Compatibility template filters for third-party apps."""

from __future__ import annotations

from django import template

register = template.Library()


@register.filter(name="length_is")
def length_is(value, arg) -> bool:
    """Return ``True`` when the length of *value* equals *arg*.

    This restores the ``length_is`` filter that was removed from Django 5.1.
    ``Jazzmin`` still references this filter in its templates, so we provide a
    drop-in replacement that mimics the original behaviour. The implementation
    intentionally mirrors Django's historic behaviour, including handling
    ``None`` values and coercing the argument to an integer.
    """

    if value is None:
        return False

    try:
        length = len(value)
    except TypeError:
        return False

    try:
        target_length = int(arg)
    except (TypeError, ValueError):
        return False

    return length == target_length
