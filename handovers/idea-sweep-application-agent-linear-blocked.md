# Handover: idea-sweep for Application Agent blocked — Linear MCP unauthorized

**Date:** 2026-10-09
**Blocked on:** Linear MCP requires OAuth in this session; no Linear tools available.

## What could not run
- Issue-cap pre-flight (needs `list_issues` with Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`)
- spec-drift, bug-error, market-feature (all need Linear to dedupe/file)
- spec-drift step 10 stale-issue sweep (needs Linear)
- No sweep ledger line written: a `clean:true` entry would be false, since nothing ran.

## Next step
Re-authorize the Linear connector in claude.ai connector settings, then re-run:
`Run the "idea-sweep" routine for Application Agent.`
