from django import template

from adminpanel.permissions import can_manage_backups as _can_manage_backups

register = template.Library()


@register.filter
def can_manage_backups(user):
    return _can_manage_backups(user)
