"""
Tests for StompConnector
"""
from __future__ import absolute_import
import mock
import pytest
import six

from pymco.connector import stomp
from pymco import exc

CONFIGSTR = '''
topicprefix = /topic/
collectives = mcollective
main_collective = mcollective
libdir = /path/to/plugins
logfile = /path/to/mcollective.log
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
plugin.yaml = /path/to/facts.yaml
'''


@pytest.fixture
def config():
    from pymco import config
    return config.Config.from_configstr(configstr=CONFIGSTR)


@pytest.fixture
def connector(config, conn_mock):
    return stomp.StompConnector(config, connection=conn_mock)


@mock.patch('stomp.Connection')
def test_default_connection(conn, config):
    connector = stomp.StompConnector(config=config)
    assert connector.connection is conn.return_value
    conn.assert_called_once_with(host_and_ports=[('localhost', 61613)])


@mock.patch('pymco.connector.Connector.security')
def test_send(security, connector, conn_mock):
    assert connector.send('foo', 'destination') is connector
    conn_mock.send.assert_called_with(body=security.encode('foo'),
                                      destination='destination')


def test_subcscribe(connector, conn_mock):
    assert connector.subscribe('destination', id='some-id') is connector
    conn_mock.subscribe.assert_called_once_with('destination', id='some-id')


@mock.patch.object(six.moves.builtins, 'next')
@mock.patch('pymco.connector.stomp.StompConnector.id_generator')
def test_subscribe_no_id(id_generator, next, connector, conn_mock):
    next.return_value = 1
    assert connector.subscribe('destination') is connector
    conn_mock.subscribe.assert_called_once_with('destination', id=1)
    next.assert_called_once_with(id_generator)


@mock.patch('pymco.listener.SingleResponseListener',
            **{'return_value.responses.__len__.return_value': 1})
class TestReceive:
    def patch_connection(self, connector):
        return mock.patch.multiple(connector,
                                   connect=mock.DEFAULT,
                                   subscribe=mock.DEFAULT,
                                   disconnect=mock.DEFAULT)

    def test_receive__sets_single_response_listener(self,
                                                    listener,
                                                    connector,
                                                    conn_mock):
        connector.receive(5)
        conn_mock.set_listener.assert_called_once_with('response_listener',
                                                       listener.return_value)

    def test_receive__sets_the_right_timeout(self,
                                             listener,
                                             connector,
                                             conn_mock):
        connector.receive(5)
        listener.assert_called_once_with(timeout=5,
                                         config=connector.config)

    def test_receive__raises_timeout_error_if_no_message(self,
                                                         listener,
                                                         connector,
                                                         conn_mock):
        listener.return_value.responses.__len__.return_value = 0
        with self.patch_connection(connector):
            with pytest.raises(exc.TimeoutError):
                connector.receive(5)


def test_get_target(connector, config):
    assert connector.get_target(collective='collective', agent='agent') == (
        '{0}collective.agent.command'.format(config['topicprefix'])
    )


def test_get_reply_target(connector, config):
    assert connector.get_reply_target(collective='collective', agent='agent') == (
        '{0}collective.agent.reply'.format(config['topicprefix'])
    )
