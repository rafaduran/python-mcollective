version = node['activemq']['version']
activemq_home = "#{node['activemq']['home']}/apache-activemq-#{version}"

template "#{activemq_home}/conf/activemq.xml" do
  source   'activemq.xml.erb'
  mode     '0755'
  owner    'root'
  group    'root'
  notifies :restart, 'service[activemq]'
end

template "#{activemq_home}/conf/keystore.jks" do
  source   'keystore.jks'
  mode     '0600'
  owner    'root'
  group    'root'
  notifies :restart, 'service[activemq]'
end

template "#{activemq_home}/conf/truststore.jks" do
  source   'truststore.jks'
  mode     '0600'
  owner    'root'
  group    'root'
  notifies :restart, 'service[activemq]'
end
