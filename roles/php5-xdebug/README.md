# Ansible Role: PHP-XDebug

[![Build Status](https://travis-ci.org/MaximeThoonsen/ansible-role-php-xdebug.svg?branch=master)](https://travis-ci.org/MaximeThoonsen/ansible-role-php-xdebug)

Installs PHP [XDebug](http://xdebug.org/) on Ubuntu Trusty(14.04) or Precise(12.04).

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `vars/main.yml`):

    php_xdebug_remote_enable: "false"

Whether remote debugging is enabled.

    php_xdebug_remote_connect_back: "false"

If this is set to true, Xdebug will respond to any request from any IP address; use only for local development on non-public installations!

    php_xdebug_remote_host: localhost
    php_xdebug_remote_port: "9000"

The host and port on which Xdebug will listen.

    php_xdebug_remote_log: /tmp/xdebug.log

The location of the xdebug log (useful if you're having trouble connecting).

    php_xdebug_idekey: XDEBUG

The IDE key to use in the URL when making Xdebug requests (e.g. `http://example.local/?XDEBUG_SESSION_START=XDEBUG`).

## Example Playbook

    - hosts: webservers
      roles:
        - { role: MaximeThoonsen.php5-xdebug }

## License

MIT

## Author Information

This role was created in 2014 by [Maxime Thoonsen](https://twitter.com/MaximeThoonsen).
It was forked from [Jeff Geerling's role](https://github.com/geerlingguy/ansible-role-php-xdebug)
