"""Tests for python-mcollective base."""
import mock
import pytest

from pymco import connector


def test_connector_is_abstract():
    """Tests Connector is an abstract class."""
    with pytest.raises(TypeError):
        connector.Connector()


class ConnectorFake(connector.Connector):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self):
        pass

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass


@pytest.fixture
def fake_connector(config):
    return ConnectorFake(config=config)


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
