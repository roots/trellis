# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

ANSIBLE_PATH = __dir__ # absolute path to Ansible directory

# Set Ansible roles_path relative to Ansible directory
ENV['ANSIBLE_ROLES_PATH'] = File.join(ANSIBLE_PATH, 'vendor', 'roles')

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
  fail_with_message "No sites found in #{static_config_file}." if static_sites.to_h.empty?
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

  ############################################################################
  # default devbox definition
  ############################################################################
  config.vm.define "default", primary: true do |default|
    # Required for NFS to work, pick any local IP
    default.vm.network :private_network, ip: '192.168.51.62'

    # Fix for: "stdin: is not a tty"
    # https://github.com/mitchellh/vagrant/issues/1673#issuecomment-28288042
    default.ssh.shell = %{bash -c 'BASH_ENV=/etc/profile exec bash'}

    # disable default mount
    default.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    hostname, *aliases = wordpress_sites.flat_map { |(_name, site)| site['site_hosts'] }
    default.vm.hostname = hostname
    aliases.concat static_sites.flat_map { |(_name, site)| site['site_hosts'] } # add aliases from the static sites
    www_aliases = ["www.#{hostname}"] + aliases.map { |host| "www.#{host}" }

    if Vagrant.has_plugin? 'vagrant-hostsupdater'
      default.hostsupdater.aliases = (aliases + www_aliases).uniq
    else
      fail_with_message "vagrant-hostsupdater missing, please install the plugin with this command:\nvagrant plugin install vagrant-hostsupdater"
    end

    if Vagrant::Util::Platform.windows?
      wordpress_sites.merge(static_sites).each_pair do |name, site|
        default.vm.synced_folder local_site_path(site), remote_site_path(name), owner: 'vagrant', group: 'www-data', mount_options: ['dmode=776', 'fmode=775']
      end
    else
      if !Vagrant.has_plugin? 'vagrant-bindfs'
        fail_with_message "vagrant-bindfs missing, please install the plugin with this command:\nvagrant plugin install vagrant-bindfs"
      else
        wordpress_sites.merge(static_sites).each_pair do |name, site|
          default.vm.synced_folder local_site_path(site), nfs_path(name), type: 'nfs'
          default.bindfs.bind_folder nfs_path(name), remote_site_path(name), u: 'vagrant', g: 'www-data', o: 'nonempty'
        end
      end
    end

    if Vagrant::Util::Platform.windows?
      default.vm.provision :shell do |sh|
        sh.path = File.join(ANSIBLE_PATH, 'windows.sh')
      end
    else
      default.vm.provision :ansible do |ansible|
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

    # Vagrant Triggers
    # https://github.com/emyl/vagrant-triggers
    #
    # If the vagrant-triggers plugin is installed, we can run various scripts on Vagrant
    # state changes like `vagrant up`, `vagrant halt`, `vagrant suspend`, and `vagrant destroy`
    #
    # These scripts are run on the host machine, so we use `vagrant ssh` to tunnel back
    # into the VM and execute things.
    if Vagrant.has_plugin? 'vagrant-triggers'
      default.trigger.before [:halt, :destroy], :stdout => true do
        wordpress_sites.each_key do |wp_site_folder|
          info "Exporting db for #{wp_site_folder}"
          run_remote "cd #{www_root}/#{wp_site_folder}/ && wp db export --allow-root"
        end
      end
    else
      info "vagrant-triggers missing, please install the plugin with this command:\nvagrant plugin install vagrant-triggers"
    end
  end

  ############################################################################
  # sandbox definition
  ############################################################################
  config.vm.define "sandbox", autostart: false do |sandbox|
    sandbox.vm.network :private_network, ip: '192.168.51.63'
    sandbox.vm.hostname = "sandbox.proteusthemes.dev"

    if Vagrant.has_plugin? 'vagrant-hostsupdater'
      sandbox.hostsupdater.aliases = ['xml-io.proteusthemes.dev']
    else
      fail_with_message "vagrant-hostsupdater missing, please install the plugin with this command:\nvagrant plugin install vagrant-hostsupdater"
    end

    sandbox.vm.provision :ansible do |ansible|
      ansible.playbook = File.join(ANSIBLE_PATH, 'dev-sandbox.yml')
      ansible.groups = {
        'web' => ['sandbox'],
        'sandbox' => ['sandbox']
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
    # vb.customize ['modifyvm', :id, '--cpus', cpus]

    # Fix for slow external network connections
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']

    # Set VM name
    vb.name = config.vm.hostname
  end

  # VMware Workstation/Fusion settings
  ['vmware_fusion', 'vmware_workstation'].each do |provider|
    config.vm.provider 'provider' do |vmw, override|
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
  "/opt/proteusnet/www/#{site_name}"
end
