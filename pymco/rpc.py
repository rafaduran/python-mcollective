"""
:py:mod:`pymco.rpc`
-------------------
MCollective RPC calls support.
"""


class SimpleAction(object):
    """Single RPC call to MCollective"""
    def __init__(self, config, msg, agent, **kwargs):
        self.config = config
        self.msg = msg
        self.agent = agent
        self._connector = None
        self.collective = (kwargs.get('collective', None) or
                           self.config['main_collective'])

    @property
    def connector(self):
        if not self._connector:
            self._connector = self.config.get_connector()
        return self._connector

    def get_target(self):
        """MCollective RPC call target."""
        return self.connector.get_target(collective=self.collective,
                                         agent=self.agent)

    def get_reply_target(self):
        """MCollective RPC call reply target.

        This should build the subscription target required for listening replies
        to this RPC call.
        """
        return self.connector.get_reply_target(collective=self.collective,
                                               agent=self.agent)

    def call(self, timeout=5):
        """Make the RPC call.

        It should subscribe to the reply target, execute the RPC call and wait
        for the result.
        """
        self.connector.connect(wait=True)
        reply_target = self.get_reply_target()
        self.connector.subscribe(destination=reply_target)
        self.connector.send(self.msg,
                            self.get_target(),
                            **{'reply-to': reply_target})
        result = self.connector.receive(timeout=timeout)
        self.connector.disconnect()
        return result
