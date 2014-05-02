# bedrock-ansible

[Ansible](http://www.ansible.com/home) [playbook](http://docs.ansible.com/playbooks.html) designed to be used with [Bedrock](http://roots.io/wordpress-stack/) to configure dev & production servers for Bedrock-based WordPress sites.

This playbook will install the common LEMP (Linux/Nginx/MySQL/PHP) stack with PHP 5.5 and [MariaDB](https://mariadb.org/) as a drop-in MySQL replacement (but better) on Ubuntu 14.04 Trusty LTS.

Vagrant is recommended to provision servers and this comes with a basic `Vagrantfile` for an easy dev setup.

## Requirements

1. Ansible >= 1.5.4 - [Installation docs](http://docs.ansible.com/intro_installation.html)
2. Virtualbox >= 4.3 - [Downloads](https://www.virtualbox.org/wiki/Downloads)
3. Vagrant >= 1.5 - [Downloads](http://www.vagrantup.com/downloads.html)

## Installation

Download/fork/clone this repo to your local machine.

## Usage

1. Edit `Vagrantfile` and set your `config.vm.synced_folder` (you can copy this `Vagrantfile` into a project's directory for a project specific VM).
2. Edit `group_vars/all` and add your WordPress site(s). See [Options](#options) below for details.
3. Optionally copy and edit `hosts.example` to `hosts` for more than the single dev host through Vagrant (since Vagrant automatically creates its own hosts inventory).
4. Optionally add any dev hostnames to your local `/etc/hosts` file (or use the [hostsupdated plugin](https://github.com/cogitatio/vagrant-hostsupdater).
5. Run `vagrant up`.

## Options

All Ansible configuration is done in [YAML](http://en.wikipedia.org/wiki/YAML).

`wordpress_sites` is the top level array used to define the WordPress sites/virtual hosts that will be created.

* `site_name` (required) - name used to identify site (commonly the domain name) (default: none)
* `site_hosts` (required) - array of hosts that Nginx will listen on (default: none)
* `user` (optional) - user owner of site directories/files (default: `root` | `user` in `site.yml`)
* `group` (optional) - group owner of site directories/files (default: `www-data`)
* `site_install` (optional) - whether to install WordPress or not (default: `true`)
* `site_title` (optional) - WP site title (default: `site_name`)
* `db_import` (optional) - Path to local `sql` dump file which will be imported (default: `false`)
* `system_cron` (optional) - Disable WP cron and use system's (default: `false`)
* `admin_user` (optional) - WP admin user name (default: `admin`)
* `admin_password` (required if `site_install`) - WP admin user password (default: none)
* `admin_email` (required if `site_install`) - WP admin email address (default: none)
* `multisite` (optional) - hash of multisite options
  * `enabled` (optional) - Multisite enabled flag (default: `false`)
  * `subdomains` (optional) - subdomains option (default: `false`)
  * `base_path` (optional) - base path/current site path (default: `/`)
* `env` (required) - hash of multisite options
  * `wp_home` (required) - `WP_HOME` constant or `home` option (default: none)
  * `wp_siteurl` (required) - `WP_SITEURL` constant or `siteurl` option (default: none)
  * `wp_env` (required) - WordPress environment (default: none)
  * `db_name` (optional) - name of database (default: `site_name`)
  * `db_user` (required) - database user name (default: none)
  * `db_password` (required) - database user password (default: none)
  * `db_host` (required) - database host (default: `localhost`)

## Todo

* Multisite: basic support is included but not yet complete. There are issues with doing a network install from scratch via WP-CLI.
* MariaDB: there's no `root` password set yet.
* Nginx: configuration needs more options and advanced setups like static files and subdomain multisite support.

