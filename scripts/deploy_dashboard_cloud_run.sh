#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="${ROOT_DIR:-/workspace}"
GCP_PROJECT_ID="${GCP_PROJECT_ID:-coplayground}"
GCP_REGION="${GCP_REGION:-us-east4}"
CLOUD_RUN_SERVICE="${CLOUD_RUN_SERVICE:-retainai-dashboard}"
ARTIFACT_REPOSITORY="${ARTIFACT_REPOSITORY:-retainai-dashboard}"
IMAGE_NAME="${IMAGE_NAME:-retainai-dashboard}"
DASHBOARD_DOCKERFILE="${DASHBOARD_DOCKERFILE:-${ROOT_DIR}/services/dashboard/Dockerfile}"
DASHBOARD_BUILD_CONTEXT="${DASHBOARD_BUILD_CONTEXT:-${ROOT_DIR}}"
IMAGE_TAG="${IMAGE_TAG:-$(git -C "${ROOT_DIR}" rev-parse --short=12 HEAD)}"
IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"

printf '\n=== RetainAI dashboard application deployment ===\n'
printf 'IMAGE_URI=%s\n' "${IMAGE_URI}"
printf 'DOCKERFILE=%s\n' "${DASHBOARD_DOCKERFILE}"
printf 'BUILD_CONTEXT=%s\n\n' "${DASHBOARD_BUILD_CONTEXT}"

if [[ ! -f "${DASHBOARD_DOCKERFILE}" ]]; then
  printf 'ERROR: dashboard Dockerfile not found: %s\n' "${DASHBOARD_DOCKERFILE}" >&2
  printf 'Available Dockerfiles:\n' >&2
  find "${ROOT_DIR}" -maxdepth 6 -name Dockerfile -print >&2 || true
  exit 2
fi

if ! grep -Rq \
  'template\[0\]\.containers\[0\]\.image' \
  "${ROOT_DIR}/infra/gcp-terraform"; then
  printf 'ERROR: Terraform does not appear to ignore the Cloud Run image field.\n' >&2
  printf 'Application deployment could be reverted by a later Terraform apply.\n' >&2
  exit 3
fi

gcloud auth configure-docker \
  "${GCP_REGION}-docker.pkg.dev" \
  --quiet

docker build \
  --platform linux/amd64 \
  --file "${DASHBOARD_DOCKERFILE}" \
  --tag "${IMAGE_URI}" \
  "${DASHBOARD_BUILD_CONTEXT}"

docker push "${IMAGE_URI}"

gcloud run services update \
  "${CLOUD_RUN_SERVICE}" \
  --project="${GCP_PROJECT_ID}" \
  --region="${GCP_REGION}" \
  --image="${IMAGE_URI}" \
  --max=1 \
  --quiet

printf '\n=== Deployed Cloud Run revision ===\n'

gcloud run services describe \
  "${CLOUD_RUN_SERVICE}" \
  --project="${GCP_PROJECT_ID}" \
  --region="${GCP_REGION}" \
  --format='yaml(
    metadata.name,
    status.url,
    status.latestReadyRevisionName,
    spec.template.spec.containers[0].image,
    metadata.annotations,
    spec.template.metadata.annotations
  )'

printf '\nApplication deployment completed.\n'
printf 'Terraform infrastructure was not applied by this script.\n'
