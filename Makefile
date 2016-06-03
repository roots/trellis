.PHONY: provision_sandbox install_ansible_deps

provision_sandbox:
	ansible-playbook server-sandbox.yml -e env=sandbox

install_ansible_deps:
	ansible-galaxy install -r requirements.yml
