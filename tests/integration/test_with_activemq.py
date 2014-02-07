import os

from pymco.test import ctxt

from . import base


class ActiveMQTestCase(base.IntegrationTestCase):
    '''RabbitMQ integration test case.'''
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
    }


class TestWithActiveMQMCo20x(base.MCollective20x, ActiveMQTestCase):
    '''MCollective integration test case.'''


class TestWithActiveMQMCo22x(base.MCollective22x, ActiveMQTestCase):
    '''MCollective integration test case.'''


class TestWithActiveMQMCo23x(base.MCollective23x, ActiveMQTestCase):
    '''MCollective integration test case.'''


class TestWithActiveMQSSLMCo23x(base.MCollective23x, ActiveMQTestCase):
    '''MCollective integration test case.'''
    CTXT = {
        'plugin.activemq.pool.1.port': 61615,
        'plugin.activemq.pool.1.password': 'marionette',
        'plugin.activemq.pool.1.ssl': 'true',
        'plugin.activemq.pool.1.ssl.ca':  os.path.join(ctxt.ROOT,
                                                       'fixtures/ca.pem'),
        'plugin.activemq.pool.1.ssl.key': os.path.join(
            ctxt.ROOT,
            'fixtures/activemq_private.pem'),
        'plugin.activemq.pool.1.ssl.cert': os.path.join(
            ctxt.ROOT,
            'fixtures/activemq_cert.pem',
        ),
    }
