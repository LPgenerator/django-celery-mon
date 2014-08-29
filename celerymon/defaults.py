# -*- encoding: utf-8 -*-

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


MON_URI = get_settings('CELERY_MON_URI', 'http://127.0.0.1')
MON_SERVER_URL = get_settings(
    'CELERY_MON_SERVER_URL', 'unix:///var/run/supervisor.sock')
MON_SERVER_USER = get_settings('CELERY_MON_SERVER_USER', None)
MON_SERVER_PASS = get_settings('CELERY_MON_SERVER_PASS', None)

MON_NOTIFICATION_SUBJECT = get_settings(
    'CELERY_MON_NOTIFICATION_SUBJECT', '[celery] worker restart')
MON_NOTIFICATION_ENABLED = get_settings(
    'CELERY_MON_NOTIFICATION_ENABLED', True)
MON_NOTIFICATION_EMAILS = get_settings(
    'CELERY_MON_NOTIFICATION_EMAILS', [n[1] for n in settings.ADMINS])

MON_CELERY_WORKERS = get_settings(
    'CELERY_MON_CELERY_WORKERS', ['default'])
