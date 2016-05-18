## What is ansible-ferm? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-ferm.png)](http://travis-ci.org/nickjj/ansible-ferm)

It is an [ansible](http://www.ansible.com/home) role to manage iptables using the ever so flexible ferm tool.

### What problem does it solve and why is it useful?

Working with iptables directly can be really painful and the ufw module is decent for basic needs but sometimes you need a bit more control. I also like the approach of writing templates rather than executing allow/deny commands with ufw. I feel like it sets the tone for a more idempotent setup.

## Role variables

Below is a list of default values along with a description of what they do.

```
# Should the firewall be enabled?
ferm_enabled: true

# Should ferm do ip-based tagging/locking when it detects someone is trying to port scan you?
ferm_limit_portscans: false

# The default actions to take for certain policies. You likely want to keep them at the default values.
# This ensures all ports are blocked until you white list them.
ferm_default_policy_input: DROP
ferm_default_policy_output: ACCEPT
ferm_default_policy_forward: DROP

# The lists to use to provide your own rules. This is explained more below.
ferm_input_list: []
ferm_input_group_list: []
ferm_input_host_list: []

# The amount in seconds to cache apt-update.
apt_cache_valid_time: 86400
```

### `ferm_input_list` with the `dport_accept` template

The use case for this would be to white list ports to be opened.

```
ferm_input_list:
    # Choose the template to use.
    # REQUIRED: It can be either `dport_accept` or `dport_limit`.
  - type: "dport_accept"

    # Which protocol should be used?
    # OPTIONAL: Defaults to tcp.
    protocol: "tcp"

    # Which ports should be open?
    # REQUIRED: It can be the port value or a service in `/etc/services`.
    dport: ["http", "https"]

    # Which IP addresses should be white listed?
    # OPTIONAL: Defaults to an empty list.
    saddr: []

    # Should all IP addresses be white listed?
    # OPTIONAL: Defaults to true.
    accept_any: true

    # Which filename should be written out?
    # OPTIONAL: Defaults to the first port listed in `dport`.

    # The filename which will get written to `/etc/ferm/filter-input.d/nginx_accept`.
    filename: "nginx_accept"

    # Should this rule be deleted?
    # OPTIONAL: Defaults to false.
    delete: false
```

### `ferm_input_list` with the `dport_limit` template

The use case for this would be to limit connections on specific ports based on an amount of time. This could be used to harden your security.

```
ferm_input_list:
    # Choose the template to use.
    # REQUIRED: It can be either `dport_accept` or `dport_limit`.
  - type: "dport_limit"

    # Which protocol should be used?
    # OPTIONAL: Defaults to tcp.
    protocol: "tcp"

    # Which ports should be open?
    # REQUIRED: It can be the port value or a service in `/etc/services`.
    dport: ["ssh"]

    # How many seconds to count in between the hits?
    # OPTIONAL: Defaults to 300.
    seconds: "300"

    # How many connections should be allowed per the amount of seconds you specified.
    # OPTIONAL: Defaults to 5.
    hits: "5"

    # Should this rule be disabled?
    # OPTIONAL: Defaults to false.
    disabled: false
```

#### `ferm_input_group_list` / `ferm_input_host_list` with either template

This would be the same as above except it would be scoped to the groups and hosts list.

## Example app play in your playbook

To open the http/https ports on your server add the following to the appropriate group or host vars file:

```
ferm_input_group_list:
  - type: "dport_accept"
    dport: ["http", "https"]
    filename: "nginx_accept"
```

I only chose the `nginx_accept` filename because I use nginx. You can name it whatever you want or even remove the filename to have this role automatically generate a filename for you.

This file will be written to `/etc/ferm/filter-input.d/nginx_accept.conf` and it will contain the rules necessary to open the `http` and `https` ports.

## Attribution

Many thanks to [nickjj](https://github.com/nickjj/) for creating the [original version](https://github.com/nickjj/ansible-ferm/) of this role.
