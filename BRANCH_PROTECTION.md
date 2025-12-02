# Branch Protection Rules

This document outlines the required branch protection rules for this repository.

## Main Branch Protection

Configure these settings in GitHub: Settings → Branches → Add rule for `main`

### Required Settings:

✅ **Require pull request reviews before merging**
- Required approving reviews: 1
- Dismiss stale pull request approvals when new commits are pushed
- Require review from Code Owners

✅ **Require status checks to pass before merging**
- Require branches to be up to date before merging
- Required status checks:
  - `security-scan`
  - `lint`
  - `test`

✅ **Require conversation resolution before merging**

✅ **Require signed commits**

✅ **Include administrators**

✅ **Restrict who can push to matching branches**
- Only allow specific people/teams to push

✅ **Allow force pushes**: ❌ Disabled

✅ **Allow deletions**: ❌ Disabled

## Develop Branch Protection

Configure these settings for `develop` branch:

✅ **Require pull request reviews before merging**
- Required approving reviews: 1

✅ **Require status checks to pass before merging**
- Required status checks:
  - `security-scan`
  - `lint`
  - `test`

✅ **Require conversation resolution before merging**

## Environment Protection Rules

### Staging Environment
- No required reviewers
- Wait timer: 0 minutes
- Deployment branches: `develop` only

### Production Environment
- Required reviewers: 2
- Wait timer: 5 minutes
- Deployment branches: `main` only
- Prevent self-review

## Workflow Permissions

Settings → Actions → General → Workflow permissions:

- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

## Security Settings

Settings → Security → Code security and analysis:

- ✅ Dependency graph: Enabled
- ✅ Dependabot alerts: Enabled
- ✅ Dependabot security updates: Enabled
- ✅ Dependabot version updates: Enabled
- ✅ Code scanning: Enabled (via Trivy)
- ✅ Secret scanning: Enabled
- ✅ Secret scanning push protection: Enabled

## Required Secrets

Add these secrets in Settings → Secrets and variables → Actions:

### Repository Secrets:
- `KUBECONFIG_STAGING` - Base64 encoded kubeconfig for staging
- `KUBECONFIG_PRODUCTION` - Base64 encoded kubeconfig for production
- `CODECOV_TOKEN` - Codecov upload token (optional)

### Environment Secrets:

**Staging:**
- Same as repository secrets

**Production:**
- Same as repository secrets
- Additional production-specific secrets

## Setup Instructions

1. **Enable Branch Protection:**
   ```bash
   # Go to: Settings → Branches → Add rule
   # Branch name pattern: main
   # Apply all settings listed above
   ```

2. **Create Environments:**
   ```bash
   # Go to: Settings → Environments → New environment
   # Create: staging, production
   # Configure protection rules as listed above
   ```

3. **Add Secrets:**
   ```bash
   # Go to: Settings → Secrets and variables → Actions
   # Add all required secrets
   ```

4. **Enable Security Features:**
   ```bash
   # Go to: Settings → Security → Code security and analysis
   # Enable all features listed above
   ```

## Verification

After setup, verify:

- [ ] Cannot push directly to `main`
- [ ] Cannot merge PR without passing tests
- [ ] Cannot merge PR without review
- [ ] Production deploys require manual approval
- [ ] Security scans run on every PR
- [ ] Dependabot creates PRs for updates
