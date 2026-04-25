SHELL := /bin/bash

.PHONY: help sonar-up sonar-down build-image minikube-start minikube-env deploy-k8s deploy-k8s-patch k8s-rollout logs clean

help:
	@echo "Available targets:"
	@echo "  help               - show this help"
	@echo "  sonar-up           - start local SonarQube (docker compose)"
	@echo "  sonar-down         - stop local SonarQube and remove volumes"
	@echo "  build-image        - build the ACEest Docker image (aceest:local)"
	@echo "  minikube-start     - start minikube (driver=docker)"
	@echo "  minikube-env       - print the command to use minikube's Docker daemon"
	@echo "  deploy-k8s         - apply manifests in k8s/"
	@echo "  deploy-k8s-patch   - patch deployment image to aceest:local and wait for rollout"
	@echo "  k8s-rollout        - wait for aceest deployment rollout to finish"
	@echo "  logs               - follow container logs for aceest-web (if running)"
	@echo "  clean              - stop demo stacks (SonarQube)"

## Start local SonarQube (docker-compose)
sonar-up:
	docker compose -f docker-compose.sonarqube.yml up -d

## Stop SonarQube and remove volumes
sonar-down:
	docker compose -f docker-compose.sonarqube.yml down --volumes

## Build the application image used for minikube / local deploy
build-image:
	docker build -t aceest:local .

## Start minikube (assumes Docker driver available)
minikube-start:
	minikube start --driver=docker

## Print the command you should eval to use minikube's Docker daemon in your shell
minikube-env:
	@echo "Run the following in your shell to point Docker to minikube's daemon:"
	@echo
	@echo "  eval \"$$(minikube -p minikube docker-env)\""

## Apply k8s manifests present in k8s/
deploy-k8s:
	kubectl apply -f k8s/

## Patch the deployment image (aceest) and wait for rollout
deploy-k8s-patch:
	kubectl set image deployment/aceest-deployment aceest-container=aceest:local || true
	kubectl rollout status deployment/aceest-deployment

k8s-rollout:
	kubectl rollout status deployment/aceest-deployment

logs:
	docker logs -f aceest-web || true

clean:
	docker compose -f docker-compose.sonarqube.yml down --volumes || true
