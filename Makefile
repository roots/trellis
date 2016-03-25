.PHONY: provision_sandbox

provision_sandbox:
	ansible-playbook server-sandbox.yml -e env=sandbox
