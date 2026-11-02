# Server startup configuration
<!-- Read ../index.md first. After changing this document, add an entry to ../log.md -->

## Purpose
This document owns how an operator configures the server through environment variables when it starts: debug mode, allowed hosts, database selection, and the password hasher. It does not cover the token lifetimes and cross-origin rule, which [API transport, authentication, and errors](../api/transport-and-errors.md) owns.

## Current behavior
### Debug mode
- If the DEBUG environment variable is "true" in any letter case, the server runs in debug mode.
- If DEBUG is unset or has any other value, the server runs without debug mode.

### Accepted host names
- In debug mode the server accepts requests for every host name.
- Without debug mode the server accepts only the host names listed in the ALLOWED_HOSTS environment variable, separated by ";".
- If ALLOWED_HOSTS is unset or empty without debug mode, the server accepts no host name.

### Database selection
- If DATABASE_URL starts with ":memory:" or "file:" and debug mode is on, the server uses SQLite with that value as the database name.
- If DATABASE_URL starts with ":memory:" or "file:" and debug mode is off, the server refuses to start with the message "In-memory SQLite should only be used with DEBUG=True".
- If DATABASE_URL has any other value, the server uses PostgreSQL with the database name, user, password, host, and port read from that URL.
- If DATABASE_URL is unset and debug mode is on, the server uses the SQLite file "db.sqlite3" in the project directory.
- If DATABASE_URL is unset and debug mode is off, the server exits with a message that lists the three ways to configure a database.

### Password hasher
- If USE_FAST_HASHER is "true" in any letter case and debug mode is on, the server hashes passwords with MD5.
- If USE_FAST_HASHER is "true" and debug mode is off, the server refuses to start with the message "USE_FAST_HASHER should only be used with DEBUG=True".
- Otherwise the server hashes passwords with PBKDF2-SHA256.

### Fixed settings
- The secret key that signs data is written in the settings file, not read from the environment.
- The server uses the UTC time zone and the language code "en-us".
- In debug mode the URL configuration also serves media files using the media URL and media root settings, which the settings file does not set.

## Flow
The table shows which database the server uses for each combination of DATABASE_URL and debug mode.

| DATABASE_URL | Debug mode on | Debug mode off |
| --- | --- | --- |
| starts with ":memory:" or "file:" | SQLite with that name | refuses to start |
| any other value | PostgreSQL from the URL | PostgreSQL from the URL |
| unset | SQLite file "db.sqlite3" | exits with a configuration message |

The in-memory and file SQLite options and the MD5 hasher are available only in debug mode; without debug mode only PostgreSQL starts.

## Policies
### Password hashing algorithm
Without debug mode and without the fast hasher, the server stores passwords hashed with PBKDF2-SHA256.

### Database selection by environment
The server chooses SQLite or PostgreSQL from DATABASE_URL and debug mode as the table under "Flow" shows, and exits when neither DATABASE_URL nor debug mode is set.
[needs confirmation] No test covers the database selection; is the table the intended contract, and should a PostgreSQL URL be the only accepted option without debug mode?

### Debug-only development options
The server refuses to start when an in-memory or file SQLite DATABASE_URL or USE_FAST_HASHER is set without debug mode, and with debug mode USE_FAST_HASHER switches the password hasher to MD5.
[needs confirmation] No test covers these guards; are they the intended safety rules, and are there other options that should require debug mode?

### Allowed hosts
In debug mode the server accepts every host name; without it, the server accepts only the names in ALLOWED_HOSTS separated by ";", and none when the variable is empty.
[needs confirmation] No test covers host checking; is accepting no host name when ALLOWED_HOSTS is empty the intended default?

### Secret key source
The secret key is a fixed value in the settings file, marked by a code comment as unsuitable for production.
[needs confirmation] Should the server read the secret key from the environment, and what should happen when it is missing?

### Debug media serving
In debug mode the URL configuration adds media file serving from the media URL and media root settings, and the settings file does not set either value.
[needs confirmation] Is media file serving intended, and if so, which media URL and media root should the settings define?

## Evidence
- `config/settings.py:24-27` — fixed secret key, debug mode from DEBUG, allowed hosts from ALLOWED_HOSTS
- `config/settings.py:87-112` — database selection from DATABASE_URL and debug mode
- `config/settings.py:124-128` — fast MD5 hasher allowed only in debug mode
- `config/settings.py:133-136` — language code and UTC time zone
- `config/urls.py:85-86` — media file serving in debug mode
- `apps/accounts/tests.py:56-57` — PBKDF2-SHA256 hash expected without debug mode and without the fast hasher

## Open questions
- [needs confirmation] [Database selection by environment](#database-selection-by-environment) — No test covers the database selection; is the table the intended contract, and should a PostgreSQL URL be the only accepted option without debug mode?
- [needs confirmation] [Debug-only development options](#debug-only-development-options) — No test covers these guards; are they the intended safety rules, and are there other options that should require debug mode?
- [needs confirmation] [Allowed hosts](#allowed-hosts) — No test covers host checking; is accepting no host name when ALLOWED_HOSTS is empty the intended default?
- [needs confirmation] [Secret key source](#secret-key-source) — Should the server read the secret key from the environment, and what should happen when it is missing?
- [needs confirmation] [Debug media serving](#debug-media-serving) — Is media file serving intended, and if so, which media URL and media root should the settings define?

## Related
- [Operations overview](overview.md)
- [API transport, authentication, and errors](../api/transport-and-errors.md)
- [User registration](../api/accounts/registration.md)
