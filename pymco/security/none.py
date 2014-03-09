"""
:py:mod:`pymco.security.none`
-----------------------------
Contains none specific security provider.
"""
import getpass

from . import SecurityProvider
from .. serializers import yaml


class NoneProvider(SecurityProvider):
    """Provides message signing for MCollective::Security::None sec. provider

    The none provider is a dummy provider just for developing that isn't
    included with MCollective but into fixtures directory."""
    serializer = yaml.Serializer()

    def sign(self, message):
        """Implement :py:meth:`pymco.security.SecurityProvider.sign`.

        Add the current user as ``:callerid`` key to the message.
        """
        message[':callerid'] = 'user={0}'.format(getpass.getuser())
        return message

    def verify(self, message):
        """Implement :py:meth:`pymco.security.SecurityProvider.verify`.

        It does nothing, returning always given message.
        """
        return message
