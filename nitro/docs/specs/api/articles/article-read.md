# Article read
<!-- Read ../../index.md first. After changing this document, add an entry to ../../log.md -->

## Purpose
This document owns GET /api/articles/:slug, which returns one article with its full body, and the article not found response that every endpoint addressing an article by slug shares. The fields are owned by [Article object](../article-object.md). The endpoint allows anonymous viewers as described in [Authentication token](../authentication-token.md).

## Current behavior
- The server looks up the article whose slug equals the path segment exactly.
- If the article exists, the server responds with status 200 and {"article": <article object>} with every field.
- If the viewer is anonymous, favorited and the author's following are false.
- If no article has the slug, the server responds with status 404 and {"errors": {"article": ["not found"]}}.

## Flow
None

## Policies
### Article not found response
When no article has the requested slug, the article read, update, delete, favorite and unfavorite endpoints and the comment list, creation and deletion endpoints respond with status 404 and {"errors": {"article": ["not found"]}}. The slug match is exact and case-sensitive. No test covers this response.
[needs confirmation] Is 404 with article "not found" the intended response for every endpoint that addresses an article by slug?

## Evidence
- `server/routes/api/articles/[slug]/index.get.ts` — finds the article by slug, returns it or 404, and allows anonymous viewers
- `server/utils/article.mapper.ts` — builds the returned article object for the viewer

## Open questions
- [needs confirmation] [Article not found response](#article-not-found-response) — Is 404 with article "not found" the intended response for every endpoint that addresses an article by slug?

## Related
- [Articles API overview](overview.md)
- [Article object](../article-object.md)
- [Article update](article-update.md)
- [Article deletion](article-delete.md)
- [Article favorite and unfavorite](article-favorite.md)
- [Comment list](../comments/comment-list.md)
- [Comment creation](../comments/comment-create.md)
- [Comment deletion](../comments/comment-delete.md)
- [Authentication token](../authentication-token.md)
