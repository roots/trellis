# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version '>= 1.5.1'

Vagrant.configure('2') do |config|
  config.vm.box = 'roots/bedrock'

  # Required for NFS to work, pick any local IP
  config.vm.network :private_network, ip: '192.168.50.5'
  config.vm.hostname = 'example.dev'

  if !Vagrant.has_plugin? 'vagrant-hostsupdater'
    puts 'vagrant-hostsupdater missing, please install the plugin:'
    puts 'vagrant plugin install vagrant-hostsupdater'
  else
    # If you have multiple sites/hosts on a single VM
    # uncomment and add them here
    #config.hostsupdater.aliases = %w(site2.dev)
  end

  # adjust paths relative to Vagrantfile
  # Use NFS for shared folders for better performance
  # Comment this line if you're on a windows machine
  # and uncomment the one below
  config.vm.synced_folder '../example.dev', '/srv/www/example.dev/current', nfs: true # *nix machines
  #config.vm.synced_folder '../example.dev', '/srv/www/example.dev/current', owner: 'vagrant', group: 'www-data', mount_options: ['dmode=776', 'fmode=775'] # windows machines

  config.vm.provision :ansible do |ansible|
    # adjust paths relative to Vagrantfile
    ansible.playbook = './site.yml'
    ansible.groups = {
      'web' => ['default'],
      'development' => ['default']
    }
    ansible.extra_vars = {
      ansible_ssh_user: 'vagrant',
      user: 'vagrant'
    }
    ansible.sudo = true
  end


  config.vm.provider 'virtualbox' do |vb|
    # Give VM access to all cpu cores on the host
    cpus = case RbConfig::CONFIG['host_os']
      when /darwin/ then `sysctl -n hw.ncpu`.to_i
      when /linux/ then `nproc`.to_i
      else 2
    end

    # Customize memory in MB
    vb.customize ['modifyvm', :id, '--memory', 1024]
    vb.customize ['modifyvm', :id, '--cpus', cpus]

    # Fix for slow external network connections
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
  end
end
