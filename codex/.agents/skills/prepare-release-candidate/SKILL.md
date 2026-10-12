---
name: prepare-release-candidate
description: 公開前の点検やリリース候補の仕上げを依頼された場合に、重大な問題を整理・修正し、公開可否と未確認事項を示す。通常制作や単純なデプロイには適用しない。
---

# Prepare Release Candidate

Produce a defensible release decision from the actual product state. Optimize for preventing severe user harm and launch failure, not for adding the most features.

## Define the release boundary

1. Identify the exact artifact, intended audience, release channel, target time, and supported platforms.
2. Read project instructions, current-state documents, recent diffs, and relevant domain skills.
3. Separate audit authority, local-fix authority, and external-release authority.
4. Preserve unrelated changes, publication state, collaborators, data, and credentials.
5. Read [references/release-lenses.md](references/release-lenses.md) and select the applicable checks.

If the request is audit-only, report findings without editing. If it asks to finish or fix the release candidate, implement safe in-scope blockers locally. Use current authorization, including applicable standing instructions, for the exact external action. Resolve any missing target, content, or impact before execution; do not repeat approval already given.

## Establish the candidate

- Record the branch or revision, working-tree state, runtime environment, configuration assumptions, and known unverified dependencies. Verify that the artifact being shown, installed, or released is the same candidate that was tested; a source edit or matching version number alone does not prove installation or runtime reflection.
- Compare public claims, screenshots, documentation, and announcement copy with the behavior actually present.
- Identify the smallest core journey that proves the release promise, plus the most damaging failure paths.
- Prefer a reproducible local or test environment. Keep production checks read-only and minimal unless live mutation is explicitly authorized.

## Audit by severity

Classify every actionable finding:

- **P0 — stop immediately:** destructive behavior, critical security/privacy exposure, unrecoverable data loss, or the product fundamentally cannot operate.
- **P1 — release blocker:** the primary journey fails, common users become stuck, a major platform is broken, claims materially contradict behavior, or rollback/operations are unsafe.
- **P2 — fix if safely achievable:** significant confusion, accessibility or performance problems, weak failure recovery, or visible quality defects that do not block the core journey.
- **P3 — defer deliberately:** low-impact polish, optional features, rare edge cases with safe recovery, and improvements without release risk.

For actionable findings, include enough evidence, impact, and verification for the owner to decide. Add reproduction or rollback detail when it materially changes that decision.

## Fix the candidate

When changes are authorized:

1. Fix P0 and P1 before adding features.
2. Take only short, low-risk P2 fixes that can be verified within the current release window.
3. Keep every change independently understandable and reversible.
4. After a substantial set of fixes, verify the affected core journey. Do not create a per-edit test or QA loop.
5. Avoid broad refactors, schema changes, dependency churn, or visual rewrites unless they are necessary to remove a blocker.

Do not hide a blocker by weakening a test, suppressing an error, removing disclosure, or narrowing supported behavior without making that product decision explicit.

## Verify the candidate

Use the real supported surface and cover, as applicable:

- new-user entry through first value;
- normal returning-user flow;
- empty, loading, partial, offline, permission-denied, and failure recovery states;
- desktop/mobile/VR/controller/browser variants in the stated support boundary;
- authentication, authorization, ownership, input validation, public visibility, privacy, and abuse resistance;
- persistence, migration, backup, rollback, monitoring, capacity, and dependency failure;
- accessibility, performance, console/log health, build, automated tests, and major links;
- announcement, help, policy, screenshots, and product behavior consistency.

Do not claim a visual, gameplay, multiplayer, migration, or production result that was not actually exercised. Check required CI against the candidate revision after push; queued, running, cancelled, or failed checks are not a pass. Treat CI success, deployment success, production behavior, and device checks as separate evidence. Give the exact remaining operation when human validation is required.

## Issue the release decision

Choose exactly one:

- **GO:** no open P0/P1; core journeys and rollback are verified; remaining risks are acceptable and explicit.
- **CONDITIONAL GO:** no open P0; narrowly bounded P1-equivalent uncertainty or operational prerequisites remain, with named owners and checks before release.
- **NO-GO:** any P0, unresolved P1, unverified destructive migration, unsafe rollback, or inability to test the product's main promise.

When a release decision is requested, report the relevant parts of:

1. candidate identity and scope;
2. severity table and fixes made;
3. verification evidence and untested areas;
4. GO / CONDITIONAL GO / NO-GO with rationale;
5. a roughly five-minute human launch checklist;
6. deferred P2/P3 work and rollback/monitoring notes.

Treat the release decision as advice. Execute external release only when current authorization covers it; do not create another approval gate if it already does.
