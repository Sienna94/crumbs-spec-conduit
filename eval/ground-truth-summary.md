# RealWorld Hurl 기준 체크리스트 요약

- 입력 파일 수: 13
- 전체 요청 블록: 154
- behavior 블록: 130
- setup 블록: 24

## 파일별 behavior 블록 수

| 파일 | behavior 수 |
| --- | ---: |
| articles.hurl | 16 |
| auth.hurl | 20 |
| comments.hurl | 10 |
| errors_articles.hurl | 17 |
| errors_auth.hurl | 20 |
| errors_authorization.hurl | 8 |
| errors_comments.hurl | 7 |
| errors_profiles.hurl | 5 |
| favorites.hurl | 6 |
| feed.hurl | 9 |
| pagination.hurl | 4 |
| profiles.hurl | 7 |
| tags.hurl | 1 |
| **합계** | **130** |

## 상태 코드별 behavior 블록 수

| HTTP 상태 | behavior 수 |
| --- | ---: |
| 200 | 58 |
| 201 | 20 |
| 204 | 3 |
| 401 | 13 |
| 403 | 3 |
| 404 | 14 |
| 409 | 2 |
| 422 | 17 |
| **합계** | **130** |

## 파서 경고

- auth.hurl:198: 바로 위 주석이 없어 제목이 비어 있음 (PUT /api/user)
- comments.hurl:94: 바로 위 주석이 없어 제목이 비어 있음 (POST /api/articles/{{slug}}/comments)
- errors_articles.hurl:124: 바로 위 주석이 없어 제목이 비어 있음 (POST /api/articles)
- errors_articles.hurl:189: 바로 위 주석이 없어 제목이 비어 있음 (DELETE /api/articles/{{slug2}})
- errors_auth.hurl:175: 주석이 빈 줄로 요청과 떨어져 제목에 연결되지 않음: === NIST 800-63B password policy for PUT /user === / Ref: https://pages.nist.gov/800-63-3/sp800-63b.html section 5.1.1.2 / Rules: min 8 chars, must accept at least 64 chars, no composition, no breach check (demo)
- errors_comments.hurl:31: 바로 위 주석이 없어 제목이 비어 있음 (POST /api/articles)
- feed.hurl:122: 바로 위 주석이 없어 제목이 비어 있음 (DELETE /api/articles/{{slug2}})
- pagination.hurl:66: 바로 위 주석이 없어 제목이 비어 있음 (DELETE /api/articles/{{slug2}})
