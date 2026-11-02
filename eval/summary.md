# Summary

## Suite rows (excluding 3 rows)

| | nitro | django |
|---|---|---|
| scored rows | 130 | 130 |
| correct | 125 | 116 |
| partial | 5 | 14 |
| wrong | 0 | 0 |
| missing | 0 | 0 |
| correct while relying on a [needs confirmation] statement | 12 | 32 |

## Policies

| | nitro | django |
|---|---|---|
| policies | 51 | 91 |
| confirmed | 6 | 50 |
| question | 45 | 41 |
| supported: yes | 50 | 85 |
| supported: partly | 1 | 6 |
| supported: no | 0 | 0 |
| asserted by the suite (in_suite yes) | 31 | 52 |
| questions asserted by the suite | 29 | 12 |

## Excluded rows

- `errors_auth-04`: nitro `wrong`, Docs say "does not check the email format" (so 201), contradicting expected 422 "is invalid"; code has no format check (server/schemas/user.schema.ts:5), so docs match code and the code itself fails this row. django `partial`, Docs say an invalid email gives 422 but never state the asserted message "is invalid" (and the code actually returns the pydantic text "value is not a valid email address: ...").
- `errors_auth-10`: nitro `wrong`, Docs describe only blank checks and 401 for an unmatched email, never 422 "is invalid" for a malformed email; code has no format check (server/schemas/user.schema.ts:15, server/routes/api/users/login.post.ts:11-45, so it answers 401), so the code itself fails this row. django `missing`, No document mentions a malformed email at login (docs imply 401 credentials invalid for any non-matching email, and a probe of the code, apps/accounts/schemas.py:70-80 + api.py:48-50, returns 401, so this ground-truth row cannot be charged to the docs).
- `errors_auth-15`: nitro `wrong`, Docs say any non-blank email is trimmed and stored (no format check), contradicting expected 422 "is invalid"; code has no format check (server/schemas/user.schema.ts:22), so the code itself fails this row. django `partial`, Invalid email gives 422 as stated, but the asserted message "is invalid" is not documented (code returns odd keys, not errors.email).

## Rows where the two implementations differ

| id | nitro | django |
|---|---|---|
| articles-02 | partial | correct |
| errors_articles-01 | correct | partial |
| errors_articles-03 | correct | partial |
| errors_articles-04 | correct | partial |
| errors_articles-05 | correct | partial |
| errors_articles-06 | correct | partial |
| errors_articles-07 | correct | partial |
| errors_auth-12 | correct | partial |
| errors_auth-13 | correct | partial |
| errors_auth-17 | partial | correct |
| errors_auth-18 | partial | correct |
| errors_auth-20 | partial | correct |
| errors_auth-23 | correct | partial |
| errors_comments-01 | correct | partial |
| errors_comments-02 | correct | partial |
| errors_profiles-02 | correct | partial |
| errors_profiles-03 | correct | partial |
