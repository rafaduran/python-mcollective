from . import base


class SSLTestCase(base.IntegrationTestCase):
    '''RabbitMQ integration test case.'''
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
        'plugin.ssl_server_public': 'tests/fixtures/server-public.pem',
        'plugin.ssl_client_private': 'tests/fixtures/client-private.pem',
        'plugin.ssl_client_public': 'tests/fixtures/client-public.pem',
    }


class TestWithSSLMCo20x(base.MCollective20x, SSLTestCase):
    '''MCollective integration test case.'''


class TestWithSSLMCo22x(base.MCollective22x, SSLTestCase):
    '''MCollective integration test case.'''


class TestWithSSLMCo23x(base.MCollective23x, SSLTestCase):
    '''MCollective integration test case.'''
