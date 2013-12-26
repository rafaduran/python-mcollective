from . import base


class RabbitMQTestCase(base.IntegrationTestCase):
    '''RabbitMQ integration test case.'''
    CTXT = {
        'daemonize': 1,
        'securityprovider': 'none',
        'collectives': ['mcollective'],
        'connector': 'rabbitmq',
        'plugin.rabbitmq.vhost': '/mcollective',
        'plugin.rabbitmq.pool.size': '1',
        'plugin.rabbitmq.pool.1.host': 'localhost',
        'plugin.rabbitmq.pool.1.port': '61613',
        'plugin.rabbitmq.pool.1.user': 'mcollective',
        'plugin.rabbitmq.pool.1.password': 'marionette',
        'topicprefix': None,
    }


class TestWithRabbitMQMCo22x(base.MCollective22x, RabbitMQTestCase):
    '''MCollective integration test case.'''


class TestWithRabbitMQMCo23x(base.MCollective23x, RabbitMQTestCase):
    '''MCollective integration test case.'''
