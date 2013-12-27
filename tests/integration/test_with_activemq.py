from . import base


class ActiveMQTestCase(base.IntegrationTestCase):
    '''RabbitMQ integration test case.'''
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
    }


class TestWithActiveMQMCo22x(base.MCollective22x, ActiveMQTestCase):
    '''MCollective integration test case.'''


class TestWithActiveMQMCo23x(base.MCollective23x, ActiveMQTestCase):
    '''MCollective integration test case.'''
