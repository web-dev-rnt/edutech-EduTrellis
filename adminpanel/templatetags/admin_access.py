from django import template

from adminpanel.permissions import is_site_owner as _is_site_owner

register = template.Library()


@register.filter
def is_site_owner(user):
    return _is_site_owner(user)


@register.filter
def can_manage_backups(user):
    return _is_site_owner(user)
