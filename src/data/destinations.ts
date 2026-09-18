// DATA-DESTINATIONS: 정적 여행지 데이터(DB 미사용). Free Traveler는 여행지 콘텐츠를
// DB Table이 아니라 이 파일의 TypeScript 배열로만 제공한다(design-reference/D-001/
// DESIGN.md Do Not: 가격·예약 UI 금지, TASKS/TASK-DATA-DESTINATIONS.md Forbidden 참고).
//
// 최소 수량: 국내 10개 이상, 해외 15개국 30개 도시 이상 — DATA-VALIDATION-SCRIPT
// Task(별도 Wave, 아직 미구현)가 build 전에 이 최소치를 강제할 예정이다.

export type DestinationRegion = "domestic" | "overseas";

export interface DestinationItinerary {
  /** 1일 코스 - 3~4개 활동 */
  oneDay: string[];
  /** 3일 코스 - Day 1/2/3 각 1줄 요약 */
  threeDay: string[];
}

export interface Destination {
  id: string;
  name: string;
  country: string;
  region: DestinationRegion;
  imageUrl: string;
  imageAlt: string;
  intro: string;
  attractions: string[];
  itinerary: DestinationItinerary;
  budget: string;
  transport: string;
  food: string[];
  etiquette: string[];
  source: string;
  updatedAt: string;
}

export const destinations: Destination[] = [
  {
    id: "seoul",
    name: "서울",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=1200",
    imageAlt: "서울 경복궁 근정전과 방문객들",
    intro:
      "고궁과 현대적 스카이라인이 함께 있는 대한민국의 수도로, 전통과 트렌드를 동시에 경험할 수 있다.",
    attractions: [
      "경복궁",
      "북촌한옥마을",
      "남산서울타워",
      "이태원",
      "한강공원",
    ],
    itinerary: {
      oneDay: [
        "경복궁 관람",
        "북촌한옥마을 산책",
        "인사동 전통차 체험",
        "남산서울타워 야경",
      ],
      threeDay: [
        "Day 1: 경복궁·북촌한옥마을·인사동",
        "Day 2: 이태원·한강공원·남산서울타워",
        "Day 3: 홍대·연남동 카페 거리",
      ],
    },
    budget: "1일 기준 숙박 제외 5~8만원(식비·교통·입장료 포함)",
    transport: "지하철·버스 교통카드(T-money) 하나로 전 구간 이용 가능",
    food: ["삼겹살", "떡볶이", "설렁탕"],
    etiquette: [
      "고궁 내 정숙 유지",
      "식당 반찬 재사용 규정 확인",
      "지하철 임산부 배려석 비우기",
    ],
    source: "서울관광재단 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "busan",
    name: "부산",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1200",
    imageAlt: "부산 해운대 해변과 고층 빌딩",
    intro: "해변과 항구, 산복도로 마을이 어우러진 대한민국 제2의 도시.",
    attractions: [
      "해운대해수욕장",
      "감천문화마을",
      "광안리해변",
      "자갈치시장",
      "태종대",
    ],
    itinerary: {
      oneDay: ["해운대해수욕장 산책", "광안리 야경 감상", "자갈치시장 회 식사"],
      threeDay: [
        "Day 1: 해운대·동백섬",
        "Day 2: 감천문화마을·자갈치시장",
        "Day 3: 태종대·광안리",
      ],
    },
    budget: "1일 기준 숙박 제외 4~7만원",
    transport: "부산도시철도 1~4호선, 해안 지역은 버스 환승 추천",
    food: ["돼지국밥", "밀면", "씨앗호떡"],
    etiquette: [
      "해수욕장 지정 구역 내 취식",
      "감천문화마을 주민 생활 공간 존중",
      "시장 흥정은 정중하게",
    ],
    source: "부산관광공사 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "jeju",
    name: "제주",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1544020907-16b9567f7f31?w=1200",
    imageAlt: "제주 성산일출봉과 유채꽃밭",
    intro: "화산지형과 해안 절경이 어우러진 대한민국 최대의 섬 여행지.",
    attractions: ["성산일출봉", "한라산", "협재해수욕장", "우도", "올레길"],
    itinerary: {
      oneDay: ["성산일출봉 일출", "우도 자전거 투어", "협재해수욕장 산책"],
      threeDay: [
        "Day 1: 성산일출봉·우도",
        "Day 2: 한라산 등반",
        "Day 3: 협재해수욕장·올레길",
      ],
    },
    budget: "1일 기준 숙박 제외 6~9만원(렌터카 포함)",
    transport: "렌터카가 사실상 필수, 시내는 버스로도 이동 가능",
    food: ["흑돼지 구이", "고기국수", "갈치조림"],
    etiquette: [
      "한라산 국립공원 입산 시간 준수",
      "해안 사유지 무단 진입 금지",
      "올레길 표지 훼손 금지",
    ],
    source: "제주관광공사 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "gyeongju",
    name: "경주",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1601926639315-6b3e93c22fe5?w=1200",
    imageAlt: "경주 불국사 전경",
    intro: "신라 천년의 역사가 남아있는 대표적인 대한민국 고도(古都).",
    attractions: ["불국사", "석굴암", "대릉원", "동궁과 월지", "첨성대"],
    itinerary: {
      oneDay: ["불국사·석굴암 관람", "대릉원 산책", "동궁과 월지 야경"],
      threeDay: [
        "Day 1: 불국사·석굴암",
        "Day 2: 대릉원·첨성대·동궁과 월지",
        "Day 3: 양동마을·보문호",
      ],
    },
    budget: "1일 기준 숙박 제외 4~6만원",
    transport: "시내버스와 자전거 대여가 유적지 이동에 편리",
    food: ["경주빵", "쌈밥", "한정식"],
    etiquette: [
      "문화재 구역 내 촬영 제한 표시 확인",
      "야간 조명 유적지 정숙",
      "지정 산책로 이용",
    ],
    source: "경주시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "jeonju",
    name: "전주",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1590766940554-153f88b6bff2?w=1200",
    imageAlt: "전주한옥마을 기와지붕 골목",
    intro: "전통 한옥마을과 미식 문화가 살아있는 도시.",
    attractions: ["전주한옥마을", "경기전", "전동성당", "오목대", "남부시장"],
    itinerary: {
      oneDay: ["전주한옥마을 산책", "경기전 관람", "남부시장 야시장"],
      threeDay: [
        "Day 1: 한옥마을·경기전·전동성당",
        "Day 2: 오목대·자만벽화마을",
        "Day 3: 남부시장·모악산",
      ],
    },
    budget: "1일 기준 숙박 제외 4~6만원",
    transport: "한옥마을 일대는 도보, 시외 이동은 시내버스",
    food: ["전주비빔밥", "콩나물국밥", "모주"],
    etiquette: [
      "한복 대여 시 골목 통행 배려",
      "성당 예배 시간 정숙",
      "상점 골목 차량 통행 주의",
    ],
    source: "전주시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "gangneung",
    name: "강릉",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1580996143723-6926fea9fb43?w=1200",
    imageAlt: "강릉 경포호수와 해변",
    intro: "커피 거리와 해변, 호수가 함께 있는 동해안 대표 여행지.",
    attractions: [
      "경포해수욕장",
      "안목해변 커피거리",
      "오죽헌",
      "정동진",
      "주문진항",
    ],
    itinerary: {
      oneDay: ["안목해변 커피거리", "경포호 산책", "정동진 일몰"],
      threeDay: [
        "Day 1: 경포해수욕장·경포호",
        "Day 2: 안목해변 커피거리·주문진항",
        "Day 3: 오죽헌·정동진",
      ],
    },
    budget: "1일 기준 숙박 제외 4~6만원",
    transport: "KTX 강릉선 이용 후 시내버스·택시로 이동",
    food: ["초당순두부", "물회", "커피"],
    etiquette: [
      "해변 캠핑은 지정 구역만",
      "카페거리 야간 소음 자제",
      "항구 조업 구역 접근 주의",
    ],
    source: "강릉시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "yeosu",
    name: "여수",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1601758228041-3caa4e0ff30c?w=1200",
    imageAlt: "여수 밤바다 야경",
    intro: "'여수 밤바다'로 알려진 해안 야경과 케이블카가 유명한 항구도시.",
    attractions: [
      "여수해상케이블카",
      "오동도",
      "이순신광장",
      "여수엑스포해양공원",
      "향일암",
    ],
    itinerary: {
      oneDay: ["여수해상케이블카", "오동도 산책", "이순신광장 야경"],
      threeDay: [
        "Day 1: 해상케이블카·오동도",
        "Day 2: 여수엑스포해양공원·이순신광장",
        "Day 3: 향일암·돌산대교",
      ],
    },
    budget: "1일 기준 숙박 제외 5~7만원(케이블카 포함)",
    transport: "여수엑스포역 하차 후 시내버스로 주요 명소 이동",
    food: ["갓김치", "돌게장", "장어탕"],
    etiquette: [
      "케이블카 탑승 순서 준수",
      "해상 공원 야간 안전선 준수",
      "사찰 경내 정숙",
    ],
    source: "여수시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "sokcho",
    name: "속초",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1592306566659-fecd7539e9d0?w=1200",
    imageAlt: "속초 설악산 단풍",
    intro: "설악산과 동해 바다를 함께 즐길 수 있는 강원도 대표 여행지.",
    attractions: [
      "설악산국립공원",
      "속초해수욕장",
      "속초중앙시장",
      "아바이마을",
      "영금정",
    ],
    itinerary: {
      oneDay: ["속초중앙시장 먹거리", "속초해수욕장 산책", "영금정 일출"],
      threeDay: [
        "Day 1: 설악산 케이블카·비룡폭포",
        "Day 2: 속초해수욕장·아바이마을",
        "Day 3: 속초중앙시장·영금정",
      ],
    },
    budget: "1일 기준 숙박 제외 5~7만원",
    transport: "설악산 방면은 시내버스, 시장 일대는 도보",
    food: ["아바이순대", "물회", "닭강정"],
    etiquette: [
      "국립공원 탐방로 야간 산행 금지",
      "시장 좁은 골목 정체 배려",
      "해변 취사 지정 구역만",
    ],
    source: "속초시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "tongyeong",
    name: "통영",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1541508857-4a3aca8db8ce?w=1200",
    imageAlt: "통영 동피랑마을 벽화 골목",
    intro:
      "동양의 나폴리로 불리는 다도해 항구도시, 벽화마을과 케이블카가 유명.",
    attractions: [
      "동피랑마을",
      "통영케이블카",
      "루지체험장",
      "강구안",
      "한산도",
    ],
    itinerary: {
      oneDay: ["동피랑마을 벽화 산책", "강구안 항구 구경", "통영케이블카 전망"],
      threeDay: [
        "Day 1: 동피랑마을·강구안",
        "Day 2: 통영케이블카·루지체험장",
        "Day 3: 한산도 이순신 유적",
      ],
    },
    budget: "1일 기준 숙박 제외 5~7만원",
    transport: "통영여객터미널에서 도서 지역행 배편 이용",
    food: ["충무김밥", "굴", "멸치쌈밥"],
    etiquette: [
      "벽화마을 주민 사생활 존중",
      "케이블카 탑승 정원 준수",
      "선착장 승선 시간 엄수",
    ],
    source: "통영시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "andong",
    name: "안동",
    country: "대한민국",
    region: "domestic",
    imageUrl:
      "https://images.unsplash.com/photo-1601758260119-0083e4a2f5c9?w=1200",
    imageAlt: "안동하회마을 전통 가옥",
    intro: "유네스코 세계유산 하회마을이 있는 한국 전통문화의 중심지.",
    attractions: ["하회마을", "안동찜닭거리", "월영교", "봉정사", "도산서원"],
    itinerary: {
      oneDay: ["하회마을 관람", "월영교 산책", "안동찜닭거리 식사"],
      threeDay: [
        "Day 1: 하회마을·부용대",
        "Day 2: 봉정사·도산서원",
        "Day 3: 월영교·안동찜닭거리",
      ],
    },
    budget: "1일 기준 숙박 제외 4~6만원",
    transport: "안동역에서 시내버스로 하회마을·서원 이동",
    food: ["안동찜닭", "헛제사밥", "간고등어"],
    etiquette: [
      "하회마을 실거주 가옥 무단 촬영 금지",
      "서원 경내 정숙",
      "전통 다리 야간 통행 주의",
    ],
    source: "안동시 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "tokyo",
    name: "도쿄",
    country: "일본",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200",
    imageAlt: "도쿄 시부야 스크램블 교차로",
    intro:
      "전통과 최첨단이 공존하는 일본의 수도, 쇼핑·미식·문화 명소가 밀집해 있다.",
    attractions: [
      "센소지",
      "시부야 스크램블",
      "신주쿠교엔",
      "아사쿠사",
      "오다이바",
    ],
    itinerary: {
      oneDay: ["센소지·아사쿠사", "시부야 스크램블·하라주쿠", "신주쿠 야경"],
      threeDay: [
        "Day 1: 아사쿠사·우에노",
        "Day 2: 시부야·하라주쿠·신주쿠",
        "Day 3: 오다이바·긴자",
      ],
    },
    budget: "1일 기준 숙박 제외 8~12만원",
    transport: "JR·지하철 1일권(Suica/Pasmo) 활용",
    food: ["스시", "라멘", "돈카츠"],
    etiquette: [
      "대중교통 내 통화 자제",
      "식당 줄서기 순서 준수",
      "쓰레기는 개인 소지 후 처리",
    ],
    source: "일본정부관광국(JNTO) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "osaka",
    name: "오사카",
    country: "일본",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1590559899731-a382839e5549?w=1200",
    imageAlt: "오사카 도톤보리 야경",
    intro: "먹거리와 유머의 도시로 불리는 일본 간사이 지역의 중심 도시.",
    attractions: [
      "도톤보리",
      "오사카성",
      "유니버설 스튜디오 재팬",
      "구로몬시장",
      "신사이바시",
    ],
    itinerary: {
      oneDay: ["도톤보리 먹거리 투어", "오사카성 관람", "신사이바시 쇼핑"],
      threeDay: [
        "Day 1: 도톤보리·구로몬시장",
        "Day 2: 유니버설 스튜디오 재팬",
        "Day 3: 오사카성·신사이바시",
      ],
    },
    budget: "1일 기준 숙박 제외 8~11만원",
    transport: "오사카 지하철·순환버스 1일권",
    food: ["타코야키", "오코노미야키", "쿠시카츠"],
    etiquette: [
      "에스컬레이터 한 줄 서기(오른쪽 비움)",
      "길거리 음식은 이동 중 취식 자제",
      "테마파크 대기열 규칙 준수",
    ],
    source: "일본정부관광국(JNTO) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "bangkok",
    name: "방콕",
    country: "태국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1200",
    imageAlt: "방콕 왓 아룬 사원",
    intro: "사원과 시장, 루프탑 바가 공존하는 동남아시아 대표 관문 도시.",
    attractions: [
      "왓 아룬",
      "왓 프라깨오",
      "카오산로드",
      "차투착 주말시장",
      "아이콘시암",
    ],
    itinerary: {
      oneDay: ["왓 프라깨오·왕궁", "왓 아룬 강변 산책", "카오산로드 야시장"],
      threeDay: [
        "Day 1: 왕궁·왓 아룬",
        "Day 2: 차투착 주말시장·아이콘시암",
        "Day 3: 카오산로드·루프탑 바",
      ],
    },
    budget: "1일 기준 숙박 제외 5~8만원",
    transport: "BTS/MRT 전철과 톡톡, 그랩(Grab) 앱 활용",
    food: ["똠얌꿍", "팟타이", "망고 스티키라이스"],
    etiquette: [
      "사원 방문 시 어깨·무릎 가리는 복장",
      "왕실 관련 발언 주의",
      "머리 쓰다듬기 금지",
    ],
    source: "태국관광청(TAT) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "chiangmai",
    name: "치앙마이",
    country: "태국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1598935888738-cd2622cce4f7?w=1200",
    imageAlt: "치앙마이 도이수텝 사원",
    intro: "고대 사원과 산악 자연이 어우러진 태국 북부의 문화 중심지.",
    attractions: [
      "도이수텝 사원",
      "올드시티",
      "님만해민",
      "쑤언 도크마이 시장",
      "매림 정글 트레킹",
    ],
    itinerary: {
      oneDay: ["올드시티 사원 투어", "님만해민 카페 거리", "선데이 마켓"],
      threeDay: [
        "Day 1: 올드시티·왓프라싱",
        "Day 2: 도이수텝·매림 트레킹",
        "Day 3: 님만해민·야시장",
      ],
    },
    budget: "1일 기준 숙박 제외 4~7만원",
    transport: "썽태우(합승 트럭)와 그랩(Grab) 앱",
    food: ["카오소이", "쏨땀", "사이우아"],
    etiquette: [
      "사원 경내 신발 벗고 입장",
      "코끼리 체험은 보호구역만 선택",
      "합승 요금 사전 확인",
    ],
    source: "태국관광청(TAT) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "hanoi",
    name: "하노이",
    country: "베트남",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?w=1200",
    imageAlt: "하노이 호안끼엠 호수",
    intro: "프랑스풍 건축과 전통 시장이 공존하는 베트남의 역사적인 수도.",
    attractions: [
      "호안끼엠 호수",
      "구시가지",
      "호치민 영묘",
      "번화가 짜짱티",
      "탕롱 수상인형극장",
    ],
    itinerary: {
      oneDay: ["호안끼엠 호수 산책", "구시가지 골목 투어", "수상인형극 관람"],
      threeDay: [
        "Day 1: 호안끼엠·구시가지",
        "Day 2: 호치민 영묘·문묘",
        "Day 3: 하롱베이 데이투어",
      ],
    },
    budget: "1일 기준 숙박 제외 3~6만원",
    transport: "그랩(Grab) 오토바이/차량, 도보로 구시가지 이동",
    food: ["퍼(쌀국수)", "분짜", "에그 커피"],
    etiquette: [
      "도로 횡단 시 일정한 속도로 걷기",
      "영묘 방문 시 정숙한 복장",
      "오토바이 흐름 주의",
    ],
    source: "베트남 국가관광청 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "danang",
    name: "다낭",
    country: "베트남",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1200",
    imageAlt: "다낭 미케 해변과 용다리",
    intro:
      "해변 리조트와 근교 고대 도시가 함께 있는 베트남 중부의 인기 여행지.",
    attractions: ["미케 해변", "용다리", "바나힐", "호이안 구시가지", "오행산"],
    itinerary: {
      oneDay: ["미케 해변 산책", "용다리 야경", "다낭 대성당"],
      threeDay: [
        "Day 1: 미케 해변·용다리",
        "Day 2: 바나힐 골든브릿지",
        "Day 3: 호이안 구시가지",
      ],
    },
    budget: "1일 기준 숙박 제외 3~6만원",
    transport: "그랩(Grab) 차량, 호이안까지는 택시·셔틀",
    food: ["미꽝", "반쎄오", "반미"],
    etiquette: [
      "호이안 구시가지 등불 훼손 금지",
      "해변 리조트 구역 경계 준수",
      "사원 방문 시 정숙",
    ],
    source: "베트남 국가관광청 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "singapore-city",
    name: "싱가포르",
    country: "싱가포르",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1200",
    imageAlt: "싱가포르 마리나베이 스카이라인",
    intro: "정원 도시로 불리는 동남아시아의 대표 국제 허브 도시국가.",
    attractions: [
      "마리나베이 샌즈",
      "가든스 바이 더 베이",
      "머라이언 파크",
      "차이나타운",
      "리버사이드",
    ],
    itinerary: {
      oneDay: [
        "마리나베이 샌즈·머라이언 파크",
        "가든스 바이 더 베이",
        "클락키 야경",
      ],
      threeDay: [
        "Day 1: 마리나베이·가든스 바이 더 베이",
        "Day 2: 센토사·유니버설 스튜디오",
        "Day 3: 차이나타운·리틀인디아",
      ],
    },
    budget: "1일 기준 숙박 제외 8~12만원",
    transport: "MRT 전철과 EZ-Link 카드",
    food: ["칠리크랩", "하이난 치킨라이스", "락사"],
    etiquette: [
      "대중교통 내 음식 섭취 금지",
      "무단횡단 벌금 유의",
      "쓰레기 무단 투기 벌금 유의",
    ],
    source: "싱가포르관광청(STB) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "sentosa",
    name: "센토사",
    country: "싱가포르",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200",
    imageAlt: "센토사 실로소 해변",
    intro: "테마파크와 해변 리조트가 모여있는 싱가포르 본섬 인근의 휴양 섬.",
    attractions: [
      "유니버설 스튜디오 싱가포르",
      "실로소 해변",
      "SEA 아쿠아리움",
      "스카이라인 루지",
      "머라이언 타워",
    ],
    itinerary: {
      oneDay: [
        "유니버설 스튜디오 싱가포르",
        "실로소 해변 산책",
        "스카이라인 루지",
      ],
      threeDay: [
        "Day 1: 유니버설 스튜디오·SEA 아쿠아리움",
        "Day 2: 실로소 해변·워터파크",
        "Day 3: 스카이라인 루지·케이블카",
      ],
    },
    budget: "1일 기준 숙박 제외 10~15만원(테마파크 입장 포함)",
    transport: "센토사 익스프레스 모노레일 또는 케이블카",
    food: ["시푸드 BBQ", "락사", "칠리크랩"],
    etiquette: [
      "해변 지정 구역 내 음주",
      "테마파크 대기열 규칙 준수",
      "야간 해변 소음 자제",
    ],
    source: "싱가포르관광청(STB) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "paris",
    name: "파리",
    country: "프랑스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200",
    imageAlt: "파리 에펠탑 전경",
    intro:
      "예술과 낭만의 도시로 불리는 프랑스의 수도, 박물관과 건축이 밀집해 있다.",
    attractions: [
      "에펠탑",
      "루브르 박물관",
      "노트르담 대성당",
      "몽마르트르",
      "샹젤리제",
    ],
    itinerary: {
      oneDay: ["루브르 박물관", "노트르담 대성당·시테섬", "에펠탑 야경"],
      threeDay: [
        "Day 1: 루브르·튈르리 정원",
        "Day 2: 에펠탑·샹젤리제·개선문",
        "Day 3: 몽마르트르·오르세 미술관",
      ],
    },
    budget: "1일 기준 숙박 제외 10~15만원",
    transport: "메트로 1일 교통권(Navigo)",
    food: ["크루아상", "에스카르고", "마카롱"],
    etiquette: [
      "식당 입장 시 인사 필수",
      "박물관 내 플래시 촬영 금지",
      "소매치기 주의로 소지품 관리",
    ],
    source: "프랑스관광청(Atout France) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "nice",
    name: "니스",
    country: "프랑스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1491166617655-0723a0999cfc?w=1200",
    imageAlt: "니스 프롬나드 데 장글레 해변",
    intro:
      "지중해 코트다쥐르의 중심 도시로, 파스텔톤 건물과 해변 산책로가 유명하다.",
    attractions: [
      "프롬나드 데 장글레",
      "구시가지",
      "콜린 뒤 샤토",
      "니스 대성당",
      "마세나 광장",
    ],
    itinerary: {
      oneDay: [
        "프롬나드 데 장글레 산책",
        "구시가지 시장",
        "콜린 뒤 샤토 전망대",
      ],
      threeDay: [
        "Day 1: 프롬나드 데 장글레·구시가지",
        "Day 2: 에즈 마을 당일투어",
        "Day 3: 마세나 광장·현대미술관",
      ],
    },
    budget: "1일 기준 숙박 제외 8~12만원",
    transport: "트램과 버스 1일권",
    food: ["살라드 니스와즈", "소카(병아리콩 크레페)", "라따뚜이"],
    etiquette: [
      "해변 상의 탈의 구역 구분 준수",
      "구시가지 좁은 골목 차량 통행 주의",
      "레스토랑 팁은 선택 사항",
    ],
    source: "프랑스관광청(Atout France) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "rome",
    name: "로마",
    country: "이탈리아",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200",
    imageAlt: "로마 콜로세움",
    intro: "고대 로마 제국의 유적이 도시 전역에 남아있는 이탈리아의 수도.",
    attractions: [
      "콜로세움",
      "바티칸 시국",
      "트레비 분수",
      "판테온",
      "스페인 광장",
    ],
    itinerary: {
      oneDay: [
        "콜로세움·포로 로마노",
        "트레비 분수·판테온",
        "스페인 광장 야경",
      ],
      threeDay: [
        "Day 1: 콜로세움·포로 로마노",
        "Day 2: 바티칸 시국·성 베드로 대성당",
        "Day 3: 트레비 분수·판테온·나보나 광장",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "메트로·버스 1일권, 유적지 밀집 구역은 도보",
    food: ["카르보나라", "젤라또", "수플리"],
    etiquette: [
      "성당 방문 시 어깨·무릎 가리는 복장",
      "분수 물에 손 담그지 않기",
      "유적지 낙서·훼손 금지",
    ],
    source: "이탈리아관광청(ENIT) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "florence",
    name: "피렌체",
    country: "이탈리아",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1543832923-44667a44c804?w=1200",
    imageAlt: "피렌체 두오모 대성당 전경",
    intro: "르네상스 예술의 발상지로 불리는 토스카나 지역의 문화 중심 도시.",
    attractions: [
      "두오모 대성당",
      "우피치 미술관",
      "베키오 다리",
      "미켈란젤로 광장",
      "피티 궁전",
    ],
    itinerary: {
      oneDay: [
        "두오모 대성당",
        "우피치 미술관",
        "베키오 다리·미켈란젤로 광장 야경",
      ],
      threeDay: [
        "Day 1: 두오모·우피치 미술관",
        "Day 2: 피티 궁전·보볼리 정원",
        "Day 3: 베키오 다리·미켈란젤로 광장",
      ],
    },
    budget: "1일 기준 숙박 제외 8~12만원",
    transport: "도심 대부분 도보 이동, 근교는 버스",
    food: ["비스테카 알라 피오렌티나", "판자넬라", "젤라또"],
    etiquette: [
      "미술관 사전 예약 권장",
      "성당 내 정숙 유지",
      "좁은 골목 자전거·차량 주의",
    ],
    source: "이탈리아관광청(ENIT) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "barcelona",
    name: "바르셀로나",
    country: "스페인",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=1200",
    imageAlt: "바르셀로나 사그라다 파밀리아",
    intro: "가우디 건축과 지중해 해변이 함께 있는 스페인 카탈루냐의 중심 도시.",
    attractions: [
      "사그라다 파밀리아",
      "구엘 공원",
      "람블라 거리",
      "바르셀로네타 해변",
      "고딕 지구",
    ],
    itinerary: {
      oneDay: ["사그라다 파밀리아", "구엘 공원", "람블라 거리·고딕 지구"],
      threeDay: [
        "Day 1: 사그라다 파밀리아·구엘 공원",
        "Day 2: 고딕 지구·람블라 거리",
        "Day 3: 바르셀로네타 해변·몬주익",
      ],
    },
    budget: "1일 기준 숙박 제외 8~12만원",
    transport: "메트로 T-casual 카드",
    food: ["타파스", "파에야", "판 콘 토마테"],
    etiquette: [
      "소매치기 주의로 소지품 관리",
      "성당 내부 정숙 및 복장 규정 준수",
      "해변 소지품 방치 금지",
    ],
    source: "스페인관광청(Turespaña) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "madrid",
    name: "마드리드",
    country: "스페인",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1200",
    imageAlt: "마드리드 시벨레스 광장",
    intro: "왕궁과 세계적인 미술관이 모여있는 스페인의 수도.",
    attractions: [
      "왕궁",
      "프라도 미술관",
      "레티로 공원",
      "마요르 광장",
      "그란비아",
    ],
    itinerary: {
      oneDay: ["왕궁·마요르 광장", "프라도 미술관", "그란비아 야경"],
      threeDay: [
        "Day 1: 왕궁·마요르 광장",
        "Day 2: 프라도 미술관·레티로 공원",
        "Day 3: 그란비아·솔 광장",
      ],
    },
    budget: "1일 기준 숙박 제외 7~10만원",
    transport: "메트로 10회권(Metrobús)",
    food: ["하몽", "츄러스", "코시도 마드리레뇨"],
    etiquette: [
      "식사 시간이 늦은 편임을 감안",
      "미술관 사진 촬영 제한 확인",
      "광장 소매치기 주의",
    ],
    source: "스페인관광청(Turespaña) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "london",
    name: "런던",
    country: "영국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200",
    imageAlt: "런던 빅벤과 웨스트민스터 다리",
    intro: "역사적 랜드마크와 현대 문화가 공존하는 영국의 수도.",
    attractions: [
      "빅벤·국회의사당",
      "타워브리지",
      "대영박물관",
      "버킹엄 궁전",
      "런던아이",
    ],
    itinerary: {
      oneDay: ["빅벤·웨스트민스터", "대영박물관", "타워브리지 야경"],
      threeDay: [
        "Day 1: 빅벤·웨스트민스터·버킹엄 궁전",
        "Day 2: 대영박물관·코벤트 가든",
        "Day 3: 타워브리지·런던아이",
      ],
    },
    budget: "1일 기준 숙박 제외 10~14만원",
    transport: "오이스터 카드로 지하철·버스 이용",
    food: ["피시 앤 칩스", "애프터눈 티", "선데이 로스트"],
    etiquette: [
      "에스컬레이터 오른쪽 서기·왼쪽 걷기",
      "펍 이용 시 카운터에서 직접 주문",
      "줄서기 문화 존중",
    ],
    source: "영국관광청(VisitBritain) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "edinburgh",
    name: "에든버러",
    country: "영국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    imageAlt: "에든버러 성과 구시가지",
    intro: "중세 성과 축제 문화가 살아있는 스코틀랜드의 수도.",
    attractions: [
      "에든버러 성",
      "로열 마일",
      "아서시트",
      "홀리루드 궁전",
      "칼튼힐",
    ],
    itinerary: {
      oneDay: ["에든버러 성", "로열 마일 산책", "칼튼힐 야경"],
      threeDay: [
        "Day 1: 에든버러 성·로열 마일",
        "Day 2: 아서시트 등산·홀리루드 궁전",
        "Day 3: 칼튼힐·근교 하이랜드 투어",
      ],
    },
    budget: "1일 기준 숙박 제외 8~11만원",
    transport: "도심은 도보, 근교는 버스·기차",
    food: ["해기스", "스코티시 브렉퍼스트", "위스키 테이스팅"],
    etiquette: [
      "성 내부 촬영 제한 구역 확인",
      "아서시트 등산로 야간 이용 자제",
      "축제 기간 예약 필수",
    ],
    source: "영국관광청(VisitBritain) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "newyork",
    name: "뉴욕",
    country: "미국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1200",
    imageAlt: "뉴욕 맨해튼 스카이라인",
    intro: "세계 금융과 문화의 중심지로 불리는 미국 최대의 도시.",
    attractions: [
      "타임스퀘어",
      "센트럴파크",
      "자유의 여신상",
      "브루클린 브릿지",
      "메트로폴리탄 미술관",
    ],
    itinerary: {
      oneDay: [
        "타임스퀘어·센트럴파크",
        "메트로폴리탄 미술관",
        "브루클린 브릿지 야경",
      ],
      threeDay: [
        "Day 1: 타임스퀘어·센트럴파크",
        "Day 2: 자유의 여신상·월스트리트",
        "Day 3: 브루클린 브릿지·메트로폴리탄 미술관",
      ],
    },
    budget: "1일 기준 숙박 제외 12~18만원",
    transport: "지하철 7일 무제한 메트로카드",
    food: ["뉴욕 스타일 피자", "베이글", "치즈케이크"],
    etiquette: [
      "지하철 탑승 시 하차객 먼저 배려",
      "레스토랑 팁 15~20% 관행",
      "횡단보도 신호 준수",
    ],
    source: "미국관광청(Brand USA) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "losangeles",
    name: "로스앤젤레스",
    country: "미국",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1544413660-299165566b1d?w=1200",
    imageAlt: "로스앤젤레스 산타모니카 해변",
    intro: "할리우드와 해변 문화가 공존하는 미국 서부의 대표 도시.",
    attractions: [
      "할리우드 사인",
      "산타모니카 해변",
      "그리피스 천문대",
      "게티 센터",
      "베니스 비치",
    ],
    itinerary: {
      oneDay: [
        "할리우드 사인·그리피스 천문대",
        "산타모니카 해변",
        "베니스 비치 야경",
      ],
      threeDay: [
        "Day 1: 할리우드·그리피스 천문대",
        "Day 2: 산타모니카·베니스 비치",
        "Day 3: 게티 센터·근교 당일투어",
      ],
    },
    budget: "1일 기준 숙박 제외 10~15만원(렌터카 포함)",
    transport: "렌터카가 사실상 필수, 시내는 메트로 일부 구간",
    food: ["타코", "인앤아웃 버거", "포케볼"],
    etiquette: [
      "렌터카 주차 규정 준수",
      "해변 일몰 시간 이후 인적 드문 구역 주의",
      "고속도로 통행료 시스템 확인",
    ],
    source: "미국관광청(Brand USA) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "vancouver",
    name: "밴쿠버",
    country: "캐나다",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1560814304-4f05b62af116?w=1200",
    imageAlt: "밴쿠버 스탠리 파크와 스카이라인",
    intro: "산과 바다를 동시에 즐길 수 있는 캐나다 서부의 대표 도시.",
    attractions: [
      "스탠리 파크",
      "그랜빌 아일랜드",
      "캐필라노 흔들다리",
      "개스타운",
      "그라우스 마운틴",
    ],
    itinerary: {
      oneDay: [
        "스탠리 파크 산책",
        "그랜빌 아일랜드 마켓",
        "개스타운 저녁 산책",
      ],
      threeDay: [
        "Day 1: 스탠리 파크·개스타운",
        "Day 2: 캐필라노 흔들다리·그라우스 마운틴",
        "Day 3: 그랜빌 아일랜드·근교 휘슬러 당일투어",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "스카이트레인·버스 콤파스 카드",
    food: ["연어 요리", "푸틴", "덤섬"],
    etiquette: [
      "야외 활동 시 야생동물 접근 자제",
      "대중교통 내 정숙",
      "국립공원 지정 트레일 이용",
    ],
    source: "캐나다관광청(Destination Canada) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "toronto",
    name: "토론토",
    country: "캐나다",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1517090504586-fde19ea6066f?w=1200",
    imageAlt: "토론토 CN 타워와 스카이라인",
    intro: "다문화가 어우러진 캐나다 최대의 경제·문화 도시.",
    attractions: [
      "CN 타워",
      "카사 로마",
      "온타리오 호수",
      "케싱턴 마켓",
      "나이아가라 폭포(근교)",
    ],
    itinerary: {
      oneDay: ["CN 타워 전망대", "카사 로마 관람", "케싱턴 마켓 저녁"],
      threeDay: [
        "Day 1: CN 타워·다운타운",
        "Day 2: 나이아가라 폭포 당일투어",
        "Day 3: 카사 로마·케싱턴 마켓",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "TTC 지하철·스트리트카 1일권",
    food: ["푸틴", "페미컨 스타일 스튜", "메이플 시럽 디저트"],
    etiquette: [
      "대중교통 탑승 시 요금 선결제",
      "나이아가라 방문 시 우비 구간 안전선 준수",
      "겨울철 방한 대비 필수",
    ],
    source: "캐나다관광청(Destination Canada) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "sydney",
    name: "시드니",
    country: "호주",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200",
    imageAlt: "시드니 오페라 하우스와 하버브릿지",
    intro: "오페라 하우스와 해변이 함께 있는 호주 최대의 항구 도시.",
    attractions: [
      "시드니 오페라 하우스",
      "하버브릿지",
      "본다이 비치",
      "달링 하버",
      "타롱가 동물원",
    ],
    itinerary: {
      oneDay: [
        "오페라 하우스·하버브릿지",
        "달링 하버 산책",
        "본다이 비치 일몰",
      ],
      threeDay: [
        "Day 1: 오페라 하우스·하버브릿지",
        "Day 2: 본다이 비치·쿠지 해안 산책로",
        "Day 3: 달링 하버·타롱가 동물원",
      ],
    },
    budget: "1일 기준 숙박 제외 10~14만원",
    transport: "오팔 카드로 전철·버스·페리 이용",
    food: ["플랫 화이트 커피", "미트 파이", "피시 앤 칩스"],
    etiquette: [
      "해변 국기 표시 안전 구역 내 수영",
      "자외선이 강해 자외선 차단제 필수",
      "국립공원 트레일 지정 경로 이용",
    ],
    source: "호주관광청(Tourism Australia) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "melbourne",
    name: "멜버른",
    country: "호주",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1514395462725-fb4566210144?w=1200",
    imageAlt: "멜버른 시내 트램과 골목 카페",
    intro: "카페 문화와 골목 예술이 발달한 호주 남동부의 문화 도시.",
    attractions: [
      "페더레이션 스퀘어",
      "호시어 레인",
      "그레이트 오션 로드(근교)",
      "퀸빅토리아 마켓",
      "야라 강변",
    ],
    itinerary: {
      oneDay: [
        "페더레이션 스퀘어·호시어 레인",
        "퀸빅토리아 마켓",
        "야라 강변 산책",
      ],
      threeDay: [
        "Day 1: 시내 트램 투어·호시어 레인",
        "Day 2: 그레이트 오션 로드 당일투어",
        "Day 3: 퀸빅토리아 마켓·야라 강변",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "무료 시내 순환 트램(City Circle)",
    food: ["플랫 화이트 커피", "미트 파이", "브런치 요리"],
    etiquette: [
      "트램 탑승 시 요금 구역 확인",
      "골목 예술 훼손 금지",
      "근교 투어 예약 시간 준수",
    ],
    source: "호주관광청(Tourism Australia) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "auckland",
    name: "오클랜드",
    country: "뉴질랜드",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=1200",
    imageAlt: "오클랜드 스카이타워와 항구",
    intro: "화산과 항구가 어우러진 뉴질랜드 최대의 도시.",
    attractions: [
      "스카이타워",
      "오클랜드 항구",
      "랑기토토 섬",
      "마운트 이든",
      "데본포트",
    ],
    itinerary: {
      oneDay: ["스카이타워 전망대", "오클랜드 항구 산책", "데본포트 페리 투어"],
      threeDay: [
        "Day 1: 스카이타워·항구",
        "Day 2: 랑기토토 섬 당일투어",
        "Day 3: 마운트 이든·데본포트",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "AT HOP 카드로 버스·페리 이용",
    food: ["미트 파이", "그린쉘 홍합", "파블로바"],
    etiquette: [
      "화산 보호구역 지정 트레일 이용",
      "페리 승선 시간 여유 있게 도착",
      "마오리 문화유산 존중",
    ],
    source: "뉴질랜드관광청(Tourism New Zealand) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "queenstown",
    name: "퀸스타운",
    country: "뉴질랜드",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1589802757409-a30f95cc4c14?w=1200",
    imageAlt: "퀸스타운 와카티푸 호수와 산맥",
    intro: "액티비티의 수도로 불리는 뉴질랜드 남섬의 산악 호수 도시.",
    attractions: [
      "와카티푸 호수",
      "스카이라인 곤돌라",
      "밀포드 사운드(근교)",
      "글레노키",
      "퀸스타운 힐 워크",
    ],
    itinerary: {
      oneDay: ["스카이라인 곤돌라", "와카티푸 호수 산책", "퀸스타운 힐 워크"],
      threeDay: [
        "Day 1: 스카이라인 곤돌라·와카티푸 호수",
        "Day 2: 밀포드 사운드 당일투어",
        "Day 3: 글레노키·번지점프 체험",
      ],
    },
    budget: "1일 기준 숙박 제외 10~15만원(액티비티 포함)",
    transport: "렌터카 또는 투어 셔틀버스",
    food: ["퍼거버거", "그린쉘 홍합", "마운트 쿡 연어"],
    etiquette: [
      "액티비티 예약 시 날씨 취소 정책 확인",
      "산악 트레일 안전 장비 지참",
      "빙하 지역 가이드 동행 권장",
    ],
    source: "뉴질랜드관광청(Tourism New Zealand) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "istanbul",
    name: "이스탄불",
    country: "터키",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200",
    imageAlt: "이스탄불 술탄아흐메트 모스크",
    intro:
      "유럽과 아시아를 잇는 다리 위의 도시, 오스만 제국의 유산이 남아있다.",
    attractions: [
      "아야소피아",
      "술탄아흐메트 모스크",
      "그랜드 바자르",
      "갈라타 타워",
      "보스포루스 해협",
    ],
    itinerary: {
      oneDay: [
        "아야소피아·술탄아흐메트 모스크",
        "그랜드 바자르",
        "갈라타 타워 야경",
      ],
      threeDay: [
        "Day 1: 아야소피아·술탄아흐메트",
        "Day 2: 그랜드 바자르·갈라타 타워",
        "Day 3: 보스포루스 해협 크루즈",
      ],
    },
    budget: "1일 기준 숙박 제외 6~9만원",
    transport: "이스탄불카트로 트램·페리 이용",
    food: ["케밥", "터키식 아이스크림(돈두르마)", "바클라바"],
    etiquette: [
      "모스크 방문 시 신발 벗고 여성은 머리 가리개 준비",
      "시장 흥정 문화 존중",
      "라마단 기간 공공장소 식사 주의",
    ],
    source: "터키문화관광부 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "cappadocia",
    name: "카파도키아",
    country: "터키",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200",
    imageAlt: "카파도키아 열기구와 기암지대",
    intro: "기암괴석 지형과 열기구 투어로 유명한 터키 중부의 이색 여행지.",
    attractions: [
      "괴레메 야외 박물관",
      "열기구 투어",
      "데린쿠유 지하도시",
      "카이막클르",
      "위치사르 성",
    ],
    itinerary: {
      oneDay: ["열기구 투어(일출)", "괴레메 야외 박물관", "위치사르 성 전망"],
      threeDay: [
        "Day 1: 열기구 투어·괴레메 야외 박물관",
        "Day 2: 데린쿠유 지하도시·카이막클르",
        "Day 3: 위치사르 성·붉은 계곡 하이킹",
      ],
    },
    budget: "1일 기준 숙박 제외 7~11만원(열기구 투어 포함)",
    transport: "투어 셔틀버스 또는 렌터카",
    food: ["테스티 케밥", "만티(터키식 만두)", "석류즙"],
    etiquette: [
      "열기구 탑승 전 기상 취소 가능성 확인",
      "지하도시 저지대 이동 시 안내자 동행",
      "동굴 호텔 화기 사용 주의",
    ],
    source: "터키문화관광부 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "athens",
    name: "아테네",
    country: "그리스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1555993539-1732b0258235?w=1200",
    imageAlt: "아테네 파르테논 신전",
    intro: "고대 서양 문명의 발상지로 불리는 그리스의 수도.",
    attractions: [
      "파르테논 신전",
      "아크로폴리스",
      "플라카 지구",
      "고대 아고라",
      "국립고고학박물관",
    ],
    itinerary: {
      oneDay: ["아크로폴리스·파르테논 신전", "고대 아고라", "플라카 지구 저녁"],
      threeDay: [
        "Day 1: 아크로폴리스·파르테논 신전",
        "Day 2: 국립고고학박물관·고대 아고라",
        "Day 3: 플라카 지구·리카비토스 언덕",
      ],
    },
    budget: "1일 기준 숙박 제외 7~10만원",
    transport: "아테네 메트로 1일권",
    food: ["수블라키", "무사카", "그릭 요거트"],
    etiquette: [
      "유적지 오르막 통행 시 미끄럼 주의",
      "박물관 사진 촬영 제한 확인",
      "한낮 폭염 시 야외 관람 시간 조정",
    ],
    source: "그리스관광청(GNTO) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "santorini",
    name: "산토리니",
    country: "그리스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1200",
    imageAlt: "산토리니 이아 마을 하얀 건물과 청록색 지붕",
    intro: "화산섬 위 하얀 마을과 에게해 일몰로 유명한 그리스의 대표 섬.",
    attractions: [
      "이아 마을",
      "피라 마을",
      "붉은 해변",
      "고대 티라 유적",
      "아크로티리 유적",
    ],
    itinerary: {
      oneDay: ["이아 마을 일몰", "피라 마을 산책", "붉은 해변"],
      threeDay: [
        "Day 1: 피라 마을·고대 티라 유적",
        "Day 2: 이아 마을·일몰 명소",
        "Day 3: 아크로티리 유적·와이너리 투어",
      ],
    },
    budget: "1일 기준 숙박 제외 9~13만원",
    transport: "렌터카 또는 로컬 버스",
    food: ["파바(그리스 완두콩 퓨레)", "토마토케프테데스", "산토리니 와인"],
    etiquette: [
      "일몰 명소는 자리 선점 시간이 필요함",
      "좁은 골목 마을 차량 진입 제한 확인",
      "해변 화산석 절벽 접근 주의",
    ],
    source: "그리스관광청(GNTO) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "zurich",
    name: "취리히",
    country: "스위스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=1200",
    imageAlt: "취리히 호수와 구시가지",
    intro: "호수와 알프스를 배경으로 한 스위스 최대의 금융·문화 도시.",
    attractions: [
      "취리히 호수",
      "린덴호프",
      "구시가지",
      "반호프 거리",
      "그로스뮌스터",
    ],
    itinerary: {
      oneDay: ["구시가지·린덴호프", "반호프 거리 쇼핑", "취리히 호수 크루즈"],
      threeDay: [
        "Day 1: 구시가지·그로스뮌스터",
        "Day 2: 취리히 호수 크루즈·반호프 거리",
        "Day 3: 근교 알프스 전망대 당일투어",
      ],
    },
    budget: "1일 기준 숙박 제외 12~17만원",
    transport: "취리히 카드로 트램·버스·보트 이용",
    food: ["퐁뒤", "라클레트", "취리히 게슈니첼테스"],
    etiquette: [
      "대중교통 정시 운행 관행 존중",
      "일요일 상점 휴무 많음을 감안",
      "산악 지역 일교차 대비",
    ],
    source: "스위스관광청(Switzerland Tourism) 공개 자료",
    updatedAt: "2026-01-05",
  },
  {
    id: "interlaken",
    name: "인터라켄",
    country: "스위스",
    region: "overseas",
    imageUrl:
      "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1200",
    imageAlt: "인터라켄과 융프라우 산맥",
    intro: "융프라우 등 알프스 명산으로 향하는 관문이자 액티비티의 중심지.",
    attractions: [
      "융프라우요흐",
      "하더쿨름 전망대",
      "브리엔츠 호수",
      "툰 호수",
      "쉴트호른",
    ],
    itinerary: {
      oneDay: ["하더쿨름 전망대", "브리엔츠 호수 산책", "인터라켄 시내"],
      threeDay: [
        "Day 1: 하더쿨름·브리엔츠 호수",
        "Day 2: 융프라우요흐 당일투어",
        "Day 3: 쉴트호른·툰 호수",
      ],
    },
    budget: "1일 기준 숙박 제외 13~18만원(등산열차 포함)",
    transport: "등산열차·케이블카, 시내는 도보",
    food: ["퐁뒤", "알프스 치즈 요리", "뢰스티"],
    etiquette: [
      "고산 지역 방한복 필수 지참",
      "등산열차 예약 시간 준수",
      "패러글라이딩 등 액티비티 안전 규정 준수",
    ],
    source: "스위스관광청(Switzerland Tourism) 공개 자료",
    updatedAt: "2026-01-05",
  },
];

export const domesticDestinations = destinations.filter(
  (d) => d.region === "domestic",
);
export const overseasDestinations = destinations.filter(
  (d) => d.region === "overseas",
);
