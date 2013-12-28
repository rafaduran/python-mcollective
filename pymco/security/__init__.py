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


def sign(self, message):
    """Signs the given message using provided security method.

    Args:
        ``message``: message to be signed.
    Returns:
        ``message``: signed message.
    """


def encode(self, message):
    """Encodes message using provided serialization.

    Args:
        ``message``: message to be encoded.
    Returns:
        ``message``: encoded message.
    """


def decode(self, message):
    """Decodes message using provided serialization.

    Args:
        ``message``: message to be decoded.
    Returns:
        ``message``: decoded message.
    """


# Building Metaclass here for Python 2/3 compatibility
SecurityProvider = abc.ABCMeta('SecurityProvider', (SecurityProviderBase,), {
    'sign': abc.abstractmethod(sign),
    'encode': abc.abstractmethod(encode),
    'decode': abc.abstractmethod(decode),
})
