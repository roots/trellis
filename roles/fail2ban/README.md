## What is this role?

This role installs and configures [Fail2ban](https://github.com/fail2ban/fail2ban).

Fail2ban is an excellent tool to harden your server with minimal configuration.

## Role variables

Below is a list of available variables, their description and their default value within Trellis.

```yaml
# Which log level should it be output as?
# Levels: CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG.
fail2ban_loglevel: INFO

# Where should log outputs be sent to?
# SYSLOG, STDERR, STDOUT, file
fail2ban_logtarget: /var/log/fail2ban.log

# Where should the socket be created?
fail2ban_socket: /var/run/fail2ban/fail2ban.sock

# Which IP address, CIDR mark or DNS host should be ignored?
fail2ban_ignoreip: 127.0.0.1/8

# How long in seconds should the ban last for?
fail2ban_bantime: 600

# How many times can they try before getting banned?
fail2ban_maxretry: 6

# How should the file changes be detected?
# gamin, polling, auto
fail2ban_backend: polling

# Where should e-mail reports be sent to?
fail2ban_destemail: root@localhost

# How should the ban be applied?
# iptables, iptables-new, iptables-multiport, shorewall, etc.
fail2ban_banaction: iptables-multiport

# What e-mail action should be used?
# sendmail or mail
fail2ban_mta: sendmail

# What should the default protocol be?
fail2ban_protocol: tcp

# Which chain would the JUMPs be added into iptables-*?
fail2ban_chain: INPUT

# What should the default ban action be?
# action_, action_mw, action_mwl
fail2ban_action: action_

# Trellis by default only monitors SSH connections
# For available parameters, see fail2ban_services_custom below.
fail2ban_services_default:
  - name: ssh
    port: ssh
    filter: sshd
    logpath: /var/log/auth.log

# In which folder did you place custom filters?
# Filters MUST have .conf.j2 extension to copied to the servers.
fail2ban_filter_templates_path: fail2ban_filters
```

The following list variable is available for custom services (to be set up in `group_vars`):

```yaml
# Which additional services should fail2ban monitor?
# You can define multiple services as a standard yaml list.
fail2ban_services_custom:
    # The name of the service
    # REQUIRED.
  - name: ssh

    # Is it enabled?
    # OPTIONAL: Defaults to "true" (must be a string).
    enabled: "true"

    # What port does the service use?
    # Separate multiple ports with a comma, no spaces.
    # REQUIRED.
    port: ssh

    # What protocol does the service use?
    # OPTIONAL: Defaults to the protocol listed above.
    protocol: tcp

    # Which filter should it use?
    # REQUIRED.
    filter: sshd

    # Which log file should it monitor?
    # REQUIRED.
    logpath: /var/log/auth.log

    # How many times can they try before getting banned?
    # OPTIONAL: Defaults to the maxretry listed above.
    maxretry: 6

    # What should the default ban action be?
    # OPTIONAL: Defaults to the action listed above.
    action: action_

    # How should the ban be applied?
    # OPTIONAL: Defaults to the banaction listed above.
    banaction: iptables-multiport

```

## Custom Settings

To add services, you might add the following to `group_vars/all/security.yml`, e.g.:

```yaml
fail2ban_services_custom:
  - name: wordpress
    filter: wordpress
    logpath: /var/log/auth.log
    maxretry: 2
```

To add the corresponding filter, add it to the folder specified in `fail2ban_filter_templates_path`, i.e. `fail2ban_filters` per default (next to the `group_vars` folder). The filter configuration must be of `.conf.j2` extension for Trellis to recognize it.

Filters might be provided by plugins as `.conf` files: it is then enough to simply append the file name with `.j2`. It is not required to modify these provided filters, but you may customize them to your liking.

To develop custom filters, refer to the Fail2ban wiki: [How Fail2ban works](https://github.com/fail2ban/fail2ban/wiki/How-fail2ban-works) and [How to ban something…](https://github.com/fail2ban/fail2ban/wiki/How-to-ban-something-other-as-host-(IP-address),-like-user-or-mail,-etc.) for simple filter rules or [Developing Filters](https://fail2ban.readthedocs.io/en/latest/filters.html) for complex setups.

If you need to edit the default services, copy the `fail2ban_services_default` list from `roles/fail2ban/defaults/main.yml` to `group_vars/all/security.yml` and edit as needed.

## Attribution

Many thanks to [nickjj](https://github.com/nickjj/) for creating the [original version](https://github.com/nickjj/ansible-fail2ban/) of this role.
