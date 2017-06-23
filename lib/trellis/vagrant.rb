# Set Ansible paths relative to Ansible directory
ENV['ANSIBLE_CONFIG'] = ANSIBLE_PATH
ENV['ANSIBLE_CALLBACK_PLUGINS'] = "~/.ansible/plugins/callback_plugins/:/usr/share/ansible_plugins/callback_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/callback')}"
ENV['ANSIBLE_FILTER_PLUGINS'] = "~/.ansible/plugins/filter_plugins/:/usr/share/ansible_plugins/filter_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/filter')}"
ENV['ANSIBLE_LIBRARY'] = "/usr/share/ansible:#{File.join(ANSIBLE_PATH, 'lib/trellis/modules')}"
ENV['ANSIBLE_ROLES_PATH'] = File.join(ANSIBLE_PATH, 'vendor', 'roles')
ENV['ANSIBLE_VARS_PLUGINS'] = "~/.ansible/plugins/vars_plugins/:/usr/share/ansible_plugins/vars_plugins:#{File.join(ANSIBLE_PATH, 'lib/trellis/plugins/vars')}"

def ensure_plugins(plugins)
  logger = Vagrant::UI::Colored.new
  installed = false

  plugins.each do |plugin|
    plugin_name = plugin['name']
    manager = Vagrant::Plugin::Manager.instance

    next if manager.installed_plugins.has_key?(plugin_name)

    logger.warn("Installing plugin #{plugin_name}")

    manager.install_plugin(
      plugin_name,
      sources: plugin.fetch('source', %w(https://rubygems.org/ https://gems.hashicorp.com/)),
      version: plugin['version']
    )

    installed = true
  end

  if installed
    logger.warn('`vagrant up` must be re-run now that plugins are installed')
    exit
  end
end

def fail_with_message(msg)
  fail Vagrant::Errors::VagrantError.new, msg
end

def hosts(sites)
  site_hosts = sites.flat_map { |(_name, site)| site['site_hosts'] }

  site_hosts.each do |host|
    if !host.is_a?(Hash) || !host.has_key?('canonical')
      fail_with_message File.read(File.join(ANSIBLE_PATH, 'roles/common/templates/site_hosts.j2')).sub!('{{ env }}', 'development').gsub!(/com$/, 'dev')
    end
  end

  site_hosts
end

def load_wordpress_sites
  config_file = File.join(ANSIBLE_PATH, 'group_vars', 'development', 'wordpress_sites.yml')

  if File.exists?(config_file)
    wordpress_sites = YAML.load_file(config_file)['wordpress_sites']
    fail_with_message "No sites found in #{config_file}." if wordpress_sites.to_h.empty?
  else
    fail_with_message "#{config_file} was not found. Please set `ANSIBLE_PATH` in your Vagrantfile."
  end

  wordpress_sites
end

def local_site_path(site)
  File.expand_path(site['local_path'], ANSIBLE_PATH)
end

def multisite_subdomains?(wordpress_sites)
  wordpress_sites.any? do |(_name, site)|
    site['multisite'].fetch('enabled', false) && site['multisite'].fetch('subdomains', false)
  end
end

def nfs_path(path)
  "/vagrant-nfs-#{File.basename(path)}"
end

def post_up_message
  msg = 'Your Trellis Vagrant box is ready to use!'
  msg << "\n* Composer and WP-CLI commands need to be run on the virtual machine"
  msg << "\n  for any post-provision modifications."
  msg << "\n* You can SSH into the machine with `vagrant ssh`."
  msg << "\n* Then navigate to your WordPress sites at `/srv/www`"
  msg << "\n  or to your Trellis files at `#{ANSIBLE_PATH_ON_VM}`."

  msg
end

def remote_site_path(site_name, site)
  "/srv/www/#{site_name}/#{site['current_path'] || 'current'}"
end
