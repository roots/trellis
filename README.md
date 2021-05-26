<p align="center">
  <a href="https://roots.io/trellis/">
    <img alt="Trellis" src="https://cdn.roots.io/app/uploads/logo-trellis.svg" height="100">
  </a>
</p>

<p align="center">
  <a href="LICENSE.md">
    <img alt="MIT License" src="https://img.shields.io/github/license/roots/trellis?color=%23525ddc&style=flat-square" />
  </a>

  <a href="https://github.com/roots/trellis/releases">
    <img alt="Release" src="https://img.shields.io/github/release/roots/trellis.svg?style=flat-square" />
  </a>

  <a href="https://circleci.com/gh/roots/trellis">
    <img alt="Build Status" src="https://img.shields.io/circleci/build/gh/roots/trellis?style=flat-square" />
  </a>

  <a href="https://twitter.com/rootswp">
    <img alt="Follow Roots" src="https://img.shields.io/twitter/follow/rootswp.svg?style=flat-square&color=1da1f2" />
  </a>
</p>

<p align="center">
  <strong>Ansible-powered LEMP stack for WordPress</strong>
  <br />
  Built with ❤️
</p>

<p align="center">
  <a href="https://roots.io">Official Website</a> | <a href="https://roots.io/docs/trellis/master/installation/">Documentation</a> | <a href="CHANGELOG.md">Change Log</a>
</p>

## Supporting

**Trellis** is an open source project and completely free to use.

However, the amount of effort needed to maintain and develop new features and products within the Roots ecosystem is not sustainable without proper financial backing. If you have the capability, please consider donating using the links below:

<div align="center">

[![Donate via Patreon](https://img.shields.io/badge/donate-patreon-orange.svg?style=flat-square&logo=patreon")](https://www.patreon.com/rootsdev)
[![Donate via PayPal](https://img.shields.io/badge/donate-paypal-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/rootsdev)

</div>

## Overview

Ansible playbooks for setting up a LEMP stack for WordPress.

- Local development environment with Vagrant
- High-performance production servers
- Zero-downtime deploys for your [Bedrock](https://roots.io/bedrock/)-based WordPress sites
- [trellis-cli](https://github.com/roots/trellis-cli) for easier management

## What's included

Trellis will configure a server with the following and more:

- Ubuntu 20.04 Focal LTS
- Nginx (with optional FastCGI micro-caching)
- PHP 7.4
- MariaDB (a drop-in MySQL replacement)
- SSL support (scores an A+ on the [Qualys SSL Labs Test](https://www.ssllabs.com/ssltest/))
- Let's Encrypt for free SSL certificates
- HTTP/2 support (requires SSL)
- Composer
- WP-CLI
- sSMTP (mail delivery)
- MailHog
- Memcached
- Fail2ban and ferm

## Documentation

Full documentation is available at [https://roots.io/docs/trellis/master/installation/](https://roots.io/docs/trellis/master/installation/).

## Requirements

Make sure all dependencies have been installed before moving on:

- [Virtualbox](https://www.virtualbox.org/wiki/Downloads) >= 4.3.10
- [Vagrant](https://www.vagrantup.com/downloads.html) >= 2.1.0
- **Recommended**: [trellis-cli](https://github.com/roots/trellis-cli)

**Windows user?** [Read the Windows getting started docs](https://roots.io/docs/getting-started/windows/#working-with-trellis) for slightly different installation instructions.

## Installation

### Using trellis-cli

Create a new project:

```bash
$ trellis new example.com
```

### Manual

The recommended directory structure for a Trellis project looks like:

```bash
example.com/      # → Root folder for the project
├── trellis/      # → Your clone of this repository
└── site/         # → A Bedrock-based WordPress site
    └── web/
        ├── app/  # → WordPress content directory (themes, plugins, etc.)
        └── wp/   # → WordPress core (don't touch!)
```

See a complete working example in the [roots-example-project.com repo](https://github.com/roots/roots-example-project.com).

1. Create a new project directory:

```bash
$ mkdir example.com && cd example.com
```

2. Install Trellis:

```bash
$ git clone --depth=1 git@github.com:roots/trellis.git && rm -rf trellis/.git
```

3. Install Bedrock into the `site` directory:

```bash
$ composer create-project roots/bedrock site
```

## Local development setup

### Using trellis-cli

1. Review the automatically created site in `group_vars/development/wordpress_sites.yml`
2. Customize settings if necessary

Start the Vagrant virtual machine:

```bash
$ trellis up
```

### Manual

1. Configure your WordPress sites in `group_vars/development/wordpress_sites.yml` and in `group_vars/development/vault.yml`
2. Ensure you're in the trellis directory: `cd trellis`
3. Run `vagrant up`

[Read the local development docs](https://roots.io/docs/trellis/master/local-development/#wordpress-installation) for more information.

## Remote server setup (staging/production)

A base Ubuntu 18.04 (Bionic) or Ubuntu 20.04 (Focal LTS) server is required for setting up remote servers.

1. Configure your WordPress sites in `group_vars/<environment>/wordpress_sites.yml` and in `group_vars/<environment>/vault.yml` (see the [Vault docs](https://roots.io/docs/trellis/master/vault/) for how to encrypt files containing passwords)
2. Add your server IP/hostnames to `hosts/<environment>`
3. Specify public SSH keys for `users` in `group_vars/all/users.yml` (see the [SSH Keys docs](https://roots.io/docs/trellis/master/ssh-keys/))

### Using trellis-cli

Initialize Trellis (Virtualenv) environment:

```bash
$ trellis init
```

Provision the server:

```bash
$ trellis provision production
```

Or take advantage of its [Digital Ocean](https://roots.io/r/digitalocean) support to create a Droplet _and_ provision it in a single command:

```bash
$ trellis droplet create production
```

### Manual

For remote servers, installing Ansible locally is an additional requirement. See the [docs](https://roots.io/docs/trellis/master/remote-server-setup/#requirements) for more information.

Provision the server:

```bash
$ ansible-playbook server.yml -e env=<environment>
```

[Read the remote server docs](https://roots.io/docs/trellis/master/remote-server-setup/) for more information.

## Deploying to remote servers

1. Add the `repo` (Git URL) of your Bedrock WordPress project in the corresponding `group_vars/<environment>/wordpress_sites.yml` file
2. Set the `branch` you want to deploy (defaults to `master`)

### Using trellis-cli

Deploy a site:

```bash
$ trellis deploy <environment> <site>
```

Rollback a deploy:

```bash
$ trellis rollback <environment> <site>
```

### Manual

Deploy a site:

```bash
$ ./bin/deploy.sh <environment> <site>
```

Rollback a deploy:

```bash
$ ansible-playbook rollback.yml -e "site=<site> env=<environment>"
```

[Read the deploys docs](https://roots.io/docs/trellis/master/deployments/) for more information.

## Contributing

Contributions are welcome from everyone. We have [contributing guidelines](https://github.com/roots/guidelines/blob/master/CONTRIBUTING.md) to help you get started.

## Trellis sponsors

Help support our open-source development efforts by [becoming a patron](https://www.patreon.com/rootsdev).

<a href="https://kinsta.com/?kaid=OFDHAJIXUDIV"><img src="https://cdn.roots.io/app/uploads/kinsta.svg" alt="Kinsta" width="200" height="150"></a> <a href="https://k-m.com/"><img src="https://cdn.roots.io/app/uploads/km-digital.svg" alt="KM Digital" width="200" height="150"></a> <a href="https://carrot.com/"><img src="https://cdn.roots.io/app/uploads/carrot.svg" alt="Carrot" width="200" height="150"></a> <a href="https://www.c21redwood.com/"><img src="https://cdn.roots.io/app/uploads/c21redwood.svg" alt="C21 Redwood Realty" width="200" height="150"></a> <a href="https://wordpress.com/"><img src="https://cdn.roots.io/app/uploads/wordpress.svg" alt="WordPress.com" width="200" height="150"></a> <a href="https://motto.ca/roots"><img src="https://cdn.roots.io/app/uploads/motto.svg" alt="Motto" width="200" height="150"></a>

## Community

Keep track of development and community news.

- Participate on the [Roots Discourse](https://discourse.roots.io/)
- Follow [@rootswp on Twitter](https://twitter.com/rootswp)
- Read and subscribe to the [Roots Blog](https://roots.io/blog/)
- Subscribe to the [Roots Newsletter](https://roots.io/subscribe/)
- Listen to the [Roots Radio podcast](https://roots.io/podcast/)
