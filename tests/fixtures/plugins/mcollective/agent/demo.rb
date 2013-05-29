module MCollective
  module Agent
    class Demo<RPC::Agent
      action :get do
        reply[:data] = {
          :host_info => {
            'rpms' => {'python' => {'version' => '123'}},
            'files'=> {'/etc/my.conf' => {'md5' => 's43534534534543sdfs'}}}
        }
      end
    end
  end
end
