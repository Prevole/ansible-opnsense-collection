.EXPORT_ALL_VARIABLES:

CURRENT_UID=$(shell id -u)
CURRENT_VERSION=$(shell yq r galaxy.yml 'version')
CURRENT_NAMESPACE=$(shell yq r galaxy.yml 'namespace')
CURRENT_COLLECTION=$(shell yq r galaxy.yml 'name')
CURRENT_PATH=$(shell pwd)

all: test build install int-test

clean:
	rm -rf assets htmlcov test_report.html .coverage $$CURRENT_NAMESPACE-$$CURRENT_COLLECTION-*.tar.gz

build:
	ansible-galaxy collection build --force

install:
	ansible-galaxy collection install $$CURRENT_NAMESPACE-$$CURRENT_COLLECTION-$$CURRENT_VERSION.tar.gz --force

test:
	pytest --flake8 --cov-report html -m "not ansible"
	open test_report.html htmlcov/index.html

int-test: up
	rm -f tests/output/*.xml
	pytest \
		--cov-config=.coveragerc-int \
		--cov-report html:htmlcov-int \
		--ansible-playbook-directory $$CURRENT_PATH/tests/playbooks \
		--ansible-playbook-inventory $$CURRENT_PATH/tests/playbooks/inventory.yml \
		-m ansible
	open htmlcov-int/index.html

playbook: up
	rm -f tests/output/*.xml
	ansible-playbook tests/playbooks/collection.yml -vvv

up:
	docker-compose -f tests/docker-compose.yml up --build -d

down:
	docker-compose -f tests/docker-compose.yml down

help:
	@echo 'Usage: make <TARGETS> ...'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@echo '    help                        Show this help screen'
	@echo '    clean                       Remove some test related folders'
	@echo '    build					   Build the Ansible Collection'
	@echo '    install                     Install the Ansible Collection'
	@echo '    test                        Run unit tests'
	@echo '    int-test                    Run integration tests'
	@echo '	   playbook					   Run the Ansible Test Playbook'
	@echo '    up 						   Instantiate the openssh container'
	@echo '    down                        Remove docker containers, networks, images, and volumes'
	@echo ''
	@echo 'Targets run by default are: test build install int-test'
	@echo ''