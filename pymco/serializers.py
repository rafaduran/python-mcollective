'''pymco Message [de]serialization

Hightly inspired on how Django handles [de]serialization.'''
import importlib

from . import exc

BUILTIN_SERIALIZERS = {}
_SERIALIZERS = {}
# Check for PyYaml and register the serializer if it's available.
try:
    import yaml
    BUILTIN_SERIALIZERS["yaml"] = "pymco.serializers.yaml"
except ImportError:
    pass


def serialize(format_, message, **options):
    '''Serializes given message using given format and options.'''
    serializer = get_serializer(format_)()
    return serializer.serialize(message, **options)


def deserialize(format_, message, **options):
    '''Deserializes given message using given format and options.'''
    deserializer = get_deserializer(format_)()
    return deserializer.deserialize(message, **options)


def register_serializer(format_, serializer_module, serializers=None):
    """Register a new serializer.

    ``serializer_module`` should be the fully qualified module name
    for the serializer.

    If ``serializers`` is provided, the registration will be added
    to the provided dictionary.

    If ``serializers`` is not provided, the registration will be made
    directly into the global register of serializers. Adding serializers
    directly is not a thread-safe operation.
    """
    if serializers is None and not _SERIALIZERS:
        _load_serializers()
    module = importlib.import_module(serializer_module)
    if serializers is None:
        _SERIALIZERS[format_] = module
    else:
        serializers[format_] = module

def unregister_serializer(format_):
    "Unregister a given serializer. This is not a thread-safe operation."
    if not _SERIALIZERS:
        _load_serializers()
    if format_ not in _SERIALIZERS:
        raise exc.SerializerDoesNotExist(format_)
    del _SERIALIZERS[format_]


def get_serializer(format_):
    '''Loads serializers (if they weren't already loaded) and returns the
    registered serializer for given format.

    Raises :py:exc:`pymco.exc.SerializerDoesNotExist` if there is not
    registered serializer for the given format.'''
    if not _SERIALIZERS:
        _load_serializers()
    if format_ not in _SERIALIZERS:
        raise exc.SerializerDoesNotExist(format_)
    return _SERIALIZERS[format_].Serializer


def get_serializer_formats():
    '''Loads serializers (if they weren't already loaded) and returns the
    a list with all supported formats.'''
    if not _SERIALIZERS:
        _load_serializers()
    return list(_SERIALIZERS)


def get_deserializer(format_):
    '''Loads serializers (if they weren't already loaded) and returns the
    registered deserializer for given format.

    Raises :py:exc:`pymco.exc.SerializerDoesNotExist` if there is not
    registered serializer for the given format.'''
    if not _SERIALIZERS:
        _load_serializers()
    if format_ not in _SERIALIZERS:
        raise exc.SerializerDoesNotExist(format_)
    return _SERIALIZERS[format_].Deserializer
    # return _SERIALIZERS[format_]


def _load_serializers():
    '''Register built-in serializers.'''
    global _SERIALIZERS
    serializers = {}
    for format_ in BUILTIN_SERIALIZERS:
        register_serializer(format_, BUILTIN_SERIALIZERS[format_], serializers)
    _SERIALIZERS = serializers
    return _SERIALIZERS
