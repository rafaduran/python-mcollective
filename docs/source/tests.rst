Running the tests
=================

Travis-CI
---------
All pull requests will be tested with `Travis-CI`_, so you can just trust on
it. However it's recommend to test locally before sending the pull request,
sections below will show you how to do that.

Vagrant setup
-------------
The repository is ready for running a `Vagrant`_ box with all needed in order
to deploy an VM with RabbitMQ and ActiveMQ with and without SSL. You can start
it just typing::

   $ vagrant up

This is required for running integration tests locally, thought you can install
both locally.

Running integration tests without Vagrant
-----------------------------------------
`Vagrant setup`_ is ready so everything may work if you install and configure
ActiveMQ and RabbitMQ locally. Next steps will guide you for getting both
working.

ActiveMQ
~~~~~~~~
From repository root:

* Run ``activemq.sh`` script::

  $ scripts/activemq.sh

RabbitMQ
~~~~~~~~
From repository ``chef`` directory:

* Install Chef if you don't have it installed::

  $ bundle install

* Run chef-solo::

  $ chef-solo -c solo.rb -j dna.json

Then from repository root:

* Run ``rabbitmq.sh`` script::

  $ scripts/rabbitmq.sh

Local MCollective setup
-----------------------
In order to run MCollective locally you will need:

* RabbitMQ or ActiveMQ running: you can use provided `Vagrant`_ setup or just
  install one of them locally.

* Clone Git submodules if you didn't clone the repository recursively::

  $ git submodule init
  $ git submodule update

* Install dependencies, from repository root::

  $ bundle install

* Then you need configuration files placed in the repository root, into
  ``examples`` directory you will find some configuration examples::

     $ cp examples/server.23x.activemq.cfg server.cfg
     $ cp examples/server.23x.activemq.cfg client.cfg

  Edit configuration files to fix paths for your working directory.

* Then you should be able to run both, the daemon and the client::

     $ scripts/mcollectived

  From another terminal::

     $ scripts/mco ping

  Now everything should be working and you should see ``mco ping`` output,
  otherwise you will need review steps before.

This is also required for running integration tests, since they spawn
MCollective daemons so we can make RPC calls to them.


Running py.test
---------------
`pytest`_ is the test framework for python-mcollective, in order to run the
tests with it:

* You probably want to create a virtualenv, with `virtualenvwrapper`_::

  $ mkvirtualenv pymco

* Install dependencies::

  $ pip install -r requirements/tests.txt

* Then just type::

  $ py.test

You can skip integration tests just typing::

   $ py.test tests/unit

or run only integration with::

   $ py.test tests/integration


Running tox
-----------
Additionally you can run `tox`_ for Python compatibility testing, style
checks and documentation building. This setup is pretty close to the
`Travis-CI`_, so if tests pass it should pass `Travis-CI`_.

.. _pytest: http://pytest.org/latest/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _Vagrant: http://www.vagrantup.com
.. _tox: http://tox.readthedocs.org/en/latest/
.. _Travis-CI: https://travis-ci.org
