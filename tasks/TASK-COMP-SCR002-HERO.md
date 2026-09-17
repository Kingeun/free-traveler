# COMP-SCR002-HERO - Profile Hero

Category: Component | Implementation Status: IMPLEMENT | Priority: P1

## Context

대표 사진과 소개 한 줄 문장을 보여주는 Hero. 높이를 제한해 다음 Section이 폴드 안에 보이게 한다.

## Project Scope

이 Task는 개별 Requirement가 아니라 공통 인프라/전역 계층에 속하며, `docs/PROJECT_SCOPE.md`상 프로젝트 범위 내 **IMPLEMENT** 구현 방식을 지원한다.

## Requirement Ref

없음(이 Task는 특정 Requirement에 직접 매핑되지 않음)

## Screen / Route / Page Entry

Screen: SCR-002  
Route: `/about`  
Page Entry: `src/app/about/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` - SCR-002 절
- `design-reference/D-001/DESIGN.md` - Color Token / Typography / Spacing / Radius / Shadow, Do / Do Not 목록

## Depends On

- DATA-REPRESENTATIVE

## Expected Files

- `src/components/about/ProfileHero.tsx`

## Functional AC

전부 `DATA-REPRESENTATIVE` 정적 데이터만 사용. Gallery 이미지는 실제 촬영 장소를 설명하는 alt 텍스트를 필수로 가진다(일반 URL 이미지, 업로드 워크플로 없음).

## Visual AC

Section마다 시각 패턴을 다르게 한다(Hero/Stat/좌우분할/Timeline/Chip/Gallery/CTA Banner가 서로 다른 레이아웃). Lorem ipsum·빈 Card 금지.

## Security/Privacy AC

전부 Public.

## Test Cases

1. 1440px에서 Hero 아래 여행 지표 Section 제목이 보인다.

## Verify

E2E-PUBLIC-SMOKE

## Definition of Done

- 위 Functional AC / Visual AC / Security-Privacy AC 항목을 모두 만족한다.
- Verify에 명시된 Task/Check가 통과한다.
- Expected Files 목록에 있는 파일만 생성·수정했다(그 외 파일 변경 없음).
- Forbidden 목록에 해당하는 요소가 결과물에 없다.
- Requirement Ref가 있는 경우 `docs/UIUX_TRACEABILITY.md`에서 이 Task ID로 추적 가능하다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정·삭제하는 것.
- Lorem ipsum, "준비 중", "정보 확인 필요" 등 placeholder 문구, 또는 내용 없는 빈 Card를 남기는 것.
- 별점(★)·리뷰 점수 UI, 실시간 항공/숙소 가격, 광고 배너를 추가하는 것.
- Airbnb 상표 요소(Rausch 색상명, Cereal 폰트, "Guest favorite" 배지, 3-Product Nav 등)를 재현하는 것.
- 자동 Merge Runner, EC2/AWS 인프라 Task로 이 Task의 범위를 확장하는 것.
- 이 문서에 명시되지 않은 새 DB 테이블·새 Screen·새 Route를 추가하는 것.
