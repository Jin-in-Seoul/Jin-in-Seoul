# Jin-in-Seoul

다국어 소설 아카이브.

https://jin-in-seoul.com

## 사이트 운영 및 관리

- [ABC — 사이트 운영 및 관리 규정](ABC.md)

## 한국의 옛소설 번역

- [한국의 옛소설 번역 및 편집 원칙](PREMODERN-KOREAN-FICTION-TRANSLATION-GUIDE.md) — 영어·한국어로 구성된 원칙 13개, 실전 번역 기준 및 공통 영어 용어집.

- [작품별 번역 가이드 — 전운치전](JEON-UNCHI-TRANSLATION-GUIDE.md)
- [작품별 번역 가이드 — 토끼전](MASTER-RABBIT-TRANSLATION-GUIDE.md)

## 발행 기록 관리

- [Publication Log 규정](PUBLICATION-LOG-POLICY.md) — 영어 작품명, 고정 언어 순서(영어·일본어·프랑스어·한국어), 실제 발행일, 이력 보존 및 검증 절차.

## 자산 관리

- [이미지, 음원, PDF/EPUB 저장 및 발행 규정](ASSET-MAINTENANCE.md) — 기존 경로와 원본 보존, 웹용 사진 최적화, 이미지 총용량 검토 및 2026년 11월 2일 디지털판 발행 중단.

## CSS 관리

- [CSS 적용 범위, 조판, 캐시 버전 규정 및 안전 점검 목록](CSS-MAINTENANCE.md)
- 읽기 전용 CSS 링크 및 버전 검사: `python3 scripts/audit_css_links.py`
- **Sweater의 일기체 조판은 공통 CSS 변경의 영향으로부터도 보호한다.**

## SEO 검사

- **[SEO 관리 규정](SEO-MAINTENANCE.md)** — 검증된 변경, 안전 규칙, 검사 링크 및 남은 확인 사항.

- 전체 소스 읽기 전용 SEO 검사: `python3 scripts/audit_seo.py`
- GitHub Actions: [SEO 소스 검사](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-audit.yml). 관련 변경 시 실행되며 수동 실행도 지원한다.
- 페이지별 검사 결과는 `seo-audit-report` 아티팩트에서 확인한다. ERROR/WARN/INFO는 진단 표시이며, 자동으로 실제 운영 환경의 오류로 확정되지 않는다.
- 이 검사는 페이지나 CSS를 **수정하지 않는다**. 소스 검사만으로 실제 HTTP 상태, Jekyll이 생성한 URL 또는 검색엔진 색인 여부를 확인할 수 없다. 검사 결과에 따른 수정은 사전 검토를 거치며, 특히 Sweater를 주의한다.

## 배포된 사이트의 SEO 검증

- 읽기 전용 실제 사이트 검사: `python3 scripts/audit_seo_live.py` (네트워크 접속 필요).
- GitHub Actions: [실제 사이트 SEO 검사](https://github.com/Jin-in-Seoul/Jin-in-Seoul/actions/workflows/seo-live-audit.yml). Pages 배포 성공 후 자동으로 실행되거나 수동 실행한다.
- `seo-live-report` 아티팩트에는 공개 사이트맵 URL에 대한 HTTP, canonical, noindex 및 hreflang 검사 결과가 포함된다.
- 실제 사이트 검사는 진단을 위한 것이며 Search Console과 Naver의 색인 보고서는 별도의 접근 권한이 필요하다. 페이지의 문장, 번역, CSS 또는 레이아웃은 변경하지 않는다.

## 이중 언어 관리 문서

저장소 최상위의 기존 문서는 전환 이전의 참조 자료로 보존한다. 영어판과 한국어판은 동일한 파일명으로 `_management/en/`, `_management/ko/`에 대응하여 관리한다. 공통 관리 문서 7개는 공개 관리 페이지 https://jin-in-seoul.com/site-management/ 및 https://jin-in-seoul.com/site-management/ko/의 원본이다. 작품별 번역 가이드는 향후 번역을 위해 저장소에 보존하며 저장소의 관리 문서에서는 참조 링크를 유지하되 공개 관리 페이지에는 전문과 개별 링크를 모두 표시하지 않는다. 규정 변경은 검토 및 승인 후 두 언어판에 함께 반영한다. 번역판이 독립적으로 규정의 내용을 변경하지 않는다. 양쪽 언어판에 불일치가 있으면 승인된 원본을 확인하고 차이를 해결한 뒤 적용한다.
