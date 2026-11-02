# Article object
<!-- Read ../index.md first. After changing this document, add an entry to ../log.md -->

## Purpose
This document owns the article object that article endpoints return: its fields, the viewer-dependent favorited flag, the favorites count and the field differences between endpoints. Each endpoint document owns when it returns the object. The embedded author is a [Profile object](profile-object.md).

## Current behavior
### Article fields
- An article object contains slug, title, description, body, tagList, createdAt, updatedAt, favorited, favoritesCount and author.
- tagList is a list of tag names.
- createdAt and updatedAt are timestamps of the article's creation and last update.
- author is the article author's [Profile object](profile-object.md).

### Favorite fields
- If the viewer is signed in and has favorited the article, favorited is true.
- If the viewer is signed in and has not favorited the article, favorited is false.
- If the viewer is anonymous, favorited is false.
- favoritesCount is the number of users who have favorited the article.

### Differences between endpoints
- In article list and feed responses, the object omits body, and the author omits bio.
- In article list responses, tagList is sorted alphabetically; in every other response, tagList follows the stored order.
- Article read, creation and update responses contain every field.
- Favorite and unfavorite responses use a different object, owned by [Article favorite and unfavorite](articles/article-favorite.md#favorite-response-contents).

## Flow
The table shows which fields each endpoint group returns.

| Endpoint group | body | author bio | tagList order | Extra fields |
| --- | --- | --- | --- | --- |
| Article list | Omitted | Omitted | Alphabetical | None |
| Article feed | Omitted | Omitted | Stored order | None |
| Article read, creation, update | Included | Included | Stored order | None |
| Favorite, unfavorite | Included | Included | Stored order | id, authorId, favoritedBy |

The list and feed omit the long text fields, and the favorite responses add internal fields.

## Policies
### Article favorited flag and count
An article object's favorited field is true only when the signed-in viewer is among the users who favorited the article, and it is false for anonymous viewers. favoritesCount is the number of users who favorited the article, whoever the viewer is. No test covers these fields.
[needs confirmation] Is this the intended contract for favorited and favoritesCount?

### Article representation variants
Article list and feed responses omit body and the author's bio, and only the article list sorts tagList alphabetically; article read, creation and update responses include every field and keep the stored tag order.
[needs confirmation] Is omitting body and author bio from list and feed responses intended, and should every endpoint return tagList in the same order?

## Evidence
- `server/utils/article.mapper.ts` — builds the article object, the favorited flag and favoritesCount
- `server/utils/author.mapper.ts` — builds the embedded author profile
- `server/routes/api/articles/index.get.ts` — loads list articles without body and author bio and sorts tags by name
- `server/routes/api/articles/feed.get.ts` — loads feed articles without body and author bio
- `server/routes/api/articles/[slug]/index.get.ts` — loads a single article with every field

## Open questions
- [needs confirmation] [Article favorited flag and count](#article-favorited-flag-and-count) — Is this the intended contract for favorited and favoritesCount?
- [needs confirmation] [Article representation variants](#article-representation-variants) — Is omitting body and author bio from list and feed responses intended, and should every endpoint return tagList in the same order?

## Related
- [API overview](overview.md)
- [Profile object](profile-object.md)
- [Article list](articles/article-list.md)
- [Article feed](articles/article-feed.md)
- [Article read](articles/article-read.md)
- [Article creation](articles/article-create.md)
- [Article update](articles/article-update.md)
- [Article favorite and unfavorite](articles/article-favorite.md)
