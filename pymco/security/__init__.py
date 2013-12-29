"""MCollective security provider implementations."""
import abc


class SecurityProviderBase(object):
    """Abstract base class for security providers."""
    plugins = {
        'none': 'pymco.security.none.NoneProvider',
        'ssl': 'pymco.security.ssl.SSLProvider',
    }

    def __init__(self, config):
        """Abstract method to be overriden for subclasses.

        Args:
            ``config``: Configuration instance.
        """
        self.config = config

    def serialize(self, message):
        """Serialize message using provided serialization.

        Args:
            ``message``: message to be encoded.
        Returns:
            ``message``: encoded message.
        """
        return self.serializer.serialize(message)

    def deserialize(self, message):
        """Deserealize message using provided serialization.

        Args:
            ``message``: message to be decoded.
        Returns:
            ``message``: decoded message.
        """
        return self.serializer.deserialize(message)


def sign(self, message):
    """Signs the given message using provided security method.

    Args:
        ``message``: message to be signed.
    Returns:
        ``message``: signed message.
    """


def verify(self, message):
    """Verify the given message using provided security method.

    Args:
        ``message``: message to be verified.
    Returns:
        ``message``: verified message.
    Raises:
        :py:exc:`pymco.exc.MessageVerificationError`: If the message
        verification failed.
    """


# Building Metaclass here for Python 2/3 compatibility
SecurityProvider = abc.ABCMeta('SecurityProvider', (SecurityProviderBase,), {
    'sign': abc.abstractmethod(sign),
    'verify': abc.abstractmethod(verify),
})
