Introduction
------------
Python bindings for `MCollective`_ inspired by `mcollective-python`_ example.
Making a ping discovery agent call is just 3 lines::

   >>> config = config.Config.from_configfile('client.cfg')
   >>> msg = message.Message(body='ping', agent='discovery', config=config)
   >>> pprint.pprint(rpc.SimpleAction(config=config, msg=msg, agent='discovery').call())
   [{':body': 'pong',
     ':msgtime': 1395419893,
     ':requestid': '003ba8142857ccb42cfc4d51262739ecafd43aca',
     ':senderagent': 'discovery',
     ':senderid': 'mco1'}]

.. _mcollective-python: https://github.com/iwebhosting/mcollective-python
.. _MCollective: http://puppetlabs.com/mcollective

Features
--------

* MCollective 2.0 - 2.4

* Python 2.6 - 3.4

* All MCollective connectors (STOMP, RabbitMQ, ActiveMQ)

* SSL security provider (YAML serialization)

* Battle tested

* MCollective configuration files parsing

* MCollective filters

Installation
------------
Install it just with pip::

   $ pip install --pre python-mcollective

The ``pre`` argument is required since there is no stable releases yet.

Contribute
----------

* Issue Tracker: https://github.com/rafaduran/python-mcollective/issues
* Source Code: https://github.com/rafaduran/python-mcollective
* Documentation: http://python-mcollective.readthedocs.org/en/latest/

Support
-------

If you are having issues, please just open an issue on GitHub.

License
-------

The project is licensed under the BSD license.
