## 1. OpenSpec setup

- [x] 1.1 Run `npm install --save-dev @fission-ai/openspec@latest`
- [x] 1.2 Run `npx openspec init --tools cursor`
- [x] 1.3 Add `npm run build` script validating specs

## 2. Vision document

- [x] 2.1 Create `openspec/project.md` with What This Is, Tech Stack, Non-Negotiables, Out of Scope, Capabilities index

## 3. Baseline capability specs

- [x] 3.1 `openspec/specs/agent-dispatch/spec.md`
- [x] 3.2 `openspec/specs/build-loop/spec.md`
- [x] 3.3 `openspec/specs/spec-conversation/spec.md`
- [x] 3.4 `openspec/specs/idea-generation/spec.md`
- [x] 3.5 `openspec/specs/routines/spec.md`
- [x] 3.6 `openspec/specs/shared-conventions/spec.md`
- [x] 3.7 `openspec/specs/integrations/spec.md`
- [x] 3.8 `openspec/specs/visual-qa/spec.md`
- [x] 3.9 `openspec/specs/design-reference/spec.md`

## 4. Validation

- [x] 4.1 All specs pass `openspec validate --specs`
- [x] 4.2 `npm run build` exits 0
