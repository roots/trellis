test_ubuntu-14.04:
	VM_BOX='ubuntu/trusty64' vagrant up --provision
	VM_BOX='ubuntu/trusty64' vagrant provision
	VM_BOX='ubuntu/trusty64' vagrant destroy -f

test_ubuntu-12.04:
	VM_BOX='hashicorp/precise64' vagrant up --provision
	VM_BOX='hashicorp/precise64' vagrant provision
	VM_BOX='hashicorp/precise64' vagrant destroy -f

test_all:
	make test_ubuntu-12.04
	make test_ubuntu-14.04
