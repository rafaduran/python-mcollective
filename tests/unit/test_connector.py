"""Tests for python-mcollective base connector."""
import pytest

from pymco import connector
from pymco.test.utils import mock


def test_connector_is_abstract():
    """Tests Connector is an abstract class."""
    with pytest.raises(TypeError):
        connector.Connector()


class ConnectorFake(connector.Connector):
    def get_target(self):
        pass

    def get_reply_target(self):
        pass

    @classmethod
    def default_connection(cls, config):
        pass


@pytest.fixture
def fake_connector(config, conn_mock):
    return ConnectorFake(config=config, connection=conn_mock)


@mock.patch('pymco.connector.Connector.set_listeners')
def test_set_listeners(set_listeners, config, conn_mock):
    ConnectorFake(config=config, connection=conn_mock)
    set_listeners.assert_called_once_with()


@mock.patch('pymco.config.Config.get_security')
def test_connector_security(get_security, fake_connector):
    assert fake_connector.security == get_security.return_value
    get_security.assert_called_once_with()


@mock.patch('pymco.config.Config.get_security')
def test_connector_security__caches_security(get_security, fake_connector):
    security = mock.Mock()
    fake_connector._security = security
    assert fake_connector.security == security
    assert get_security.called is False


def test_connect(fake_connector, conn_mock, config):
    conn_mock.connected = False
    conn_mock.current_host_and_port = ('localhost', 6163)
    assert fake_connector.connect() is fake_connector
    conn_mock.connect.assert_called_once_with(
        username=config['plugin.activemq.pool.1.user'],
        passcode=config['plugin.activemq.pool.1.password'],
        wait=None,
    )
    conn_mock.start.assert_called_once_with()


def test_connect_already_connected(fake_connector, conn_mock):
    conn_mock.connected = True
    assert fake_connector.connect() is fake_connector
    assert 0 == conn_mock.connect.call_count
    assert 0 == conn_mock.start.call_count


def test_disconnect(fake_connector, conn_mock):
    conn_mock.connected.return_value = True
    assert fake_connector.disconnect() is fake_connector
    conn_mock.disconnect.assert_called_once_with()
    conn_mock.stop.assert_called_once_with()


def test_disconnect_not_connected(fake_connector, conn_mock):
    conn_mock.connected = False
    assert fake_connector.disconnect() is fake_connector
    assert 0 == conn_mock.disconnect.call_count
    assert 0 == conn_mock.stop.call_count
