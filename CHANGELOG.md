# Changelog

All notable RetainAI changes are documented here.

## [Unreleased]

### Planned

- GitHub Actions with short-lived cloud identity federation.
- Monitoring, validation reports, and drift detection.
- English and Spanish internationalization.

## [0.4.0] - 2026-07-20

### Added

- Cloud Run dashboard with branded managed HTTPS.
- API Gateway HTTP API with branded managed HTTPS.
- AWS Lambda container backend.
- Terraform infrastructure for AWS and GCP.
- GCP Secret Manager integration.
- Server-side bearer-token authentication.
- DynamoDB-backed request quotas.
- Cloud Run service and revision scaling guards.
- Decoupled dashboard image deployment.
- Domain-oriented product and engineering documentation.

### Changed

- Standardized active infrastructure management on Terraform.
- Changed the dashboard API contract to
  `https://api.retainai.hubertronald.dev`.
- Separated application delivery from infrastructure delivery.
- Reframed the roadmap around product capabilities and releases.
- Defined a provider-neutral path for Gemini and Amazon Bedrock.
- Added bilingual architecture as a pre-v1.0 requirement.

### Removed

- External dashboard load-balancer infrastructure.
- Pulumi from active infrastructure documentation.
- Temporary iteration-plan documents from active documentation.
- Unsupported psychometric commitments from v1.0.

### Security

- AI providers remain disabled by default.
- Backend secrets remain outside browser code.
- Cloud Run is bounded to zero minimum and one maximum instance.
- Protected requests require authentication and quota allowance.

Earlier implementation history remains available in Git.
