#!/usr/bin/env bash
# Delete orphaned preview/* branches in AI-Workspace.
# See agents/spec-drift.md step 10 and agents/shared/conventions.md.
set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

if [[ -z "${LINEAR_API_KEY:-}" ]]; then
  echo "error: LINEAR_API_KEY is required" >&2
  exit 1
fi

linear_issue() {
  local identifier="$1"
  local team_key number
  if [[ ! "$identifier" =~ ^([A-Z]+)-([0-9]+)$ ]]; then
    echo "error: invalid issue identifier: $identifier" >&2
    return 1
  fi
  team_key="${BASH_REMATCH[1]}"
  number="${BASH_REMATCH[2]}"

  local query='query($teamKey: String!, $number: Float!) {
    issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
      nodes {
        identifier
        state { type name }
        labels { nodes { name } }
      }
    }
  }'

  local payload
  payload=$(jq -n \
    --arg query "$query" \
    --arg teamKey "$team_key" \
    --argjson number "$number" \
    '{query: $query, variables: {teamKey: $teamKey, number: $number}}')

  curl -sf -X POST https://api.linear.app/graphql \
    -H "Authorization: $LINEAR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

should_delete_branch() {
  local issue_id="$1"
  local version="$2"
  local max_version="$3"

  if (( version < max_version )); then
    echo "older version (v${version} < v${max_version})"
    return 0
  fi

  local response node state_type has_spec_needed
  response=$(linear_issue "$issue_id") || return 1
  node=$(echo "$response" | jq -r '.data.issues.nodes[0] // empty')
  if [[ -z "$node" ]]; then
    echo "issue not found in Linear — keeping branch" >&2
    return 1
  fi

  state_type=$(echo "$node" | jq -r '.state.type')
  case "$state_type" in
    completed|canceled|duplicate)
      echo "issue state is ${state_type}"
      return 0
      ;;
  esac

  has_spec_needed=$(echo "$node" | jq -r '[.labels.nodes[].name] | index("spec-needed") != null')
  if [[ "$has_spec_needed" != "true" ]]; then
    echo "issue no longer labeled spec-needed (state: $(echo "$node" | jq -r '.state.name'))"
    return 0
  fi

  return 1
}

delete_branch() {
  local branch="$1"
  local reason="$2"
  if $DRY_RUN; then
    echo "would delete $branch ($reason)"
  else
    echo "deleting $branch ($reason)"
    git push origin --delete "$branch"
  fi
}

git fetch origin --prune >/dev/null

mapfile -t branches < <(git branch -r --list 'origin/preview/*' | sed 's|^[[:space:]]*origin/||')

declare -A max_version
for branch in "${branches[@]}"; do
  if [[ "$branch" =~ ^preview/([A-Z]+-[0-9]+)-v([0-9]+)$ ]]; then
    issue_id="${BASH_REMATCH[1]}"
    version="${BASH_REMATCH[2]}"
    if [[ -z "${max_version[$issue_id]:-}" ]] || (( version > max_version[$issue_id] )); then
      max_version[$issue_id]=$version
    fi
  fi
done

deleted=0
kept=0
skipped=0

for branch in "${branches[@]}"; do
  if [[ ! "$branch" =~ ^preview/([A-Z]+-[0-9]+)-v([0-9]+)$ ]]; then
    echo "skip: unrecognized branch name $branch" >&2
    ((skipped++)) || true
    continue
  fi

  issue_id="${BASH_REMATCH[1]}"
  version="${BASH_REMATCH[2]}"
  max_v="${max_version[$issue_id]}"

  if reason=$(should_delete_branch "$issue_id" "$version" "$max_v"); then
    delete_branch "$branch" "$reason"
    ((deleted++)) || true
  else
    echo "keep: $branch (issue $issue_id still spec-needed)"
    ((kept++)) || true
  fi
done

if $DRY_RUN; then
  echo "dry-run complete: would delete $deleted, keep $kept, skip $skipped"
else
  echo "cleanup complete: deleted $deleted, kept $kept, skipped $skipped"
fi
