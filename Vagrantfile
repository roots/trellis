# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

ip = '192.168.50.5' # pick any local IP
cpus = 1
memory = 1024 # in MB

ANSIBLE_PATH = __dir__ # absolute path to Ansible directory

# Set Ansible paths relative to Ansible directory
ENV['ANSIBLE_CONFIG'] = ANSIBLE_PATH
ENV['ANSIBLE_CALLBACK_PLUGINS'] = "~/.ansible/plugins/callback_plugins/:/usr/share/ansible_plugins/callback_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/callback')}"
ENV['ANSIBLE_FILTER_PLUGINS'] = "~/.ansible/plugins/filter_plugins/:/usr/share/ansible_plugins/filter_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/filter')}"
ENV['ANSIBLE_LIBRARY'] = "/usr/share/ansible:#{File.join(ANSIBLE_PATH, 'lib/trellis/modules')}"
ENV['ANSIBLE_ROLES_PATH'] = File.join(ANSIBLE_PATH, 'vendor', 'roles')
ENV['ANSIBLE_VARS_PLUGINS'] = "~/.ansible/plugins/vars_plugins/:/usr/share/ansible_plugins/vars_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/vars')}"

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

Vagrant.require_version '>= 1.8.5'

Vagrant.configure('2') do |config|
  config.vm.box = 'bento/ubuntu-16.04'
  config.vm.box_version = '2.2.9'
  config.ssh.forward_agent = true

  config.vm.post_up_message = post_up_message

  # Fix for: "stdin: is not a tty"
  # https://github.com/mitchellh/vagrant/issues/1673#issuecomment-28288042
  config.ssh.shell = %{bash -c 'BASH_ENV=/etc/profile exec bash'}

  # Required for NFS to work
  config.vm.network :private_network, ip: ip, hostsupdater: 'skip'

  site_hosts = wordpress_sites.flat_map { |(_name, site)| site['site_hosts'] }

  site_hosts.each do |host|
    if !host.is_a?(Hash) or !host.has_key?('canonical')
      fail_with_message File.read(File.join(ANSIBLE_PATH, 'roles/common/templates/site_hosts.j2')).sub!('{{ env }}', 'development').gsub!(/com$/, 'dev')
    end
  end

  main_hostname, *hostnames = site_hosts.map { |host| host['canonical'] }
  config.vm.hostname = main_hostname

  redirects = site_hosts.flat_map { |host| host['redirects'] }.compact

  if Vagrant.has_plugin? 'vagrant-hostmanager'
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.aliases = hostnames + redirects
  else
    fail_with_message "vagrant-hostmanager missing, please install the plugin with this command:\nvagrant plugin install vagrant-hostmanager"
  end

  if Vagrant::Util::Platform.windows? and !Vagrant.has_plugin? 'vagrant-winnfsd'
    wordpress_sites.each_pair do |name, site|
      config.vm.synced_folder local_site_path(site), remote_site_path(name, site), owner: 'vagrant', group: 'www-data', mount_options: ['dmode=776', 'fmode=775']
    end
    config.vm.synced_folder File.join(ANSIBLE_PATH, 'hosts'), File.join(ANSIBLE_PATH.sub(__dir__, '/vagrant'), 'hosts'), mount_options: ['dmode=755', 'fmode=644']
  else
    if !Vagrant.has_plugin? 'vagrant-bindfs'
      fail_with_message "vagrant-bindfs missing, please install the plugin with this command:\nvagrant plugin install vagrant-bindfs"
    else
      wordpress_sites.each_pair do |name, site|
        config.vm.synced_folder local_site_path(site), nfs_path(name), type: 'nfs'
        config.bindfs.bind_folder nfs_path(name), remote_site_path(name, site), u: 'vagrant', g: 'www-data', o: 'nonempty'
      end
    end
  end

  if Vagrant::Util::Platform.windows?
    config.vm.provision :shell do |sh|
      sh.path = File.join(ANSIBLE_PATH, 'windows.sh')
      sh.args = [Vagrant::VERSION]
      sh.keep_color = true
    end
  else
    config.vm.provision :ansible do |ansible|
      ansible.playbook = File.join(ANSIBLE_PATH, 'dev.yml')
      ansible.groups = {
        'web' => ['default'],
        'development' => ['default']
      }

      if tags = ENV['ANSIBLE_TAGS']
        ansible.tags = tags
      end

      ansible.extra_vars = {'vagrant_version' => Vagrant::VERSION}
      if vars = ENV['ANSIBLE_VARS']
        extra_vars = Hash[vars.split(',').map { |pair| pair.split('=') }]
        ansible.extra_vars.merge(extra_vars)
      end
    end
  end

  # Virtualbox settings
  config.vm.provider 'virtualbox' do |vb|
    vb.name = config.vm.hostname
    vb.customize ['modifyvm', :id, '--cpus', cpus]
    vb.customize ['modifyvm', :id, '--memory', memory]

    # Fix for slow external network connections
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
  end

  # VMware Workstation/Fusion settings
  ['vmware_fusion', 'vmware_workstation'].each do |provider|
    config.vm.provider provider do |vmw, override|
      vmw.name = config.vm.hostname
      vmw.vmx['numvcpus'] = cpus
      vmw.vmx['memsize'] = memory
    end
  end

  # Parallels settings
  config.vm.provider 'parallels' do |prl, override|
    prl.name = config.vm.hostname
    prl.cpus = cpus
    prl.memory = memory
  end

end

def local_site_path(site)
  File.expand_path(site['local_path'], ANSIBLE_PATH)
end

def nfs_path(site_name)
  "/vagrant-nfs-#{site_name}"
end

def post_up_message
  msg = 'Your Trellis Vagrant box is ready to use!'
  msg << "\n* Composer and WP-CLI commands need to be run on the virtual machine."
  msg << "\n* You can SSH into the machine with `vagrant ssh`."
  msg << "\n* Then navigate to your WordPress sites at `/srv/www`."

  msg
end

def remote_site_path(site_name, site)
  "/srv/www/#{site_name}/#{site['current_path'] || 'current'}"
end
