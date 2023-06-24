# MAKEFILE SETTINGS
# Silence default command echoing
.SILENT:
# Use one shell for all commands in a target recipe
.ONESHELL:
.EXPORT_ALL_VARIABLES:
# Set phony targets
.PHONY: help build up down
# Set default goal
.DEFAULT_GOAL := help
# Use bash shell in Makefile instead of sh
SHELL = /bin/bash

build: ## Build docker image
	docker compose build

up: build  ## Run docker compose service
	docker compose up -d
	sleep 3
	echo "open http://127.0.0.1:8888/lab"
	bash -c "open http://127.0.0.1:8888/lab"
	sleep 2
	docker logs -n 1000 -f pgadmin-jupyterlab

down:  ## Stop docker compose service
	docker compose down
	docker compose down --volumes

rebuild: down up  ## Rebuild docker compose service

# Display target comments in 'make help'
help: ## Show this help
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
