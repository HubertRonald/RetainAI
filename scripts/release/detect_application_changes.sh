#!/usr/bin/env bash

set -Eeuo pipefail

COMPONENT="${1:-}"
ENVIRONMENT="${2:-}"
FORCE_RELEASE="${3:-false}"
HEAD_REF="${4:-HEAD}"
BASE_REF_OVERRIDE="${5:-${RELEASE_BASE_REF:-}}"

case "${COMPONENT}" in
  dashboard|backend|both)
    ;;
  *)
    printf 'ERROR: component must be dashboard, backend, or both.\n' >&2
    exit 2
    ;;
esac

case "${ENVIRONMENT}" in
  dev|prod)
    ;;
  *)
    printf 'ERROR: environment must be dev or prod.\n' >&2
    exit 2
    ;;
esac

case "${FORCE_RELEASE}" in
  true|false)
    ;;
  *)
    printf 'ERROR: force release must be true or false.\n' >&2
    exit 2
    ;;
esac

git rev-parse --is-inside-work-tree >/dev/null
git rev-parse --verify "${HEAD_REF}^{commit}" >/dev/null

resolve_commit() {
  local ref="$1"

  git rev-parse \
    --verify \
    "${ref}^{commit}"
}

if [[ -n "${BASE_REF_OVERRIDE}" ]]; then
  if ! resolve_commit "${BASE_REF_OVERRIDE}" >/dev/null 2>&1; then
    printf 'ERROR: baseline ref does not resolve to a commit: %s\n' \
      "${BASE_REF_OVERRIDE}" >&2
    exit 2
  fi
fi

is_selected() {
  local candidate="$1"

  [[ "${COMPONENT}" == "${candidate}" || "${COMPONENT}" == "both" ]]
}

latest_non_deployment_tag() {
  {
    git tag \
      --list 'v[0-9]*' \
      --sort=-version:refname

    git tag \
      --list 'RetainAI-v[0-9]*' \
      --sort=-version:refname
  } \
    | awk 'NF && !seen[$0]++' \
    | head -n 1
}

baseline_for() {
  local candidate="$1"
  local marker_pattern="deploy-${candidate}-${ENVIRONMENT}-*"
  local marker
  local fallback

  if [[ -n "${BASE_REF_OVERRIDE}" ]]; then
    resolve_commit "${BASE_REF_OVERRIDE}"
    return 0
  fi

  marker="$(
    git tag \
      --list "${marker_pattern}" \
      --sort=-creatordate \
      | head -n 1
  )"

  if [[ -n "${marker}" ]]; then
    resolve_commit "${marker}"
    return 0
  fi

  fallback="$(latest_non_deployment_tag)"

  if [[ -n "${fallback}" ]]; then
    resolve_commit "${fallback}"
    return 0
  fi

  git rev-list \
    --max-parents=0 \
    "${HEAD_REF}" \
    | tail -n 1
}

is_eligible_dashboard_path() {
  local path="$1"

  case "${path}" in
    apps/dashboard/*|\
    services/dashboard/*|\
    .streamlit/*|\
    src/retainai/*|\
    modules/classification/*|\
    modules/dashboard/*|\
    modules/eda/*|\
    modules/explainability/*|\
    modules/io/*|\
    modules/mlops/*|\
    modules/preprocessing/*|\
    modules/security/*|\
    modules/survival/*|\
    configs/*|\
    requirements/*|\
    pyproject.toml|\
    tox.ini|\
    .dockerignore|\
    scripts/release/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_eligible_backend_path() {
  local path="$1"

  case "${path}" in
    apps/api/*|\
    services/api-lambda/*|\
    src/retainai/*|\
    modules/classification/*|\
    modules/data_lake/*|\
    modules/explainability/*|\
    modules/io/*|\
    modules/mlops/*|\
    modules/preprocessing/*|\
    modules/rag/*|\
    modules/security/*|\
    modules/survival/*|\
    configs/*|\
    requirements/*|\
    pyproject.toml|\
    tox.ini|\
    .dockerignore|\
    scripts/release/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

write_output() {
  local name="$1"
  local value="$2"

  printf '%s=%s\n' "${name}" "${value}"

  if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    printf '%s=%s\n' "${name}" "${value}" \
      >> "${GITHUB_OUTPUT}"
  fi
}

write_multiline_summary() {
  local title="$1"
  local body="$2"

  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    {
      printf '### %s\n\n' "${title}"
      printf '```text\n%s\n```\n\n' "${body}"
    } >> "${GITHUB_STEP_SUMMARY}"
  fi
}

DASHBOARD_BASE="$(baseline_for dashboard)"
BACKEND_BASE="$(baseline_for backend)"

DASHBOARD_CHANGED=false
BACKEND_CHANGED=false

DASHBOARD_FILES=""
BACKEND_FILES=""

while IFS= read -r path; do
  [[ -n "${path}" ]] || continue

  if is_eligible_dashboard_path "${path}"; then
    DASHBOARD_CHANGED=true
    DASHBOARD_FILES+="${path}"$'\n'
  fi
done < <(
  git diff \
    --name-only \
    "${DASHBOARD_BASE}..${HEAD_REF}"
)

while IFS= read -r path; do
  [[ -n "${path}" ]] || continue

  if is_eligible_backend_path "${path}"; then
    BACKEND_CHANGED=true
    BACKEND_FILES+="${path}"$'\n'
  fi
done < <(
  git diff \
    --name-only \
    "${BACKEND_BASE}..${HEAD_REF}"
)

DEPLOY_DASHBOARD=false
DEPLOY_BACKEND=false

if is_selected dashboard; then
  if [[ "${FORCE_RELEASE}" == "true" || "${DASHBOARD_CHANGED}" == "true" ]]; then
    DEPLOY_DASHBOARD=true
  fi
fi

if is_selected backend; then
  if [[ "${FORCE_RELEASE}" == "true" || "${BACKEND_CHANGED}" == "true" ]]; then
    DEPLOY_BACKEND=true
  fi
fi

write_output dashboard_base "${DASHBOARD_BASE}"
write_output backend_base "${BACKEND_BASE}"
write_output dashboard_changed "${DASHBOARD_CHANGED}"
write_output backend_changed "${BACKEND_CHANGED}"
write_output deploy_dashboard "${DEPLOY_DASHBOARD}"
write_output deploy_backend "${DEPLOY_BACKEND}"

if [[ -n "${DASHBOARD_FILES}" ]]; then
  write_multiline_summary \
    "Dashboard-eligible changes" \
    "${DASHBOARD_FILES%$'\n'}"
fi

if [[ -n "${BACKEND_FILES}" ]]; then
  write_multiline_summary \
    "Backend-eligible changes" \
    "${BACKEND_FILES%$'\n'}"
fi

if [[ "${DEPLOY_DASHBOARD}" != "true" && "${DEPLOY_BACKEND}" != "true" ]]; then
  printf '%s\n' \
    'No selected component has eligible application changes.' \
    'Documentation, figures, and Markdown do not qualify by themselves.'
fi
