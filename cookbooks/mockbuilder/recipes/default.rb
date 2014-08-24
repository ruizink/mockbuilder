#
# Cookbook Name:: mock
# Recipe:: default
#

version = node["platform_version"].to_i

# Add EPEL repo
yum_repository "epel" do
  description "Extra Packages for Enterprise Linux"
  mirrorlist "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-#{version}&arch=$basearch"
  gpgkey "http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-#{version}"
  action :create
end

# Create mock group
group "mock" do
	action :create
end

user "vagrant" do
    gid "mock"
    action :modify
end

# Create a clean build environment
%w{
  /home/vagrant/packages
  /home/vagrant/packages/buildroot.clean
  /home/vagrant/packages/buildroot.clean/RPMS
  /home/vagrant/packages/buildroot.clean/SRPMS
  /home/vagrant/packages/buildroot.clean/SPECS
  /home/vagrant/packages/buildroot.clean/BUILD
  /home/vagrant/packages/buildroot.clean/SOURCES
}.each do |d|
	directory d do
		action :create
		owner "vagrant"
		group "mock"
		mode "0755"
	end
end

template "/home/vagrant/.rpmmacros" do
	source "rpmmacros.erb"
	owner "vagrant"
	group "mock"
	mode "0644"
  backup false
end

# Install required packages
%w{
  mock
  rpm-build
  redhat-rpm-config
  vim-enhanced
  git
}.each do |p|
	package p do
		action :install
	end
end

# Deploy mock configs
%w{
  el5-x86_64.cfg
  el6-x86_64.cfg
}.each do |f|
  cookbook_file f do
    path "/etc/mock/#{f}"
    action :create
    owner "vagrant"
    group "mock"
    mode "0644"
    backup false
  end
end
