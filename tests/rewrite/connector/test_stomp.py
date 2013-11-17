"""
Tests for StompConnector
"""
from __future__ import absolute_import
import mock
import pytest

from pymco.connector import stomp


def test_connect(stomp_connector, conn_mock, config_stomp):
    conn_mock.connected = False
    assert stomp_connector.connect() is stomp_connector
    conn_mock.connect.assert_called_once_with(username=config_stomp['plugin.stomp.user'],
                                              passcode=config_stomp['plugin.stomp.password'])
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


def test_send(stomp_connector, conn_mock):
    assert stomp_connector.send('foo', 'destination') is stomp_connector
    conn_mock.send.assert_called_with('foo', 'destination')


def test_receive(stomp_connector):
    with pytest.raises(NotImplementedError):
        stomp_connector.receive('foo', 'foo')
