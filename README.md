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

  <a href="https://github.com/roots/trellis/actions">
    <img alt="Build Status" src="https://img.shields.io/github/workflow/status/roots/trellis/ci?style=flat-square" />
  </a>

  <a href="https://twitter.com/rootswp">
    <img alt="Follow Roots" src="https://img.shields.io/twitter/follow/rootswp.svg?style=flat-square&color=1da1f2" />
  </a>
</p>

<p align="center">
  <strong>Ansible-powered LEMP stack for WordPress</strong>
</p>

<p align="center">
  <a href="https://roots.io/"><strong><code>Website</code></strong></a> &nbsp;&nbsp; <a href="https://docs.roots.io/trellis/master/installation/"><strong><code>Documentation</code></strong></a> &nbsp;&nbsp; <a href="https://github.com/roots/trellis/releases"><strong><code>Releases</code></strong></a> &nbsp;&nbsp; <a href="https://discourse.roots.io/"><strong><code>Support</code></strong></a>
</p>

## Supporting

**Trellis** is an open source project and completely free to use.

However, the amount of effort needed to maintain and develop new features and products within the Roots ecosystem is not sustainable without proper financial backing. If you have the capability, please consider donating using the links below:

<div align="center">

[![Sponsor on GitHub](https://img.shields.io/static/v1?label=sponsor&message=%E2%9D%A4&logo=GitHub&style=flat-square)](https://github.com/sponsors/roots)
[![Sponsor on Patreon](https://img.shields.io/badge/sponsor-patreon-orange.svg?style=flat-square&logo=patreon")](https://www.patreon.com/rootsdev)
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
- PHP 8.0
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

## Requirements

See the full [installation](https://docs.roots.io/trellis/master/installation/#installation) docs for requirements and our [getting started pages](https://docs.roots.io/getting-started) for more OS specific instructions.

## Installation

Create a new project:

```bash
$ trellis new example.com
```

## Local development setup

1. Review the automatically created site in `group_vars/development/wordpress_sites.yml`
2. Customize settings if necessary

Start the Vagrant virtual machine:

```bash
$ trellis up
```

[Read the local development docs](https://docs.roots.io/trellis/master/local-development/#wordpress-installation) for more information.

## Remote server setup (staging/production)

A base Ubuntu 18.04 (Bionic) or Ubuntu 20.04 (Focal LTS) server is required for setting up remote servers.

1. Configure your WordPress sites in `group_vars/<environment>/wordpress_sites.yml` and in `group_vars/<environment>/vault.yml` (see the [Vault docs](https://docs.roots.io/trellis/master/vault/) for how to encrypt files containing passwords)
2. Add your server IP/hostnames to `hosts/<environment>`
3. Specify public SSH keys for `users` in `group_vars/all/users.yml` (see the [SSH Keys docs](https://docs.roots.io/trellis/master/ssh-keys/))

Provision the server:

```bash
$ trellis provision production
```

Or take advantage of its [Digital Ocean](https://roots.io/r/digitalocean) support to create a Droplet _and_ provision it in a single command:

```bash
$ trellis droplet create production
```

[Read the remote server docs](https://docs.roots.io/trellis/master/remote-server-setup/) for more information.

## Deploying to remote servers

1. Add the `repo` (Git URL) of your Bedrock WordPress project in the corresponding `group_vars/<environment>/wordpress_sites.yml` file
2. Set the `branch` you want to deploy (defaults to `master`)

Deploy a site:

```bash
$ trellis deploy <environment> <site>
```

Rollback a deploy:

```bash
$ trellis rollback <environment> <site>
```

[Read the deploys docs](https://roots.io/docs/trellis/master/deployments/) for more information.

## Migrating existing projects to trellis-cli:

Assuming you're using the standard project structure, you just need to make the
project trellis-cli compatible by initializing it:

```bash
$ trellis init
```

## Trellis sponsors

Help support our open-source development efforts by [becoming a GitHub sponsor](https://github.com/sponsors/roots) or [patron](https://www.patreon.com/rootsdev).

<a href="https://k-m.com/"><img src="https://cdn.roots.io/app/uploads/km-digital.svg" alt="KM Digital" width="200" height="150"></a> <a href="https://carrot.com/"><img src="https://cdn.roots.io/app/uploads/carrot.svg" alt="Carrot" width="200" height="150"></a> <a href="https://www.c21redwood.com/"><img src="https://cdn.roots.io/app/uploads/c21redwood.svg" alt="C21 Redwood Realty" width="200" height="150"></a> <a href="https://wordpress.com/"><img src="https://cdn.roots.io/app/uploads/wordpress.svg" alt="WordPress.com" width="200" height="150"></a> <a href="https://pantheon.io/"><img src="https://cdn.roots.io/app/uploads/pantheon.svg" alt="Pantheon" width="200" height="150"></a>

## Community

Keep track of development and community news.

- Join us on Roots Slack by becoming a [GitHub sponsor](https://github.com/sponsors/roots) or [patron](https://www.patreon.com/rootsdev)
- Participate on the [Roots Discourse](https://discourse.roots.io/)
- Follow [@rootswp on Twitter](https://twitter.com/rootswp)
- Read and subscribe to the [Roots Blog](https://roots.io/blog/)
- Subscribe to the [Roots Newsletter](https://roots.io/subscribe/)
