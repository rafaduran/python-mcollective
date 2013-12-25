'''Test configuration for the re-write unit tests'''
import os

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

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

CONFIGSTR_STOMP = '''
topicprefix = /topic/
collectives = mcollective
main_collective = mcollective
libdir = /Users/rafaduran/workspace/python-mcollective/tests/integration/vendor/plugins
logfile = /Users/rafaduran/workspace/python-mcollective/mcollective.log
loglevel = debug
daemonize = 0
identity = mco1

# Plugins
securityprovider = none

direct_addressing = yes
direct_addressing_threshold = 5

connector = stomp
plugin.stomp.host = localhost
plugin.stomp.password = guest
plugin.stomp.port = 61613
plugin.stomp.user = guest

factsource = yaml
plugin.yaml = /Users/rafaduran/workspace/python-mcollective/tests/fixtures/facts.yaml
'''


def pytest_runtest_setup(item):
    base.configfile()


@pytest.fixture
def configstr():
    return CONFIGSTR


@pytest.fixture
def config(configstr):
    # Importing here since py-cov will ignore code imported on conftest files
    # imports
    from pymco import config
    return config.Config.from_configstr(configstr=configstr)


@pytest.fixture
def config_stomp():
    # Importing here since py-cov will ignore code imported on conftest files
    # imports
    from pymco import config
    return config.Config.from_configstr(configstr=CONFIGSTR_STOMP)


@pytest.fixture
def filter_():
    '''Creates a new :py:class:`pymco.message.Filter` instance.'''
    # Importing here since py-cov will ignore code imported on conftest files
    # imports
    from pymco import message
    return message.Filter()


@pytest.fixture
def msg(config, filter_):
    '''Creates a new :py:class:`pymco.message.Message` instance.'''
    # Importing here since py-cov will ignore code imported on conftest files
    # imports
    from pymco import message
    with mock.patch('time.time') as time:
        with mock.patch('hashlib.sha1') as sha1:
            time.return_value = base.MSG['msgtime']
            sha1.return_value.hexdigest.return_value = base.MSG['requestid']
            msg_ = message.Message(body=base.MSG['body'],
                                   agent=base.MSG['agent'],
                                   filter_=filter_,
                                   config=config)
            time.assert_called_once_with()
            sha1.return_value.hexdigest.assert_called_once_with()
    return msg_


@pytest.fixture
def msg2(config):
    '''Creates a new :py:class:`pymco.message.Message` instance.'''
    # Importing here since py-cov will ignore code imported on conftest files
    # imports
    from pymco import message
    return message.Message(body=base.MSG['body'],
                           agent=base.MSG['agent'],
                           config=config)


@pytest.fixture
def none_security(config):
    from pymco.security import none
    return none.NoneProvider(config)


@pytest.fixture
def condition():
    return mock.Mock()

conn_mock = security = condition


@pytest.fixture
def result_listener(config, none_security, condition):
    from pymco import listener
    return listener.ResponseListener(config, condition=condition, count=2)


@pytest.fixture
def simple_action(config, msg):
    from pymco import rpc
    return rpc.SimpleAction(agent=base.MSG['agent'],
                            config=config,
                            msg=msg)


@pytest.fixture
def client_public():
    path = os.path.join(os.path.dirname(__file__),
                        os.path.pardir,
                        'fixtures',
                        'client-public.pem')
    with open(path, 'rt') as cpf:
        content = cpf.read()

    return content
