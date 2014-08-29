Django-Celery-Monitor
=====================

.. image:: https://api.travis-ci.org/LPgenerator/django-celery-mon.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/LPgenerator/django-celery-mon
.. image:: https://pypip.in/v/django-celery-mon/badge.png
    :alt: Current version on PyPi
    :target: https://crate.io/packages/django-celery-mon/
.. image:: https://pypip.in/d/django-celery-mon/badge.png
    :alt: Downloads from PyPi
    :target: https://crate.io/packages/django-celery-mon/


What's that
-----------
Simple app for monitoring Celery workers. If worker was die, supervisor process will be restarted.


Installation
------------

1. Using pip

.. code-block:: bash

    $ pip install django-celery-mon

2. Add the ``celerymon`` application to ``INSTALLED_APPS`` in your settings file (usually ``settings.py``)
3. Configure your celery settings. For example:

.. code-block:: python

    CELERY_DEFAULT_QUEUE = 'default'
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_SEND_EVENTS = True
    CELERY_TASK_RESULT_EXPIRES = 10
    CELERY_IGNORE_RESULT = True
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_ACKS_LATE = True
    CELERY_DISABLE_RATE_LIMITS = True
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_RESULT_BACKEND = BROKER_URL

    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
    CELERYD_PREFETCH_MULTIPLIER = 4

    CELERY_QUEUES = {
        'default': {"exchange": "default"},
        'mail': {"exchange": "mail"},
    }

4. Configure CeleryMon:

.. code-block:: python

    CELERY_MON_CELERY_WORKERS = ['default', 'mail']
    CELERY_MON_NOTIFICATION_ENABLED = True
    CELERY_MON_NOTIFICATION_EMAILS = ['root@local.host']

5. Configure supervisor (name of program should be equal into celery worker):

.. code-block:: bash

    [program:default]
    command=./manage.py celeryd -Q default -n default
    directory=/home/example.com/www
    stdout_logfile=/var/log/celery/default_worker.log
    stderr_logfile=/var/log/celery/default_worker.err.log

    [program:mail]
    command=./manage.py celeryd -Q mail -n mail
    directory=/home/example.com/www
    stdout_logfile=/var/log/celery/mail_worker.log
    stderr_logfile=/var/log/celery/mail_worker.err.log

6. Run Celery, Redis, Supervisor

.. code-block:: bash

    $ service redis restart
    $ service supervisor restart

7. Add to crontab

    SHELL=/bin/bash
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
    MAILTO=root@local.host
    PYTHON_BIN=/home/example.com/venv/bin/python
    MANAGE_PY=/home/lpgenerator.ru/www/manage.py
    LOGS_DIR=/var/log/celery
    
    */5 * * * * flock -n /dev/shm/celery_state.lock -c "$PYTHON_BIN $MANAGE_PY check_celery_state >> $LOGS_DIR/monitor.log"


Usage examples
--------------

.. code-block:: bash

    ./manage.py check_celery_state


Local demo installation
-----------------------

.. code-block:: bash

    $ sudo apt-get install virtualenvwrapper supervisor git-core
    $ mkvirtualenv django-celery-mon
    $ git clone https://github.com/LPgenerator/django-celery-mon.git
    $ cd django-celery-mon
    $ python setup.py develop
    $ pip install -r requirements/package.txt
    $ pip install -r requirements/tests.txt
    $ cd demo
    $ python manage.py syncdb --noinput
    $ cp supervisor/worker.conf /etc/supervisor/conf.d/
    $ sed -i "s'./manage.py'`which python` `pwd`/manage.py'g" /etc/supervisor/conf.d/worker.conf
    $ sed -i "s'/home/example.com/www'`pwd`'g" /etc/supervisor/conf.d/worker.conf
    $ /etc/init.d/supervisor stop; /etc/init.d/supervisor start
    $ supervisorctl -c /etc/supervisor/supervisord.conf status
    $ python manage.py check_celery_state
        # not you can stop some queue, check state and stop it, for checking by monitor
    $ supervisorctl -c /etc/supervisor/supervisord.conf stop mail
    $ supervisorctl -c /etc/supervisor/supervisord.conf status
    $ python manage.py check_celery_state
    $ supervisorctl -c /etc/supervisor/supervisord.conf status



Compatibility
-------------
* Python: 2.6, 2.7
* Django: 1.4, 1.5, 1.6
