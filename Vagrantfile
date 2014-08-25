# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Base box
  config.vm.box = "centos65-minimal-x86_64"
  config.vm.box_url = "https://dl.dropboxusercontent.com/s/o8eorprrih1zt22/centos65-minimal-x86_64.box"

  # Install chef with omnibus
  config.omnibus.chef_version = "latest"

  # Customize VM
  config.vm.hostname = "mockbuilder"
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cpus", 2]
    vb.customize ["modifyvm", :id, "--memory", 1024]
  end

  config.vm.provision :chef_solo do |chef|

    # Chef config
    chef.log_level = :debug
    chef.verbose_logging = false
    chef.custom_config_path = "Vagrantfile.chef"

    chef.cookbooks_path   = "cookbooks"

    chef.add_recipe "mockbuilder"

  end
end
