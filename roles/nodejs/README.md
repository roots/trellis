# Ansible Role: Node.js

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-nodejs.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-nodejs)

Installs Node.js on RHEL/CentOS or Debian/Ubuntu.

## Requirements

Requires the EPEL repository on RedHat/CentOS (you can install it by simply adding the `geerlingguy.repo-epel` role to your playbook).

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    nodejs_version: "6.x"

The Node.js version to install. "6.x" is the default and works on most supported OSes. Other versions such as "0.12", "4.x", "5.x", "6.x", etc. should work on the latest versions of Debian/Ubuntu and RHEL/CentOS.

    nodejs_install_npm_user: "{{ ansible_ssh_user }}"

The user for whom the npm packages will be installed can be set here, this defaults to `ansible_user`.

    npm_config_prefix: "/usr/local/lib/npm"

The global installation directory. This should be writeable by the `nodejs_install_npm_user`.

    npm_config_unsafe_perm: "false"

Set to true to suppress the UID/GID switching when running package scripts. If set explicitly to false, then installing as a non-root user will fail.

    nodejs_npm_global_packages: []

A list of npm packages with a `name` and (optional) `version` to be installed globally. For example:

    nodejs_npm_global_packages:
      # Install a specific version of a package.
      - name: jslint
        version: 0.9.3
      # Install the latest stable release of a package.
      - name: node-sass
      # This shorthand syntax also works (same as previous example).
      - node-sass
<!-- code block separator -->

    nodejs_package_json_path: ""

Set a path pointing to a particular `package.json` (e.g. `"/var/www/app/package.json"`). This will install all of the defined packages globally using Ansible's `npm` module.

## Dependencies

None.

## Example Playbook

    - hosts: utility
      vars_files:
        - vars/main.yml
      roles:
        - geerlingguy.nodejs

*Inside `vars/main.yml`*:

    nodejs_npm_global_packages:
      - name: jslint
      - name: node-sass

## License

MIT / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).
