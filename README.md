# Trellis
[![Release](https://img.shields.io/github/release/roots/trellis.svg?style=flat-square)](https://github.com/roots/trellis/releases)
[![Build Status](https://img.shields.io/travis/roots/trellis.svg?style=flat-square)](https://travis-ci.org/roots/trellis)
[![Backers on Open Collective](https://opencollective.com/trellis/backers/badge.svg)](#backers) 
[![Sponsors on Open Collective](https://opencollective.com/trellis/sponsors/badge.svg)](#sponsors)
 

Ansible playbooks for setting up a LEMP stack for WordPress.

- Local development environment with Vagrant
- High-performance production servers
- One-command deploys for your [Bedrock](https://roots.io/bedrock/)-based WordPress sites

## What's included

Trellis will configure a server with the following and more:

* Ubuntu 16.04 Xenial LTS
* Nginx (with optional FastCGI micro-caching)
* PHP 7.2
* MariaDB (a drop-in MySQL replacement)
* SSL support (scores an A+ on the [Qualys SSL Labs Test](https://www.ssllabs.com/ssltest/))
* Let's Encrypt integration for free SSL certificates
* HTTP/2 support (requires SSL)
* Composer
* WP-CLI
* sSMTP (mail delivery)
* MailHog
* Memcached
* Fail2ban
* ferm

## Documentation

Full documentation is available at [https://roots.io/trellis/docs/](https://roots.io/trellis/docs/).

## Requirements

Make sure all dependencies have been installed before moving on:

* [Virtualbox](https://www.virtualbox.org/wiki/Downloads) >= 4.3.10
* [Vagrant](https://www.vagrantup.com/downloads.html) >= 2.0.1

## Installation

The recommended directory structure for a Trellis project looks like:

```shell
example.com/      # → Root folder for the project
├── trellis/      # → Your clone of this repository
└── site/         # → A Bedrock-based WordPress site
    └── web/
        ├── app/  # → WordPress content directory (themes, plugins, etc.)
        └── wp/   # → WordPress core (don't touch!)
```

See a complete working example in the [roots-example-project.com repo](https://github.com/roots/roots-example-project.com).

1. Create a new project directory: `$ mkdir example.com && cd example.com`
2. Clone Trellis: `$ git clone --depth=1 git@github.com:roots/trellis.git && rm -rf trellis/.git`
3. Clone Bedrock: `$ git clone --depth=1 git@github.com:roots/bedrock.git site && rm -rf site/.git`

Windows user? [Read the Windows docs](https://roots.io/trellis/docs/windows/) for slightly different installation instructions. VirtualBox is known to have poor performance in Windows — use VMware or [see some possible solutions](https://discourse.roots.io/t/virtualbox-performance-in-windows/3932).

## Local development setup

1. Configure your WordPress sites in `group_vars/development/wordpress_sites.yml` and in `group_vars/development/vault.yml`
2. Run `vagrant up`

[Read the local development docs](https://roots.io/trellis/docs/local-development-setup/) for more information.

## Remote server setup (staging/production)

For remote servers, installing Ansible locally is an additional requirement. See the [docs](https://roots.io/trellis/docs/remote-server-setup/#requirements) for more information.

A base Ubuntu 16.04 server is required for setting up remote servers. OS X users must have [passlib](http://pythonhosted.org/passlib/install.html#installation-instructions) installed.

1. Configure your WordPress sites in `group_vars/<environment>/wordpress_sites.yml` and in `group_vars/<environment>/vault.yml` (see the [Vault docs](https://roots.io/trellis/docs/vault/) for how to encrypt files containing passwords)
2. Add your server IP/hostnames to `hosts/<environment>`
3. Specify public SSH keys for `users` in `group_vars/all/users.yml` (see the [SSH Keys docs](https://roots.io/trellis/docs/ssh-keys/))
4. Run `ansible-playbook server.yml -e env=<environment>` to provision the server

[Read the remote server docs](https://roots.io/trellis/docs/remote-server-setup/) for more information.

## Deploying to remote servers

1. Add the `repo` (Git URL) of your Bedrock WordPress project in the corresponding `group_vars/<environment>/wordpress_sites.yml` file
2. Set the `branch` you want to deploy
3. Run `./bin/deploy.sh <environment> <site name>`
4. To rollback a deploy, run `ansible-playbook rollback.yml -e "site=<site name> env=<environment>"`

[Read the deploys docs](https://roots.io/trellis/docs/deploys/) for more information.

## Contributing

Contributions are welcome from everyone. We have [contributing guidelines](https://github.com/roots/guidelines/blob/master/CONTRIBUTING.md) to help you get started.

## Gold sponsors

Help support our open-source development efforts by [contributing to Trellis on OpenCollective](https://opencollective.com/trellis).

<a href="https://kinsta.com/?kaid=OFDHAJIXUDIV"><img src="https://roots.io/app/uploads/kinsta.svg" alt="Kinsta" width="200" height="150"></a> <a href="https://www.harnessup.com/"><img src="https://roots.io/app/uploads/harness-software.svg" alt="Harness Software" width="200" height="150"></a> <a href="https://k-m.com/"><img src="https://roots.io/app/uploads/km-digital.svg" alt="KM Digital" width="200" height="150"></a>

## Community

Keep track of development and community news.

* Participate on the [Roots Discourse](https://discourse.roots.io/)
* Follow [@rootswp on Twitter](https://twitter.com/rootswp)
* Read and subscribe to the [Roots Blog](https://roots.io/blog/)
* Subscribe to the [Roots Newsletter](https://roots.io/subscribe/)
* Listen to the [Roots Radio podcast](https://roots.io/podcast/)

## Contributors

This project exists thanks to all the people who contribute. [[Contribute](https://github.com/roots/guidelines/blob/master/CONTRIBUTING.md)].
<a href="graphs/contributors"><img src="https://opencollective.com/trellis/contributors.svg?width=890&button=false" /></a>


## Backers

Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/trellis#backer)]

<a href="https://opencollective.com/trellis#backers" target="_blank"><img src="https://opencollective.com/trellis/backers.svg?width=890"></a>


## Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/trellis#sponsor)]

<a href="https://opencollective.com/trellis/sponsor/0/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/1/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/2/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/3/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/4/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/5/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/6/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/7/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/8/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/trellis/sponsor/9/website" target="_blank"><img src="https://opencollective.com/trellis/sponsor/9/avatar.svg"></a>


