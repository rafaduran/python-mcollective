"""
Tests for StompConnector
"""
from __future__ import absolute_import
import mock

from pymco.connector import stomp


def test_connection_start(stomp_connector, conn_mock, config_stomp):
    conn_mock.connected.side_effect = (False, True)
    # First use, this should sart the connection
    assert stomp_connector.connection is conn_mock
    # Now nothing should occur
    assert stomp_connector.connection is conn_mock
    conn_mock.connect.assert_called_once_with(username=config_stomp['plugin.stomp.user'],
                                              passcode=config_stomp['plugin.stomp.password'])
    conn_mock.start.assert_called_once_with()


@mock.patch('stomp.Connection')
def test_default_connection(conn, config_stomp):
    connector = stomp.StompConnector(config=config_stomp)
    assert connector.connection is conn.return_value


def test_send(stomp_connector, conn_mock):
    assert stomp_connector.send('foo', 'destination') is stomp_connector
    conn_mock.send.assert_called_with('foo', 'destination')
