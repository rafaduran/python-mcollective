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
            self.connection = StompConnector.default_connection()
        else:
            self.connection = connection

    def connect(self):
        if not self.connection.connected:
            self.connection.start()
            self.connection.connect(username=self.config['plugin.stomp.user'],
                                    passcode=self.config['plugin.stomp.password'])

        return self

    def disconnect(self):
        if self.connection.connected:
            self.connection.disconnect()
            self.connection.stop()

        return self

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
