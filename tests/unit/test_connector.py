"""Tests for python-mcollective base connector."""
import pytest
import six

from pymco import connector
from pymco import exc
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


@pytest.fixture
def fake_connector(config, conn_mock):
    return ConnectorFake(config=config, connection=conn_mock)


def test_set_listeners(config, conn_mock):
    listener = mock.Mock()
    with mock.patch.dict(ConnectorFake.listeners, {'tracker': listener}):
        connector = ConnectorFake(config=config, connection=conn_mock)

    conn_mock.set_listener.assert_called_once_with('tracker',
                                                   listener.return_value)
    listener.assert_called_once_with(connector=connector, config=config)


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


@mock.patch('pymco.connector.Connector.get_current_host_and_port')
def test_connect(host_and_port, fake_connector, conn_mock, config):
    conn_mock.connected = False
    host_and_port.return_value = ('localhost', 6163)
    assert fake_connector.connect() is fake_connector
    conn_mock.connect.assert_called_once_with(
        username=config['plugin.activemq.pool.1.user'],
        passcode=config['plugin.activemq.pool.1.password'],
        wait=None,
    )
    conn_mock.start.assert_called_once_with()
    host_and_port.assert_called_once_with()


def test_connect_already_connected(fake_connector, conn_mock):
    conn_mock.connected = True
    assert fake_connector.connect() is fake_connector
    assert 0 == conn_mock.connect.call_count
    assert 0 == conn_mock.start.call_count


def test_disconnect(fake_connector, conn_mock):
    conn_mock.is_connected.return_value = True
    assert fake_connector.disconnect() is fake_connector
    conn_mock.disconnect.assert_called_once_with()


def test_disconnect_not_connected(fake_connector, conn_mock):
    conn_mock.is_connected.return_value = False
    assert fake_connector.disconnect() is fake_connector
    assert 0 == conn_mock.disconnect.call_count


def test_get_current_host_and_port(fake_connector, conn_mock):
    conn_mock.get_listener.return_value.get_host.return_value = 'localhost'
    conn_mock.get_listener.return_value.get_port.return_value = 61613

    assert fake_connector.get_current_host_and_port() == ('localhost', 61613)

    conn_mock.get_listener.assert_called_once_with('tracker')
    conn_mock.get_listener.return_value.get_host.assert_called_once_with()
    conn_mock.get_listener.return_value.get_port.assert_called_once_with()


@mock.patch('pymco.connector.Connector.security')
def test_send(security, fake_connector, conn_mock):
    assert fake_connector.send('foo', 'destination') is fake_connector
    conn_mock.send.assert_called_with(body=security.encode('foo'),
                                      destination='destination')


def test_subcscribe(fake_connector, conn_mock):
    assert fake_connector.subscribe('destination', id='some-id') is fake_connector
    conn_mock.subscribe.assert_called_once_with('destination', id='some-id')


@mock.patch.object(six.moves.builtins, 'next')
@mock.patch('pymco.connector.Connector.id_generator')
def test_subscribe_no_id(id_generator, next, fake_connector, conn_mock):
    next.return_value = 1
    assert fake_connector.subscribe('destination') is fake_connector
    conn_mock.subscribe.assert_called_once_with('destination', id=1)
    next.assert_called_once_with(id_generator)


def test_set_ssl(config, conn_mock):
    calls = [
        mock.call(for_hosts=(('localhost', 6163),),
                  cert_file='tests/fixtures/activemq_cert.pem',
                  key_file='tests/fixtures/activemq_private.pem',
                  ca_certs='tests/fixtures/ca.pem'),
        mock.call(for_hosts=(('localhost', 6164),),
                  cert_file='tests/fixtures/activemq_cert.pem',
                  key_file='tests/fixtures/activemq_private.pem',
                  ca_certs='tests/fixtures/ca.pem'),
    ]
    ConnectorFake(config, conn_mock)
    assert conn_mock.transport.set_ssl.call_args_list == calls


@mock.patch('pymco.listener.SingleResponseListener',
            **{'return_value.responses.__len__.return_value': 1})
class TestReceive:
    def patch_connection(self, fake_connector):
        return mock.patch.multiple(fake_connector,
                                   connect=mock.DEFAULT,
                                   subscribe=mock.DEFAULT,
                                   disconnect=mock.DEFAULT)

    def test_receive__sets_single_response_listener(self,
                                                    listener,
                                                    fake_connector,
                                                    conn_mock):
        fake_connector.receive(5)
        assert mock.call('response_listener', listener.return_value
                         ) in conn_mock.set_listener.call_args_list

    def test_receive__sets_the_right_timeout(self,
                                             listener,
                                             fake_connector,
                                             conn_mock):
        fake_connector.receive(5)
        listener.assert_called_once_with(connector=fake_connector,
                                         timeout=5,
                                         config=fake_connector.config)

    def test_receive__raises_timeout_error_if_no_message(self,
                                                         listener,
                                                         fake_connector,
                                                         conn_mock):
        listener.return_value.responses.__len__.return_value = 0
        with self.patch_connection(fake_connector):
            with pytest.raises(exc.TimeoutError):
                fake_connector.receive(5)


@mock.patch('pymco.config.Config.get_conn_params')
@mock.patch('stomp.connect.StompConnection11')
def test_default_connection(conn_mock, get_conn_params, config):
    get_conn_params.return_value = {}
    connector = ConnectorFake(config=config)
    assert connector.connection is conn_mock.return_value
    conn_mock.assert_called_once_with(**{'try_loopback_connect': False})


@mock.patch('pymco.config.Config.get_conn_params')
@mock.patch('stomp.connect.StompConnection11')
def test_default_connection__rabbitmq(conn_mock, get_conn_params, config):
    config.config['connector'] = 'rabbitmq'
    config.config['plugin.rabbitmq.vhost'] = 'mcollective'
    config.config['plugin.rabbitmq.pool.size'] = 1
    config.config['plugin.rabbitmq.pool.1.host'] = 'localhost'
    config.config['plugin.rabbitmq.pool.1.port'] = 61612
    config.config['plugin.rabbitmq.pool.1.user'] = 'mcollective'
    config.config['plugin.rabbitmq.pool.1.password'] = 'marionette'
    get_conn_params.return_value = {}
    connector = ConnectorFake(config=config)
    assert connector.connection is conn_mock.return_value
    conn_mock.assert_called_once_with(**{'vhost': 'mcollective',
                                         'try_loopback_connect': False})


def test_use_b64__disabled(config, fake_connector):
    assert fake_connector.use_b64 is False


def test_use_b64__enabled(config, fake_connector):
    for value in ('1', 'y', 'true'):
        config.config['plugin.activemq.base64'] = value
        assert fake_connector.use_b64 is True


def test_use_b64__non_activmeq(config, fake_connector):
    config.config['plugin.activemq.base64'] = 'true'
    config.config['connector'] = 'rabbitmq'
    assert fake_connector.use_b64 is False
