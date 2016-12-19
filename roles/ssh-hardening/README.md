# ssh-hardening (Ansible Role)

## Description

This role provides secure ssh-client and ssh-server configurations.

## Requirements

* Ansible

## Role Variables
| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
|`network_ipv6_enable` | false |true if IPv6 is needed|
|`ssh_client_cbc_required` | false |true if CBC for ciphers is required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure ciphers enabled. CBC is a weak alternative. Anything weaker should be avoided and is thus not available.|
|`ssh_server_cbc_required` | false |true if CBC for ciphers is required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure ciphers enabled. CBC is a weak alternative. Anything weaker should be avoided and is thus not available.|
|`ssh_client_weak_hmac` | false |true if weaker HMAC mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure HMACs enabled.|
|`ssh_server_weak_hmac` | false |true if weaker HMAC mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure HMACs enabled.|
|`ssh_client_weak_kex` | false |true if weaker Key-Exchange (KEX) mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure KEXs enabled.|
|`ssh_server_weak_kex` | false |true if weaker Key-Exchange (KEX) mechanisms are required. This is usually only necessary, if older M2M mechanism need to communicate with SSH, that don't have any of the configured secure KEXs enabled.|
|`ssh_server_ports` | ['22'] |ports to which ssh-server should listen to|
|`ssh_client_ports` | ['22'] |ports to which ssh-client should connect to|
|`ssh_listen_to` | ['0.0.0.0'] |one or more ip addresses, to which ssh-server should listen to. Default is all adresseses, but should be configured to specific addresses for security reasons!|
|`ssh_host_key_files` | ['/etc/ssh/ssh_host_ed25519_key', '/etc/ssh/ssh_host_rsa_key'] |Host keys to look for when starting sshd.|
|`ssh_host_key_algorithms` | ['ssh-ed25519-cert-v01@openssh.com', 'ssh-rsa-cert-v01@openssh.com', 'ssh-ed25519', 'ssh-rsa'] |Host key algorithms that the ssh-client wants to use, in order of preference.|
|`ssh_client_alive_interval` | 600 | specifies an interval for sending keepalive messages |
|`ssh_client_alive_count` | 3 | defines how often keep-alive messages are sent |
|`ssh_remote_hosts` | [] | one or more hosts and their custom options for the ssh-client. Default is empty. See examples in `defaults/main.yml`.|
|`ssh_allow_root_with_key` | false | false to disable root login altogether. Set to true to allow root to login via key-based mechanism.|
|`ssh_allow_tcp_forwarding` | false | false to disable TCP Forwarding. Set to true to allow TCP Forwarding.|
|`ssh_allow_agent_forwarding` | true | false to disable Agent Forwarding. Set to true to allow Agent Forwarding.|
|`ssh_use_pam` | true | pam authentication enabled to avoid Debian [bug #751636](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=751636) with openssh-server.|
|`ssh_deny_users` | '' | if specified, login is disallowed for user names that match one of the patterns.|
|`ssh_allow_users` | '' | if specified, login is allowed only for user names that match one of the patterns.|
|`ssh_deny_groups` | '' | if specified, login is disallowed for users whose primary group or supplementary group list matches one of the patterns.|
|`ssh_allow_groups` | '' | if specified, login is allowed only for users whose primary group or supplementary group list matches one of the patterns.|
|`ssh_print_motd` | false | false to disable printing of the MOTD|
|`ssh_print_last_log` | false | false to disable display of last login information|
|`ssh_send_env` | '' | if specified, indicates which variables the ssh-client should send to the remote server.|
|`ssh_accept_env` | '' | if specified, indicates which variables sent by the client will be copied into the ssh-server's session environ. Avoid accepting any variables, if possible.|
|`sftp_enabled` | false | true to enable sftp configuration|
|`sftp_chroot_dir` | /home/%u | change default sftp chroot location|
|`ssh_client_roaming` | false | enable experimental client roaming|

## FAQ / Pitfalls

**I can't log into my account. I have registered the client key, but it still doesn't let me it.**

If you have exhausted all typical issues (firewall, network, key missing, wrong key, account disabled etc.), it may be that your account is locked. The quickest way to find out is to look at the password hash for your user:

    sudo grep myuser /etc/shadow

If the hash includes an `!`, your account is locked:

    myuser:!:16280:7:60:7:::

The proper way to solve this is to unlock the account (`passwd -u myuser`). If the user doesn't have a password, you should can unlock it via:

    usermod -p "*" myuser

Alternatively, if you intend to use PAM, you enabled it via `ssh_use_pam: true`. PAM will allow locked users to get in with keys.


**Why doesn't my application connect via SSH anymore?**

Always look into log files first and if possible look at the negotation between client and server that is completed when connecting.

We have seen some issues in applications (based on python and ruby) that are due to their use of an outdated crypto set. This collides with this hardening module, which reduced the list of ciphers, message authentication codes (MACs) and key exchange (KEX) algorithms to a more secure selection.

If you find this isn't enough, feel free to activate the attributes `cbc_requires` for ciphers, `weak_hmac` for MACs and `weak_kex`for KEX in the variables `ssh_client` or `ssh_server` based on where you want to support them.

**After using the role Ansibles template/copy/file module does not work anymore!**

This role deactivates SFTP. Ansible uses by default SFTP to transfer files to the remote hosts. You have to set `scp_if_ssh = True` in your ansible.cfg. This way Ansible uses SCP to copy files.

**Cannot restart sshd-service due to lack of privileges**

If you get the following error when running handler "restart sshd"
```
Unable to restart service ssh: Failed to restart ssh.service: Access denied
```
or
```
failure 1 running systemctl show for 'ssh': Failed to connect to bus: No such file or directory
```
either run the playbook as `root` (without `become: yes` at the playbook level), or add `become: yes` to the handler.

This is a bug with Ansible: see [here](https://github.com/dev-sec/ansible-ssh-hardening/pull/81) and [here](https://github.com/ansible/ansible/issues/17490) for more information.

## Attribution

This role has been modified from the original to work with the defaults that have been established in Trellis.

Many thanks to [dev-sec](https://github.com/dev-sec/) for creating the [original version](https://github.com/dev-sec/ansible-ssh-hardening) of this role.
