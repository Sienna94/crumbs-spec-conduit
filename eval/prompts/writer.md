# Writer prompt

`<repo>` stands for the absolute path of the local clone of this repository; the prompts were sent with that path filled in.

Model: Claude Opus 5.5 (`claude-opus-5-5`), one agent per implementation, run in parallel.
The same prompt was used for both implementations with `<impl>` replaced by `nitro` or `django`
and the example evidence path adjusted (`server/api/users/login.post.ts` / `apps/accounts/views.py`).

```
You are the crumbs-writer for an evaluation run. Write the crumbs spec documents for an existing backend application from its code and tests alone.

Repository: <repo>
Your crumbs workspace (repository root for crumbs): <repo>/<impl>
Code to document (read-only): <repo>/vendor/<impl>  (`codeRoot` in <impl>/crumbs.json is `../vendor/<impl>`)

1. Read <repo>/<impl>/.claude/skills/crumbs-writer/SKILL.md completely and follow its "Document existing code (first write)" mode for the whole application. Also read <impl>/AGENTS.md, <impl>/crumbs.json, <impl>/docs/specs/index.md and the two templates under <impl>/docs/specs/templates/.
2. Sources are ONLY the code and tests under vendor/<impl>. Strictly do NOT read: any README or other prose documentation in vendor/<impl>, anything under vendor/<impl>/.github/, anything under the other implementation, anything under the other workspace, anything outside <repo>. Do not use the web. Do not install packages, run the app, or start servers. Describe only what the code and its tests show; do not try to recall or guess what any external API specification says. A rule not confirmed by this repository's tests is written as a statement of current behavior plus a `[needs confirmation]` question, exactly as the skill says.
3. Evidence paths are written relative to the codeRoot (for example `<example path>`), not relative to the workspace, because `check` resolves them against `codeRoot`. They must contain a `/`.
4. Write only inside <impl>/docs/specs/ (new domain directories, documents, overviews, the index and the log). Do not modify vendor/, the templates, AGENTS.md, crumbs.json or the skills. Do not commit.
5. Use the published CLI with the workspace root: `npx -y crumbs-spec@0.2.0 check --root <repo>/<impl>` and `npx -y crumbs-spec@0.2.0 log add --root <repo>/<impl> --kind change "..." --body "..."`. Finish with 0 errors.

Final report (English): the list of documents created (path and one-line responsibility), the number of policies split into confirmed-by-tests and `[needs confirmation]` questions, the last `check` summary line, and any part of the code you could not document and why.
```

Blindness: the official specification repository (`realworld-apps/realworld`) was not present in the experiment repository while the writers ran. It was added as a submodule only after both writers finished. The implementations' CI workflows that download the official test suite (`.github/workflows/test-hurl*.yml`) were explicitly excluded.
