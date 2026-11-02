# Grader prompt

`<repo>` stands for the absolute path of the local clone of this repository; the prompts were sent with that path filled in.

Model: Claude Sonnet 5.5 (`claude-sonnet-5-5`), one agent per implementation, run after both writers finished.
The writer model (Opus 5.5) did not grade its own output.

```
You are grading spec documents that another model wrote from an implementation's code, against the official RealWorld API test suite. Be strict and literal. Report in English.

Inputs (read-only):
- Ground truth: <repo>/eval/ground-truth.csv. Grade only rows whose `kind` is `behavior` (133 rows). Each row is one request from the official Hurl suite: method, path, auth, body, expected status and the asserted values. The original Hurl files are in <repo>/vendor/realworld/specs/api/hurl/ if you need context for a row.
- Spec documents under test: <repo>/<impl>/docs/specs/ (start at index.md).
- The implementation's code: <repo>/vendor/<impl> (use it only to confirm a suspected error, see below).
- The official spec for context: <repo>/vendor/realworld/specs/api/openapi.yml.
Do not read anything under <repo>/<other>/ or vendor/<other>, and do not read other files in eval/ except ground-truth.csv.

The implementation passes the full official suite, so every ground-truth row describes what the code really does.

Task A. Write <repo>/eval/grading-<impl>.csv with one row per behavior row of the ground truth and these columns:
- `id` (from the ground truth)
- `verdict`, exactly one of:
  - `correct`: the documents state the behavior that leads to this status and every essential asserted value (error field and message text, counts, ordering, presence or absence of a field, values derived from the request). Plain type checks such as isString or isInteger need not be stated, unless the documents contradict them.
  - `partial`: the documents cover this case but leave out or blur at least one essential asserted value. Say which in `note`.
  - `wrong`: the documents state something that contradicts the expected status or an asserted value. Open the code to confirm the documents are wrong (not the ground truth) and cite file:line in `note`.
  - `missing`: no document describes this case.
- `marked`: `confirmed` if the statement you relied on is a plain policy or behavior statement, `question` if it is the statement part of a policy that carries a `[needs confirmation]` marker, `na` for `missing`.
- `doc`: the document path (relative to <impl>/docs/specs/) and heading anchor you relied on, empty for `missing`.
- `note`: one sentence.

Task B. Write <repo>/eval/policies-<impl>.csv with one row per `###` policy heading found under a "Policies" section in any document, columns:
- `doc`, `policy` (heading text), `marked` (`confirmed` or `question`)
- `supported`: `yes` if the code supports the statement as written, `partly` if part of it is wrong or overstated, `no` if the code does not do this (an invented policy). Open the code for every row and cite file:line in `note`.
- `in_suite`: `yes` if any ground-truth behavior row asserts this rule, otherwise `no`.
- `note`: one sentence.

Rules: judge each row independently; do not give credit for something you inferred but the documents do not say; when in doubt between two verdicts, choose the lower one and say why in `note`. Use proper CSV quoting (Python csv module is fine; run python with -I). Do not modify any file other than the two CSVs. Do not commit.

At the end, print counts: verdicts by value, `marked` by value among non-missing rows, policies by `supported` and by `in_suite`, and the five most important `wrong` or `partial` rows with one-line reasons.
```

The Django grader also ran the code in a scratch virtualenv to confirm suspected errors; the Nitro grader only read the code.
