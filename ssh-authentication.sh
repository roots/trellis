#!/usr/bin/env bash

# --------------------------------------------------------------------
# Creates a new authorized_keys file for the vagrant user with (only)
# the yaml-specified public key. Thus effectively:
# - disabling the Vagrant insecure key
# - requiring all SSH logins to require the yaml-specified private key
#
# Please note that the public key (e.g. cakebox_rsa.pub) has already
# been copied from the local machine to the /home/vagrant/.ssh/ folder
# inside the vm before this script executes. Private key is used for
# user feedback only, never leaves local machine.
#
# Also note creation of the flag file generated so the default Vagrant
# 1.7.x private key on the local machine will only be removed once this
# script has successfully replaced the public key on the vm (to prevent
# SSH timeouts running vagrant reload --provision against a running vm )
# --------------------------------------------------------------------

#credit: https://github.com/alt3/cakebox


# Convenience variables
PUBLIC_KEY=$1
PRIVATE_KEY=$2
SSH_DIR='/home/vagrant/.ssh'
AUTHORIZED_KEYS="$SSH_DIR/authorized_keys"
#VAGRANT_FLAG_FILE='.cakebox/remove-vagrant-key.flag'
VAGRANT_17X_KEY='/vagrant/machines/default/virtualbox/private_key'

printf %63s |tr " " "-"
printf '\n'
printf "Restricting Trellis SSH logins\n"
printf %63s |tr " " "-"
printf '\n'

# Do nothing if Vagrantfile-specified public key is already the only key in authorized_keys
if diff "$AUTHORIZED_KEYS" "$SSH_DIR/$PUBLIC_KEY" >/dev/null ; then
	echo "* Skipping: SSH logins already require Vagrantfile-specified private key ($PRIVATE_KEY)"
	exit 0
fi

# Still here, verify the public key is valid before applying (to prevent locking out user)
echo "* Validating Vagrantfile-specified public key ($PUBLIC_KEY)"
OUTPUT=$(ssh-keygen -l -f "$SSH_DIR/$PUBLIC_KEY" 2>&1)
EXITCODE=$?
if [ "$EXITCODE" -ne 0 ]; then
	echo $OUTPUT
	echo "FATAL: key did not pass validation, make sure it is in OpenSSH format"
	exit 1
fi

# Make Vagrantfile-specified public key the only key in authorized_keys
echo "* Replacing current public keys in $AUTHORIZED_KEYS"
cat "$SSH_DIR/$PUBLIC_KEY" > "$AUTHORIZED_KEYS"

# Remove Vagrant 1.7.x secure private key on host using Synced Folder
if [ -f "$VAGRANT_17X_KEY" ]; then
	echo "* Removing Vagrant 1.7.x generated private key"
	OUTPUT=$(rm "$VAGRANT_17X_KEY" 2>&1)
	EXITCODE=$?
	if [ "$EXITCODE" -ne 0 ]; then
		echo $OUTPUT
		echo "FATAL: error removing key"
		exit 1
	fi
fi

# All done
echo "* SSH logins now require Vagrantfile-specified private key ($PRIVATE_KEY)"
echo "Command completed successfully"