import os

from pymco.test import ctxt

from . import base


class RabbitMQTestCase(base.IntegrationTestCase):
    '''RabbitMQ integration test case.'''
    CTXT = {
        'connector': 'rabbitmq',
        'plugin.rabbitmq.vhost': '/mcollective',
        'plugin.rabbitmq.pool.size': '1',
        'plugin.rabbitmq.pool.1.host': 'localhost',
        'plugin.rabbitmq.pool.1.port': '61613',
        'plugin.rabbitmq.pool.1.user': 'mcollective',
        'plugin.rabbitmq.pool.1.password': 'marionette',
    }


class TestWithRabbitMQMCo22x(base.MCollective22x, RabbitMQTestCase):
    '''MCollective integration test case.'''


class TestWithRabbitMQMCo23x(base.MCollective23x, RabbitMQTestCase):
    '''MCollective integration test case.'''


class TestWithRabbitMQSSLMCo23x(base.MCollective23x, RabbitMQTestCase):
    """MCollective integration test case."""
    CTXT = {
        'connector': 'rabbitmq',
        'plugin.rabbitmq.vhost': '/mcollective',
        'plugin.rabbitmq.pool.size': '1',
        'plugin.rabbitmq.pool.1.host': 'localhost',
        'plugin.rabbitmq.pool.1.port': 61612,
        'plugin.rabbitmq.pool.1.user': 'mcollective',
        'plugin.rabbitmq.pool.1.password': 'marionette',
        'plugin.rabbitmq.pool.1.ssl': 'true',
        'plugin.rabbitmq.pool.1.ssl.ca':  os.path.join(ctxt.ROOT,
                                                       'fixtures/ca.pem'),
        'plugin.rabbitmq.pool.1.ssl.key': os.path.join(
            ctxt.ROOT,
            'fixtures/activemq_private.pem'),
        'plugin.rabbitmq.pool.1.ssl.cert': os.path.join(
            ctxt.ROOT,
            'fixtures/activemq_cert.pem',
        ),
    }
