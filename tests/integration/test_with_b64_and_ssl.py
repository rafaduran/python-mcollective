import os

from pymco.test import ctxt
from . import base

FIXTURES_PATH = os.path.join(ctxt.ROOT, 'fixtures')


class Base64SSLTestCase(base.IntegrationTestCase):
    """ActiveMQ integration test case."""
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
        'plugin.activemq.pool.1.base64': 'yes',
        'plugin.ssl_server_public': 'tests/fixtures/server-public.pem',
        'plugin.ssl_client_private': 'tests/fixtures/client-private.pem',
        'plugin.ssl_client_public': 'tests/fixtures/client-public.pem',
        'plugin.ssl_server_private': os.path.join(FIXTURES_PATH,
                                                  'server-private.pem'),
        'securityprovider': 'ssl',
        'plugin.ssl_client_cert_dir': FIXTURES_PATH,
    }


class TestWithBase64SSLMCo20x(base.MCollective20x, Base64SSLTestCase):
    """MCollective integration test case."""


class TestWithBase64SSLMCo22x(base.MCollective22x, Base64SSLTestCase):
    """MCollective integration test case."""


class TestWithBase64SSLMCo23x(base.MCollective23x, Base64SSLTestCase):
    """MCollective integration test case."""


class TestWithBase64SSLMCo24x(base.MCollective24x, Base64SSLTestCase):
    """MCollective integration test case."""
