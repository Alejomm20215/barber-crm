# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: security@barber-crm.example.com

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Security Measures

### Application Security

- ✅ **Authentication**: All API endpoints require authentication
- ✅ **Authorization**: Row Level Security (RLS) enforced at database level
- ✅ **CORS**: Configured to allow only trusted origins
- ✅ **CSRF**: Django CSRF protection enabled
- ✅ **SQL Injection**: Using ORM prevents SQL injection
- ✅ **XSS**: Django auto-escaping prevents XSS
- ✅ **Secrets**: Environment variables, never committed to repo
- ✅ **HTTPS**: TLS/SSL enforced in production (Ingress)

### Infrastructure Security

- ✅ **Container Scanning**: Trivy scans for vulnerabilities
- ✅ **Secret Scanning**: TruffleHog checks for leaked secrets
- ✅ **Least Privilege**: Non-root user in Docker containers
- ✅ **Network Policies**: Kubernetes network isolation
- ✅ **Resource Limits**: CPU/Memory limits prevent DoS
- ✅ **Health Checks**: Automated health monitoring

### CI/CD Security

- ✅ **Branch Protection**: Main branch requires PR reviews
- ✅ **Test Requirements**: All tests must pass before merge
- ✅ **Code Coverage**: Minimum 80% coverage required
- ✅ **Security Scans**: Automated vulnerability scanning
- ✅ **Manual Approval**: Production deploys require approval
- ✅ **Staging First**: Changes deployed to staging before production

## Security Checklist for Contributors

Before submitting a PR:

- [ ] No secrets or credentials in code
- [ ] All tests pass
- [ ] Security scan passes
- [ ] Dependencies are up to date
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't include sensitive data

## Dependency Updates

We use Dependabot to keep dependencies up to date and patch security vulnerabilities automatically.

## Security Audits

- Regular security audits are performed quarterly
- Penetration testing is conducted annually
- All findings are addressed within 30 days
