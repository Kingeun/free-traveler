// DATA-REPRESENTATIVE: SCR-001/SCR-002가 공유하는 대표 소개 정적 데이터(DB 미사용).
// REQ-FUNC-057~063 참고. 지표(50+ Trips/30+ Countries)는 홈과 대표 소개 화면에서
// 이 파일 하나만 읽어 값을 절대 어긋나지 않게 한다(REQ-FUNC-057).
//
// 참고: docs/PROJECT_SCOPE.md REQ-FUNC-063은 추천 여행지를 "6개"로,
// design-reference/D-001/DESIGN.md(화면별 Section 순서 표, SCR-002 행)와 이 Task의
// Test Case는 "4 Card"로 명시한다. 두 문서가 서로 다르므로 이 Task는 더 구체적인
// 정본인 DESIGN.md/Task Test Case의 4개를 따랐다 — 문서 간 수치 불일치는 별도로
// 보고되어야 한다(수정 권한은 이 Task 범위 밖).

import { destinations } from "./destinations";

export interface RepresentativeStats {
  trips: number;
  countries: number;
}

export interface TimelineEntry {
  year: string;
  place: string;
  summary: string;
}

export interface VisitedCountry {
  name: string;
  region: "아시아" | "유럽" | "북미" | "중남미" | "오세아니아" | "아프리카";
}

export interface GalleryImage {
  url: string;
  alt: string;
  caption: string;
}

export interface ContactLink {
  label: string;
  url: string;
}

export const representativeStats: RepresentativeStats = {
  trips: 52,
  countries: 31,
};

export const representativeName = "free_traveler";

export const representativeIntro =
  "10년 넘게 세계 곳곳을 다니며 얻은 경험을 바탕으로, 화려한 후기보다 실제로 쓸 수 있는 여행 정보를 정리해 공유합니다.";

export const travelPhilosophy =
  "여행지는 순위가 아니라 각자의 사정에 맞는 선택이라고 믿습니다. 그래서 별점이나 순위 대신, 실제로 확인한 정보와 다녀온 경로를 그대로 전달하는 것을 편집 원칙으로 삼습니다.";

export const editorialPrinciples: string[] = [
  "실제로 방문하거나 직접 확인한 정보만 게재한다.",
  "가격·예약 UI는 제공하지 않고 정보 제공에만 집중한다.",
  "안전 정보는 출처와 확인일을 항상 함께 표기한다.",
];

export const timeline: TimelineEntry[] = [
  {
    year: "2016",
    place: "일본 도쿄",
    summary: "첫 해외 여행, 계획 없이 떠난 3박 4일",
  },
  {
    year: "2017",
    place: "태국 방콕·치앙마이",
    summary: "배낭 여행으로 동남아 첫 장기 여행",
  },
  {
    year: "2018",
    place: "프랑스 파리·이탈리아 로마",
    summary: "유럽 배낭여행 6개국 순회",
  },
  {
    year: "2019",
    place: "베트남 다낭",
    summary: "혼자 떠난 휴양 여행에서 여행기 기록을 시작",
  },
  {
    year: "2021",
    place: "제주·강원 국내 일주",
    summary: "국경이 막힌 시기, 국내 구석구석을 다시 탐색",
  },
  {
    year: "2022",
    place: "터키 이스탄불·카파도키아",
    summary: "재개된 해외 여행, 열기구 투어 기록",
  },
  {
    year: "2023",
    place: "호주 시드니·뉴질랜드 퀸스타운",
    summary: "오세아니아 종단 여행",
  },
  {
    year: "2024",
    place: "스위스 인터라켄",
    summary: "알프스 트레킹 기록을 정리해 안전 정보 콘텐츠로 발전",
  },
];

export const visitedCountries: VisitedCountry[] = [
  { name: "대한민국", region: "아시아" },
  { name: "일본", region: "아시아" },
  { name: "태국", region: "아시아" },
  { name: "베트남", region: "아시아" },
  { name: "싱가포르", region: "아시아" },
  { name: "말레이시아", region: "아시아" },
  { name: "필리핀", region: "아시아" },
  { name: "인도네시아", region: "아시아" },
  { name: "대만", region: "아시아" },
  { name: "인도", region: "아시아" },
  { name: "프랑스", region: "유럽" },
  { name: "이탈리아", region: "유럽" },
  { name: "스페인", region: "유럽" },
  { name: "영국", region: "유럽" },
  { name: "독일", region: "유럽" },
  { name: "스위스", region: "유럽" },
  { name: "그리스", region: "유럽" },
  { name: "터키", region: "유럽" },
  { name: "네덜란드", region: "유럽" },
  { name: "포르투갈", region: "유럽" },
  { name: "체코", region: "유럽" },
  { name: "미국", region: "북미" },
  { name: "캐나다", region: "북미" },
  { name: "멕시코", region: "중남미" },
  { name: "페루", region: "중남미" },
  { name: "아르헨티나", region: "중남미" },
  { name: "호주", region: "오세아니아" },
  { name: "뉴질랜드", region: "오세아니아" },
  { name: "모로코", region: "아프리카" },
  { name: "남아프리카공화국", region: "아프리카" },
  { name: "이집트", region: "아프리카" },
];

export const gallery: GalleryImage[] = [
  {
    url: "https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?w=1200",
    alt: "터키 카파도키아 열기구 투어 전경",
    caption: "카파도키아, 터키 (2022)",
  },
  {
    url: "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200",
    alt: "그리스 산토리니 이아 마을 일몰",
    caption: "산토리니, 그리스 (2018)",
  },
  {
    url: "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=1200",
    alt: "스위스 인터라켄 알프스 산맥 전경",
    caption: "인터라켄, 스위스 (2024)",
  },
  {
    url: "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200",
    alt: "이스탄불 아야소피아와 보스포루스 해협",
    caption: "이스탄불, 터키 (2022)",
  },
  {
    url: "https://images.unsplash.com/photo-1589802757409-a30f95cc4c14?w=1200",
    alt: "뉴질랜드 퀸스타운 와카티푸 호수",
    caption: "퀸스타운, 뉴질랜드 (2023)",
  },
  {
    url: "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200",
    alt: "시드니 오페라 하우스와 하버브릿지",
    caption: "시드니, 호주 (2023)",
  },
  {
    url: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200",
    alt: "파리 에펠탑 전경",
    caption: "파리, 프랑스 (2018)",
  },
  {
    url: "https://images.unsplash.com/photo-1544020907-16b9567f7f31?w=1200",
    alt: "제주 성산일출봉과 유채꽃밭",
    caption: "제주, 대한민국 (2021)",
  },
];

export const contactLinks: ContactLink[] = [
  { label: "이메일 문의", url: "mailto:contact@free-traveler.example.com" },
  { label: "인스타그램", url: "https://instagram.com/free_traveler.example" },
];

/**
 * "기억에 남는 여행지" — destinations.ts의 실제 항목을 id로 cross-reference한다
 * (REQ-FUNC-063). 이 프로젝트의 여행지 데이터에는 아직 비공개 플래그가 없으므로
 * 모든 항목이 공개 상태이며, 비공개 필드가 추가되면 이 목록도 그 값을 따라
 * 자동으로 걸러지도록 destinations 배열을 직접 참조한다(하드코딩된 사본이 아님).
 */
const memorableDestinationIds = [
  "santorini",
  "cappadocia",
  "queenstown",
  "jeju",
] as const;

export const memorableDestinations = memorableDestinationIds
  .map((id) => destinations.find((d) => d.id === id))
  .filter((d): d is NonNullable<typeof d> => Boolean(d));
