# SecureBank — Final Reference Architecture

SecureBank is a production-style DevSecOps banking platform built to demonstrate secure software delivery, Kubernetes operations, GitOps deployment, service mesh security, external secrets management, database resilience, observability, and compliance-aware audit logging.

## Approved Architecture Flow

Users access SecureBank through the edge layer:

```text
Users → DNS → WAF → Load Balancer → NGINX Ingress
