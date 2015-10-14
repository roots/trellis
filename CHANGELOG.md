### HEAD
* Add nonempty option to config.bindfs.bind_folder ([#382](https://github.com/roots/trellis/pull/382))
* Add proper hooks for task files during deploys ([#378](https://github.com/roots/trellis/pull/378))
* Fix logrotate's Nginx postrotate script ([#377](https://github.com/roots/trellis/pull/377))
* Add static HTML files as fallbacks for Nginx's `index` directive ([#376](https://github.com/roots/trellis/pull/376))
* Use Windows environment variable to determine number of CPUs ([#366](https://github.com/roots/trellis/pull/366))
* Check for galaxy roles before `vagrant up` ([#365](https://github.com/roots/trellis/pull/365))
* Install Xdebug by default in development environment ([#363](https://github.com/roots/trellis/pull/363))
* Ensure admin_user can connect before disabling root ([#345](https://github.com/roots/trellis/pull/345))
* Prevent PHP execution in uploads directory ([#356](https://github.com/roots/trellis/pull/356))
* Update h5bp Nginx configs ([#355](https://github.com/roots/trellis/pull/355))
* Convert sshd role variables to booleans ([#344](https://github.com/roots/trellis/pull/344))
* Add check to validate `subtree_path` during deploy ([#334](https://github.com/roots/trellis/pull/334))
* Rename WP site variable `subtree` to `subtree_path` ([#329](https://github.com/roots/trellis/pull/329))
* Add extra HTTP security headers ([#322](https://github.com/roots/trellis/pull/322))
* HHVM restart cron job fix ([#327](https://github.com/roots/trellis/pull/327))
* Improve SSH remote user detection ([#321](https://github.com/roots/trellis/pull/321))
* Add variable + better default for Nginx fastcgi buffers ([#302](https://github.com/roots/trellis/pull/302))
* WP Multisite install fixes ([#319](https://github.com/roots/trellis/pull/319))
* Re-organize `group_vars` files into subdirectories and separate files ([#308](https://github.com/roots/trellis/pull/308))

### 0.9.1: August 18th, 2015
* Capture development mail with MailHog ([#304](https://github.com/roots/trellis/pull/304))
* Update git remote URL before cloning on deploys ([#299](https://github.com/roots/trellis/pull/299))
* Allow user to set the timezone ([#301](https://github.com/roots/trellis/pull/301))
* Improvements to custom Nginx includes ([#242](https://github.com/roots/trellis/pull/242))
* Fix comment in Vagrantfile: use absolute path for ANSIBLE_PATH ([#292](https://github.com/roots/trellis/pull/292))
* Fix remote user handling for AWS ([#290](https://github.com/roots/trellis/pull/290))

### 0.9.0: August 3rd, 2015
* Allow auto-generation of self signed SSL certificate
* Merge secure-root.yml into server.yml
* Bump Ansible requirement to >= 1.9.2
* Validate that at least the minimum required version of Ansible is used
* Fix PHP error handling
* Flush wp db theme roots on deploy
* Stop recursive copying of vendor
* Update the windows.sh script with absolute path
* Conditionally copy .env into web root
* Add subtree commented out
* Add Composer binary path to the default path
* Change base box to stock Ubuntu 14.04
* Rename bedrock-ansible to Trellis
* Restore strip_www functionality
* Protect against Logjam attack by generating a strong and unique Diffie-Hellman group
* Move SSH key handling to users role
* Fix multisite conditional in wordpress-site.conf
* Allow use of FastCGI caching
* Wrap octal mode in quotes
* Fix project_shared_children mode defaults
* Allow for custom permissions for shared sources
* Provide a mechanism for custom Nginx includes
* Add trailing slash to WP core rewrite, preventing possible redirect loop
* Insert full path to service command, add hhvm restart minute
* Disable exposing PHP version to the world
* wordpress-install improvements
* Nginx h5bp config improvements
* Make composer self-update idempotent
* Fix project_subtree conditional
* Remove redundant site_name when naming log files
* Fix project_subtree check
* Fix conditional check for multi-site deploys
* Fix .env generation for wordpress-install
* Mirror `server_name` in SSL and non-SSL blocks
* Windows compatibility
* Add swapfile role
* Nginx: better worker_processes setting
* Use inventory_hostname instead of ansible_hostname
* Update Ansible version requirements
* Add information on how to deploy with the git strategy
* Define provider as virtualbox to avoid failure
* Don't set HSTS header over HTTP
* Add note about generating keys from the WordPress API
* Use site instead of example.com
* Be consistent with roots-example-project repo
* Add vagrant-hostsupdater to requirements
* SSL support
* Vagrant: resolve site paths relative to Ansible
* Subtree should be defined on a site
* Remove static IP from site_hosts
* Deploy improvements
* WP subdomain multisite support
* Add xdebug role
* Add logrotate role
* Add ntpd role
* Ansible deploys
* HHVM implementation
* Add SMTP role
* Install php5-memcached
* Update to PHP 5.6
* Simplify Vagrantfile
* Add better SSH defaults
* Add fail2ban, ferm for added security
* Remove naming restriction on Bedrock path
* Add vagrant-bindfs for custom NFS permissions
* Limit `sendfile off` directive to development env
* Add better upload size and execution time defaults
* Use H5BP server configs
* Hardcode Vagrant VM memory to 1GB
* Replace dots in cron file names
* Use NFS for shared folders and better performance
* Tagged playbook roles

### 0.4.0: September 9th, 2014
* Complete memcached implementation
* Better PHP production configs: errors and opcache
* Always set fastcgi param `SCRIPT_FILENAME` in Nginx for better version compatibility

### 0.3.0: August 20th, 2014
* Ansible 1.6.8 compatibility (bug fix)
* Fix for slow network connections
* Nginx reload after DB import
* Integrate vagrant-hostsupdater
* Improve organization and file/folder structure
* MySQL password support
* Memcached role
* Improved hosts file and group_vars for separate environments

### 0.2.0: May 15th, 2014
* Add roots/bedrock Vagrant box
* Add `run_composer` option to `wordpress_sites` so Composer can be run on the VM removing the requirement for it on the host
* Remove upgrade role since we can't control package versions with it

### 0.1.1: May 1st, 2014
* Initial release
