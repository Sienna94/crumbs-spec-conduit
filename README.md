# crumbs-spec-conduit

An open, reproducible experiment for [crumbs-spec](https://github.com/Sienna94/crumbs-spec): can an agent write correct living specs for a codebase from its code and tests alone?

We ran the crumbs-writer skill (crumbs-spec 0.2.0) on two backends of the [RealWorld](https://github.com/realworld-apps/realworld) "Conduit" API and graded the documents against RealWorld's official API test suite.

## Layout

| Path | Content |
|---|---|
| `vendor/nitro` | [nitro-prisma-zod-realworld-example-app](https://github.com/realworld-apps/nitro-prisma-zod-realworld-example-app) @ `c8c6685` (submodule, MIT) |
| `vendor/django` | [realworld-django-ninja](https://github.com/c4ffein/realworld-django-ninja) @ `04ef47c` (submodule, MIT) |
| `vendor/realworld` | [realworld](https://github.com/realworld-apps/realworld) @ `2558884`, the official spec and Hurl suite (submodule, MIT) |
| `nitro/`, `django/` | crumbs workspaces (`codeRoot` points at `vendor/<impl>`); the generated documents are in `docs/specs/` |
| `eval/ground-truth.csv` | One row per request in the official Hurl suite, made by `eval/scripts/hurl_to_checklist.py` |
| `eval/grading-<impl>.csv` | One verdict per behavior row |
| `eval/policies-<impl>.csv` | Every policy in the documents, checked against the code |
| `eval/summary.md` | Totals, made by `eval/scripts/summarize.py` |
| `eval/prompts/` | The writer and grader prompts as sent |
| `eval/timeline.txt` | Start and finish of each agent, tokens and duration |

## Procedure

1. **Blind writing.** One Claude Opus 5.5 agent per implementation followed the crumbs-writer skill's "document existing code" mode. It could read only `vendor/<impl>` code and tests, no README, no CI workflows (they download the official suite), no web. `realworld` was not in the repository yet. The writers' output was committed first (`572b0db`), and the spec was added afterwards (`e23326e`).
2. **Ground truth.** `hurl_to_checklist.py` turns the 13 Hurl files into 157 requests: 133 behavior rows, 24 setup and cleanup rows that are not graded.
3. **Grading.** One Claude Sonnet 5.5 agent per implementation graded every behavior row (`correct`, `partial`, `wrong`, `missing`) and every policy (`supported` yes, partly, no; `in_suite` yes, no). The author checked that every cited document and anchor exists and spot-checked rows.

## Results

| | Nitro + Prisma | Django Ninja |
|---|---|---|
| Documents / policies | 28 / 51 | 26 / 91 |
| Policies confirmed by tests / left as `[needs confirmation]` | 6 / 45 | 50 / 41 |
| Suite rows correct | **125 / 130** | **116 / 130** |
| Partial / wrong / missing | 5 / 0 / 0 | 14 / 0 / 0 |
| Correct on a statement still marked `[needs confirmation]` | 12 | 32 |
| Policies: supported / partly / not supported | 50 / 1 / 0 | 85 / 6 / 0 |
| Writer tokens / wall time | 165k / 2 h 40 min | 202k / 2 h 47 min |

**Excluded rows.** `errors_auth-04`, `errors_auth-10` and `errors_auth-15` test an email-format rule added to the suite on 2026-10-31 (realworld `b8a37f1`). Both implementations were last changed on 2026-05-05 and do not have it, so these rows are left out of the scores. The Nitro documents state that the email format is not checked.

**Where the documents fall short.** Nitro: `null` inputs on user and article update, and whether tags keep request order. Django: twelve rows on the 401 body, where the app's error handler and its tests disagree and the writer left it as a question, plus a password maximum and `tagList: null` on update.

**What the writers raised that no suite row tests** (each written as a question):
- Nitro: the favorite and unfavorite responses spread the whole article record, including the full user rows of everyone who favorited it (email and password hash) — `server/routes/api/articles/[slug]/favorite/index.post.ts`.
- Nitro: the initial migration and `prisma/schema.prisma` disagree (default image, a `demo` column).
- Django: the article list ignores the token and reads the session user, so `favorited` and `following` are false for token clients.
- Django: the `createUser` management command looks users up by a field a migration renamed.

## Limits

- One run per implementation, one writer model, one grader model.
- RealWorld is well known; the writer may have seen it in training even though the spec was not in the repository.
- The suite asserts only part of what the documents say. 20 Nitro and 39 Django policies were checked against code only.
- The Django grader ran the code in a scratch virtualenv with unpinned dependencies (jwtninja 1.1.0); some of its `partly` verdicts may depend on library versions.

## Reproduce

```bash
git clone --recurse-submodules https://github.com/Sienna94/crumbs-spec-conduit.git
cd crumbs-spec-conduit
python3 -I eval/scripts/hurl_to_checklist.py   # regenerates eval/ground-truth.csv
python3 -I eval/scripts/summarize.py           # regenerates eval/summary.md
npx -y crumbs-spec@0.2.0 check --root nitro
npx -y crumbs-spec@0.2.0 check --root django
```

To rerun the writers, delete `<impl>/docs/specs/api` (and `operations` for Django), restore `index.md` and `log.md` from commit `fda78ad`, and send the prompt in `eval/prompts/writer.md`.

## License

MIT for this repository's own files. Each submodule keeps its own license.
