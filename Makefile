.PHONY: provision_sandbox provision_production install_ansible_deps vagrant_manual_provisioning clean

provision_sandbox:
	ansible-playbook server.yml -e env=sandbox

provision_production:
	ansible-playbook server.yml -e env=production

install_ansible_deps:
	rm -rf vendor/
	ansible-galaxy install -r requirements.yml

vagrant_manual_provisioning:
	# in case SSH conn. gets rejected, remove the line starting with 127.0.0.1 in ~/.ssh/known_hosts
	ansible-playbook -u vagrant -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory dev.yml

clean:
	rm *.retry
