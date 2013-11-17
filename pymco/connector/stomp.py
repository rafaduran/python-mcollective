"""
:py:mod:`pymco.connector.stomp`
"""
from __future__ import absolute_import
import stomp

from . import Connector


class StompConnector(Connector):
    def __init__(self, config, connection=None):
        super(StompConnector, self).__init__(config)
        self._started = False
        self.config = config

        if connection is None:
            self._connection = StompConnector.default_connection()
        else:
            self._connection = connection

    @property
    def connection(self):
        """Property wrapper over stomp.py connection

        It starts the connection and connect using credentials from ``config``
        object on first use.
        """
        if not self._connection.connected():
            self._connection.start()
            self._connection.connect(username=self.config['plugin.stomp.user'],
                                     passcode=self.config['plugin.stomp.password'])

        return self._connection

    def send(self, msg, destination, *args, **kwargs):
        self.connection.send(msg, destination)
        return self

    def subscribe(self, destination, *args, **kwargs):
        pass

    def unsubscribe(self, destination, *args, **kwargs):
        pass

    @staticmethod
    def default_connection():
        """Creates a :py:class:`stomp.Connection` object with defaults"""
        return stomp.Connection()
