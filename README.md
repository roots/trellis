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

* Ansible >= 1.8 (except 1.9.1 - see this [bug](https://github.com/roots/bedrock-ansible/issues/205)) - [Install](http://docs.ansible.com/intro_installation.html) • [Docs](http://docs.ansible.com/)
* Virtualbox >= 4.3.10 - [Install](https://www.virtualbox.org/wiki/Downloads)
* Vagrant >= 1.5.4 - [Install](http://www.vagrantup.com/downloads.html) • [Docs](https://docs.vagrantup.com/v2/)
* vagrant-bindfs >= 0.3.1 - [Install](https://github.com/gael-ian/vagrant-bindfs#installation) • [Docs](https://github.com/gael-ian/vagrant-bindfs) (Windows users may skip this)
* vagrant-hostsupdater - [Install](https://github.com/cogitatio/vagrant-hostsupdater#installation) • [Docs](https://github.com/cogitatio/vagrant-hostsupdater)

## Installation

1. Download/fork/clone this repo to your local machine.
2. Run `ansible-galaxy install -r requirements.yml` to install external Ansible roles/packages.
3. Download/fork/clone [Bedrock](https://github.com/roots/bedrock) or have an existing Bedrock-based site ready.

Note on `.env` files: You **do not** need a configured `.env` file. bedrock-ansible will automatically create and configure one.

You should now have the following directories at the same level somewhere:

```
example.com/    - Primary folder for the project
├── ansible/    - Your version of this repo (renamed to just `ansible`)
└── site/       - A Bedrock-based site (suggested to name this the generic `site` since your project name is already at the top level)
```

To see a complete working example of this, visit the [roots-example-project.com repo](https://github.com/roots/roots-example-project.com).

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

1. Add the `repo` (Git url) of your Bedrock WordPress project in the corresponding `group_vars/<environment>` file.
2. Set the `branch` you want to deploy.
3. Run `./deploy.sh <environment> <site name>`
4. To rollback a deploy, run `ansible-playbook -i hosts/<environment> rollback.yml --extra-vars="site=<site name>"`

## Configuration

### HHVM

[HHVM](http://hhvm.com/) can be used instead of PHP 5.6 by setting `hhvm: true` in `group_vars/all`.

### WordPress Sites

Since bedrock-ansible is all about automatically creating servers for your WordPress sites, you need to configure your sites before anything else.

This configuration is done in the environment files inside the `group_vars` directory. The `group_vars` files are in [YAML](http://en.wikipedia.org/wiki/YAML) format.

To configure the sites you want on your Vagrant development VM, you'd edit `group_vars/development` for example. For staging, `group_vars/staging`. And likewise for production: `group_vars/production`.

`wordpress_sites` is the top level dictionary used to define the WordPress sites, databases, Nginx vhosts, etc that will be created.

The following variables are all nested under the site "key". The key is just a descriptive name although it's used as a default value of other variables in some cases.

For a complete, working example you can see our [example project](https://github.com/roots/roots-example-project.com/blob/master/ansible/group_vars/development).

* `site_hosts` - array of hosts that Nginx will listen on (required, include main domain at least) * `local_path` - path targeting Bedrock-based site directory (required for development)
* `repo` - URL of the Git repo of your Bedrock project (required, used when deploying)
* `branch` - the branch of the repo you want to deploy. You can also use a tag or the SHA1 of a commit (default: `master`)
* `ssl` - enable SSL and set paths
  * `enabled` - `true` or `false` (required, set to `false`)
  * `key` - local relative path to private key
  * `cert` - local relative path to certificate
* `site_install` - whether to install WordPress or not (*development* only, required)
* `site_title` - WP site title (*development* only, default: project name)
* `db_create` - whether to auto create a database or not (default: `true`)
* `db_import` - Path to local `sql` dump file which will be imported (optional)
* `system_cron` - Disable WP cron and use system's (default: `true`)
* `admin_user` - WP admin user name (*development* only, required)
* `admin_email` - WP admin email address (*development* only, required)
* `admin_password` - WP admin user password (*development* only, required)
* `multisite` - hash of multisite options
  * `enabled` - Multisite enabled flag (required, set to `false`)
  * `subdomains` - subdomains option
  * `base_path` - base path/current site path
* `env` - environment variables
  * `wp_home` - `WP_HOME` constant (required)
  * `wp_siteurl` - `WP_SITEURL` constant (required)
  * `wp_env` - WordPress environment (required, matches group name: `development`, `staging`, `production`)
  * `db_name` - database name (required)
  * `db_user` - database username (required)
  * `db_password` - database password (required)
  * `db_host` - database hostname (default: `localhost`)
  * `domain_current_site` (required if multisite.enabled is `true`)

### Mail

Outgoing mail is done by the sSMTP role. Configure SMTP credentials in `group_vars/all`.

## SSL

Full SSL support is available for your WordPress sites. Note that this will configure your site to be HTTPS **only** by default.

Our HTTPS implementation has all the best practices for performance and security.

Read the Wiki section on [SSL](https://github.com/roots/bedrock-ansible/wiki/SSL) for more documentation.

## Security

The `secure-root.yml` playbook is provided to help secure your remote servers including better SSH security. See the Wiki for [Locking down root](https://github.com/roots/bedrock-ansible/wiki/Security#locking-down-root).
