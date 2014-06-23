"""
Tests for pymco.listener
"""
import pytest

from pymco import listener
from pymco.test.utils import mock


@pytest.fixture
def condition():
    return mock.Mock()


@pytest.fixture
def result_listener(config, condition):
    return listener.ResponseListener(config, condition=condition, count=2)


@pytest.fixture
def track_listener():
    return listener.CurrentHostPortListener()


@mock.patch('threading.Condition')
def test_default_condition(cond, config):
    """Tests condition is a new threading.Condition by default."""
    res_lis = listener.ResponseListener(config, 1)
    assert res_lis.condition == cond.return_value


def test_given_condition_is_used(result_listener, condition):
    """Test condition is used when given"""
    assert result_listener.condition == condition


@mock.patch('pymco.config.Config.get_security')
class TestOnMessage():
    def test_acquire_notify_release_condtion(self, get_security, result_listener, condition):
        result_listener.on_message(body='---\nfoo: spam', headers={})
        condition.acquire.assert_called_once_with()
        condition.notify.assert_called_once_with()
        condition.release.assert_called_once_with()

    def test_decode_message(self, get_security, result_listener):
        decode = get_security.return_value.decode
        decode.return_value = {'foo': 'spam'}
        result_listener.on_message(body='---\nfoo: spam', headers={})
        decode.assert_called_once_with('---\nfoo: spam')

    def test_appends_messages(self, get_security, result_listener):
        result_listener.on_message(body='---\nfoo: spam', headers={})
        decode = get_security.return_value.decode
        decode.assert_called_once_with('---\nfoo: spam')
        assert result_listener.responses == [decode.return_value]


def test_wait_on_message__acquire_release_condition(result_listener, condition):
    result_listener.received = result_listener.count + 1
    assert result_listener.wait_on_message() == result_listener
    condition.acquire.assert_called_once_with()
    condition.release.assert_called_once_with()


def test_wait_on_message__reset_received_count(result_listener, condition):
    result_listener.received = result_listener.count + 1
    assert result_listener.wait_on_message().received == 0


def test_wait_on_message__runs_wait_loop(result_listener, condition):
    with mock.patch.object(result_listener, '_wait_loop') as wait_loop:
        result_listener.received = result_listener.count + 1
        result_listener.wait_on_message()
    wait_loop.assert_called_once_with(result_listener.timeout)


def test_wait_loop__exits_when_count_is_reached(result_listener, condition):
    type(result_listener).received = mock.PropertyMock(side_effect=(0, 3))
    result_listener._wait_loop(5)
    condition.wait.assert_called_once_with(5)
    del type(result_listener).received  # undo the mock


@mock.patch('time.time', name='time mock')
def test_wait_loop__exits_on_timeout(time, result_listener, condition):
    time.side_effect = (0, 2, 3, 6)
    result_listener._wait_loop(5)
    assert condition.wait.call_args_list == [mock.call(5), mock.call(3)]


@mock.patch('pymco.config.Config.get_security')
def test_security(get_security, result_listener):
    assert result_listener.security == get_security.return_value
    get_security.assert_called_once_with()


@mock.patch('pymco.config.Config.get_security')
def test_security__caches_security(get_security, result_listener):
    security = mock.Mock()
    result_listener._security = security
    assert result_listener.security == security
    assert get_security.called is False


def test_current_host_port_listener(track_listener):
    track_listener.on_connecting(('localhost', 61613))
    assert track_listener.get_host() == 'localhost'
    assert track_listener.get_port() == 61613
