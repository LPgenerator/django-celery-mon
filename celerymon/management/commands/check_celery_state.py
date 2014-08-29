import logging
import time
import os

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

import supervisor.xmlrpc
import xmlrpclib
import celery

from celerymon import defaults

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.app = celery.Celery(broker=settings.BROKER_URL)
        self.server = xmlrpclib.ServerProxy(
            defaults.MON_URI,
            transport=supervisor.xmlrpc.SupervisorTransport(
                defaults.MON_SERVER_USER, defaults.MON_SERVER_PASS,
                defaults.MON_SERVER_URL)
        )
        self.queue = None

    @staticmethod
    def send_mail(message):
        if defaults.MON_NOTIFICATION_ENABLED is True:
            send_mail(
                defaults.MON_NOTIFICATION_SUBJECT,
                message, settings.DEFAULT_FROM_EMAIL,
                defaults.MON_NOTIFICATION_EMAILS, fail_silently=True
            )
        logger.warning(message)

    def supervisor_exec(self, method, *args):
        try:
            return getattr(self.server.supervisor, method)(*args)
        except xmlrpclib.Fault:
            return None

    def queue_is_available(self):
        result = self.app.control.ping([self.queue])
        if result:
            return result[-1].get(self.queue) == {'ok': 'pong'}

    def worker_is_run(self):
        info = self.supervisor_exec('getProcessInfo', self.queue)
        if info and info.get('state') == 20:
            return True

    def worker_restart(self):
        self.supervisor_exec('stopProcess', self.queue)
        self.supervisor_exec('startProcess', self.queue)

    def notify_admins(self):
        self.send_mail('Queue "%s" was restarted.' % self.queue)

    def check_all_queues(self):
        for self.queue in settings.MON_CELERY_QUEUES.keys():
            if not self.queue_is_available() or not self.worker_is_run():
                self.worker_restart()
                self.notify_admins()

    def check_supervisor(self):
        if self.supervisor_exec('getState').get('statecode') != 1:
            os.system('service supervisor restart')
            self.send_mail('Supervisor is down')
            time.sleep(180)

    def handle(self, *args, **options):
        self.check_supervisor()
        self.check_all_queues()
