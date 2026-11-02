# Usage scenario results

## A. Find (Sonnet 5.5, crumbs-finder) — no files changed, no commit
Request: "How many tags does GET /api/tags return, and in what order?"
Answer: at most 10 names, sorted by number of articles using each tag (most used first), only tags used by ≥1 article, no pagination, 200 {"tags": [...]}; same for anonymous/signed-in. Two unconfirmed points: tie order undefined; no basis for 10 (no test).
Source cited: docs/specs/api/articles/tag-list.md > Policies > Popular tag list
Files read: AGENTS.md, .claude/skills/crumbs-finder/SKILL.md, docs/specs/index.md, docs/specs/api/overview.md, docs/specs/api/articles/overview.md, docs/specs/api/articles/tag-list.md (4 spec docs, no code)
Tokens 69,952, tool uses 9, 41 s

## B1. Interview (Sonnet 5.5, crumbs-interview) — no files changed
Request: "I want to change how the tag list is ordered. What do I need to confirm first?"
Output: policy table (confirmed: most-used-first sort, only used tags, same for all viewers; unconfirmed: tie order, 10 cap basis, no pagination, tagList order in articles, scope) + 7 [needs confirmation] questions; stopped and waited. Read 4 spec docs + code/server/routes/api/tags/index.get.ts (+ grep of 3 docs).
Reply was half Korean: subagent inherited the user's global CLAUDE.md "answer in Korean" rule (environment, not crumbs).
Finding: agent thought evidence paths lacked `code/`; nothing in AGENTS block/skills says evidence paths are relative to codeRoot. → crumbs-spec follow-up.
Tokens 76,910, tool uses 13, 44 s
Maintainer answer: keep most-used-first; ties undefined on purpose; 10 cap stays (sidebar), applied after sort; same for all, no pagination; tagList out of scope.

## B2. Decision (same agent, crumbs-writer) — commit 7b86052
tag-list.md: Current behavior +2 bullets (limit after sort; ties undefined; same list, no pagination), Flow None→Mermaid (missing-flow warning fired at 7 steps), policy confirmed with "(decision: [2026-11-03](../../log.md#2026-11-03-decision--popular-tag-list-most-used-first-stays-ties-are-undefined-10-tags-are-cut-after-sorting-and-every-viewer-gets-the-same-unpaginated-list))", Open questions → None.
Log: "## [2026-11-03] decision | Popular tag list: most used first stays, ties are undefined, 10 tags are cut after sorting, and every viewer gets the same unpaginated list" + Result/Reason/Document body.
check caught broken decision link (../log.md → ../../log.md). Final: 28 documents, 0 errors, 20 warnings (was 21).
Agent grepped npm cache for slug rules (outside repo, disclosed).
Tokens 96,831 (cumulative), 28 tool uses, 11 min

## C. Ingest — raw file usage/docs/raw/realworld-b8a37f1-validate-email-format.diff (git show b8a37f1, openapi format: email ×4, errors_auth.hurl +3 requests)
C1 (crumbs-ingest, Sonnet): request "The upstream API spec changed. Apply docs/raw/realworld-b8a37f1-validate-email-format.diff." Read raw, index, api overview, registration/login/current-user-update/users overview/http-transport, code/server/schemas/user.schema.ts, log. Listed claims C1–C4, found conflict (registration.md says no format check; code has none) and asked A (material = contract) vs B (keep current behavior, question). Proposed 8 changes, stopped. 86,644 tokens, 15 tools, 57 s.
Answer: B — keep current behavior, record upstream contract as question in registration (single owner), short links from login/update, raw evidence, ingest log.
C2 applied (B): registration.md new policy "Email format" (current: no check; upstream expects 422 "is invalid"; question), "Registration required fields" lost email clause; login.md & current-user-update.md one link bullet each; evidence `../docs/raw/...diff` (first check: missing-code-path because evidence resolves against codeRoot=code — skill says docs/raw/<file>; crumbs-spec gap). Log: "## [2026-11-03] ingest | The upstream API spec expects 422 with is invalid for a malformed email on registration, login and account update, and the server checks no email format yet". check 28 docs, 0 errors, 20 warnings. 104,079 tokens cumulative, 26 tools, 2.6 min.

## D. Reflect change (crumbs-writer "Reflect a change", Sonnet) — code + docs one commit
Code: user.schema.ts .email('is invalid') ×3 (verified with zod 3.24.4: 1–3 → {"email":["is invalid"]}, blank → ["can't be blank","is invalid"], valid passes).
Found owner by `grep -rl 'user.schema' docs/specs` → registration/login/current-user-update; "Email format" policy confirmed (422 is invalid before hashing/lookup/write; update only when email present); new question policy "Accepted email address forms" (which addresses, does blank also report is invalid — it does); login/update bullets rewritten with link; flows updated in registration & login. Log: "## [2026-11-03] change | A malformed email on registration, login and account update is rejected with 422 and is invalid". check 28/0/20. 19 files read, 103,290 tokens, 11 tools, 1.7 min.
