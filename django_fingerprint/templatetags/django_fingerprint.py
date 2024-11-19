from __future__ import annotations

from django import template

from django_fingerprint.jinja import django_fingerprint_script

register = template.Library()
register.simple_tag(django_fingerprint_script)
