# SEO 관리 규정 — Jin-in-Seoul

최종 갱신: 2026-11-26. 저장소: `Jin-in-Seoul/Jin-in-Seoul` (`main`). 공개 사이트: https://jin-in-seoul.com/.

## 적용 범위와 필수 원칙

1. **SEO 관리 시 문학 본문, 번역, 문단 구분, 의도적인 공백, 조판, CSS 및 Sweater의 일기체 레이아웃을 보호한다.** 수정 범위는 검증된 SEO 메타데이터, 사이트맵, robots, 리디렉션 또는 읽기 전용 검사 도구로 한정한다.
2. GitHub Actions 작업의 성공은 모든 실제 URL의 유효성이나 Google/Naver 색인을 입증하지 않는다.
3. 검사 경고는 자동으로 변경을 승인하지 않는다. 수정에 앞서 해당 페이지, Jekyll 생성 방식, 언어판과 의도된 색인 정책을 검토한다.
4. 검증에는 변경된 GitHub 파일의 커밋 후 재조회, Pages 배포 및 관련 검사 보고서가 포함된다.
5. Naver 사이트 인증과 기존 분석 태그를 보존한다.

## 사이트 설정과 SEO 규약

- GitHub Pages / Jekyll. `_config.yml`에 `url: https://jin-in-seoul.com`을 정의하며 Gray Note는 번호가 붙은 HTML 페이지(`/gray-note/001/{lang}/`, `/gray-note/002/`)를 사용한다.
- `robots.txt`는 크롤링을 허용하며 `https://jin-in-seoul.com/sitemap.xml`을 참조한다.
- `sitemap.xml`은 프런트 매터가 있는 Jekyll 템플릿 XML 소스이다. 소스의 Liquid 자리표시자 자체만으로 배포 결과에 오류가 있다고 볼 수 없다.
- Gray Note는 번호가 붙은 폴더 아래 독립 HTML(`gray-note/001/{lang}/index.html`, `gray-note/002/index.html`)을 사용한다. `_posts`에는 Gray Note 게시물이 없다.
- Canonical과 hreflang은 실제로 존재하며 색인 가능한 언어판을 참조한다. 적절한 경우 `x-default`는 통상 영어판을 가리킨다.
- 의도적 `noindex` 페이지에는 전체 보기 및 리디렉션 페이지가 포함된다. 이러한 URL은 사이트맵에서 제외한다.
- 검색 페이지의 메타데이터 경고는 선택적 개선 사항이며 자동으로 오류가 되는 것은 아니다.

## 기술 변경 이력 (2026-10-14)

| 분야 | 변경 | 검증 |
| --- | --- | --- |
| 사이트맵 정리 (1단계) | 오래된 `/short-stories/books-rule/` 항목, 리디렉션 항목 및 소스 사이트맵의 Liquid 문자열 항목 제거 | 소스 재조회; 배포 사이트맵은 별도 확인 필요 |
| 리디렉션 (1단계) | 언어별 부의 메타 리프레시 페이지 6개에 `noindex,follow`를 적용하고 언어별 랜딩 페이지로 canonical 지정; 리디렉션 페이지 hreflang 제거; 프랑스어 HTML lang 수정 | 소스 재조회 |
| 리디렉션 (3단계) | `sweater/index.html`과 `a-dictionary-of-galactic-extinction/index.html`에 `noindex,follow`를 적용하고 영어 도착 페이지로 canonical 지정 | 소스 재조회 |
| 사이트맵 추가 (3단계) | 은하 멸망 사전 한국어 항목 20개 추가(3부 1개, 4부 12개, 5부 7개), 최상위 리디렉션 URL 2개 제거 | 소스 `<loc>` 항목 233개 |
| 소스 검사 | `scripts/audit_seo.py`와 `.github/workflows/seo-audit.yml` 추가; 독립 페이지 검사에서 Jekyll `_includes`, `_layouts` 제외 | 실행 38583032725에서 HTML 240개, 사이트맵 233개, ERROR 0, WARN 1, INFO 2 |
| 실제 사이트 검사 | `scripts/audit_seo_live.py`와 `.github/workflows/seo-live-audit.yml` 추가; 배포 사이트맵을 읽고 공개 URL 검사 | 실제 실행 38584877114: 사이트맵 URL 233개, 233개 모두 HTTP 200, ERROR 0, WARN 1(검색 OG), INFO 1(검색 JSON-LD) |

소스 검사의 남은 WARN 1개와 INFO 2개는 `search/index.html`의 선택적 메타데이터와 관련되었다. 검색 색인 정책의 변경은 별도의 결정이 필요하다.

## 자동 검사 및 보고서

### 소스 SEO 검사
- 실행: 저장소 최상위에서 `python3 scripts/audit_seo.py`.
- 워크플로: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml
- 보고서 아티팩트: `seo-audit-report`에 `seo-audit-report.md` 포함.
- 확인된 소스 검사 성공 실행: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38583032725
- 완전히 렌더링된 Jekyll 결과가 아니라 저장소의 원시 HTML을 검사한다. 소스 경고에는 오탐이 있을 수 있다.

### 공개 사이트 SEO 검사
- 실행: 네트워크에 연결된 환경에서 `python3 scripts/audit_seo_live.py`.
- 워크플로: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-live-audit.yml
- 보고서 아티팩트: `seo-live-report`에 `seo-live-report.md` 포함.
- 검사 스크립트나 워크플로 변경 푸시, Pages 배포 성공 이후 또는 수동 실행으로 작동한다. 최초 푸시로 시작된 검증은 실행 38584877114에서 성공했다.
- 실제 사이트맵, URL 응답, 메타데이터 및 사이트맵 URL 간 hreflang 상호 참조를 검사한다.
- 실제 사이트 검사기는 읽기 전용이다. 실제 Google/Naver 색인을 입증하지 않으며 사이트맵에 없는 URL이 작동하는지도 입증하지 않는다.

### 배포
- GitHub Pages 워크플로: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions
- 3단계 SEO 변경의 Pages 배포 성공: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38583033007
- 이후 실제 검사 문서 관련 Pages 배포: 실행 `38583823275` 성공. 검증은 최신 관련 실행을 기준으로 한다.

## 정기 관리와 검증

1. **2026-10-14 완료:** 실제 검사 실행 [38584877114](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38584877114), 보고서 아티팩트 `11904801736`: 사이트맵 HTTP 200, HTML 233/233개 조회, ERROR 0, WARN 1(`/search/` OG), INFO 1(`/search/` JSON-LD). 검색 페이지의 선택적 사항 2개는 즉각적인 수정이 필요하지 않다.
2. 정기 검증에는 `robots.txt` 및 의도적으로 사이트맵에서 제외한 리디렉션 페이지의 별도 확인이 포함된다. 233개 URL 검사는 사이트맵 URL만을 대상으로 한다.
3. 배포된 canonical/hreflang 상호 참조와 언어 코드를 확인하며 실제 문제와 생성 페이지 및 의도된 예외를 구별한다.
4. Google Search Console 및 Naver Search Advisor 색인·사이트맵 보고서는 **승인된 접근 권한이 있을 때만** 검토한다. GitHub 검사는 검색엔진 계정 데이터를 대신할 수 없다.
5. 수정 후 소스·실제 사이트 검사와 Pages 배포 검증을 수행하며 정확한 커밋 SHA와 결과를 기록한다.

## 변경 기록 원칙

SEO 변경 기록마다 날짜, 변경 파일, 이유, GitHub 커밋, 소스 검사, 실제 사이트 검사 및 Pages 배포 결과를 포함한다. 이 문서는 현재 상태의 참조 자료로 유지하며 검증되지 않은 성공 주장은 제외한다.

관련 문서: [README.md](README.md) · [CSS-MAINTENANCE.md](CSS-MAINTENANCE.md).

## 사이트 품질 검증 (2026-10-14)

읽기 전용 사이트 품질 워크플로: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38585658888
- `scripts/audit_site_quality.py` + `.github/workflows/site-quality-audit.yml`
- 공개 사이트맵 페이지 조회: **233/233**; 고유 내부 링크 대상 **254개**, 자산 **35개**.
- **ERROR 0, WARN 0, INFO 5**. 제목 단계 건너뜀 3건(동화, 음악, 단편소설), 검색 버튼 접근성 이름 검토 1건, 메인 페이지 이미지 PNG 약 1.22MB 1건. 연결이 끊어진 내부 링크 대상이나 누락된 자산은 발견되지 않았다.
- 정적 HTML/HTTP 검사이며 전체 대화형 접근성 검사나 기기 검사는 아니다.

모바일 Lighthouse 워크플로: https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/38585718512
- `.github/workflows/browser-quality-audit.yml`은 헤드리스 Chrome 및 Lighthouse로 대표 공개 페이지 3개를 검사한다.
- 메인 페이지: 성능 **68**, 접근성 **100**, 모범 사례 **100**; FCP 3.8초, LCP 4.6초, CLS 0.
- Sweater 영어 랜딩 페이지: 성능 **91**, 접근성 **100**, 모범 사례 **100**; FCP/LCP 2.1초, CLS 0.
- 은하 멸망 사전 한국어 5부 7항: 성능 **59**, 접근성 **100**, 모범 사례 **100**; FCP 6.0초, LCP 7.0초, CLS 0.
- 점수는 한 차례의 모바일 시뮬레이션 결과이며 실제 사용자의 Core Web Vitals나 모든 휴대전화에서 완벽한 시각적 레이아웃을 입증하는 것은 아니다.
- **성능 개선은 선택적 후속 작업**이다. 특히 메인 페이지 이미지와 렌더링 차단 리소스가 대상이다. 본문, CSS 또는 조판 변경에는 명시적 승인과 시각적 회귀 검증 계획이 필요하다.

## 구조화 데이터의 저작 주체 표기 통일 (2026-11-26)

**승인된 공개 정체성:** Jin-in-Seoul은 공개 창작물에 사용하는 필명이다. 사이트의 창작물 및 해당되는 번역·발행 주체의 Schema.org JSON-LD 표기는 `{"@type":"Person","name":"Jin-in-Seoul","url":"https://jin-in-seoul.com/"}`을 사용한다. 이는 공개 필명이며, **법적 실명의 공개가 아니고** 등록된 조직이라는 주장도 아니다. `Person`에서 `Organization`으로 변경하려면 새로운 승인이 필요하다.

- 창작물(소설, 개별 항목, 단편소설, 동화, Gray Note 에세이, 하이쿠, 음악): 기존 `author` 또는 해당되는 저작 주체에 동일한 공개 필명을 유지한다. 모든 언어판에 `translator` 속성을 무분별하게 추가하지 않는다.
- 작자 미상의 고전 원전 『전운치전』(`tales-from-premodern-korea/jeon-unchi/ko/index.html` 및 `en/index.html`): `"author":"Anonymous"`와 `Person / Jin-in-Seoul`인 `translator`를 유지한다. 한국어 현대어판의 기존 번역자 표기도 포함한다. 현대어판에 대한 설명은 공개된 안내문에 유지한다.
- `Book`, `Article`, `CreativeWork`, `MusicRecording`, `CollectionPage`, `WebSite` 등을 포함한 콘텐츠 `@type` 분류는 보존한다. 저작 주체 표기 통일만으로 본문, 번역, 레이아웃, canonical URL, hreflang, 사이트맵 또는 분석 태그의 변경을 정당화할 수 없다.

**작업 및 검증 이력:**

1. 앞서 분류하지 않은 저작 주체로 일회성 통일을 시행하여 커밋 [db303d77e](https://github.com/Jin-in-Seoul/Jin-in-Seoul/commit/db303d77e5a56252f1b5b792f0d9c270b6cf6ed6)가 생성되었다. 이 결정은 승인된 `Person` 표기 정책으로 **대체되었다**.
2. 최종 일회성 워크플로 `restore-pen-name-person-once.yml`이 성공했다([실행 45641099753](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/45641099753)). 로그에는 **수정된 HTML 306개**, **저자 표기 303개**, **번역자 표기 2개**, **발행자 표기 1개**, **파싱 실패 0건**으로 기록되었다. 결과 콘텐츠 커밋은 [7c57cad976](https://github.com/Jin-in-Seoul/Jin-in-Seoul/commit/7c57cad97685db425f3a605922b3b6aa44be1dec)이다.
3. 이 콘텐츠 커밋의 GitHub Pages 배포가 성공했다([실행 45641135130](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/runs/45641135130)). 메인 페이지, 은하 멸망 사전 랜딩 페이지와 본문, Sweater, 단편소설, 동화, Gray Note, 하이쿠, 음악, 전운치전 양쪽 언어판의 대표 소스 파일을 재조회했다.
4. 독립 페이지와 함께 Gray Note Liquid 레이아웃 `_layouts/gray-note-post.html`도 갱신했다. 소스 검사의 Liquid 템플릿 JSON 파싱은 배포 HTML의 파싱과 동일하지 않다. 사이트 전체 JSON-LD 검사에는 렌더링된 결과의 별도 검증이 필요하다.
5. 일회성 워크플로는 재실행할 수 없도록 **완료 후 제거해야 한다**. 제거에는 별도의 커밋과 Pages 배포 검증이 필요하다.

**검사 범위:** 해당 워크플로는 변경이 JSON-LD 스크립트에 한정되었음을 검증했고 검사 대상 파일에서 JSON 파싱 실패가 없다고 보고했다. 이것만으로 실제 HTML 전체의 유효성이나 Google/Naver 색인이 입증되는 것은 아니다. 해당 주장은 필요에 따라 배포 사이트 SEO 검사 및 승인된 Search Console 접근을 통해 확인한다. 작자 미상 원전의 저자 표기와 공개 필명은 계속 보호한다.
