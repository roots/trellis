#!/bin/bash
vagrant_host=$1

# Add Vagrant ssh-config to ~/.ssh/config
sed "/^$/d;s/Host /$NL&/" ~/.ssh/config | sed '/^Host '"$vagrant_host"'$/,/^$/d;' > config &&
cat config > ~/.ssh/config &&
rm config &&
vagrant ssh-config --host ${vagrant_host} >> ~/.ssh/config
