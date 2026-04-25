#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script: updates image on the deployment and waits for rollout
# Usage: ./scripts/deploy_k8s.sh <image:tag>

IMAGE=${1:-}
if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image:tag>" >&2
  exit 2
fi

echo "Deploying image: $IMAGE to Kubernetes deployment/aceest-deployment"

kubectl -n default set image deployment/aceest-deployment aceest=$IMAGE --record
kubectl -n default rollout status deployment/aceest-deployment -w

echo "Deployment finished. Verifying pods:"
kubectl -n default get pods -l app=aceest -o wide

echo "Service endpoints:"
kubectl -n default get svc aceest-svc -o wide || true

echo "You can perform a smoke test with: curl -sS <cluster-ip-or-loadbalancer>/:/"
