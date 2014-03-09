"""
:py:mod:`pymco.connector.rabbitmq`
----------------------------------
RabbitMQ specific connector plugin.
"""
from __future__ import absolute_import

from . import Connector


class RabbitMQConnector(Connector):
    """RabbitMQ middleware specific connector."""

    def get_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_target`"""
        return '/exchange/{collective}_broadcast/{agent}'.format(
            agent=agent,
            collective=collective,
        )

    def get_reply_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_reply_target`"""
        return '/queue/{collective}_reply_{agent}'.format(
            agent=agent,
            collective=collective,
        )
