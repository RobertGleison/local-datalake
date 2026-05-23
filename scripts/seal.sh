#!/usr/bin/env bash
# Generates and seals MinIO and Nessie secrets for local-lakehouse.
# Prerequisites: cluster running, sealed-secrets controller ready, kubeseal installed.
# Run: bash secrets/local-lakehouse/seal.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Ensuring local-lakehouse namespace exists..."
kubectl create namespace local-lakehouse --dry-run=client -o yaml | kubectl apply -f -

echo "==> Sealing minio-credentials..."
kubectl create secret generic minio-credentials \
  --namespace local-lakehouse \
  --from-literal=root-user=minioadmin \
  --from-literal=root-password=minioadmin123 \
  --dry-run=client -o yaml \
| kubeseal \
  --controller-name sealed-secrets \
  --controller-namespace kube-system \
  --scope namespace-wide \
  --format yaml \
  > "$REPO_ROOT/infra/minio/application/templates/minio-credentials.yaml"

echo "==> Sealing grafana-admin..."
kubectl create secret generic grafana-admin \
  --namespace local-lakehouse \
  --from-literal=admin-user=admin \
  --from-literal=admin-password=admin \
  --dry-run=client -o yaml \
| kubeseal \
  --controller-name sealed-secrets \
  --controller-namespace kube-system \
  --scope namespace-wide \
  --format yaml \
  > "$REPO_ROOT/infra/grafana/application/templates/grafana-admin.yaml"

echo ""
echo "Sealed secrets written alongside their services."
echo ""
echo "Next: commit and push, then deploy:"
echo "  git add infra/minio/application/templates/minio-credentials.yaml infra/grafana/application/templates/grafana-admin.yaml"
echo "  git commit -m 'feat: add sealed local-lakehouse secrets'"
echo "  git push"
echo "  kubectl apply -f argocd/appsets/"
