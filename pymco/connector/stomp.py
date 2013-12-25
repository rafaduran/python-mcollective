"""
:py:mod:`pymco.connector.stomp`
"""
from __future__ import absolute_import

import stomp

from . import Connector


class StompConnector(Connector):
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

    @classmethod
    def default_connection(cls, config):
        """Creates a :py:class:`stomp.Connection` object with defaults"""
        return stomp.Connection(host_and_ports=config.get_host_and_ports())
