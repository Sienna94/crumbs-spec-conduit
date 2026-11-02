# Profile lookup
<!-- Read ../../index.md first. After changing this document, add an entry to ../../log.md -->

## Purpose
This document owns GET /api/profiles/:username, which returns another user's public profile. Following and unfollowing are owned by [Profile follow and unfollow](profile-follow.md), and the profile fields by [Profile object](../profile-object.md). The endpoint allows anonymous viewers as described in [Authentication token](../authentication-token.md).

## Current behavior
- The server looks up the user whose username equals the path segment exactly.
- If the user exists, the server responds with status 200 and {"profile": <profile object>}.
- If the viewer is anonymous, following is false; if the viewer is signed in, following shows whether the viewer follows the user, as described in [Profile following flag](../profile-object.md#profile-following-flag).
- If no user has the username, the server responds with status 404 and {"errors": {"profile": ["not found"]}}.

## Flow
None

## Policies
### Profile not found response
When no user has the requested username, the profile lookup, follow and unfollow endpoints respond with status 404 and {"errors": {"profile": ["not found"]}}. The username match is exact and case-sensitive. No test covers this response.
[needs confirmation] Is 404 with profile "not found" the intended response, and should the username match ignore letter case?

## Evidence
- `server/routes/api/profiles/[username]/index.get.ts` — finds the user by username, returns the profile or 404, and allows anonymous viewers
- `server/utils/profile.utils.ts` — builds the profile object for the viewer

## Open questions
- [needs confirmation] [Profile not found response](#profile-not-found-response) — Is 404 with profile "not found" the intended response, and should the username match ignore letter case?

## Related
- [Profiles API overview](overview.md)
- [Profile follow and unfollow](profile-follow.md)
- [Profile object](../profile-object.md)
- [Authentication token](../authentication-token.md)
