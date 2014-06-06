require 'puppet'

module MCollective
  module Agent
    class Demo<RPC::Agent
      action :mounts  do
        reply[:mounts] = Puppet::Resource.indirection.search('mount/', {})
      end
    end
  end
end
