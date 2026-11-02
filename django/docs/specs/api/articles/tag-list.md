# Tag list
<!-- Read ../../index.md first. After changing this document, add an entry to ../../log.md -->

## Purpose
This document owns listing the known tags with GET /api/tags. It does not cover attaching tags to an article, which [Article tag list input](article-create.md#article-tag-list-input) owns, or filtering articles by tag, which [Article list filters](article-list-and-feed.md#article-list-filters) owns.

## Current behavior
- The endpoint is public and does not read the Authorization header.
- The server answers 200 with a "tags" list holding the name of every tag it has stored.
- The list includes a tag even when no article uses it any more, for example after its articles were deleted or retagged.
- The server applies no ordering and no paging to the list.

## Flow
None

## Policies
### Tag list contents
GET /api/tags answers 200 with a "tags" list holding the names of the stored tags.

### Tag list unused tags and order
The list holds every stored tag, including tags that no article uses any more, and the server applies no ordering or paging.
[needs confirmation] Should the list leave out tags that no article uses, and should it have a defined order?

## Evidence
- `apps/articles/api.py:130-132` — tag list endpoint returning every stored tag name
- `apps/articles/models.py:14-18` — tag with a unique name, stored apart from articles
- `apps/articles/tests.py:478-500` — tag list holds the tags of an article

## Open questions
- [needs confirmation] [Tag list unused tags and order](#tag-list-unused-tags-and-order) — Should the list leave out tags that no article uses, and should it have a defined order?

## Related
- [Articles API overview](overview.md)
- [Article creation](article-create.md)
- [Article list and feed](article-list-and-feed.md)
- [Article deletion](article-delete.md)
- [API transport, authentication, and errors](../transport-and-errors.md)
