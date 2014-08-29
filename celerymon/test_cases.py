# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase
from django.core import mail

import supervisor.xmlrpc
import xmlrpclib


class CeleryMonTestCase(TestCase):
    def setUp(self):
        server = xmlrpclib.ServerProxy(
            'http://127.0.0.1',
            transport=supervisor.xmlrpc.SupervisorTransport(
                None, None, 'unix:///var/run/supervisor.sock')
        )
        server.supervisor.stopProcess('default')

    def test_a_is_down(self):
        call_command('check_celery_state')
        self.assertEquals(len(mail.outbox), 1)

    def test_b_is_work(self):
        call_command('check_celery_state')
        self.assertEquals(len(mail.outbox), 0)
