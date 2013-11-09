# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Ubuntu 12.04, 64 bit
  config.vm.box     = "precise64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"

  # For RabbitMQ stomp local use
  config.vm.network 'forwarded_port', guest:  61613, host: 61613

  config.vm.provider :virtualbox do |vb|
    # changing nictype partially helps with Vagrant issue #516, VirtualBox NAT interface chokes when
    # of slow outgoing connections is large (in dozens or more).
    vb.customize ["modifyvm", :id, "--nictype1", "Am79C973", "--cpus", "2", "--ioapic", "on"]

    # see https://github.com/mitchellh/vagrant/issues/912
    vb.customize ["modifyvm", :id, "--rtcuseutc", "on"]

    # Don't boot with headless mode
    # vb.gui = true

    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      gem install chef --no-ri --no-rdoc --no-user-install
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
  # This would be managed by travis
  config.vm.provision :shell, :inline => 'service rabbitmq-server start'
  config.vm.provision :shell, :inline => 'cp /vagrant/scripts/rabbitmqadmin /tmp'
  # Script to be run by travis too
  config.vm.provision :shell, :path => 'scripts/rabbitmq.sh'
end
