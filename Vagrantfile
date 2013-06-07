Vagrant::Config.run do |config|
  # config.vm.box     = "oneiric32_base"
  # config.vm.box_url = "http://files.travis-ci.org/boxes/bases/oneiric32_base_v2.box"

  # Ubuntu 12.04, 32 bit
  config.vm.box     = "precise32_base"
  config.vm.box_url = "http://files.travis-ci.org/boxes/bases/precise32_base_v2.box"

  # Ubuntu 12.04, 64 bit
  # config.vm.box     = "precise64_base"
  # config.vm.box_url = "http://files.travis-ci.org/boxes/bases/precise64_base_v2.box"


  config.ssh.username = "travis"
  config.vm.forward_port 22, 2220

  #
  # For Vagrant 0.9.x and 1.0.x
  #

  config.vm.forward_port 22, 2220

  # For RabbitMQ stomp local use
  config.vm.forward_port 61613, 61613

  # changing nictype partially helps with Vagrant issue #516, VirtualBox NAT interface chokes when
  # # of slow outgoing connections is large (in dozens or more).
  config.vm.customize ["modifyvm", :id, "--nictype1", "Am79C973", "--memory", "1536", "--cpus", "2", "--ioapic", "on"]

  # see https://github.com/mitchellh/vagrant/issues/912
  config.vm.customize ["modifyvm", :id, "--rtcuseutc", "on"]

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      /opt/ruby/bin/gem install chef --no-ri --no-rdoc --no-user-install
    EOF
  end

  config.vm.provision :chef_solo do |chef|
    # this assumes you have travis-ci/travis-cookbooks cloned at ./cookbooks
    chef.cookbooks_path = ["cookbooks/ci_environment"]
    chef.log_level      = :debug

    # Highly recommended to keep apt packages metadata in sync and
    # be able to use apt mirrors.
    chef.add_recipe     "apt"

    # List the recipies you are going to work on/need.
    # chef.add_recipe     "build-essential"
    # chef.add_recipe     "networking_basic"

    # chef.add_recipe     "travis_build_environment"
    # chef.add_recipe     "git"

    # chef.add_recipe     "java::openjdk7"
    # chef.add_recipe     "leiningen"

    chef.add_recipe     "rabbitmq::with_management_plugin"

    # chef.add_recipe     "rvm"
    # chef.add_recipe     "rvm::multi"
    # chef.add_recipe     "nodejs::multi"
    # chef.add_recipe     "python::multi"

    # chef.add_recipe     "libqt4"
    # chef.add_recipe     "xserver"
    # chef.add_recipe     "firefox"

    # chef.add_recipe     "memcached"
    # chef.add_recipe     "redis"
    # chef.add_recipe     "riak"
    # chef.add_recipe     "mongodb"
    # chef.add_recipe     "mysql::client"
    # chef.add_recipe     "mysql::server"
    # chef.add_recipe     "postgresql::client"
    # chef.add_recipe     "postgresql::server"
    # chef.add_recipe     "couchdb::ppa"
    # chef.add_recipe     "neo4j-server::tarball"
    # chef.add_recipe     "firebird"

    # chef.add_recipe     "elasticsearch"
    # chef.add_recipe     "cassandra::datastax"
    # chef.add_recipe     "hbase::ppa"
    # chef.add_recipe     "pypy::ppa"
  end
  # Script to be run by trabvis too
  config.vm.provision :shell, :inline => 'cp /vagrant/scripts/rabbitmqadmin /tmp'
  config.vm.provision :shell, :path => 'scripts/rabbitmq.sh'
  # This would be managed by travis
  config.vm.provision :shell, :inline => 'service rabbitmq-server start'
end
