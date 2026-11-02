<!-- crumbs:start -->
## Spec documents (crumbs)

Spec documents live under `docs/specs/` and describe how the system works now.
Always read `docs/specs/index.md` first. Raw source material under `docs/raw/` is read-only.

Navigation order: index → domain overview → detail document → that document's "Related" section.
Stop as soon as you find the document that owns the answer, and quote it.

Rules when behavior changes:
- Every policy is owned by exactly one detail document. Even if nobody asks you to update the document,
  update it in the same change as the code.
- Describe the current behavior, not the change. Do not add change history or requirement IDs.
- List the code you relied on in the "Evidence" section. Keep links in both directions: detail documents link to the overview
  and related documents, and those documents link back.
- If code, tests, or approved material cannot confirm a policy, write `[needs confirmation]` and a question.
  Do not guess.
- After reflecting new material or changing a document, add an entry to `docs/specs/log.md` in the form
  `## [YYYY-MM-DD] kind | title` (kind: ingest, query, lint, drift, change, decision).
- Before finishing, run `npx crumbs-spec check` and fix every reported error.
<!-- crumbs:end -->
