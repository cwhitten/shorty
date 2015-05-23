# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure('2') do |config|
  ram_gb = 512
  cpus = 1

  config.vm.box = 'precise64'
  config.vm.hostname = 'shorty'
  config.ssh.forward_agent = true
  config.vm.network :private_network, ip: '192.168.1.101'

  config.vm.synced_folder './', '/var/www/shorty', nfs: true

  config.vm.provider 'vmware_fusion' do |provider, override|
    override.vm.box_url = 'http://files.vagrantup.com/precise64_vmware.box'
    provider.vmx['memsize'] = ram_gb.to_s
    provider.vmx['numvcpus'] = cpus.to_s
  end
end
