metadata :name        => "demo",
         :description => "demo agent",
         :author      => "Rafael Durán Castañeda",
         :license     => "GPLv2",
         :version     => "1.0",
         :url         => "https://github.com/rafaduran/python-mcollective",
         :timeout     => 5

action "mounts", :description => "Get filesystem mounts with puppet" do
  display :always

  output :mounts,
         :description => "Filesystem mounts",
         :display_as  => "Mounts"
end
