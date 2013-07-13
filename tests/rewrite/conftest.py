'''Test configuration for the re-write unit tests'''
import pytest
import six

from .. import base

CONFIGSTR = '''
topicprefix = /topic/
collectives = mcollective,sub1,sub2
main_collective = mcollective
libdir = /opt/workspace/mcollective-python/tests/integration/vendor/plugins
logfile = /opt/workspace/mcollective-python/tests/mcollective.log
loglevel = debug
daemonize = 0
identity = mco1

# Plugins
securityprovider = ssl
plugin.ssl_server_public = mcserver-public.pem
plugin.ssl_client_private = /opt/workspace/mcollective-python/tests/fixtures/testkey-private.pem
plugin.ssl_serializer = yaml
plugin.ssl_client_public = /opt/workspace/mcollective-python/tests/fixtures/testkey-public.pem

direct_addressing = yes
direct_addressing_threshold = 5

connector = activemq
plugin.activemq.pool.1.port = 6163
plugin.activemq.pool.1.host = localhost
plugin.activemq.pool.size = 1
plugin.activemq.pool.1.password = secret
plugin.activemq.pool.1.user = mcollective
plugin.activemq.pool.1.ssl = false

factsource = yaml
plugin.yaml = /opt/workspace/mcollective-python/tests/tests/fixtures/facts.yaml
'''


def pytest_runtest_setup(item):
    base.configfile()


@pytest.fixture
def configstr():
    return CONFIGSTR


@pytest.fixture
def config(configstr):
    # Importing here since py-cov will ignored code imported on conftest files
    # imports
    from pymco import config
    return config.Config.from_configstr(configstr=configstr)


@pytest.fixture
def filter_():
    '''Creates a new :py:class:`pymco.Filter` instance.'''
    from pymco import message
    return message.Filter()
