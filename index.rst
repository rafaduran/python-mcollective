Python MCollective RPC Client
=============================

mcollective-python is an attempt to build Python compatible RPC bindings for
PuppetLabs' MCollective.

Only an RPC client is included.

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

.. automodule:: mcollective
  :members:

.. autoexception:: AlreadySentException
  :members:

.. autoclass:: Message
  :members: __init__, sign, subscribe_to_replies, send, collect_results, send_and_await_results

.. autoclass:: Filter
  :members: __init__, add_fact, dump
