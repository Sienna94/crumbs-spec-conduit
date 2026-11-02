# Authentication token
<!-- Read ../index.md first. After changing this document, add an entry to ../log.md -->

## Purpose
This document owns how a client proves its identity on API requests: how the server issues a token, which Authorization header forms it accepts, how endpoints that require authentication differ from endpoints that allow anonymous viewers, and how the server rejects missing, expired and invalid tokens. Each endpoint document states which authentication mode it uses and links here. The error body shape is owned by [HTTP transport and error responses](http-transport.md#json-error-body-format).

## Current behavior
### Token issuance
- When registration, login, current user read or current user update succeeds, the server returns a newly issued token in the user.token field of the response.
- The token is a JSON Web Token (JWT) that the server signs with the secret in the JWT_SECRET environment variable.
- The token carries the user's numeric id and expires 60 days after it is issued.
- The server keeps no record of issued tokens, so a token stays valid until it expires.

### Presenting the token
- A client sends the token in the Authorization header as "Token <jwt>" or as "Bearer <jwt>".
- If the Authorization header is absent, uses another scheme, or has nothing after the scheme, the server treats the request as carrying no token.

### Endpoints that require authentication
- If an endpoint requires authentication and the request carries no token, the server responds with status 401 and {"errors": {"token": ["is missing"]}}.
- If the request carries a token, the server verifies it and processes the request as the user whose id the token holds.

### Endpoints that allow anonymous viewers
- If an endpoint allows anonymous viewers and the request carries no token, the server processes the request as an anonymous viewer.
- If an endpoint allows anonymous viewers and the request carries a token, the server verifies the token in the same way as on endpoints that require authentication.
- An expired or invalid token on such an endpoint is rejected with status 401; the server does not fall back to an anonymous viewer.

### Token verification
- If the token is valid, the server uses the user id it holds.
- If the token has expired, the server responds with status 401 and {"errors": {"token": ["has expired"]}}.
- If the token is malformed or was signed with a different secret, the server responds with status 401 and {"errors": {"token": ["is invalid"]}}.
- If the JWT_SECRET environment variable is not set, issuing and verifying tokens both fail, and the response falls to [Unhandled server error response](http-transport.md#unhandled-server-error-response).

## Flow
The table shows the result for each combination of endpoint mode and token state.

| Token state | Endpoint requires authentication | Endpoint allows anonymous viewers |
| --- | --- | --- |
| No token or unsupported scheme | 401 token "is missing" | Processed as anonymous viewer |
| Valid token | Processed as the token's user | Processed as the token's user |
| Expired token | 401 token "has expired" | 401 token "has expired" |
| Malformed token or wrong secret | 401 token "is invalid" | 401 token "is invalid" |

A request reaches the endpoint only with a valid token or, on endpoints that allow anonymous viewers, with no token at all.

## Policies
### Valid token identifies the user
When a request carries a token that the server's secret verifies and that has not expired, the server identifies the request as the user whose numeric id the token holds.

### Expired token rejection
When a request carries a token whose expiry time has passed, the server rejects it with status 401 and {"errors": {"token": ["has expired"]}}.

### Invalid token rejection
When a request carries a token that is not a well-formed JWT, or that was signed with a secret other than the server's, the server rejects it with status 401 and {"errors": {"token": ["is invalid"]}}.

### Token signing secret is required
The server signs and verifies tokens with the value of the JWT_SECRET environment variable. If the variable is not set, the server raises the error "JWT_SECRET environment variable is not set" instead of issuing or verifying a token.

### Accepted Authorization header schemes
The server reads a token from the Authorization header only when the header starts with exactly "Token" or "Bearer" followed by a space and the token. The scheme comparison is case-sensitive, and any other header value counts as no token.
[needs confirmation] Is accepting both "Token" and "Bearer" intended, and should the scheme comparison be case-insensitive?

### Missing token rejection
When an endpoint requires authentication and the request carries no token, the server rejects it with status 401 and {"errors": {"token": ["is missing"]}}. No test covers this response.
[needs confirmation] Is 401 with token "is missing" the intended response when a required token is absent?

### Invalid token on endpoints that allow anonymous viewers
When an endpoint allows anonymous viewers and the request carries an expired or invalid token, the server rejects the request with status 401 instead of serving it to an anonymous viewer.
[needs confirmation] Should an expired or invalid token on an endpoint that allows anonymous viewers be rejected, or should the request continue as an anonymous viewer?

### Token lifetime
Every issued token expires 60 days after issue, and the server issues a fresh token with a new 60-day lifetime on registration, login, current user read and current user update. The server cannot revoke a token before it expires.
[needs confirmation] What is the basis of the 60-day lifetime, and is it acceptable that tokens cannot be revoked, for example after a password change?

## Evidence
- `server/auth-event-handler.ts` — reads the Authorization header, enforces required authentication and passes the verified user id or an anonymous viewer to the endpoint
- `server/utils/generate-token.ts` — issues a token holding the user id with a 60-day expiry
- `server/utils/verify-token.ts` — verifies a token and maps expired and invalid tokens to 401 errors
- `server/utils/jwt-secret.ts` — reads the signing secret and fails when it is not set
- `server/utils/verify-token.test.ts` — tests that a valid token yields the user id, that expired, malformed and wrongly signed tokens yield 401 with "has expired" or "is invalid", and that a missing secret raises an error

## Open questions
- [needs confirmation] [Accepted Authorization header schemes](#accepted-authorization-header-schemes) — Is accepting both "Token" and "Bearer" intended, and should the scheme comparison be case-insensitive?
- [needs confirmation] [Missing token rejection](#missing-token-rejection) — Is 401 with token "is missing" the intended response when a required token is absent?
- [needs confirmation] [Invalid token on endpoints that allow anonymous viewers](#invalid-token-on-endpoints-that-allow-anonymous-viewers) — Should an expired or invalid token on an endpoint that allows anonymous viewers be rejected, or should the request continue as an anonymous viewer?
- [needs confirmation] [Token lifetime](#token-lifetime) — What is the basis of the 60-day lifetime, and is it acceptable that tokens cannot be revoked, for example after a password change?

## Related
- [API overview](overview.md)
- [HTTP transport and error responses](http-transport.md)
- [User registration](users/registration.md)
- [User login](users/login.md)
- [Current user read](users/current-user.md)
- [Current user update](users/current-user-update.md)
- [Profile lookup](profiles/profile-lookup.md)
- [Profile follow and unfollow](profiles/profile-follow.md)
- [Article list](articles/article-list.md)
- [Article feed](articles/article-feed.md)
- [Article read](articles/article-read.md)
- [Article creation](articles/article-create.md)
- [Article update](articles/article-update.md)
- [Article deletion](articles/article-delete.md)
- [Article favorite and unfavorite](articles/article-favorite.md)
- [Tag list](articles/tag-list.md)
- [Comment list](comments/comment-list.md)
- [Comment creation](comments/comment-create.md)
- [Comment deletion](comments/comment-delete.md)
