#!/bin/bash
#
# Windows provisioner for Trellis
# heavily modified and based on KSid/windows-vagrant-ansible
# @author Andrea Brandi
# @version 1.0

ANSIBLE_PATH=$1
TEMP_HOSTS="/tmp/ansible_hosts"

# Create an ssh key if not already created.
if [ ! -f ~/.ssh/id_rsa ]; then
  echo -e "\n\n\n" | ssh-keygen -t rsa
fi

# Install Ansible and its dependencies if not installed.
if [ ! -f /usr/bin/ansible ]; then
  echo "Adding Ansible repository..."
  sudo apt-add-repository ppa:ansible/ansible
  echo "Updating system..."
  sudo apt-get -y update
  echo "Installing Ansible..."
  sudo apt-get -y install ansible
fi

if [ ! -d /vagrant/${ANSIBLE_PATH}/vendor ]; then
  echo "Running Ansible Galaxy install"
  ansible-galaxy install -r /vagrant/${ANSIBLE_PATH}/requirements.yml -p /vagrant/${ANSIBLE_PATH}/vendor/roles
fi

if [ -d ${TEMP_HOSTS} ]; then
  echo "Cleaning old Ansible Hosts"
  rm -rf ${TEMP_HOSTS}
fi

cp -R /vagrant/${ANSIBLE_PATH}/hosts ${TEMP_HOSTS} && chmod -x ${TEMP_HOSTS}/*
echo "Running Ansible Playbooks"
cd /vagrant/${ANSIBLE_PATH}/
ansible-playbook /vagrant/${ANSIBLE_PATH}/dev.yml -i ${TEMP_HOSTS}/development --sudo --user=vagrant --connection=local
rm -rf ${TEMP_HOSTS}
