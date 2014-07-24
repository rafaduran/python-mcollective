"""
:py:mod:`pymco.connector.activemq`
----------------------------------
Contains ActiveMQ specific connector.
"""
import logging
import os

from . import Connector

LOG = logging.getLogger(__name__)


class ActiveMQConnector(Connector):
    """ActiveMQ middleware specific connector."""
    def __init__(self, config, connection=None, logger=LOG):
        super(ActiveMQConnector, self).__init__(config,
                                                connection=connection,
                                                logger=logger)

    def send(self, msg, destination, *args, **kwargs):
        """Re-implement :py:meth:`pymco.connector.Connector.send`

        This implementation adds extra features for ActiveMQ.
        """
        if 'plugin.activemq.priority' in self.config:
            kwargs['priority'] = self.config['plugin.activemq.priority']

        self.logger.debug("ActiveMQ send destination={d}".format(d=destination))
        super(ActiveMQConnector, self).send(msg, destination, *args, **kwargs)

    def get_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_target`"""
        target = '/topic/{collective}.{agent}.agent'.format(
            agent=agent,
            collective=collective,
        )
        self.logger.debug("ActiveMQConnector target: {t}".format(t=target))
        return target

    def get_reply_target(self, agent, collective):
        """Implement :py:meth:`pymco.connector.Connector.get_reply_target`"""
        target = '/queue/{collective}.reply.{identity}_{pid}'.format(
            collective=collective,
            identity=self.config['identity'],
            pid=os.getpid(),
        )
        self.logger.debug("ActiveMQConnector reply target: {t}".format(t=target))
        return target
