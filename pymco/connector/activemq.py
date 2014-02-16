"""
:py:mod:`pymco.connector.activemq`
----------------------------------
Contains ActiveMQ specific connector.
"""
import os

from . import Connector


class ActiveMQConnector(Connector):
    """ActiveMQ middleware specific connector."""
    def send(self, msg, destination, *args, **kwargs):
        """Re-implement :py:meth:`pymco.connector.Connector.send`

        This implementation adds extra features for ActiveMQ.
        """
        if 'plugin.activemq.priority' in self.config:
            kwargs['priority'] = self.config['plugin.activemq.priority']

        super(ActiveMQConnector, self).send(msg, destination, *args, **kwargs)

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
