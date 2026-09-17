---
version: D-001
name: Free-Traveler-design-system
status: LOCKED
description: An original, photo-led travel-discovery design system for "Free Traveler" — a white canvas, dark charcoal ink, and a single coral accent (#FF6F59) carrying every primary CTA. Structurally informed by the generous section rhythm and photo-first card language documented in design-reference/vendor/airbnb/DESIGN.md, but no Airbnb brand asset (wordmark, color name, 3-product nav, "NEW" badge, booking/payment flow) is reused. Validated against 5 approved Stitch screens (SCR-001–SCR-005, mobile variants for SCR-001/SCR-003) — see docs/STITCH_VALIDATION_REPORT.md for the audit trail that produced several of the explicit prohibitions below (star ratings and real-time prices were found on early drafts and removed).

colors:
  canvas: "#FFFFFF"
  surface-soft: "#F7F6F4"
  surface-strong: "#EFEDEA"
  ink: "#2B2E33"
  body: "#4A4E54"
  muted: "#6B7078"
  hairline: "#E2E0DD"
  border-strong: "#C7C4C0"
  primary: "#FF6F59"
  primary-active: "#E6543F"
  primary-disabled: "#FFD9CE"
  on-primary: "#FFFFFF"
  success: "#2E8B57"
  warning: "#B25E00"
  danger: "#C6362E"
  focus-ring: "#1F6FEB"

typography:
  display-xl:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.3
  display-lg:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.35
  display-md:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 22px
    fontWeight: 600
    lineHeight: 1.4
  title-md:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.45
  body-md:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  caption:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.4
  button:
    fontFamily: "'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.3

rounded:
  sm: 8px
  md: 12px
  lg: 16px
  full: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 12px
  base: 16px
  lg: 24px
  xl: 32px
  section-desktop: 64-96px
  section-mobile: 40-64px

elevation:
  card-hover: "0 1px 2px rgba(0,0,0,.04), 0 4px 10px rgba(0,0,0,.08)"

breakpoints:
  desktop: 1440px
  tablet: 744-1023px
  mobile: 390px
---

## Overview

Free Traveler is a Korean-language travel discovery and trip-prep service. This document is the **locked design reference (D-001)** for every screen — it is the single source of truth a builder consults before writing UI code. It supersedes ad-hoc judgment calls; where this file and a screenshot disagree, this file wins unless the file itself is revised through a new version.

The system borrows only the *structural* ideas that make `design-reference/vendor/airbnb/DESIGN.md` work as a marketplace layout — generous section padding that compresses into denser card grids, a single accent color used sparingly, one shallow shadow tier, and pill-shaped search/filter controls. It does not reuse anything that identifies the page as Airbnb: no Rausch color name, no Cereal typeface, no three-product top nav, no "Guest favorite" / "NEW" badge language, no booking or payment flow. Every token below is Free Traveler's own.

This version was locked after 5 Stitch screens (SCR-001–SCR-005, plus mobile variants for SCR-001 and SCR-003) were generated and audited (`docs/STITCH_VALIDATION_REPORT.md`). Two concrete violations were caught and removed during that audit — star-rating badges on destination cards, and real-looking flight prices on a route-comparison strip — and are now explicit prohibitions in this document (§ Do / Do Not) rather than just a memory of what happened once.

---

## Visual Theme

- **Canvas:** pure white (`{colors.canvas}`) everywhere, on every screen, at every breakpoint. There is no dark mode.
- **Ink over black:** body and headline text sit on `{colors.ink}` (#2B2E33), a dark charcoal — never `#000000`.
- **One accent, used sparingly:** `{colors.primary}` (#FF6F59, coral) is the *only* accent color in the system. It appears on primary buttons, the search/filter submit affordance, selected chips, and small highlight accents (active nav underline, focus stat numbers). A page that is 90% white/ink with one or two coral moments is correct; a page with coral everywhere is not.
- **Photography-led:** every Hero and every destination/gallery card is dominated by a real travel photograph, not illustration or abstract graphics. Alt text names the actual place shown (e.g. "페루 마추픽추 전망대에서 바라본 유적지 전경"), never generic filler like "travel photo."
- **Soft, shallow shapes:** rounded corners everywhere (see Radius), a single shallow shadow tier (see Shadow), pill shapes reserved for search bars, filter chips, and status badges — never for full cards.

---

## Color Token

| Token | Hex | Use |
|---|---|---|
| `color.canvas` | `#FFFFFF` | Page background, every screen |
| `color.surface-soft` | `#F7F6F4` | Section background tint used to separate two adjacent Card Grids (e.g. 해외 destinations band vs. 국내 band above it) |
| `color.surface-strong` | `#EFEDEA` | Inactive chip fill, disabled field background |
| `color.ink` | `#2B2E33` | Primary text — headings, body, nav labels |
| `color.body` | `#4A4E54` | Secondary running text inside long descriptions |
| `color.muted` | `#6B7078` | Captions, meta text, placeholder text |
| `color.hairline` | `#E2E0DD` | 1px dividers, card borders, footer column rules |
| `color.border-strong` | `#C7C4C0` | Emphasized (non-focus) input outline |
| `color.primary` | `#FF6F59` | The one accent — primary buttons, submit affordances, selected chip fill, active nav indicator |
| `color.primary-active` | `#E6543F` | Press/active state of `color.primary` |
| `color.primary-disabled` | `#FFD9CE` | Disabled primary button fill |
| `color.on-primary` | `#FFFFFF` | Text/icon color on any coral surface |
| `color.success` | `#2E8B57` | "최신" / verified safety badge, success toast |
| `color.warning` | `#B25E00` | "재확인 필요" (stale) badge, non-blocking warning toast |
| `color.danger` | `#C6362E` | Form validation errors, destructive action text, blocking error toast |
| `color.focus-ring` | `#1F6FEB` | Keyboard focus outline only — never used as a content color |

**Rule:** no color may be introduced outside this table. If a new state needs a color (e.g. a future "추천" badge), it must be added to this token table and this file re-versioned — never hard-coded inline in a component.

**Semantic separation:** `success` / `warning` / `danger` are visually distinct from `primary` by hue, not just tone, so a safety badge or form error is never mistaken for a coral CTA. Every semantic color is always paired with a text label or icon — never color alone (this directly satisfies the SRS requirement that safety advisories not rely on color-only signaling).

---

## Typography

**Font stack:** `'Inter', 'Apple SD Gothic Neo', 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`. Inter carries Latin glyphs and numerals; Korean text renders through the system Korean fallback automatically. No proprietary/licensed font file is bundled (see Do Not).

| Token | Size | Weight | Line height | Use |
|---|---:|---:|---:|---|
| `type.display-xl` | 36px | 700 | 1.3 | SCR-001 / SCR-002 Hero heading |
| `type.display-lg` | 28px | 700 | 1.35 | Section heading (e.g. "국내에서 지금 가장 인기 있는 여행지") |
| `type.display-md` | 22px | 600 | 1.4 | Card-group sub-heading, Drawer title |
| `type.title-md` | 18px | 600 | 1.45 | Card title, form section label |
| `type.body-md` | 16px | 400 | 1.6 | Default paragraph copy |
| `type.body-sm` | 14px | 400 | 1.55 | Card meta line, caption-adjacent copy |
| `type.caption` | 13px | 500 | 1.4 | Badge text, status label, timestamp |
| `type.button` | 16px | 600 | 1.3 | Button and CTA labels |

Headlines are confidently sized but never shout past weight 700; body copy stays at 1.55–1.6 line-height because Korean sentences need more breathing room than Latin text at the same size.

---

## Spacing

Base unit 4px.

| Token | Value |
|---|---|
| `space.xs` | 4px |
| `space.sm` | 8px |
| `space.md` | 12px |
| `space.base` | 16px |
| `space.lg` | 24px |
| `space.xl` | 32px |
| `space.section-desktop` | **64–96px** vertical padding per Section, Desktop |
| `space.section-mobile` | **40–64px** vertical padding per Section, Mobile |

Card-internal padding uses `space.lg` (24px); gutters between cards in a grid use `space.base` (16px) on desktop, collapsing to a single column with `space.base` vertical gaps on mobile.

---

## Radius

| Token | Value | Use |
|---|---|---|
| `radius.sm` | 8px | Buttons, form inputs |
| `radius.md` | 12px | Cards (destination, safety, mate post), Drawer/Modal panels |
| `radius.lg` | 16px | Large feature cards, founder/intro band container |
| `radius.full` | 9999px | Pill search bar, filter chips, status badges, avatars |

No sharp (0px) corners appear anywhere except the outer page/body grid itself.

---

## Shadow

The system has exactly **one** shadow tier plus flat:

- **Flat (no shadow):** default state for 95% of surfaces — cards at rest, Hero, Footer, all section bands.
- **`elevation.card-hover`:** `0 1px 2px rgba(0,0,0,.04), 0 4px 10px rgba(0,0,0,.08)` — used only on: card hover/focus lift, Drawer/Modal panels, and open dropdown/menu surfaces.

No second, heavier shadow tier exists. Depth comes from photography and the rounded-corner card language, not from stacked shadows.

---

## Header · Footer

Shared, identical component instance on every one of the 5 screens (SCR-001–SCR-005).

**Header**
- Desktop (1440px, height 72px): wordmark "Free Traveler" left (links to `/`) · center nav — 여행지, 여행 도구, 동행, 대표소개, current page shown with a coral underline/bold weight · right — 로그인 button when signed out, avatar+닉네임 when signed in (links to `/account`).
- Mobile (390px, height 56px): wordmark left · hamburger icon right, opening a full-screen nav sheet containing the same 4 links plus the auth action.
- 1px `color.hairline` border along the bottom edge. No shadow.

**Footer**
- Desktop: 3 columns — 서비스 (여행지, 여행 도구, 동행, 대표소개), 정책 (이용약관, 개인정보처리방침, 동행 안전수칙, 콘텐츠 면책 안내), 문의 (대표 연락처/SNS). Mobile: columns stack to 1.
- Bottom band: copyright line + the standing disclaimer "안전정보 등 콘텐츠는 참고용이며 출국 전 공식 출처 재확인이 필요합니다."

---

## Search · Filter

- **Search bar (SCR-001 Hero):** single full-width pill (`radius.full`), white fill, `color.hairline` border, a magnifying-glass icon, and a coral circular/pill submit button labeled "검색하기". It accepts a **destination/country/theme keyword only**. It must never grow a date-picker or guest-count stepper — that shape belongs to a booking flow, which this product does not have (see Do Not).
- **Filter bar (SCR-004):** a row of pill chips/dropdowns for 국가, 지역, 기간, 연령대, 성별, 여행 스타일, 모집 상태, with a selected-filter tag summary and a "필터 초기화" reset action, followed by a result-count line ("총 N개의 모집글") and a sort control. Selected chip = coral fill + white text; default chip = `color.surface-strong` fill, `color.ink` text.
- **Theme chip row (SCR-001):** the same chip component used as a single-select or toggle row under "어떤 여행을 떠나고 싶으신가요", horizontally scrollable on mobile.

---

## Destination Card

Photo-first, `radius.md` corners, used for domestic/overseas destinations (SCR-001) and the "기억에 남는 여행지" grid (SCR-002).

- Structure top→bottom: photo (aspect ~4:3), small country/region tag chip overlapping the photo's top-left corner if applicable, title (`type.title-md`), 1–2 theme hashtag chips, 1–2 line description (`type.body-sm`, `color.body`), a footer row with a recommended-duration line and a `상세보기` text/coral link.
- **No star rating, no numeric score, no review count anywhere on the card.** (Confirmed violation in the Stitch audit — see Do Not.)
- **No price of any kind.** Destination cards are discovery cards, not booking cards.
- Selecting a card opens the SCR-001 detail Drawer (see Drawer · Modal) in place — it does not navigate to a new page.

---

## Form · Tabs

- **Tabs (SCR-003):** a 3-item segmented control — 항공편 찾기 / 숙소 찾기 / 동행 구하기. Active tab = coral fill or coral underline + bold label; inactive = `color.muted` label, `color.surface-strong` or outline chrome. Switching tabs must **not** discard input already entered in another tab — each tab keeps its own state.
- **Condition form (항공/숙소 tabs):** stacked or 2-column fields — 국가, 지역 (dependent dropdown, resets when 국가 changes), 출발일/체크인, 귀국일/체크아웃 — each with a `radius.sm` bordered input, label above in `type.caption`, and a full-width or right-aligned coral submit ("요약 확인하기").
- **Summary + Action Card:** a 2-column split (stacks on mobile) — left: read-only summary list of the submitted conditions with a "수정" edit link; right: an Action Card naming the external partner (e.g. "Google Flights에서 항공권 보기") with a coral "외부 사이트로 이동" button. The non-transmission notice ("입력값은 외부로 전달되지 않아요") is mandatory copy near this component.
- **Mate post write form (동행 구하기 tab):** only rendered for an authenticated, adult-verified member; a signed-out or unverified visitor instead sees the Login Gate pattern below.

---

## Mate Post Card

Used in the SCR-004 list.

- Structure: top row — 모집중 (coral-tinted pill) or 마감 (muted gray pill) status badge, 국가·지역, 기간, 모집 인원 (e.g. "모집 2 / 4명"); title (`type.title-md`); up to 4 theme hashtag chips; footer row — author avatar/initial + nickname + a **text** trust indicator (e.g. "매너온도 96.4°C" or a "본인인증 완료" icon+label) and a coral "동행 신청"/"참가 요청" button (or a disabled muted button when 마감).
- **No star rating.** A text-based trust/manner indicator is permitted (it is not a 1–5 star review mechanic), but it must never be rendered as a star icon or numeric review score.
- **No price of any kind.**
- Desktop: list (left) + sticky detail panel (right) showing the selected post's full description and a participation-message textarea. Mobile: list only, tapping a card opens the detail as a bottom Drawer.

---

## Drawer · Modal

- Used for: SCR-001 destination detail (opens over the current page when a Destination Card is selected), SCR-001 country safety detail, SCR-004 mate post detail on mobile.
- Desktop: slides in from the right, fixed width (~480–560px), full viewport height, `radius.md` on the leading edge only, `elevation.card-hover` shadow, `color.scrim`-style dim backdrop (black at ~40–50% opacity) behind it.
- Mobile: bottom sheet, `radius.lg` on the top two corners only, draggable/dismissible, same dim backdrop.
- Content follows the same title → 1–3 sentence description → body/CTA hierarchy as a Section (see below) — a Drawer is a Section rendered in an overlay, not a different content grammar.

---

## Alert · Toast

- **Inline alert / notice box** (e.g. the "동행을 모집하려면 로그인이 필요해요" safety notice, or a stale-safety-info warning): rounded (`radius.md`) box, `color.surface-soft` or tinted-by-semantic-color background, an icon + text label pairing — never a bare color field.
- **Toast:** transient, bottom-center or bottom-right, `radius.sm`, appears for state changes (예: 참가 요청 접수, 신고 접수, 저장 완료) and auto-dismisses. Success toast uses `color.success` accent, error toast `color.danger`, both with an icon — color is never the only signal.
- Toasts and alerts never use `color.primary` (coral) for anything except a neutral/informational tone — coral is reserved for actionable CTAs, not for status messaging.

---

## Loading · Empty · Error 상태

- **Loading:** skeleton placeholders shaped like the real content (card silhouettes, text bars) — never a spinner-only blank screen, and never longer than the content it replaces.
- **Empty:** a *complete* state, not a bare message — icon, one-sentence explanation ("아직 등록된 동행글이 없어요"), a short "이용 방법" (how-it-works, 2–3 steps), and one primary coral CTA ("동행 모집글 작성하기"). This exact pattern was validated on SCR-001's 동행 Empty State and is the template for every future empty state (empty 신고 큐, empty 내 활동 목록, etc.).
- **Error:** inline, human-readable Korean message + a retry action where retry is meaningful (e.g. 외부 사이트 연결 실패 → "다시 시도"). Never a raw error code or English stack trace shown to the user.
- None of these three states may ever fall back to placeholder copy — see the Placeholder 문구 금지 규칙 below.

---

## Desktop · Mobile 규칙

| | Desktop | Mobile |
|---|---|---|
| Reference width | **1440px** | **390px** |
| Page content max-width | 1200–1280px, centered, remaining width absorbed as side gutter | full width minus side padding |
| Section vertical padding | **64–96px** | **40–64px** |
| Card grid columns | up to 3 per row (destination/safety/mate grids) | 1 column, full width |
| Filter/theme chip rows | wrap or inline | horizontally scrollable, no wrap |
| Split layouts (Summary+Action, List+Detail) | 2-column side-by-side | stacked; List+Detail becomes list + Drawer |
| Nav | full inline nav in Header | hamburger sheet |
| Touch targets | n/a (pointer) | **minimum 44×44px** hit area on every interactive element, even when the visible glyph is smaller |
| Keyboard focus | 2px `color.focus-ring` outline, 2px offset, on every focusable element | same (external keyboard / accessibility) |

A Tablet range (744–1023px) exists as a fluid step between the two anchors — it narrows grid column counts (e.g. 3→2) and split ratios without introducing new component shapes.

---

## Page Section 최대 폭과 Desktop·Mobile 상하 여백

- **Desktop content max-width:** 1200–1280px, horizontally centered; anything wider than that (photo backgrounds, full-bleed tint bands) may extend edge-to-edge but the text/card content inside stays within this max-width.
- **Section vertical padding:** 64–96px on Desktop, 40–64px on Mobile, applied per Section (top+bottom), not per page. Two adjacent Sections may share a visual boundary via a background-tint change (e.g. `color.surface-soft`) instead of a hard rule line.

---

## Hero 높이와 다음 Section 노출 규칙

- A Hero (SCR-001, SCR-002) is **capped in height** — it must not fill the entire first viewport. At the 1440px desktop reference width, the *heading of the next Section* must already be visible below the Hero without scrolling.
- A Hero always contains: heading (`type.display-xl`), a 1–2 sentence subtext, and either a search affordance (SCR-001) or a single supporting visual + intro line (SCR-002) — never just a full-bleed image with no content.
- This rule was visually confirmed on the approved SCR-001 and SCR-002 Desktop screenshots (Hero → immediately followed by a visible Section heading, no dead full-height banner).

---

## Section별 제목·설명·본문·CTA 계층과 시각적 리듬

Every Section, on every screen, follows the same internal hierarchy:

1. **Title** — `type.display-lg` (or `type.display-md` for a sub-band), a complete Korean phrase, never a fragment.
2. **Description** — 1–3 sentences, `type.body-md` or `type.body-sm`, `color.body`/`color.muted`.
3. **Body** — the actual content: a Card Grid, a split layout, a Chip list, a step guide, a Gallery, or a Drawer trigger.
4. **CTA** (where applicable) — one primary coral action per Section; a Section never has more than one coral primary button (a secondary action, if present, uses the outline/text button style).

**Rhythm rule:** across a single screen, Section *patterns* must alternate — Hero, Card Grid, 좌우 분할(Split), Chip 목록, 3단계 안내(Step Guide), CTA Banner — so that no two adjacent Sections read as the same shape. Where content forces two Card Grids to sit next to each other (e.g. 국내 → 해외 destinations), they must be visually differentiated by background tint, photo emphasis, or badge type, never left identical.

---

## 화면별 Section 순서와 최소 콘텐츠 수

| Screen | Section 순서 | 최소 콘텐츠 수 |
|---|---|---|
| **SCR-001** `/` | Hero(검색) → 국내 인기 여행지 → 해외 인기 여행지 → 여행 동기·테마 → 국가별 주의사항 → 최근 동행글/Empty State → free_traveler 요약 | 국내 6 Card · 해외 6 Card · 테마 6 Chip · 안전정보 6 Card · 동행 3 Card 또는 완성형 Empty State |
| **SCR-002** `/about` | Hero → 여행 지표 → 소개·철학 → Timeline → 방문 국가 → Gallery → 기억에 남는 여행지+CTA | Timeline **6개 이상** 시점 · 방문 국가 **30개** (권역별 그룹) · Gallery **8장 이상** (실제 지명 캡션) · 기억에 남는 여행지 **4 Card** |
| **SCR-003** `/travel-tools` | Intro(3단계 안내) → 탭(3개) → 조건 Form → 요약+외부이동 Action Card → 비전달 고지+Tip → 동행 탭(로그인 안내 또는 작성 Form+안전 안내) | 3탭 전부 존재 · Tip **3개** · 안전 안내 항목 **3개 이상** |
| **SCR-004** `/mates` | Intro+작성 CTA → Filter+결과 요약 → 동행글 목록 → 목록+상세(Desktop 분할/Mobile Drawer) → 신청 방법 3단계 → 안전·신고·차단 안내+CTA | 목록 **최대 8 Card** 우선 노출 · 신청 방법 **3단계** · 안전 안내 **3개 이상** |
| **SCR-005** `/account` | 역할별(Guest/Member/Admin) — Intro, 핵심 작업, 도움말/다음 행동 | 역할에 없는 탭은 렌더링하지 않음 · Dashboard/통계 화면 금지 |

---

## 완성형 Empty State와 Placeholder 문구 금지 규칙

- **절대 금지 문자열:** "Lorem ipsum", "준비 중", "정보 확인 필요", 그리고 의미 없이 반복되는 문구. 이 4가지는 어떤 언어·어떤 상태(로딩 제외)에서도 화면에 나타나서는 안 된다.
- **빈 Card 금지:** 콘텐츠가 없는 빈 Card, 텍스트 없는 장식용 빈 영역을 만들지 않는다.
- **완성형 Empty State 정의:** 아이콘 + 한 문장 설명 + 짧은 이용 방법(2~3단계) + 명확한 CTA 버튼 1개. 이 4요소가 모두 있어야 "완성형"으로 인정한다 (SCR-001 동행 섹션에서 검증된 패턴).
- **DB 데이터가 없을 때도** 위 4요소를 갖춘 Empty State를 표시해 빈 화면처럼 보이지 않게 한다.

---

## Do / Do Not

### Do
- 코랄(`color.primary`)은 화면당 핵심 CTA 1~2곳에만 아껴서 사용한다.
- 모든 안전·오류·경고 표시는 텍스트/아이콘과 함께 표시한다(색상 단독 금지).
- 모든 사진에는 실제 장소를 설명하는 alt 텍스트를 붙인다.
- Empty State는 항상 아이콘+설명+이용 방법+CTA를 갖춘 완성형으로 만든다.
- Section은 제목·설명·본문·CTA 계층을 지키고, 인접 Section끼리 패턴을 교차시킨다.
- Hero는 높이를 제한해 1440px 데스크톱 기준 다음 Section이 바로 보이게 한다.
- 신뢰 지표가 필요하면 "매너온도", "본인인증 완료" 같은 텍스트/아이콘 기반 지표만 사용한다.
- 새로운 색상이 필요하면 이 문서의 Color Token 표에 먼저 추가하고 버전을 올린다.

### Do Not
- **Airbnb 상표 요소** — Airbnb 로고/워드마크, Rausch 등 Airbnb 고유 컬러명, 3-Product 상단 내비게이션, "NEW"/"Guest favorite" 배지 문구를 그대로 가져오지 않는다.
- **구매·예약·결제 UI** — 가격 표시, 날짜·인원 선택이 결합된 예약 검색바, 결제/체크아웃 폼, 실시간 항공권·호텔 가격을 어떤 화면에도 추가하지 않는다(SCR-003의 "인기 비교 노선" 카드에서 실제로 발견되어 제거된 위반 사례).
- **별점/리뷰 점수** — 여행지 Card, 동행글 Card 어디에도 별점(★)이나 숫자 평점을 넣지 않는다(SCR-001 Desktop/Mobile에서 실제로 발견되어 제거된 위반 사례).
- **Proprietary Font 파일** — Inter 및 시스템 한글 폰트 스택만 사용하고, 라이선스가 필요한 폰트 파일을 프로젝트에 포함하지 않는다.
- **토큰에 없는 임의 색상** — 위 Color Token 표에 없는 hex 값을 컴포넌트에 직접 박아넣지 않는다.
- **광고 배너** — 서드파티 광고, 스폰서 배너를 어떤 Section에도 넣지 않는다.
- Lorem ipsum, "준비 중", "정보 확인 필요", 의미 없는 빈 Card, 과도한 빈 여백.
- 한 Section에 코랄 Primary CTA를 2개 이상 배치하지 않는다.
- 로그인/성인 인증이 필요한 기능(동행 작성 등)에 인증 상태를 우회하는 UI를 넣지 않는다.
