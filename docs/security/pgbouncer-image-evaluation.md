# PgBouncer Image Security Evaluation

SecureBank requires a PostgreSQL connection pooler as part of the final architecture.

The initial candidate image was:

`edoburu/pgbouncer:v1.25.1-p0`

A Trivy scan was performed before deployment.

## Scan Result

- Critical vulnerabilities: 4
- High vulnerabilities: 23
- Medium vulnerabilities: 30
- Low vulnerabilities: 3

## Decision

This image was rejected for the SecureBank project because the vulnerability profile is not acceptable for a banking-style DevSecOps platform.

## DevSecOps Rationale

A connection pooler sits in the database path:

`Backend API → PgBouncer → PostgreSQL`

Because it is part of the critical data path, the image must meet a higher security bar.

## Next Action

Evaluate hardened alternatives such as:

- Docker Hardened Images PgBouncer
- Chainguard PgBouncer
- CloudNativePG-compatible PgBouncer image
- internally built and scanned PgBouncer image

Until a suitable image is selected, SecureBank will continue with:

`Backend API → PostgreSQL`

and PgBouncer will remain an approved architecture component pending hardened image selection.
