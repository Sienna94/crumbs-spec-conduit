# Spec log

A chronological record of what was done to the documents. The newest entry comes last.
Entry heading: `## [YYYY-MM-DD] kind | title`; kind is one of ingest, query, lint, drift, change, decision.

## [2026-11-02] change | crumbs-spec initialized

## [2026-11-02] change | The API under /api is documented from code and tests, covering transport, authentication, users, profiles, articles and comments
Result: 21 draft detail documents for api, 45 open questions. Reason: first documented from code and tests. Document: [Unique conflict field selection](api/http-transport.md#unique-conflict-field-selection)

## [2026-11-03] decision | Popular tag list: most used first stays, ties are undefined, 10 tags are cut after sorting, and every viewer gets the same unpaginated list
Result: GET /api/tags keeps the most-used-first order, leaves the order of equally used tags undefined, applies the 10-tag limit after sorting, and returns the same list without pagination to every viewer. Reason: answers from the maintainer; existing clients may rely on most-used-first and the limit keeps the tag sidebar short. Document: [Popular tag list](api/articles/tag-list.md#popular-tag-list)

## [2026-11-03] ingest | The upstream API spec expects 422 with is invalid for a malformed email on registration, login and account update, and the server checks no email format yet
Result: the Email format question is open in the registration document; the documents still describe no format check. Reason: docs/raw/realworld-b8a37f1-validate-email-format.diff. Document: [Email format](api/users/registration.md#email-format)
