"""
:py:mod:`pymco.connector.activemq`
----------------------------------
Contains ActiveMQ specific connector.
"""
import os

from .stomp import StompConnector


class ActiveMQConnector(StompConnector):
    """ActiveMQ middleware specific connector."""

    def get_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_target`"""
        return '/topic/{collective}.{agent}.agent'.format(
            agent=agent,
            collective=collective,
        )

    def get_reply_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_reply_target`"""
        return '/queue/{collective}.reply.{identity}_{pid}'.format(
            collective=collective,
            identity=self.config['identity'],
            pid=os.getpid(),
        )
