# Edge Gateway Decision — SecureBank

## Context

SecureBank originally considered using the community Kubernetes `ingress-nginx` controller as the external entry point.

However, SecureBank is a production-style DevSecOps banking platform, and the edge layer must be selected carefully because it becomes part of the security perimeter.

The approved SecureBank architecture also includes Istio for:

- service-to-service mTLS
- authorization policies
- traffic control
- service mesh telemetry
- secure workload communication

## Decision

SecureBank will not use the community `ingress-nginx` controller for the final architecture.

Instead, SecureBank will use the Gateway API / Istio Gateway path.

The target edge flow is:

```text
Users
  ↓
DNS / WAF / Load Balancer
  ↓
Gateway API / Istio Gateway
  ↓
Frontend Service
  ↓
Backend Service
  ↓
PostgreSQL
