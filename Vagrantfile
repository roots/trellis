# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

ANSIBLE_PATH = __dir__ # absolute path to Ansible directory

# Set Ansible roles_path relative to Ansible directory
ENV['ANSIBLE_ROLES_PATH'] = File.join(ANSIBLE_PATH, 'vendor', 'roles')

config_file = File.join(ANSIBLE_PATH, 'group_vars', 'development', 'wordpress_sites.yml')

def fail_with_message(msg)
  fail Vagrant::Errors::VagrantError.new, msg
end

if File.exists?(config_file)
  wordpress_sites = YAML.load_file(config_file)['wordpress_sites']
  fail_with_message "No sites found in #{config_file}." if wordpress_sites.to_h.empty?
else
  fail_with_message "#{config_file} was not found. Please set `ANSIBLE_PATH` in your Vagrantfile."
end

if !Dir.exists?(ENV['ANSIBLE_ROLES_PATH']) && !Vagrant::Util::Platform.windows?
  fail_with_message "You are missing the required Ansible Galaxy roles, please install them with this command:\nansible-galaxy install -r requirements.yml"
end

Vagrant.require_version '>= 1.5.1'

Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.ssh.forward_agent = true

  # Fix for: "stdin: is not a tty"
  # https://github.com/mitchellh/vagrant/issues/1673#issuecomment-28288042
  config.ssh.shell = %{bash -c 'BASH_ENV=/etc/profile exec bash'}

  # Required for NFS to work, pick any local IP
  config.vm.network :private_network, ip: '192.168.50.5', hostsupdater: 'skip'

  hostname, *aliases = wordpress_sites.flat_map { |(_name, site)| site['site_hosts'] }
  config.vm.hostname = hostname
  www_aliases = ["www.#{hostname}"] + aliases.map { |host| "www.#{host}" }

  if Vagrant.has_plugin? 'vagrant-hostmanager'
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.aliases = aliases + www_aliases
  else
    fail_with_message "vagrant-hostmanager missing, please install the plugin with this command:\nvagrant plugin install vagrant-hostmanager"
  end

  if Vagrant::Util::Platform.windows?
    wordpress_sites.each_pair do |name, site|
      config.vm.synced_folder local_site_path(site), remote_site_path(name), owner: 'vagrant', group: 'www-data', mount_options: ['dmode=776', 'fmode=775']
    end
    config.vm.synced_folder File.join(ANSIBLE_PATH, 'hosts'), File.join(ANSIBLE_PATH.sub(__dir__, '/vagrant'), 'hosts'), mount_options: ['dmode=755', 'fmode=644']
  else
    if !Vagrant.has_plugin? 'vagrant-bindfs'
      fail_with_message "vagrant-bindfs missing, please install the plugin with this command:\nvagrant plugin install vagrant-bindfs"
    else
      wordpress_sites.each_pair do |name, site|
        config.vm.synced_folder local_site_path(site), nfs_path(name), type: 'nfs'
        config.bindfs.bind_folder nfs_path(name), remote_site_path(name), u: 'vagrant', g: 'www-data', o: 'nonempty'
      end
    end
  end

  if Vagrant::Util::Platform.windows?
    config.vm.provision :shell do |sh|
      sh.path = File.join(ANSIBLE_PATH, 'windows.sh')
    end
  else
    config.vm.provision :ansible do |ansible|
      ansible.playbook = File.join(ANSIBLE_PATH, 'dev.yml')
      ansible.groups = {
        'web' => ['default'],
        'development' => ['default']
      }

      if vars = ENV['ANSIBLE_VARS']
        extra_vars = Hash[vars.split(',').map { |pair| pair.split('=') }]
        ansible.extra_vars = extra_vars
      end
    end
  end

  # Give VM access to all cpu cores on the host
  cpus = case RbConfig::CONFIG['host_os']
    when ENV['NUMBER_OF_PROCESSORS'] then ENV['NUMBER_OF_PROCESSORS'].to_i
    when /darwin/ then `sysctl -n hw.ncpu`.to_i
    when /linux/ then `nproc`.to_i
    else 2
  end

  # Give VM more memory
  memory = 1024

  # Virtualbox settings
  config.vm.provider 'virtualbox' do |vb|
    # Customize  VM settings
    vb.customize ['modifyvm', :id, '--memory', memory]
    vb.customize ['modifyvm', :id, '--cpus', cpus]

    # Fix for slow external network connections
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']

    # Set VM name
    vb.name = config.vm.hostname
  end

  # VMware Workstation/Fusion settings
  ['vmware_fusion', 'vmware_workstation'].each do |provider|
    config.vm.provider provider do |vmw, override|
      # Override provider box
      override.vm.box = 'puppetlabs/ubuntu-14.04-64-nocm'

      # Customize  VM settings
      vmw.vmx['memsize'] = memory
      vmw.vmx['numvcpus'] = cpus

      # Set VM name
      vmw.name = config.vm.hostname
    end
  end

  # Parallels settings
  config.vm.provider 'parallels' do |prl, override|
    # Override provider box
    override.vm.box = 'parallels/ubuntu-14.04'

    # Customize  VM settings
    prl.memory = memory
    prl.cpus = cpus

    # Set VM name
    prl.name = config.vm.hostname
  end

end

def local_site_path(site)
  File.expand_path(site['local_path'], ANSIBLE_PATH)
end

def nfs_path(site_name)
  "/vagrant-nfs-#{site_name}"
end

def remote_site_path(site_name)
  "/srv/www/#{site_name}/current"
end
