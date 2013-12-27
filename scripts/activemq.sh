ROOT="`dirname $0`/.."
ROOT=`readlink -e $ROOT`

cat << EOF > /tmp/dna.json
{
  "run_list": [
    "recipe[activemq]",
    "recipe[activemq_mco]"
  ]
}
EOF

cat << EOF > /tmp/solo.rb
file_cache_path    "/tmp/chef/cache"
file_backup_path   "/tmp/chef/backup"
cookbook_path ["${ROOT}/cookbooks/ci_environment", "${ROOT}/extra_cookbooks"]
log_level :debug
verbose_logging    false

encrypted_data_bag_secret "/tmp/encrypted_data_bag_secret"
EOF

chef-solo -c /tmp/solo.rb -j /tmp/dna.json
