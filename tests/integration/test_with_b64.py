import os

from pymco.test import ctxt
from . import base

FIXTURES_PATH = os.path.join(ctxt.ROOT, 'fixtures')


class Base64TestCase(base.IntegrationTestCase):
    '''ActiveMQ integration test case.'''
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
        'plugin.activemq.pool.1.base64': 'yes'
    }

class TestWithBase64MCo20x(base.MCollective20x, Base64TestCase):
    '''MCollective integration test case.'''


class TestWithBase64MCo22x(base.MCollective22x, Base64TestCase):
    '''MCollective integration test case.'''


class TestWithBase64MCo23x(base.MCollective23x, Base64TestCase):
    '''MCollective integration test case.'''


class TestWithBase64MCo24x(base.MCollective24x, Base64TestCase):
    """MCollective integration test case."""

