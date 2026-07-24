#!/usr/bin/env bash
# Archive completed OpenSpec changes after merge to main.
# See agents/shared/conventions.md and agents/spec-drift.md step 12.
set -euo pipefail

MODE="from-push"
DRY_RUN=false
BASE_SHA=""
HEAD_SHA=""

usage() {
  cat <<'EOF'
Usage: archive-merged-openspec-changes.sh [--from-push | --sweep] [--dry-run]
       archive-merged-openspec-changes.sh --from-push --base <sha> --head <sha> [--dry-run]

Modes:
  --from-push   Archive completed changes touched in a push to main (default).
                Uses HEAD~1..HEAD unless --base/--head are set (GitHub Actions).
  --sweep       Archive any completed active change with no open PR (weekly backup).

Options:
  --dry-run     Report actions without archiving or committing.
  --base SHA    Start of diff range (optional, for CI).
  --head SHA    End of diff range (optional, for CI; default HEAD).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-push) MODE="from-push" ;;
    --sweep) MODE="sweep" ;;
    --dry-run) DRY_RUN=true ;;
    --base) BASE_SHA="${2:-}"; shift ;;
    --head) HEAD_SHA="${2:-}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

if [[ -z "$HEAD_SHA" ]]; then
  HEAD_SHA="$(git rev-parse HEAD)"
fi

if [[ "$MODE" == "from-push" && -z "$BASE_SHA" ]]; then
  if git rev-parse --verify "${HEAD_SHA}^" >/dev/null 2>&1; then
    BASE_SHA="${HEAD_SHA}^"
  else
    echo "skip: no parent commit to diff against"
    exit 0
  fi
fi

extract_change_names_from_paths() {
  local paths="$1"
  echo "$paths" | grep -E '^openspec/changes/[^/]+/' | grep -v '^openspec/changes/archive/' \
    | sed -E 's|^openspec/changes/([^/]+)/.*|\1|' | sort -u
}

changed_paths_in_push() {
  git diff --name-only "$BASE_SHA" "$HEAD_SHA"
}

is_change_complete() {
  local name="$1"
  npx openspec list --json | jq -e --arg name "$name" \
    '.changes[] | select(.name == $name and .status == "complete")' >/dev/null
}

has_open_pr_for_change() {
  local change="$1"
  if ! command -v gh >/dev/null 2>&1; then
    echo "warn: gh not available; skipping open-PR check for $change" >&2
    return 1
  fi

  local repo="${GITHUB_REPOSITORY:-}"
  if [[ -z "$repo" ]]; then
    repo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
  fi
  if [[ -z "$repo" ]]; then
    echo "warn: could not resolve GitHub repo; skipping open-PR check for $change" >&2
    return 1
  fi

  local count
  count="$(gh search prs --repo "$repo" --state open \
    "path:openspec/changes/${change}/" --json number -q 'length' 2>/dev/null || echo 0)"
  [[ "$count" -gt 0 ]]
}

change_older_than_hours() {
  local change="$1"
  local hours="$2"
  local dir="openspec/changes/$change"
  [[ -d "$dir" ]] || return 1
  local now_ts dir_ts age_hours
  now_ts="$(date +%s)"
  dir_ts="$(date -r "$dir" +%s)"
  age_hours=$(( (now_ts - dir_ts) / 3600 ))
  (( age_hours >= hours ))
}

archive_change() {
  local name="$1"
  local reason="$2"

  if ! is_change_complete "$name"; then
    echo "skip: $name ($reason) — not complete or not active"
    return 0
  fi

  if $DRY_RUN; then
    echo "would archive $name ($reason)"
    return 0
  fi

  echo "archiving $name ($reason)"
  if npx openspec archive "$name" -y --skip-specs; then
    return 0
  fi
  echo "skip: could not archive $name (may already be archived)" >&2
  return 0
}

collect_from_push() {
  local paths names
  paths="$(changed_paths_in_push)"
  names="$(extract_change_names_from_paths "$paths")"
  if [[ -z "$names" ]]; then
    return 0
  fi
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    archive_change "$name" "touched in push ${BASE_SHA:0:7}..${HEAD_SHA:0:7}"
  done <<< "$names"
}

collect_from_sweep() {
  local names name
  names="$(npx openspec list --json | jq -r '.changes[] | select(.status == "complete") | .name')"
  if [[ -z "$names" ]]; then
    echo "sweep: no completed active changes"
    return 0
  fi

  while IFS= read -r name; do
    [[ -n "$name" ]] || continue

    if has_open_pr_for_change "$name"; then
      echo "skip: $name — open PR still references this change"
      continue
    fi

    if ! change_older_than_hours "$name" 24; then
      echo "skip: $name — younger than 24h (possible in-flight build)"
      continue
    fi

    archive_change "$name" "weekly sweep orphan"
  done <<< "$names"
}

case "$MODE" in
  from-push) collect_from_push ;;
  sweep) collect_from_sweep ;;
  *) echo "error: unknown mode $MODE" >&2; exit 1 ;;
esac

echo "archive script complete (mode=$MODE, dry_run=$DRY_RUN)"
