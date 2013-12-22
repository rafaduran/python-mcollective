"""
:py:mod:`pymco.connector`
-------------------------
python-mcollective connectors for MCollective.
"""
import abc


class BaseConnector(object):
    """Base abstract class for MCollective connectors."""
    plugins = {
        'stomp': 'pymco.connector.stomp.StompConnector',
    }

    def __init__(self, config):
        self.config = config

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
        raise NotImplementedError


def connect(self):
    """Connect to MCollective middleware."""


def disconnect(self):
    """Disconnet from MCollective middleware."""


def send(self, msg, *args, **kwargs):
    """Send an MCollective message.

    Args:
        ``msg``: message to be sent.
    Returns:
        ``self``: so you can chain calls.
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


def get_target(self, agent, collective, topciprefix=None):
    """Get the message target for the given agent and collective.

    Params:
        ``agent``: MCollective target agent name.
        ``collective``: MCollective target collective.
        ``topicprefix``: Required for older versions of MCollective
    Returns:
        ``target``: Message target string representation for given agent and
        collective.
    """


def get_reply_target(self, agent, collective):
    """Get the message target for the given agent and collective.

    Params:
        ``agent``: MCollective target agent name.
        ``collective``: MCollective target collective.
    Returns:
        ``reply_target``: Message reply target string representation for given
        agent and collective.
    """


# Building Metaclass here for Python 2/3 compatibility
Connector = abc.ABCMeta('Connector', (BaseConnector,), {
    'connect': abc.abstractmethod(connect),
    'disconnect': abc.abstractmethod(disconnect),
    'send': abc.abstractmethod(send),
    'subscribe': abc.abstractmethod(subscribe),
    'unsubscribe': abc.abstractmethod(unsubscribe),
})
