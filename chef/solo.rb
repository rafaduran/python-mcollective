basedir = File.expand_path(File.join '..', (File.dirname __FILE__))
cookbook_path [File.join(basedir, 'extra_cookbooks'), File.join(basedir, 'cookbooks/ci_environment')]
file_cache_path    "/var/chef/cache"
file_backup_path   "/var/chef/backup"
log_level :debug
verbose_logging    false

encrypted_data_bag_secret "/tmp/encrypted_data_bag_secret"





http_proxy nil
http_proxy_user nil
http_proxy_pass nil
https_proxy nil
https_proxy_user nil
https_proxy_pass nil
no_proxy nil


