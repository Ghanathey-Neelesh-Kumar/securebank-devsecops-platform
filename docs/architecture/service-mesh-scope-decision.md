# Service Mesh Scope Decision

## Decision

Istio was removed from the active SecureBank implementation scope.

## Reason

Istio introduced additional operational complexity during the local Kubernetes implementation phase. The project already demonstrates strong DevSecOps controls through CI/CD, image scanning, Kubernetes manifests, HPA/PDB, Calico NetworkPolicies, database readiness checks, and PostgreSQL persistence.

## Current Active Security Controls

- Calico NetworkPolicies
- Default deny ingress
- Frontend to Backend allowed
- Backend to PostgreSQL allowed
- Frontend to PostgreSQL blocked
- Non-root containers
- Readiness and liveness probes
- Resource requests and limits
- CI security scanning with Bandit, Semgrep, and Trivy

## Future Consideration

Service mesh may be revisited later using either Istio, Linkerd, or another mesh once the core platform is complete.
