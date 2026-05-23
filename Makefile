.PHONY: help install deps cluster seal deploy stop start destroy argocd-password validate

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────────────

deps: ## Install prerequisites (macOS only)
	brew install k3d kubectl helm kubeseal

# ── Cluster lifecycle ────────────────────────────────────────────────────────

up: cluster seal ## Full bootstrap: create cluster, re-seal secrets, push, and deploy
	git add infra/minio/application/templates/minio-credentials.yaml infra/grafana/application/templates/grafana-admin.yaml
	git commit -m "chore: re-seal secrets for new cluster"
	git push
	kubectl apply -f argocd/appsets/

cluster: ## Create k3d cluster + install ArgoCD + Sealed Secrets
	bash scripts/bootstrap.sh

stop: ## Pause the cluster (state is preserved)
	k3d cluster stop local-lakehouse

start: ## Resume a paused cluster
	k3d cluster start local-lakehouse

destroy: ## Delete the k3d cluster
	k3d cluster delete local-lakehouse

# ── Secrets ──────────────────────────────────────────────────────────────────

seal: ## Encrypt secrets with kubeseal (run before committing secrets)
	bash scripts/seal.sh

# ── Validation ───────────────────────────────────────────────────────────────

validate: ## Validate ArgoCD service registry JSON
	@python3 -m json.tool argocd/appsets/services.json > /dev/null && echo "argocd/appsets/services.json is valid"

# ── Services ─────────────────────────────────────────────────────────────────

deploy: ## Apply all ArgoCD applications (MinIO, Nessie, Secrets)
	kubectl apply -f argocd/appsets/

# ── Helpers ──────────────────────────────────────────────────────────────────

argocd-password: ## Print the ArgoCD admin password
	@kubectl get secret argocd-initial-admin-secret -n argocd \
		-o jsonpath="{.data.password}" | base64 -d && echo

argocd-ui: ## Port-forward ArgoCD UI to https://localhost:8080
	kubectl port-forward svc/argocd-server -n argocd 8080:443
