"""
:py:mod:`pymco.rpc`
-------------------
MCollective RPC calls support.
"""


class SimpleAction(object):
    """Single RPC call to MCollective"""
    def __init__(self, config, msg, agent, connector, **kwargs):
        self.config = config
        self.msg = msg
        self.agent = agent
        self.connector = connector
        self.collective = (kwargs.get('collective', None) or
                           self.config['main_collective'])

    def get_target(self):
        """MCollective RPC call target."""
        # this is hardcoded
        return '/topic/mcollective.{agent}.command'.format(agent=self.agent)

    def get_reply_target(self):
        """MCollective RPC call reply target.

        This should build the subscription target required for listening replies
        to this RPC call.
        """
        # this is hardcoded
        return '/topic/mcollective.{agent}.reply'.format(agent=self.agent)

    def call(self, timeout=5):
        """Make the RPC call.

        It should subscribe to the reply target, execute the RPC call and wait
        for the result.
        """
        self.connector.connect(wait=True)
        self.connector.subscribe(destination=self.get_reply_target())
        self.connector.send(self.msg, self.get_target())
        result = self.connector.receive(timeout=timeout)
        self.connector.disconnect()
        return result
