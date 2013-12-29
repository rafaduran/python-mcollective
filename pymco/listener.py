"""
:py:mod:`pymco.listeners`
-------------------------
stomp.py listeners for python-mcollective.
"""
import functools
import threading
import time

from stomp import listener


class ResponseListener(listener.ConnectionListener):
    """Listener that waits for a message response."""
    def __init__(self, config, count, timeout=30, condition=None):
        self.config = config
        self._security = None
        self.timeout = timeout
        if not condition:
            condition = threading.Condition()

        self.condition = condition
        self.received = 0
        self.responses = []
        self.count = count

    @property
    def security(self):
        """Security provider property"""
        if not self._security:
            self._security = self.config.get_security()

        return self._security

    def on_message(self, headers, body):
        self.condition.acquire()
        self.responses.append(self.security.deserialize(body))
        self.received += 1
        self.condition.notify()
        self.condition.release()

    def wait_on_message(self):
        """Wait until we get a message."""
        self.condition.acquire()
        self._wait_loop(self.timeout)
        self.condition.release()
        self.received = 0
        return self

    def _wait_loop(self, timeout):
        while self.received < self.count:
            init_time = time.time()
            self.condition.wait(timeout)
            current_time = time.time()
            timeout -= (current_time - init_time)
            if timeout <= 0:
                break


SingleResponseListener = functools.partial(ResponseListener, count=1)
