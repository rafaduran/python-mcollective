"""
Tests for StompConnector
"""
from __future__ import absolute_import
import mock
import pytest
import six

from pymco.connector import stomp
from pymco import exc


def test_connect(stomp_connector, conn_mock, config_stomp):
    conn_mock.connected = False
    conn_mock.current_host_and_port = ('localhost', 6163)
    assert stomp_connector.connect() is stomp_connector
    conn_mock.connect.assert_called_once_with(username=config_stomp['plugin.stomp.user'],
                                              passcode=config_stomp['plugin.stomp.password'],
                                              wait=None)
    conn_mock.start.assert_called_once_with()


def test_connect_already_connected(stomp_connector, conn_mock):
    conn_mock.connected = True
    assert stomp_connector.connect() is stomp_connector
    assert 0 == conn_mock.connect.call_count
    assert 0 == conn_mock.start.call_count


def test_disconnect(stomp_connector, conn_mock):
    conn_mock.connected.return_value = True
    assert stomp_connector.disconnect() is stomp_connector
    conn_mock.disconnect.assert_called_once_with()
    conn_mock.stop.assert_called_once_with()


def test_disconnect_not_connected(stomp_connector, conn_mock):
    conn_mock.connected = False
    assert stomp_connector.disconnect() is stomp_connector
    assert 0 == conn_mock.disconnect.call_count
    assert 0 == conn_mock.stop.call_count


@mock.patch('stomp.Connection')
def test_default_connection(conn, config_stomp):
    connector = stomp.StompConnector(config=config_stomp)
    assert connector.connection is conn.return_value
    conn.assert_called_once_with(host_and_ports=[('localhost', 61613)])


@mock.patch('pymco.connector.Connector.security')
def test_send(security, stomp_connector, conn_mock):
    assert stomp_connector.send('foo', 'destination') is stomp_connector
    conn_mock.send.assert_called_with(body=security.encode('foo'),
                                      destination='destination')


def test_subcscribe(stomp_connector, conn_mock):
    assert stomp_connector.subscribe('destination', id='some-id') is stomp_connector
    conn_mock.subscribe.assert_called_once_with('destination', id='some-id')


@mock.patch.object(six.moves.builtins, 'next')
@mock.patch('pymco.connector.stomp.StompConnector.id_generator')
def test_subscribe_no_id(id_generator, next, stomp_connector, conn_mock):
    next.return_value = 1
    assert stomp_connector.subscribe('destination') is stomp_connector
    conn_mock.subscribe.assert_called_once_with('destination', id=1)
    next.assert_called_once_with(id_generator)


@mock.patch('pymco.listener.SingleResponseListener',
            **{'return_value.responses.__len__.return_value': 1})
class TestReceive:
    def patch_connection(self, stomp_connector):
        return mock.patch.multiple(stomp_connector,
                                   connect=mock.DEFAULT,
                                   subscribe=mock.DEFAULT,
                                   disconnect=mock.DEFAULT)

    def test_receive__sets_single_response_listener(self,
                                                    listener,
                                                    stomp_connector,
                                                    conn_mock):
        stomp_connector.receive(5)
        conn_mock.set_listener.assert_called_once_with('response_listener',
                                                       listener.return_value)

    def test_receive__sets_the_right_timeout(self,
                                             listener,
                                             stomp_connector,
                                             conn_mock):
        stomp_connector.receive(5)
        listener.assert_called_once_with(timeout=5,
                                         config=stomp_connector.config)

    def test_receive__raises_timeout_error_if_no_message(self,
                                                         listener,
                                                         stomp_connector,
                                                         conn_mock):
        listener.return_value.responses.__len__.return_value = 0
        with self.patch_connection(stomp_connector):
            with pytest.raises(exc.TimeoutError):
                stomp_connector.receive(5)


def test_get_target(stomp_connector, config_stomp):
    assert stomp_connector.get_target(collective='collective', agent='agent') == (
        '{0}collective.agent.command'.format(config_stomp['topicprefix'])
    )


def test_get_reply_target(stomp_connector, config_stomp):
    assert stomp_connector.get_reply_target(collective='collective', agent='agent') == (
        '{0}collective.agent.reply'.format(config_stomp['topicprefix'])
    )
