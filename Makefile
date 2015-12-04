.PHONY: provision_sandbox provision_devbox

provision_sandbox:
	ansible-playbook -i hosts/sandbox --vault-password-file ~/Dropbox/www/pt-ops/vault-key server-sandbox.yml

provision_devbox:
	PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o ForwardAgent=yes -o ControlMaster=auto -o ControlPersist=60s' ansible-playbook --private-key=/home/primoz/projects/pt/pt-ops/.vagrant/machines/default/virtualbox/private_key --user=vagrant --connection=ssh --limit='default' --inventory-file=/home/primoz/projects/pt/pt-ops/.vagrant/provisioners/ansible/inventory --vault-password-file ~/Dropbox/www/pt-ops/vault-key /home/primoz/projects/pt/pt-ops/dev.yml
