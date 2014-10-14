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

  # Make sure ot have vagrant-berkshelf installed before enabling it
  if Vagrant.has_plugin?("vagrant-berkshelf")
    config.berkshelf.enabled = true
  else
    error = "The vagrant-berkshelf plugin is not installed! Try running:\nvagrant plugin install vagrant-berkshelf"
    raise Exception, error
  end

  config.vm.provision :chef_solo do |chef|
    # Chef config
    chef.custom_config_path = ".Vagrantfile.chef"
    chef.cookbooks_path   = "chef/cookbooks"
    chef.add_recipe "mockbuilder"
  end
end
