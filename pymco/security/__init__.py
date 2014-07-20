"""
Security providers base
-----------------------
MCollective security providers base.
"""
import abc
import base64


class SecurityProviderBase(object):
    """Abstract base class for security providers.

    :arg config: :py:class:`pymco.config.Config` instance.
    """
    plugins = {
        'none': 'pymco.security.none.NoneProvider',
        'ssl': 'pymco.security.ssl.SSLProvider',
    }

    def __init__(self, config):
        self.config = config

    def serialize(self, msg):
        """Serialize message using provided serialization.

        :arg pymco.message.Message msg: message to be encoded.
        :return: encoded message.
        """
        return self.serializer.serialize(msg)

    def deserialize(self, msg):
        """Deserealize message using provided serialization.

        :arg pymco.message.Message msg: message to be decoded.
        :return: decoded message.
        """
        return self.serializer.deserialize(msg)

    def encode(self, msg, b64=False):
        """Encode given message using provided security method.

        Encode will consist just on singing the message and serialize it, so
        we can sent it and verified for the receivers.

        :arg pymco.message.Message msg: Message to be serialized.
        :return: Encoded message.
        """
        signed_msg = self.serialize(self.sign(msg))
        if b64:
            signed_msg = base64.b64encode(signed_msg)
        return signed_msg

    def decode(self, msg, b64=False):
        """Decode given message using provided security method.

        Decode will consist just on de-serialize the given message and verify
        it, raising a verification error if the message can't be verified.

        :arg pymco.message.Message msg: Message to be serialized.
        :return: Decoded message, a :py:class:`dict` like object.
        """
        if b64:
            msg = base64.b64decode(msg)
        return self.verify(self.deserialize(msg))


def sign(self, msg):
    """Signs the given message using provided security method.

    :arg pymco.message.Message msg: message to be signed.
    :return: signed message.
    """


def verify(self, msg):
    """Verify the given message using provided security method.

    :arg pymco.message.Message msg: message to be verified.
    :return: verified message.
    :raise pymco.exc.MessageVerificationError: If the message verification
        failed.
    """


# Building Metaclass here for Python 2/3 compatibility
SecurityProvider = abc.ABCMeta('SecurityProvider', (SecurityProviderBase,), {
    'sign': abc.abstractmethod(sign),
    'verify': abc.abstractmethod(verify),
})
