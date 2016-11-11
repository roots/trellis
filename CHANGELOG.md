### HEAD
* Add myhostname to nsswitch.conf to ensure resolvable hostname ([#686](https://github.com/roots/trellis/pull/686))
* Add `bin/xdebug-tunnel.sh` to manage Xdebug and SSH tunnels on remote hosts ([#678](https://github.com/roots/trellis/pull/678))
* Move Xdebug installation/configuration into its own role ([#678](https://github.com/roots/trellis/pull/678))
* Disable wp-cron emails ([#685](https://github.com/roots/trellis/pull/685))
* Make `raw_vars` compatible with play vars and Ansible 2.1 ([#684](https://github.com/roots/trellis/pull/684))
* Ensure there is always at least one PHP-FPM pool defined ([#682](https://github.com/roots/trellis/pull/682))
* Update galaxy roles for Ansible 2.2 compatibility ([#681](https://github.com/roots/trellis/pull/681))
* Update to WP-CLI 0.25.0 for WP 4.7 compat ([#673](https://github.com/roots/trellis/pull/673))
* Enable per-site setup for permalink structure ([#661](https://github.com/roots/trellis/pull/661))
* WP 4.6 Compat: set WP_HOME/SITEURL directly ([#647](https://github.com/roots/trellis/pull/647))
* Create WordPress php-fpm conf after web_root exists ([#642](https://github.com/roots/trellis/pull/642))
* Fix #637 - Fix condition for permalink structure task ([#643](https://github.com/roots/trellis/pull/643))
* Fix #639 - WP 4.6 compatibility: update WP-CLI to 0.24.1 ([#640](https://github.com/roots/trellis/pull/640))

### 0.9.8: August 14th, 2016
* Ansible 2.1 compatibility fixes ([#631](https://github.com/roots/trellis/pull/631))
* [BREAKING] Upgrade Ubuntu from 14.04 Trusty to 16.04 Xenial ([#626](https://github.com/roots/trellis/pull/626))
* [BREAKING] Add `vault_users` for easier password management ([#614](https://github.com/roots/trellis/pull/614))
* Fix #581 - Use WP-CLI to run WP cron ([#583](https://github.com/roots/trellis/pull/583))
* [BREAKING] Require explicit redirects and drop `www_redirect` ([#622](https://github.com/roots/trellis/pull/622))
* Fix #612 - Bump nginx_fastcgi_buffer_size to `8k` ([#620](https://github.com/roots/trellis/pull/620))
* Setup permalink structure for multisite installs too ([#617](https://github.com/roots/trellis/pull/617))
* Fix `wp_home` option in Multisite after install in development ([#616](https://github.com/roots/trellis/pull/616))
* Add `current_path` var and default to enable custom current release path ([#607](https://github.com/roots/trellis/pull/607))
* Add Vagrant post up message ([#602](https://github.com/roots/trellis/pull/602))
* Fix #468 - Use curl to install wp-cli tab completions ([#593](https://github.com/roots/trellis/pull/593))
* Require Ansible 2.0.2 and remove deploy_helper ([#579](https://github.com/roots/trellis/pull/579))
* Add connection-related cli options to ping command ([#578](https://github.com/roots/trellis/pull/578))
* Wrap my.cnf password in quotes ([#577](https://github.com/roots/trellis/pull/577))
* Update to WP-CLI v0.23.1 ([#576](https://github.com/roots/trellis/pull/576))
* Fix #563 - Improve remote databases ([#573](https://github.com/roots/trellis/pull/573))
* Fix #569 - Only skip subdomains for non-www domains ([#570](https://github.com/roots/trellis/pull/570))
* Enable Let's Encrypt to transition http sites to https ([#565](https://github.com/roots/trellis/pull/565))

### 0.9.7: April 10th, 2016
* Fix #550 - Properly skip permalink setup for MU ([#551](https://github.com/roots/trellis/pull/551))
* Escape salts and keys to avoid templating errors ([#548](https://github.com/roots/trellis/pull/548))
* Add plugin to pretty print Ansible msg output ([#544](https://github.com/roots/trellis/pull/544))
* Fix #482 - Multisite is-installed deploy check ([#543](https://github.com/roots/trellis/pull/543))
* Skip setting permalink for multisite installs ([#546](https://github.com/roots/trellis/pull/546))
* Fix #489 - Add $realpath_root to fastcgi_cache_key ([#542](https://github.com/roots/trellis/pull/542))
* Move modules and plugins to `lib/trellis` directory ([#538](https://github.com/roots/trellis/pull/538))
* Automatically set `wp_home` and `wp_siteurl` variables ([#533](https://github.com/roots/trellis/pull/533))
* Switch to Let's Encrypt X3 intermediate certificate and fix chain issues ([#534](https://github.com/roots/trellis/pull/534))
* Supply better defaults for `db_name` and `db_user` ([#529](https://github.com/roots/trellis/pull/529))
* Fix deploy env template to use valid ansible vars ([#530](https://github.com/roots/trellis/pull/530))
* Simplify and improve `wordpress_sites` with better defaults ([#528](https://github.com/roots/trellis/pull/528))
* Allow option for WinNFSD sync folder provider on Windows ([#527](https://github.com/roots/trellis/pull/527))
* Improve Let's Encrypt challenge pre-flight tests ([#526](https://github.com/roots/trellis/pull/526))
* `reverse_www` filter improvements (ignore subdomains) ([#525](https://github.com/roots/trellis/pull/525))
* Fix deprecation warnings on deploy, use current stable WP-CLI ([#523](https://github.com/roots/trellis/pull/523))
* Fix #520 - Disable MariaDB binary logging by default ([#521](https://github.com/roots/trellis/pull/521))
* Let's Encrypt integration ([#518](https://github.com/roots/trellis/pull/518))
* Improve Git repo format validation ([#516](https://github.com/roots/trellis/pull/516))
* Fix #505 - Git ignore \*.retry file
* Fix Ansible deprecations for bare variables ([#510](https://github.com/roots/trellis/pull/510))
* Fixes #508 - update php-xdebug config file path ([#509](https://github.com/roots/trellis/pull/509))
* Add php-mbstring extension ([#504](https://github.com/roots/trellis/pull/504))
* Add more necessary PHP extensions ([#503](https://github.com/roots/trellis/pull/503))

### 0.9.6: February 18th, 2016
* Update to latest ansible-role-mailhog version ([#497](https://github.com/roots/trellis/pull/497))
* Add `reverse_www` filter to fix `www_redirect` ([#486](https://github.com/roots/trellis/pull/486))
* Add IP address variable, move some variables to top of Vagrantfile ([#494](https://github.com/roots/trellis/pull/494))
* Keep Composer updated ([#493](https://github.com/roots/trellis/pull/493))
* Use prestissimo Composer plugin ([#492](https://github.com/roots/trellis/pull/492))
* Use ansible-role-composer ([#491](https://github.com/roots/trellis/pull/491))
* Fix bad `curl` output ([#490](https://github.com/roots/trellis/pull/490))
* Fixes #410 - Default to 1 CPU in Vagrant ([#487](https://github.com/roots/trellis/pull/487))

### 0.9.5: February 10th, 2016
* Fix Nginx includes for Ansible 2.0 ([#473](https://github.com/roots/trellis/pull/473))
* Use `ondrej/php` PPA since `ondrej/php-7.0` is deprecated ([#479](https://github.com/roots/trellis/pull/479))
* Fix Ansible 2.x deploys and require version 2.x ([#478](https://github.com/roots/trellis/pull/478))
* Update to PHP 7.0 and remove HHVM ([#432](https://github.com/roots/trellis/pull/432))
* Windows: Sync `hosts` dir with proper permissions ([#460](https://github.com/roots/trellis/pull/460))
* Fix `inventory_file` variable in connection tests ([#470](https://github.com/roots/trellis/pull/470))
* Fix conditional logic for permalink setup task ([#467](https://github.com/roots/trellis/pull/467))
* Fix permalink setup during WordPress Install ([#466](https://github.com/roots/trellis/pull/466))
* Fix deploy pre-flight check for verifying repo ([#463](https://github.com/roots/trellis/pull/463))
* Ansible 2.0 compatibility ([#461](https://github.com/roots/trellis/pull/461))
* Add pre-flight checks for common deploy problems ([#459](https://github.com/roots/trellis/pull/459))
* Prevent duplicate hosts entries made by `vagrant-hostsupdater` ([#458](https://github.com/roots/trellis/pull/458))
* Fix README's `ansible-playbook` command for server.yml ([#456](https://github.com/roots/trellis/pull/456))
* Fix development hosts file ([#455](https://github.com/roots/trellis/pull/455))
* Add tags to select includes and tasks ([#453](https://github.com/roots/trellis/pull/453))
* Improve Git deploy implementation via `git archive` ([#451](https://github.com/roots/trellis/pull/451))
* Replace strip_www with optional redirect to www/non-www ([#452](https://github.com/roots/trellis/pull/452))
* Accommodate file encryption via ansible vault ([#317](https://github.com/roots/trellis/pull/317))
* Fixes #353 - Allow insecure curl reqs for cron ([#450](https://github.com/roots/trellis/pull/450))
* Fixes #374 - Remove composer vendor/bin from $PATH ([#449](https://github.com/roots/trellis/pull/449))
* Refactor hosts files ([#313](https://github.com/roots/trellis/pull/313))
* Fixes #436 - Let WP handle 404s for PHP files ([#448](https://github.com/roots/trellis/pull/448))
* Fixes #297 - Use `php_flag` vs `php_admin_flag` ([#447](https://github.com/roots/trellis/pull/447))
* Fixes #316 - Set WP permalink structure during install ([#316](https://github.com/roots/trellis/pull/316))
* Switch to https://api.ipify.org for IP lookup ([#444](https://github.com/roots/trellis/pull/444))
* Replace `vagrant-hostsupdater` with `vagrant-hostmanager` ([#442](https://github.com/roots/trellis/pull/442))
* Switch to mainline Nginx, replaces SPDY with HTTP2 ([#389](https://github.com/roots/trellis/issues/389))
* Add `wp core update-db` to deploy finalize hook ([#411](https://github.com/roots/trellis/pull/411))
* Use WP-CLI 0.21.1 ([#392](https://github.com/roots/trellis/pull/392))
* Add variable for whitelisted IPs ([#435](https://github.com/roots/trellis/pull/435))

### 0.9.3: November 29th, 2015
* Nginx role improvements: use more h5bp configs ([#428](https://github.com/roots/trellis/pull/428))
* Add global `deploy_before` and `deploy_after` hooks ([#427](https://github.com/roots/trellis/pull/427))
* Fix HSTS headers ([#424](https://github.com/roots/trellis/pull/424))
* Notify Windows users about SSH forwarding ([#423](https://github.com/roots/trellis/pull/423))
* Use append_privs for WP DB privileges ([#422](https://github.com/roots/trellis/pull/422))
* Stop WP cron job emails ([#421](https://github.com/roots/trellis/pull/421))
* Add WP-CLI bash completion script ([#407](https://github.com/roots/trellis/pull/407))
* Add Composer config `github-oauth` variable ([#402](https://github.com/roots/trellis/pull/402))
* Fix copy project local files in example hook ([#404](https://github.com/roots/trellis/pull/404))
* Update cron variable to match Bedrock ([#394](https://github.com/roots/trellis/pull/394))
* Add deploy_build_before example hook for theme assets ([#397](https://github.com/roots/trellis/pull/37))
* Use curl instead of dig for IP lookups ([#390](https://github.com/roots/trellis/pull/390))
* Update SSL cipher suite ([#386](https://github.com/roots/trellis/pull/386))
* Support for other Vagrant providers (VirtualBox, VMWare, Parallels) ([#340](https://github.com/roots/trellis/pull/340))
* Specify versions for Ansible Galaxy requirements ([#385](https://github.com/roots/trellis/pull/385))
* Adds ability to configure [HSTS headers](https://developer.mozilla.org/en-US/docs/Web/Security/HTTP_strict_transport_security) with site variables. ([#388](https://github.com/roots/trellis/pull/388))

### 0.9.2: October 15th, 2015
* Add dev's IP to ferm whitelist ([#381](https://github.com/roots/trellis/pull/381))
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
