# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase

import supervisor.xmlrpc
import xmlrpclib


class CeleryMonTestCase(TestCase):
    def test_a_is_down(self):
        server = xmlrpclib.ServerProxy(
            'http://127.0.0.1',
            transport=supervisor.xmlrpc.SupervisorTransport(
                None, None, 'unix:///var/run/supervisor.sock')
        )

        self.assertEquals(
            server.supervisor.getProcessInfo('default').get('state'), 20)
        self.assertEquals(
            server.supervisor.getProcessInfo('mail').get('state'), 20)

        server.supervisor.stopProcess('default')

        self.assertEquals(
            server.supervisor.getProcessInfo('default').get('state'), 0)
        self.assertEquals(
            server.supervisor.getProcessInfo('mail').get('state'), 20)

        call_command('check_celery_state')

        self.assertEquals(
            server.supervisor.getProcessInfo('default').get('state'), 20)
        self.assertEquals(
            server.supervisor.getProcessInfo('mail').get('state'), 20)
