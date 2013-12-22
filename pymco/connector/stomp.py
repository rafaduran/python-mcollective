"""
:py:mod:`pymco.connector.stomp`
"""
from __future__ import absolute_import
import itertools

import stomp

from . import Connector
from .. import exc
from .. import listener


class StompConnector(Connector):
    id_generator = itertools.count()

    def __init__(self, config, security=None, connection=None):
        super(StompConnector, self).__init__(config)
        self._started = False
        self.config = config
        self._id = None
        self.security = security

        if connection is None:
            self.connection = StompConnector.default_connection()
        else:
            self.connection = connection

    def connect(self, wait=None):
        if not self.connection.connected:
            self.connection.start()
            self.connection.connect(username=self.config['plugin.stomp.user'],
                                    passcode=self.config['plugin.stomp.password'],
                                    wait=wait)

        return self

    def disconnect(self):
        if self.connection.connected:
            self.connection.disconnect()
            self.connection.stop()

        return self

    def send(self, msg, destination, *args, **kwargs):
        self.connection.send(body=self.security.encode(self.security.sign(msg)),
                             destination=destination)
        return self

    def subscribe(self, destination, id=None, *args, **kwargs):
        if not id:
            id = self.id

        self.connection.subscribe(destination, id=id)
        return self

    def unsubscribe(self, destination, *args, **kwargs):
        pass

    @property
    def id(self):
        if not self._id:
            self._id = next(self.id_generator)

        return self._id

    @staticmethod
    def default_connection():
        """Creates a :py:class:`stomp.Connection` object with defaults"""
        return stomp.Connection()

    def receive(self, timeout, *args, **kwargs):
        response_listener = listener.SingleResponseListener(timeout=timeout,
                                                            security=self.security,
                                                            config=self.config)
        self.connection.set_listener('response_listener', response_listener)
        response_listener.wait_on_message()

        if len(response_listener.responses) != 1:
            raise exc.TimeoutError

        return response_listener.responses[0]

    def get_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_target`"""
        return '{topic_prefix}{collective}.{agent}.command'.format(
            agent=agent,
            collective=collective,
            topic_prefix=self.config['topicprefix'],
        )

    def get_reply_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_reply_target`"""
        return '{topic_prefix}{collective}.{agent}.reply'.format(
            agent=agent,
            collective=collective,
            topic_prefix=self.config['topicprefix'],
        )
