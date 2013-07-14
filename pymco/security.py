'''MCollective security provider implementations.'''
import abc
import getpass

import six


class SecurityProvider(six.with_metaclass(abc.ABCMeta)):
    '''Abstract base class for security providers.'''

    def __init__(self, config):
        '''
        Abstract method to be overriden for subclasses.

        Args:
            config: Configuration instance
        '''
        self.config = config

    @abc.abstractmethod
    def sign(self, message):
        '''
        Signs the given message using provided security method.

        Args:
            message: message to be signed.
        Returns: signed message
        '''

    def encode(self, message):
        '''
        Encodes message using provided serialization.

        Args:
            message: message to be encoded.
        Returns: encoded message
        '''

    def decode(self, message):
        '''
        Decodes message using provided serialization.

        Args:
            message: message to be decoded.
        Returns: decoded message
        '''


class NoneProvider(SecurityProvider):
    '''Provides message signing for MCollective::Security::None security
    provider (included into fixtures directory)'''
    def sign(self, message):
        '''
        Signs the given message using provided security method. Implements
        super abstract method.

        Args:
            message: message to be signed.
        Returns: signed message
        '''
        message[':callerid'] = 'user={0}'.format(getpass.getuser())
        return message
