# Design Manifest — Free Traveler

| Field | Value |
|---|---|
| **Active Design Version** | D-001 |
| **Status** | LOCKED |
| **Active File** | `design-reference/D-001/DESIGN.md` |
| **Vendor Reference** | `design-reference/vendor/airbnb/DESIGN.md` (구조적 참고 전용 — 상표 요소 미사용) |
| **Approved Screens** | SCR-001, SCR-002, SCR-003, SCR-004, SCR-005 |
| **Mobile Variants** | SCR-001, SCR-003 |

`LOCKED` 상태에서는 `design-reference/D-001/DESIGN.md`의 토큰·규칙을 임의로 변경하지 않는다. 변경이 필요하면 새 버전(D-002)을 만들고 본 Manifest의 Active Design Version을 갱신한다.

---

## 근거 문서

- `docs/04_UIUX_PLAN.md` — 화면별 Section 계약, 색상/타이포/spacing 토큰 초안의 출처.
- `docs/STITCH_VALIDATION_REPORT.md` — Stitch Project `10641995830734191514`에서 생성된 화면의 검증 기록. 별점·실시간 가격 위반을 실제로 발견하고 제거한 근거이며, D-001의 Do Not 항목에 직접 반영되었다.
- `design-reference/vendor/airbnb/DESIGN.md` — 사진 중심 카드, Section 여백 리듬, 단일 shadow tier 등 구조적 아이디어의 참고본(상표 요소는 채택하지 않음).

## Screen 추적표

| Screen | Stitch Screen ID | Device | Section 수(계약) | 상태 |
|---|---|---|---:|---|
| SCR-001 `/` | `597374ad452d4d898bd1f0770aec011d` | Desktop 1440px | 7 | PASS |
| SCR-001 Mobile | `48d9e4fdee9d4f04b713ba8cae711d0e` | Mobile 390px | 7 | PASS |
| SCR-002 `/about` | `bacf922dca9b4180a8e41307729e3d39` | Desktop 1440px | 7 | PASS |
| SCR-003 `/travel-tools` | `62895f446b5f46a6a53362cd766d40ab` | Desktop 1440px | 6 | NEEDS_REVISION (미해결 항목 있음) |
| SCR-003 Mobile | `1f8bc82791f8422bbac54b74b9a9a85a` | Mobile 390px | 6 | NEEDS_REVISION (Section 6 누락) |
| SCR-004 `/mates` | 작업 진행 중 (Stitch Project 내 초안 존재) | Desktop 1440px | 6 | 미완성 |
| SCR-005 `/account` | 미생성 | Desktop 1440px | 역할별 | 미생성 |

> 위 상태는 `docs/STITCH_VALIDATION_REPORT.md` 작성 시점 기준이다. SCR-003의 미해결 항목(중복 Section, 실시간 가격 텍스트), SCR-004의 목록+상세 분할/신청 방법/안전 안내 Section, SCR-005 전체는 D-001 규칙을 그대로 적용해 후속 세션에서 마무리한다. Manifest의 "Approved Screens"는 제품 범위상 승인된 화면 집합(SCR-001~005)을 뜻하며, 개별 화면의 현재 구현 완성도는 이 추적표와 `docs/STITCH_VALIDATION_REPORT.md`를 따른다.

## 금지 항목 요약 (전체 목록은 D-001 § Do Not 참조)

- Airbnb 상표 요소(로고·워드마크·컬러명·3-Product 내비게이션·배지 문구)
- 구매·예약·결제 UI, 실시간 항공권·호텔 가격
- Proprietary Font 파일 (Inter + 시스템 한글 폰트 스택만 허용)
- D-001 Color Token 표에 없는 임의 색상 추가
- 별점/숫자 평점, 광고 배너, Lorem ipsum/준비 중/정보 확인 필요, 빈 Card

## 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| D-001 | 2026-09-15 | 최초 잠금. `docs/04_UIUX_PLAN.md` + Stitch 검증 결과를 통합한 최초 디자인 정본. |
