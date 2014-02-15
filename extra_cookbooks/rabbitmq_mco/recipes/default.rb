template "/etc/rabbitmq/ca.pem" do
  source "ca.pem"
  owner "root"
  group "root"
  mode 0644
end

template "/etc/rabbitmq/cert.pem" do
  source "cert.pem"
  owner "root"
  group "root"
  mode 0644
end

template "/etc/rabbitmq/key.pem" do
  source "cert.pem"
  owner "root"
  group "root"
  mode 0644
end

template "/etc/rabbitmq/rabbitmq.config" do
  source "rabbitmq.config.erb"
  owner "root"
  group "root"
  mode 0644
  notifies :restart, "service[rabbitmq-server]", :delayed
end
