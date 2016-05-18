## What is ansible-fail2ban?

It is an [ansible](http://www.ansible.com/home) role to install and configure fail2ban.

### What problem does it solve and why is it useful?

Security is important and fail2ban is an excellent tool to harden your server with minimal or even no configuration.

## Role variables

Below is a list of default values along with a description of what they do.

```
# Which log level should it be output as?
# 1 = ERROR, 2 = WARN, 3 = INFO, 4 = DEBUG
fail2ban_loglevel: 3

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

# What services should fail2ban monitor?
# You can define fail2ban_services as an empty string to not monitor anything.
# You can define multiple services as a standard yaml list.
fail2ban_services:
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

    # What filter should it use?
    # REQUIRED.
    filter: sshd

    # Which log path should it monitor?
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

## Example playbook

Let's say you want to edit a few values, you can do this by opening `group_vars/all` and then add the following:

```
fail2ban_services:
  - name: ssh
    port: ssh
    filter: sshd
    logpath: /var/log/auth.log
  - name: postfix
    port: smtp,ssmtp
    filter: postfix
    logpath: /var/log/mail.log
```

## Attribution

Many thanks to [nickjj](https://github.com/nickjj/) for creating the [original version](https://github.com/nickjj/ansible-fail2ban/) of this role.
