# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

ip = '192.168.51.62' # pick any local IP
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

wp_config_file = File.join(ANSIBLE_PATH, 'group_vars', 'development', 'wordpress_sites.yml')
static_config_file = File.join(ANSIBLE_PATH, 'group_vars', 'development', 'static_sites.yml')
main_config_file = File.join(ANSIBLE_PATH, 'group_vars', 'all', 'main.yml')

def fail_with_message(msg)
  fail Vagrant::Errors::VagrantError.new, msg
end

if File.exists?(wp_config_file)
  wordpress_sites = YAML.load_file(wp_config_file)['wordpress_sites']
  static_sites = YAML.load_file(static_config_file)['static_sites']
  www_root = YAML.load_file(main_config_file)['www_root']
  fail_with_message "No sites found in #{wp_config_file}." if wordpress_sites.to_h.empty?
else
  fail_with_message "#{wp_config_file} was not found. Please set `ANSIBLE_PATH` in your Vagrantfile."
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

  if Vagrant.has_plugin? 'vagrant-hostmanager'
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
  else
    fail_with_message "vagrant-hostmanager missing, please install the plugin with this command:\nvagrant plugin install vagrant-hostmanager"
  end

  ############################################################################
  # local_as devbox definition
  ############################################################################
  config.vm.define "local_as", primary: true do |local_as|

    # Required for NFS to work
    local_as.vm.network :private_network, ip: ip, hostsupdater: 'skip'

    # disable default mount
    local_as.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    hostname, *aliases = wordpress_sites.flat_map { |(_name, site)| site['site_hosts'] }
    local_as.vm.hostname = hostname
    aliases.concat static_sites.flat_map { |(_name, site)| site['site_hosts'] } # add aliases from the static sites
    www_aliases = ["www.#{hostname}"] + aliases.map { |host| "www.#{host}" }

    local_as.hostmanager.aliases = (aliases + www_aliases).uniq


    if Vagrant::Util::Platform.windows? and !Vagrant.has_plugin? 'vagrant-winnfsd'
      wordpress_sites.each_pair do |name, site|
        local_as.vm.synced_folder local_site_path(site), remote_site_path(name), owner: 'vagrant', group: 'www-data', mount_options: ['dmode=776', 'fmode=775']
      end
      local_as.vm.synced_folder File.join(ANSIBLE_PATH, 'hosts'), File.join(ANSIBLE_PATH.sub(__dir__, '/vagrant'), 'hosts'), mount_options: ['dmode=755', 'fmode=644']
    else
      if !Vagrant.has_plugin? 'vagrant-bindfs'
        fail_with_message "vagrant-bindfs missing, please install the plugin with this command:\nvagrant plugin install vagrant-bindfs"
      else
        wordpress_sites.merge(static_sites).each_pair do |name, site|
          local_as.vm.synced_folder local_site_path(site), nfs_path(name), type: 'nfs'
          local_as.bindfs.bind_folder nfs_path(name), remote_site_path(name), u: 'vagrant', g: 'www-data', o: 'nonempty'
        end
      end
    end

    if Vagrant::Util::Platform.windows?
      local_as.vm.provision :shell do |sh|
        sh.path = File.join(ANSIBLE_PATH, 'windows.sh')
        sh.args = [Vagrant::VERSION]
      end
    else
      local_as.vm.provision :ansible do |ansible|
        ansible.playbook = File.join(ANSIBLE_PATH, 'dev.yml')
        ansible.vault_password_file = "../vault-key"
        ansible.groups = {
          'web' => ['local_as'],
          'development' => ['local_as']
        }

        ansible.extra_vars = {'vagrant_version' => Vagrant::VERSION}
        if vars = ENV['ANSIBLE_VARS']
          extra_vars = Hash[vars.split(',').map { |pair| pair.split('=') }]
          ansible.extra_vars.merge(extra_vars)
        end
      end
    end

    # Vagrant Triggers
    # https://github.com/emyl/vagrant-triggers
    #
    # If the vagrant-triggers plugin is installed, we can run various scripts on Vagrant
    # state changes like `vagrant up`, `vagrant halt`, `vagrant suspend`, and `vagrant destroy`
    #
    # These scripts are run on the host machine, so we use `vagrant ssh` to tunnel back
    # into the VM and execute things.
    if Vagrant.has_plugin? 'vagrant-triggers'
      local_as.trigger.before [:halt, :destroy], :stdout => true do
        wordpress_sites.each_key do |wp_site_folder|
          info "Exporting db for #{wp_site_folder}"
          run_remote "cd #{www_root}/#{wp_site_folder}/ && wp db export --allow-root"
        end
      end
    else
      fail_with_message "vagrant-triggers missing, please install the plugin with this command:\nvagrant plugin install vagrant-triggers"
    end
  end

  ############################################################################
  # sandbox definition
  ############################################################################
  config.vm.define "sandbox", autostart: false do |sandbox|
    sandbox.vm.network :private_network, ip: '192.168.51.63'
    sandbox.vm.hostname = "sandbox.proteusthemes.dev"

    if Vagrant.has_plugin? 'vagrant-hostmanager'
      sandbox.hostmanager.enabled = true
      sandbox.hostmanager.manage_host = true
      sandbox.hostmanager.aliases = ['xml-io.proteusthemes.dev']
    end

    sandbox.vm.provision :ansible do |ansible|
      ansible.playbook = File.join(ANSIBLE_PATH, 'dev.yml')
      ansible.groups = {
        'web' => ['sandbox'],
        'sandbox' => ['sandbox']
      }

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
      override.vm.box = 'puppetlabs/ubuntu-14.04-64-nocm'
      vmw.name = config.vm.hostname
      vmw.vmx['numvcpus'] = cpus
      vmw.vmx['memsize'] = memory
    end
  end

  # Parallels settings
  config.vm.provider 'parallels' do |prl, override|
    override.vm.box = 'parallels/ubuntu-14.04'
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

def remote_site_path(site_name)
  "/opt/proteusnet/www/#{site_name}"
end
