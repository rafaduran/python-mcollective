"""
Connectors base
---------------
python-mcollective base for MCollective connector plugins.
"""
from __future__ import absolute_import

import abc
import itertools
import logging

from stomp import connect

from .. import exc
from .. import listener

LOG = logging.getLogger(__name__)


class BaseConnector(object):
    """Base abstract class for MCollective connectors.

    :arg pymco.config.Config config: configuration instance.
    :arg stomp.Connection connection: connection object. Optional
        parameter, if not given :py:meth:`default_connection` result
        will be used.
    """
    listeners = {'tracker': listener.CurrentHostPortListener}

    plugins = {
        'activemq': 'pymco.connector.activemq.ActiveMQConnector',
        'rabbitmq': 'pymco.connector.rabbitmq.RabbitMQConnector',
        'stomp': 'pymco.connector.stomp.StompConnector',
    }

    id_generator = itertools.count()

    def __init__(self, config, connection=None, logger=LOG):
        self.logger = logger
        self.logger.debug("initializing connector")
        self.config = config
        self._security = None
        self._started = False
        self._id = None

        if connection is None:
            self.connection = self.default_connection(config)
        else:
            self.connection = connection

        self.set_listeners()
        self.set_ssl()

    def connect(self, wait=None):
        """Connect to MCollective middleware.

        :arg bool wait: wait for connection to be established or not.
        :return: ``self``
        """
        if not self.connection.connected:
            self.connection.start()
            user, password = self.config.get_user_and_password(
                self.get_current_host_and_port())
            self.logger.debug("connecting to middleware...")
            self.connection.connect(username=user,
                                    passcode=password,
                                    wait=wait)
            self.logger.debug("connected to middleware.")
        return self

    def disconnect(self):
        """Disconnet from MCollective middleware.

        :return: ``self``
        """
        if self.connection.is_connected():
            self.logger.debug("disconnecting")
            self.connection.disconnect()

        return self

    def send(self, msg, destination, *args, **kwargs):
        """Send an MCollective message.

        :arg pymco.message.Message msg: message to be sent.
        :arg \*args: extra positional arguments.
        :arg \*\*kwargs: extra keyword arguments.
        :return: ``self``.
        """
        self.logger.debug("sending message to {d}: {m}".format(d=destination, m=msg))
        self.connection.send(body=self.security.encode(msg, b64=self.use_b64),
                             destination=destination,
                             **kwargs)
        return self

    def subscribe(self, destination, id=None, *args, **kwargs):
        """Subscribe to MCollective queue.

        :arg destination: Target to subscribe.
        :arg \*args: extra positional arguments.
        :arg \*\*kwargs: extra keyword arguments.
        :return: ``self``.
        """
        if not id:
            id = self.id

        self.connection.subscribe(destination, id=id)
        return self

    def unsubscribe(self, destination, *args, **kwargs):
        """Unsubscribe to MCollective queue.

        :arg destination: Target to unsubscribe.
        :arg \*args: extra positional arguments.
        :arg \*\*kwargs: extra keyword arguments.
        :return: ``self``.
        """

    def receive(self, timeout, *args, **kwargs):
        """Subscribe to MCollective topic queue and wait for just one message.

        :arg float timeout: how long we should wait for the message in seconds.
        :arg \*args: extra positional arguments.
        :arg \*\*kwargs: extra keyword arguments.
        :return: received message.
        :raise: :py:exc:`pymco.exc.TimeoutError` if expected messages doesn't
            come in given ``timeout`` seconds.
        """
        self.logger.debug("setting up SingleResponseListener, timeout={t}".format(t=timeout))
        response_listener = listener.SingleResponseListener(timeout=timeout,
                                                            config=self.config,
                                                            connector=self)
        self.connection.set_listener('response_listener', response_listener)
        self.logger.debug("listener waiting for message...")
        response_listener.wait_on_message()
        self.logger.debug("listener wait exited.")

        if len(response_listener.responses) == 0:
            self.logger.debug("listener got 0 responses, raising TimeoutError")
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

    @property
    def use_b64(self):
        """Determines if the message should be base64 encoded."""
        if self.config['connector'] != 'activemq':
            self.logger.debug("not using ActiveMQ; not using base64")
            return False

        config_b64 = self.config.getboolean('plugin.activemq.base64', default=False)
        self.logger.debug("config plugin.activemq.base64={c}".format(c=config_b64))
        return config_b64

    def set_listeners(self):
        """Set default listeners."""
        for key, value in self.listeners.items():
            self.connection.set_listener(key, value(config=self.config,
                                                    connector=self))

    def get_current_host_and_port(self):
        """Get the current host and port from the tracker listener.

        :return: A two-tuple, where the first element is the current host and
            the second the current port.
        """
        tracker = self.connection.get_listener('tracker')
        return tracker.get_host(), tracker.get_port()

    def set_ssl(self):
        """Set the SSL configuration for the current connection."""
        for params in self.config.get_ssl_params():
            self.connection.transport.set_ssl(**params)

    @classmethod
    def default_connection(cls, config):
        """Creates a :py:class:`stomp.Connection` object with defaults

        :return: :py:class:`stomp.Connection` object.
        """
        params = config.get_conn_params()
        if config['connector'] == 'rabbitmq':
            params['vhost'] = config['plugin.rabbitmq.vhost']

        return connect.StompConnection11(try_loopback_connect=False, **params)


def get_target(self, agent, collective, topciprefix=None):
    """Get the message target for the given agent and collective.

    :arg agent: MCollective target agent name.
    :arg collective: MCollective target collective.
    :arg topicprefix: Required for older versions of MCollective
    :return: Message target string representation for given agent and
        collective.
    """


def get_reply_target(self, agent, collective):
    """Get the message target for the given agent and collective.

    :arg agent: MCollective target agent name.
    :arg collective: MCollective target collective.
    :return: message reply target string representation for given
        agent and collective.
    """


# Building Metaclass here for Python 2/3 compatibility
Connector = abc.ABCMeta('Connector', (BaseConnector,), {
    'get_target': abc.abstractmethod(get_target),
    'get_reply_target': abc.abstractmethod(get_reply_target),
})
