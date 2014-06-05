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
RubyCompatibleLoader.add_constructor(
    u'!ruby/object:Puppet::Resource',
    RubyCompatibleLoader.construct_yaml_map,
)


class Serializer(SerializerBase):
    """YAML specific serializer."""
    def serialize(self, msg):
        return yaml.safe_dump(dict(msg))

    def deserialize(self, msg):
        return yaml.load(msg, Loader=RubyCompatibleLoader)
