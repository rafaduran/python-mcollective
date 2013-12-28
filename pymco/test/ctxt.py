"""
:py:mod:`pymco.test.ctxt`
-------------------------
Context information for sourcing test templates.
"""
import os

ROOT = os.path.abspath(os.path.join(__file__,
                                    os.path.pardir,
                                    os.path.pardir,
                                    os.path.pardir,
                                    'tests'))

DEFAULT_CTXT = {
    'topicprefix': 'topic',
    'collectives': ['mcollective', 'sub1', 'sub2'],
    'main_collective': 'mcollective',
    'libdir': '{root}/integration/vendor/plugins'.format(root=ROOT),
    'logfile': '{root}/mcollective.log'.format(root=ROOT),
    'loglevel': 'debug',
    'daemonize': 0,
    'identity': 'mco1',
    'securityprovider': 'ssl',
    'plugin.ssl_server_public': 'mcserver-public.pem',
    'plugin.ssl_client_private': '{root}/fixtures/testkey-private.pem'.format(
        root=ROOT),
    'plugin.ssl_client_public': '{root}/fixtures/testkey-public.pem'.format(
        root=ROOT),
    'plugin.ssl_serializer': 'yaml',
    'connector': 'activemq',
    'plugin.activemq.pool.size': '1',
    'plugin.activemq.pool.1.host': 'localhost',
    'plugin.activemq.pool.1.port': '6163',
    'plugin.activemq.pool.1.user': 'mcollective',
    'plugin.activemq.pool.1.password': 'secret',
    'plugin.activemq.pool.1.ssl': 'false',
}

TEST_CFG = os.path.join(ROOT, 'server.cfg')

MSG = {
    'msgtime': 123.45,
    'requestid': '6ef11a5053008b54c03ca934972fdfa45448439d',
    'body': 'ping',
    'agent': 'discovery',
}
