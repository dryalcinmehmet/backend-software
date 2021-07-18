.DEFAULT_GOAL := all
ROOT_DIR ?= .

.PHONY: all
all: build setup start

.PHONY: apply
apply: build restartapps

.PHONY: build
build:
	docker build -t backend-software .

.PHONY: setup
setup:
	docker-compose up -d
	echo "Waiting 10s for services to start"
	sleep 5
	docker-compose run --rm --entrypoint 'python3 manage.py' app migrate
	docker-compose run --rm --entrypoint 'python3 manage.py' app createsuperuser

.PHONY: start
start:
	echo "Setup copleted. Try to open http://127.0.0.1/admin"

.PHONY: shell
shell:
	docker-compose run --rm --entrypoint 'python3 manage.py' app shell

.PHONY: test
test:
	docker-compose run --rm --entrypoint 'python3 manage.py' app test --keepdb --verbosity 2 \
		$(PATTERN) \
		$(ARGS)


.PHONY: manage
manage:
	docker-compose run --rm --entrypoint 'python3 manage.py' app \
		$(PATTERN) \
		$(ARGS)

.PHONY: restartenv
restartenv:
	docker-compose stop
	docker-compose start

.PHONY: restartapps
restartapps:
	docker-compose rm -s -v -f app
	docker-compose up -d app


#| Assign ARGS variable to tokens after first given target
#| and then evaluate them into new noop targets if require-args.
#| Example: make <target> <ARGS>
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

#| Target dependency helper, ensuring target arg is given.
.PHONY: require-args
require-args:
ifndef ARGS
	$(error Missing target args, i.e. make <target> <arg>)
endif
