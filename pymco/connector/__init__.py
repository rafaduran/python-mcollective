"""
:py:mod:`pymco.connector`
-------------------------
python-mcollective connectors for MCollective.
"""
import abc
import itertools

from .. import exc
from .. import listener


class BaseConnector(object):
    """Base abstract class for MCollective connectors."""
    listeners = {'tracker': listener.CurrentHostPortListener}

    plugins = {
        'activemq': 'pymco.connector.activemq.ActiveMQConnector',
        'rabbitmq': 'pymco.connector.rabbitmq.RabbitMQConnector',
        'stomp': 'pymco.connector.stomp.StompConnector',
    }

    id_generator = itertools.count()

    def __init__(self, config, connection=None):
        self.config = config
        self._security = None
        self._started = False
        self._id = None

        if connection is None:
            self.connection = self.default_connection(config)
        else:
            self.connection = connection

        self.set_listeners()

    def connect(self, wait=None):
        """Connect to MCollective middleware."""
        if not self.connection.connected:
            self.connection.start()
            user, password = self.config.get_user_and_password(
                self.connection.current_host_and_port)
            self.connection.connect(username=user,
                                    passcode=password,
                                    wait=wait)

        return self

    def disconnect(self):
        """Disconnet from MCollective middleware."""
        if self.connection.connected:
            self.connection.disconnect()
            self.connection.stop()

        return self

    def send(self, msg, destination, *args, **kwargs):
        """Send an MCollective message.

        Args:
            ``msg``: message to be sent.

        Returns:
            ``self``: so you can chain calls.
        """
        self.connection.send(body=self.security.serialize(self.security.sign(msg)),
                             destination=destination,
                             **kwargs)
        return self

    def subscribe(self, destination, id=None, *args, **kwargs):
        """Subscribe to MCollective queue.

        Args:
            ``destination``: Target to subscribe.

            ``args``: extra positional arguments.

            ``kwargs``: extra keyword arguments.

        Returns:
            ``self``: so you can chain calls.
        """
        if not id:
            id = self.id

        self.connection.subscribe(destination, id=id)
        return self

    def unsubscribe(self, destination, *args, **kwargs):
        """Unsubscribe to MCollective queue.

        Args:
            ``destination``: Target to unsubscribe.

            ``args``: extra positional arguments.

            ``kwargs``: extra keyword arguments.

        Returns:
            ``self``: so you can chain calls.
        """

    def receive(self, timeout, *args, **kwargs):
        """Subscribe to MCollective topic queue and wait for just one message.

        Args:
            ``timeout``: how long we should wait for the message.

            ``args``: extra positional arguments.

            ``kwargs``: extra keyword arguments.

        Returns:
            ``message``: received message.

        Raises: :py:exc:`pymco.exc.TimeoutError`
        """
        response_listener = listener.SingleResponseListener(timeout=timeout,
                                                            config=self.config)
        self.connection.set_listener('response_listener', response_listener)
        response_listener.wait_on_message()

        if len(response_listener.responses) == 0:
            raise exc.TimeoutError

        return response_listener.responses

    @property
    def id(self):
        if not self._id:
            self._id = next(self.id_generator)

        return self._id

    @property
    def security(self):
        """Security provider property."""
        if not self._security:
            self._security = self.config.get_security()

        return self._security

    def set_listeners(self):
        """Set default listeners."""
        for key, value in self.listeners.items():
            self.connection.set_listener(key, value)


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


def default_connection(cls, config):
    """Creates a :py:class:`stomp.Connection` object with defaults.

    This method should be defined as a classmethod.
    """


# Building Metaclass here for Python 2/3 compatibility
Connector = abc.ABCMeta('Connector', (BaseConnector,), {
    'get_target': abc.abstractmethod(get_target),
    'get_reply_target': abc.abstractmethod(get_reply_target),
    'default_connection': abc.abstractmethod(default_connection),
})
