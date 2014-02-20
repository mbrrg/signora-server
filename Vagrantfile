# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "debian7-untrusted"
  config.vm.box_url = "https://dl.dropboxusercontent.com/s/xymcvez85i29lym/vagrant-debian-wheezy64.box"
  config.vm.network :forwarded_port, guest: 8000, host: 8080
  config.vm.network :forwarded_port, guest: 9000, host: 9000
  config.vm.provision :shell, :path => "bootstrap.sh"
end
