# Security Policy

## Reporting a Vulnerability

Please do not open a public GitHub issue for security-sensitive problems.

Instead:

1. Contact the repository maintainer privately through GitHub.
2. Include the affected files, impact, and reproduction steps.
3. If possible, include a proposed fix or mitigation.

## What Counts as Security-Relevant Here

- unsafe file discovery or path traversal
- unintended writes outside the declared workspace
- snapshot generation that leaks secrets
- registry sync behavior that trusts hostile input too broadly

## Response Goal

The project should acknowledge credible reports quickly and coordinate a fix before public disclosure when practical.
