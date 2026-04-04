#!/usr/bin/env bash
# remote-deploy.sh
# Usage: ./remote-deploy.sh <user@host> [git-branch]
# Example: ./remote-deploy.sh ubuntu@3.12.45.67 main

set -euo pipefail

REMOTE=${1:-}
BRANCH=${2:-main}

if [ -z "$REMOTE" ]; then
  echo "Usage: $0 <user@host> [branch]"
  exit 2
fi

REPO_URL="https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1.git"
REMOTE_DIR="~/aceest-deploy"

echo "=== Deploying to $REMOTE (branch=$BRANCH) ==="

SSH_OPTS="-o StrictHostKeyChecking=accept-new"

echo "Step 1: Install Docker & dependencies on remote (sudo may be required)"
ssh $SSH_OPTS $REMOTE bash -c "'
set -e
if ! command -v docker >/dev/null 2>&1; then
  echo "Installing Docker Engine (apt)"
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg lsb-release
  sudo mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  sudo usermod -aG docker \$(whoami) || true
fi
if ! command -v git >/dev/null 2>&1; then
  sudo apt-get install -y git
fi
']"

echo "Step 2: Clone or update repository on remote"
ssh $SSH_OPTS $REMOTE bash -lc "'
set -e
mkdir -p $REMOTE_DIR
cd $REMOTE_DIR
if [ -d .git ]; then
  git fetch origin
  git checkout $BRANCH
  git pull origin $BRANCH
else
  rm -rf ./*
  git clone --depth 1 --branch $BRANCH $REPO_URL .
fi
sudo chown -R \$(whoami):\$(whoami) .
']"

echo "Step 3: Launch with docker compose"
ssh $SSH_OPTS $REMOTE bash -lc "'
set -e
cd $REMOTE_DIR/deploy
# Use docker compose plugin if available
if docker compose version >/dev/null 2>&1; then
  docker compose pull || true
  docker compose up -d --build
else
  # fallback to docker-compose
  sudo apt-get install -y docker-compose
  docker-compose pull || true
  docker-compose up -d --build
fi
']"

echo "Deployment completed. The application should be reachable on http://<remote-host>/"
echo "If the remote instance is behind a firewall, make sure TCP port 80 is open."

echo "Tip: to view logs: ssh $REMOTE 'docker logs -f aceest_app'"
