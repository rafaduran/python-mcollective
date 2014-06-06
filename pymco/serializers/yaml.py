"""
Security providers base
-----------------------
Provides YAML [de]serialization.
"""
from __future__ import print_function
from __future__ import absolute_import

from . import SerializerBase

try:
    import yaml
except ImportError as exc:
    print("You must install PyYAML in order to use YAML serializer.")
    raise exc


def ruby_object_constructor(loader, suffix, node):
    """YAML constructor for Ruby objects.

    This constructor may be registered with '!ruby/object:' tag as multi
    constructor supporting Ruby objects. This will handle give objects as maps,
    so any non mapping based object may produce some issue.
    """
    return loader.construct_yaml_map(node)


def symbol_constructor(loader, node):
    """YAML constructor for Ruby symbols.

    This constructor may be registered with '!ruby/sym' tag in order to
    support Ruby symbols serialization (you can use
    :py:meth:`register_constructors` for that), so it just need return the
    string scalar representation of the key.
    """
    return loader.construct_scalar(node)


class RubyCompatibleLoader(yaml.SafeLoader):
    """YAML loader compatible with Ruby Symbols"""


RubyCompatibleLoader.add_constructor(u'!ruby/sym', symbol_constructor)
RubyCompatibleLoader.add_multi_constructor(u'!ruby/object:',
                                           ruby_object_constructor)


class Serializer(SerializerBase):
    """YAML specific serializer."""
    def serialize(self, msg):
        return yaml.safe_dump(dict(msg))

    def deserialize(self, msg):
        return yaml.load(msg, Loader=RubyCompatibleLoader)
