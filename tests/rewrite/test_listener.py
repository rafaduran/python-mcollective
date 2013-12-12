"""
Tests for pymco.listener
"""
import mock

from pymco import listener


@mock.patch('threading.Condition')
def test_default_condition(cond, config, none_security):
    """Tests condition is a new threading.Condition by default."""
    res_lis = listener.ResponseListener(config, none_security, 1)
    assert res_lis.condition == cond.return_value


def test_given_condition_is_used(result_listener, condition):
    """Test condition is used when given"""
    assert result_listener.condition == condition


def test_on_message_acquire_notify_release_condtion(result_listener, condition):
    result_listener.on_message(body='---\nfoo: spam', headers={})
    condition.acquire.assert_called_once_with()
    condition.notify.assert_called_once_with()
    condition.release.assert_called_once_with()


def test_on_message_decode_message(result_listener):
    with mock.patch.object(result_listener.security, 'decode') as decode:
        decode.return_value = {'foo': 'spam'}
        result_listener.on_message(body='---\nfoo: spam', headers={})
        decode.assert_called_once_with('---\nfoo: spam')


def test_on_message_appends_messages(result_listener):
    with mock.patch.object(result_listener.security, 'decode') as decode:
        result_listener.on_message(body='---\nfoo: spam', headers={})
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
