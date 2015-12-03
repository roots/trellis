.PHONY: provision_sandbox

provision_sandbox:
	ansible-playbook -i hosts/sandbox --vault-password-file ~/Dropbox/www/pt-ops/vault-key server-sandbox.yml
