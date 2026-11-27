# CSS 관리 — Jin-in-Seoul

구조 확인: 2026-11-27(CSS 파일 8개). 아래 캐시 버전 예시는 2026년 10월 14일의 과거 기록이며, 이 문서는 디자인 변경을 승인하지 않는다.

## 보존 및 변경 관리 원칙

1. **기존 `sweater/` 파일 전체와 일기체 조판을 보호한다**(굵은 날짜, 날짜 위아래 여백, 의도적인 줄바꿈, 문단 형식). Sweater에 간접적인 영향을 줄 수 있는 공통 CSS 변경도 제외한다.
2. 모든 문학 작품의 본문, 문단 경계, 제목, 의도적인 빈 줄과 인라인 마크업을 보존한다.
3. 개별 작품이나 언어의 조정에는 필요한 경우 적용 범위가 한정된 스타일시트를 사용하며, 이를 이유로 `assets/style.css` 자체를 변경하지 않는다.
4. 한국어·일본어 산문은 첫 문단을 포함하여 첫 줄 들여쓰기(통상 `1em`)를 유지한다. 영어·프랑스어는 서술 시작 문단을 왼쪽에 맞추고 이후 일반 문단은 `1em` 들여쓰기를 유지한다. 일률적인 문단 들여쓰기 제거를 배제한다.
5. 절 번호 형식을 보존한다. 단편소설의 `<p class="section-number">N</p>`에는 들여쓰기가 없다. 일본어판 `the-basics-of-logic`의 1~5절은 이 마크업을 사용한다.
6. 저장소 전체의 CSS 캐시 키 변경에는 검증된 이유와 영향받는 모든 페이지의 검사가 필요하다. 서로 다른 `?v=` 값은 캐시 키이지 서로 다른 CSS 소스 파일이 아니다.
7. 스타일시트 변경 전 선택자와 HTML을 확인하고 커밋 후 변경된 모든 파일을 재조회한다.

## 스타일시트 적용 범위 (CSS 파일 8개)

| 파일 | 용도 | 변경 영향 |
| --- | --- | --- |
| `assets/style.css` | 사이트 전체 조판, 내비게이션, 제목, 본문 및 작품별 기본 규칙 | **전체; 위험도 높음**, Sweater 포함 |
| `a-dictionary-of-galactic-extinction/ko/entry-common.css` | 은하 멸망 사전 한국어 장의 레이아웃 | 한국어 장 |
| `a-dictionary-of-galactic-extinction/en/entry-common.css` | 영어 장의 레이아웃과 시작 문단 | 영어 장 |
| `a-dictionary-of-galactic-extinction/fr/entry-common.css` | 프랑스어 장의 레이아웃과 시작 문단 | 프랑스어 장 |
| `a-dictionary-of-galactic-extinction/ja/entry-common.css` | 일본어 장의 레이아웃; 첫 줄 들여쓰기 보존 | 일본어 장 |
| `short-stories/latin-first-paragraph.css` | 영어·프랑스어 단편 시작 문단 및 절 번호 다음 첫 문단 | 연결된 영어·프랑스어 단편 페이지만 |
| `childrens-books/latin-first-paragraph.css` | 영어·프랑스어 동화 시작 문단 및 `h2` 다음 첫 문단 | 연결된 영어·프랑스어 동화 페이지만 |
| `scarecrow-distance/latin-first-paragraph.css` | 허수아비 거리 영어·프랑스어 각 장의 시작 문단 | 연결된 영어·프랑스어 1~4장만 |

- 스타일시트 로딩 순서: 공통 CSS를 먼저 연결하고 작품별 CSS를 그 뒤에 연결한다. 라틴 문자 언어 전용 스타일시트는 한국어·일본어 페이지에 적용하지 않는다.

## 과거 캐시 버전 예시 (2026-10-14, 현재 목록이 아님)

- 메인 페이지: `assets/style.css?v=088`
- 단편소설 목록: `assets/style.css?v=046`
- 동화 목록: `assets/style.css?v=049`
- 은하 멸망 사전 본문 예시: `assets/style.css?v=051`, 언어별 CSS `?v=001`
- 동화 본문 예시: `assets/style.css?v=053`, 라틴 문자 언어 전용 CSS `?v=001`
- Sweater 영어 장 예시: `assets/style.css?v=052`

- 모두 **동일한** `assets/style.css` 리소스를 가리킨다. **일괄 교체는 배제한다**. 버전 변경은 캐시를 강제로 갱신하므로 정당한 변경과 함께 수행해야 한다. 검사 스크립트 `scripts/audit_css_links.py`는 페이지를 수정하지 않고 전체 목록을 생성한다.

## 신규 페이지 및 수정 점검 목록

1. 작품, 언어, 정확한 대상 HTML과 영향을 받을 수 있는 페이지를 식별하여 기록한다.
2. `assets/style.css`와 기존 작품별 CSS를 사전에 검토한다.
3. 기존의 적용 범위가 한정된 CSS를 새 인라인 스타일보다 우선한다.
4. 허수아비 거리 영어·프랑스어 1~4장은 `scarecrow-distance/<lang>/chapter-XX/index.html`에서 `../../latin-first-paragraph.css?v=001`을 연결하며 한국어·일본어 장은 변경하지 않는다. 영어·프랑스어 단편은 `short-stories/<slug>/<lang>/index.html`에서 `../../latin-first-paragraph.css?v=001`을 연결한다. 영어·프랑스어 동화는 `childrens-books/` 아래의 이에 해당하는 경로를 사용한다.
5. 은하 멸망 사전 본문은 해당 언어의 `entry-common.css`를 사용한다. 전체 보기 및 개별 장의 특수 형식을 보존한다.
6. 검증은 한국어·일본어 페이지에 라틴 문자 언어 전용 CSS 링크가 없는지, `section-number`와 `h2` 구조가 올바른지를 포함한다.
7. 저장소 최상위에서 `python3 scripts/audit_css_links.py`를 실행하고 경고를 검토하며 변경 전후 영향받는 페이지 수를 비교한다.
8. HTML 변경이 **오직** 의도한 스타일시트 링크 또는 합의한 마크업에 한정되는지 확인하고 커밋 후 변경 파일을 GitHub에서 재조회한다.
9. Sweater는 일괄 변경에서 제외한다. 공통 CSS 변경에는 별도의 명시적 승인과 회귀 검증 계획이 필요하다.

## 충돌 및 중복에 관한 기록

- 공통 스타일시트에는 `.galactic-prose`, `.short-story-prose`, `.children-prose`, `.sweater-prose` 등의 서로 다른 선택자가 의도적으로 존재한다. 이들 클래스에서 유사한 선언이 자동으로 중복인 것은 아니다. 작품 단위의 형식을 분리하고 특수한 콘텐츠를 보호하기 위한 것이다. 라틴 문자 언어 전용 규칙은 의도적으로 `text-indent`만 재정의한다. 유사하다는 이유만으로 해당 규칙을 통합하거나 삭제하지 않는다.

## 관리 결정

- 기존 CSS 파일 8개를 강제 통합 없이 유지한다.
- 공통 CSS를 새로 배포하여 캐시 무효화가 필요해질 때까지 현재 캐시 쿼리 문자열을 유지한다.
- 변경 전 읽기 전용 목록 확인과 대상별 검사를 수행한다. 선택자를 삭제하려면 실제 미사용 여부를 입증해야 한다.
- 모바일 및 시각적 검증은 사이트 운영자가 관리한다.
