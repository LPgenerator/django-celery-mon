# Django settings for demo project.

import os

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('root', 'root@local.host'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite'),
    }
}

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'f969z_xc+^g*^gmt9oe7@og%kxd)54b!c!do)d7f2w2**f6%c0'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.i18n",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djcelery',
    'celerymon',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celerymon.management.commands.check_celery_state': {
            'handlers': ['mail_admins', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_MON_CELERY_WORKERS = ['default', 'mail']

try:
    from local_settings import *

except ImportError:
    pass

import djcelery
djcelery.setup_loader()
