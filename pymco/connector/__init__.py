"""
:py:mod:`pymco.connector`
-------------------------
python-mcollective connectors for MCollective.
"""
import abc


class BaseConnector(object):
    """Base abstract class for MCollective connectors."""
    def __init__(self, config):
        self.config = config


def send(self, msg, *args, **kwargs):
    """Send an MCollective message.

    Args:
        ``msg``: message to be sent.
    Returns:
        ``self``: so you can chain calls.
    """


def receive(self, topic, timeout, *args, **kwargs):
    """Subscribe to MCollective topic queue and wait for just one message.

    Args:
        ``topic``: message topic to wait for.
        ``timeout``: how long we should wait for the message.
        ``args``: extra positional arguments.
        ``kwargs``: extra keyword arguments.
    Returns:
        ``message``: received message.
    Raises: :py:exc:`pymco.exc.TimeoutError`
    """


def subscribe(self, destination, *args, **kwargs):
    """Subscribe to MCollective queue.

    Args:
        ``destination``: Target to subscribe.
        ``args``: extra positional arguments.
        ``kwargs``: extra keyword arguments.
    Returns:
        ``self``: so you can chain calls.
    """


def unsubscribe(self, destination, *args, **kwargs):
    """Unsubscribe to MCollective queue.

    Args:
        ``destination``: Target to unsubscribe.
        ``args``: extra positional arguments.
        ``kwargs``: extra keyword arguments.
    Returns:
        ``self``: so you can chain calls.
    """


# Building Metaclass here for Python 2/3 compatibility
Connector = abc.ABCMeta('Connector', (BaseConnector,), {
    'send': abc.abstractmethod(send),
    'receive': abc.abstractmethod(receive),
    'subscribe': abc.abstractmethod(subscribe),
    'unsubscribe': abc.abstractmethod(unsubscribe),
})
