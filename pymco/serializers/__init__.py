"""
Serializers base
----------------
pymco Message [de]serialization.
"""
import abc


def serialize(self, msg):
    """Serialize a MCollective msg.

    :arg msg: message to be serialized.
    :return: serialized message.
    """


def deserialize(self, msg):
    """De-serialize a MCollective msg.

    :arg pymco.message.Message msg: message to be de-serialized.
    :return: de-serialized message.
    """

# Building Metaclass here for Python 2/3 compatibility
SerializerBase = abc.ABCMeta('SerializerBase', (object,), {
    '__doc__': 'Base class for all serializers.',
    'serialize': abc.abstractmethod(serialize),
    'deserialize': abc.abstractmethod(deserialize),
    'plugins': {
        'yaml': 'pymco.serializers.yaml.Serializer',
    }
})
