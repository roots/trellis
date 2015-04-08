# bedrock-ansible

[![Build Status](https://travis-ci.org/roots/bedrock-ansible.svg)](https://travis-ci.org/roots/bedrock-ansible)

bedrock-ansible is a set of [Ansible](http://www.ansible.com/home) [playbooks](http://docs.ansible.com/playbooks.html) to automatically configure servers and deploy WordPress sites. It easily creates development environments with Vagrant to help achieve development & production parity.

Configure complete [Bedrock](https://roots.io/bedrock/)-based WordPress ready servers with a single command:

|                        | Command
| ---------------------- | ------------------------------------------------ |
| **Development**        | `vagrant up`                                     |
| **Staging/Production** |`ansible-playbook -i hosts/production server.yml` |
| **Deploying**          | `./deploy.sh production <site name>`             |

## What's included

bedrock-ansible will configure a server with the following and more:

* Ubuntu 14.04 Trusty LTS
* Nginx
* PHP 5.6 (or [HHVM](http://hhvm.com/))
* [MariaDB](https://mariadb.org/) as a drop-in MySQL replacement (but better)
* sSMTP (mail delivery)
* Memcached
* Composer
* WP-CLI
* Fail2ban
* ferm
* SSL support

## Requirements

* Ansible >= 1.8 - [Installation docs](http://docs.ansible.com/intro_installation.html)
* Virtualbox >= 4.3.10 - [Downloads](https://www.virtualbox.org/wiki/Downloads)
* Vagrant >= 1.5.4 - [Downloads](http://www.vagrantup.com/downloads.html)
* Vagrant-bindfs >= 0.3.1 - [Docs](https://github.com/gael-ian/vagrant-bindfs) (Windows users may skip this)

## Installation

1. Download/fork/clone this repo to your local machine.
2. Run `ansible-galaxy install -r requirements.yml -p vendor/roles` to install external Ansible roles/packages.
3. Download/fork/clone [Bedrock](https://github.com/roots/bedrock) or have an existing Bedrock-based site ready.

You should now have the following directories at the same level somewhere:

```
project/                - Primary folder for the project
├── bedrock-ansible/    - Your version of this repo
└── example.com/        - A Bedrock-based site
```

Note: The full paths to these directories must not contain spaces or else [Ansible will fail](https://github.com/ansible/ansible/issues/8555).

## Development setup

1. Edit `group_vars/development` and add your WordPress sites
2. Run `vagrant up`

## Remote server setup (staging/production)

For remote servers you'll need to have a base Ubuntu 14.04 server already created.

1. Edit `group_vars/<environment>` and add your WordPress sites
2. Edit `hosts/<environment>` and add your server IP/hostnames
3. Set up SSH keys. See the [Wiki page](https://github.com/roots/bedrock-ansible/wiki/SSH-Keys)
4. Run `ansible-playbook -i hosts/<environment> server.yml`

## Deploying to remote servers

1. Run `./deploy.sh <environment> <site name>`
2. To rollback a deploy, run `ansible-playbook -i hosts/<environment> rollback.yml --extra-vars="site=<site name>"`

## Configuration

### HHVM

[HHVM](http://hhvm.com/) can be used instead of PHP 5.6 by setting `hhvm: true` in `group_vars/all`.

### WP Sites

In the environment files inside the `group_vars` directory, `wordpress_sites` is the top level dictionary used to define the WordPress sites/virtual hosts that will be created.

* `site_hosts` - hosts that Nginx will listen on
* `local_path` - path targeting Bedrock-based site directory
* `ssl` - enable SSL and set paths
  * `enabled` - `true` or `false` (defaults to `false`)
  * `key` - local relative path to private key
  * `cert` - local relative path to certificate
* `env` - environment variables
  * `wp_home` - `WP_HOME` constant
  * `wp_siteurl` - `WP_SITEURL` constant
  * `wp_env` - WordPress environment
  * `db_name` - database name
  * `db_user` - database username
  * `db_password` - database password
  * `db_host` - database hostname
  * `domain_current_site` (required for multisite)

Additional options:

* `admin_password` - WP admin user password
* `admin_email` - WP admin email address
* `site_install` - whether to install WordPress or not
* `site_title` - WP site title
* `db_create` - whether to auto create a database or not
* `db_import` - Path to local `sql` dump file which will be imported
* `system_cron` - Disable WP cron and use system's
* `admin_user` - WP admin user name
* `multisite` - hash of multisite options
  * `enabled` - Multisite enabled flag
  * `subdomains` - subdomains option
  * `base_path` - base path/current site path

### Mail

Outgoing mail is done by the sSMTP role. Configure SMTP credentials in `group_vars/all`.

## SSL

Full SSL support is available for your WordPress sites. Note that this will configure your site to be HTTPS **only** by default.

Our HTTPS implementation has all the best practices for performance and security.

Read the Wiki section on [SSL](https://github.com/roots/bedrock-ansible/wiki/SSL) for more documentation.

## Security

The `secure-root.yml` playbook is provided to help secure your remote servers including better SSH security. See the Wiki for [Locking down root](https://github.com/roots/bedrock-ansible/wiki/Security#locking-down-root).
