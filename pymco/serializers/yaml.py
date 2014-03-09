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


class Serializer(SerializerBase):
    """YAML specific serializer."""
    def serialize(self, msg):
        return yaml.safe_dump(dict(msg))

    def deserialize(self, msg):
        return yaml.safe_load(msg)
