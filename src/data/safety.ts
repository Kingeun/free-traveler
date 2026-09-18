// DATA-SAFETY: 해외 국가 안전정보 정적 데이터(DB 미사용). REQ-FUNC-046~048·053,
// REQ-NF-027 참고. destinations.ts에 게시된 모든 해외 국가(overseas)는 이 파일에
// 정확히 1개의 SafetyInfo 레코드를 가져야 한다(1:1 매핑, REQ-FUNC-046/REQ-NF-027) —
// 이 최소 커버리지는 DATA-VALIDATION-SCRIPT Task(별도 Wave, 아직 미구현)가
// build 전에 자동으로 강제할 예정이다.

import { overseasDestinations } from "./destinations";

export interface SafetyCategories {
  security: string;
  scam: string;
  law: string;
  disaster: string;
  health: string;
  culture: string;
  traffic: string;
  emergencyContacts: string;
}

export interface SafetyInfo {
  country: string;
  categories: SafetyCategories;
  source: string;
  sourceUrl: string;
  checkedAt: string;
  editor: string;
}

export const safetyInfoByCountry: Record<string, SafetyInfo> = {
  일본: {
    country: "일본",
    categories: {
      security: "전반적으로 치안이 양호하나 관광지 소매치기는 드물게 발생한다.",
      scam: "다카다노바바 등 유흥가의 바가지 요금 유인(캐치바) 사기에 주의한다.",
      law: "길거리 흡연 금지 구역이 많고 위반 시 벌금이 부과될 수 있다.",
      disaster: "지진·태풍 다발 지역으로 숙소의 대피 경로를 미리 확인한다.",
      health: "여행자 보험 가입을 권장하며 의료비가 높은 편이다.",
      culture:
        "신발을 벗고 들어가는 실내 공간이 많고 대중교통 내 통화는 자제한다.",
      traffic: "차량이 좌측 통행이므로 도로 횡단 시 방향에 주의한다.",
      emergencyContacts:
        "긴급전화 110(경찰)/119(구급·화재), 주일본 대한민국 대사관 영사콜센터 +82-2-3210-0404",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  태국: {
    country: "태국",
    categories: {
      security: "관광지 소매치기·핸드백 날치기에 주의가 필요하다.",
      scam: "보석·투어 바가지 상술, 가짜 사원 안내인 사기가 흔하다.",
      law: "왕실 모독죄가 엄격히 처벌되며 사원 방문 시 복장 규정을 지켜야 한다.",
      disaster: "우기(5~10월) 홍수·산사태 가능성을 사전에 확인한다.",
      health: "뎅기열 등 모기 매개 질병 예방을 위해 방충제를 준비한다.",
      culture: "왕실·불상 관련 발언과 행동에 특히 주의한다.",
      traffic: "톡톡·오토바이 택시 이용 시 요금을 사전에 협의한다.",
      emergencyContacts:
        "긴급전화 191(경찰)/1669(구급), 주태국 대한민국 대사관 +66-2-481-6000",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  베트남: {
    country: "베트남",
    categories: {
      security: "번화가에서 오토바이를 이용한 날치기 사고가 종종 발생한다.",
      scam: "택시 미터기 조작, 환전소 바가지 환율에 주의한다.",
      law: "마약류에 대해 매우 엄격한 처벌(사형 포함)이 적용된다.",
      disaster: "중부 지역은 우기에 홍수·태풍 영향을 받을 수 있다.",
      health:
        "생수 이외의 수돗물 섭취를 피하고 노점 음식은 위생 상태를 확인한다.",
      culture: "사원·영묘 방문 시 정숙한 복장과 태도를 지킨다.",
      traffic: "오토바이 통행량이 많아 도로 횡단 시 일정한 속도로 건넌다.",
      emergencyContacts:
        "긴급전화 113(경찰)/115(구급), 주베트남 대한민국 대사관 +84-24-3771-0404",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  싱가포르: {
    country: "싱가포르",
    categories: {
      security: "치안이 매우 우수하나 야간 유흥가에서는 소지품을 관리한다.",
      scam: "관광지 인근 고가 렌트/투어 상술에 유의한다.",
      law: "무단횡단, 껌 반입, 쓰레기 투기에 높은 벌금이 부과된다.",
      disaster: "열대성 폭우로 인한 일시적 침수에 대비한다.",
      health: "의료 수준은 높지만 진료비가 비싼 편이라 보험이 필요하다.",
      culture: "다민족 사회로 종교·민족 관련 발언에 주의한다.",
      traffic: "대중교통이 매우 편리해 차량 렌트가 거의 필요하지 않다.",
      emergencyContacts:
        "긴급전화 999(경찰)/995(구급·화재), 주싱가포르 대한민국 대사관 +65-6256-1188",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  프랑스: {
    country: "프랑스",
    categories: {
      security: "관광지·대중교통에서 소매치기와 집단 절도가 빈번하다.",
      scam: "가짜 서명 모금, 팔찌 강매 사기에 주의한다.",
      law: "공공장소 흡연 제한 구역이 있고 시위 지역 접근을 피해야 한다.",
      disaster: "폭염기 온열질환에 대비해 수분을 충분히 섭취한다.",
      health: "약국(Pharmacie) 표시가 있는 곳에서 상비약을 구매할 수 있다.",
      culture: "식당 입장 시 인사를 건네는 것이 일반적인 예의다.",
      traffic: "지하철 파업이 잦아 대체 경로를 미리 확인한다.",
      emergencyContacts:
        "긴급전화 17(경찰)/15(구급)/18(화재), 주프랑스 대한민국 대사관 +33-1-4753-6996",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  이탈리아: {
    country: "이탈리아",
    categories: {
      security: "관광 밀집 지역(로마·나폴리 등)에서 소매치기가 매우 흔하다.",
      scam: "팔찌 강매, 가짜 청원서 사기, 부정확한 택시 요금에 주의한다.",
      law: "유적지 낙서·훼손은 형사 처벌 대상이 될 수 있다.",
      disaster: "화산·지진 활동 지역(나폴리 인근)의 안내를 확인한다.",
      health:
        "여행자 보험 가입을 권장하며 응급실 이용 시 대기시간이 길 수 있다.",
      culture: "성당 방문 시 어깨와 무릎을 가리는 복장이 필요하다.",
      traffic: "구시가지 골목이 좁아 차량·스쿠터 통행에 주의한다.",
      emergencyContacts:
        "긴급전화 112(통합)/113(경찰), 주이탈리아 대한민국 대사관 +39-06-802461",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  스페인: {
    country: "스페인",
    categories: {
      security: "바르셀로나·마드리드 도심에서 소매치기·가방 날치기가 잦다.",
      scam: "카드 게임(카드 트릭) 사기, 가짜 경찰 사기에 주의한다.",
      law: "투우 등 지역 축제 기간 통제 구역에 주의한다.",
      disaster: "여름철 폭염으로 인한 열사병에 대비한다.",
      health:
        "응급 의료 서비스는 신속하나 진료비 청구를 위해 보험 서류를 보관한다.",
      culture: "식사 시간이 늦은 편(저녁 21시 이후)임을 감안한다.",
      traffic: "대도시 지하철은 편리하나 야간 인적 드문 구역은 피한다.",
      emergencyContacts:
        "긴급전화 112(통합), 주스페인 대한민국 대사관 +34-91-353-2000",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  영국: {
    country: "영국",
    categories: {
      security:
        "대도시 소매치기, 야간 인적 드문 구역의 소규모 강도에 주의한다.",
      scam: "가짜 티켓 판매, 거리 모금 사기에 주의한다.",
      law: "공공장소 음주 제한 구역이 있으며 위반 시 벌금이 부과된다.",
      disaster: "겨울철 강풍·폭우로 인한 교통 지연이 흔하다.",
      health:
        "NHS 응급실은 비거주자에게 요금이 청구될 수 있어 보험이 필요하다.",
      culture: "줄서기(Queue) 문화를 지키는 것이 중요한 예의다.",
      traffic: "차량이 좌측 통행이므로 도로 횡단 시 방향에 특히 주의한다.",
      emergencyContacts:
        "긴급전화 999 또는 112(통합), 주영국 대한민국 대사관 +44-20-7227-5500",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  미국: {
    country: "미국",
    categories: {
      security: "도시별 치안 차이가 크며 야간 인적 드문 구역은 피한다.",
      scam: "가짜 렌터카 보험 강매, 관광지 인근 소액 사기에 주의한다.",
      law: "주(State)마다 법규가 달라 총기·음주 관련 규정을 사전에 확인한다.",
      disaster: "지역별로 허리케인·지진·산불 위험이 다르므로 계절을 확인한다.",
      health: "의료비가 매우 높아 여행자 보험 가입이 필수적이다.",
      culture: "레스토랑 팁 문화(15~20%)가 일반적이다.",
      traffic:
        "대중교통이 약한 도시가 많아 렌터카 이용 시 교통 법규를 확인한다.",
      emergencyContacts:
        "긴급전화 911(통합), 주미국 대한민국 대사관 +1-202-939-5600",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  캐나다: {
    country: "캐나다",
    categories: {
      security:
        "전반적으로 치안이 양호하나 대도시 일부 구역은 야간에 주의한다.",
      scam: "온라인 숙소 예약 사기, 가짜 관광 상품 판매에 주의한다.",
      law: "주류 구매·소지 연령과 장소 규정이 주(Province)마다 다르다.",
      disaster: "겨울철 폭설로 인한 도로 통제가 흔하다.",
      health: "비거주자 의료비가 높아 여행자 보험이 필요하다.",
      culture: "야외 활동 시 야생동물과의 접촉을 피하는 것이 중요하다.",
      traffic: "겨울철 결빙 도로 운전 시 각별한 주의가 필요하다.",
      emergencyContacts:
        "긴급전화 911(통합), 주캐나다 대한민국 대사관 +1-613-244-5010",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  호주: {
    country: "호주",
    categories: {
      security: "치안이 우수하나 관광지 소지품 방치는 피해야 한다.",
      scam: "가짜 투어 예약, 렌터카 손해보험 강매성 판매에 주의한다.",
      law: "해변 음주 제한 구역과 흡연 제한 구역이 있다.",
      disaster: "여름철 산불·폭염, 해파리 등 해양 생물에 주의한다.",
      health: "자외선이 매우 강해 자외선 차단제를 꼭 사용한다.",
      culture: "해변에서는 지정된 깃발 구역 안에서만 수영한다.",
      traffic: "차량이 좌측 통행이며 장거리 구간은 휴식을 충분히 취한다.",
      emergencyContacts:
        "긴급전화 000(통합), 주호주 대한민국 대사관 +61-2-6270-4100",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  뉴질랜드: {
    country: "뉴질랜드",
    categories: {
      security: "치안이 매우 양호하나 렌터카 차량 내 물품 도난에 주의한다.",
      scam: "고가의 액티비티 예약 취소 수수료 관련 분쟁에 주의한다.",
      law: "국립공원 내 지정되지 않은 야영은 금지된다.",
      disaster: "지진·화산 활동 지역이 있어 안내 표지를 확인한다.",
      health:
        "의료 시설이 도시에 집중되어 있어 산간 지역 이동 시 대비가 필요하다.",
      culture: "마오리 전통 문화유산과 장소에 대한 존중이 중요하다.",
      traffic: "차량이 좌측 통행이며 산길 구간은 급커브가 많다.",
      emergencyContacts:
        "긴급전화 111(통합), 주뉴질랜드 대한민국 대사관 +64-4-473-9073",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  터키: {
    country: "터키",
    categories: {
      security: "대도시 관광지 소매치기, 국경 인접 지역 접근에 주의한다.",
      scam: "카펫·투어 바가지 상술, 부정확한 환전에 주의한다.",
      law: "국가 지도자·상징물에 대한 모욕은 처벌 대상이 될 수 있다.",
      disaster: "지진 다발 지역으로 숙소의 대피 경로를 미리 확인한다.",
      health:
        "여행자 보험 가입을 권장하며 열기구 등 액티비티는 보험 포함 여부를 확인한다.",
      culture: "모스크 방문 시 신발을 벗고 여성은 머리 가리개를 준비한다.",
      traffic: "대도시 교통 혼잡이 심해 이동 시간을 여유 있게 잡는다.",
      emergencyContacts:
        "긴급전화 155(경찰)/112(구급), 주터키 대한민국 대사관 +90-312-468-4822",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  그리스: {
    country: "그리스",
    categories: {
      security: "관광지 소매치기에 주의하고 시위 지역 접근을 피한다.",
      scam: "택시 바가지 요금, 레스토랑 계산서 조작에 주의한다.",
      law: "고대 유적지에서 돌·유물 채취는 엄격히 금지된다.",
      disaster: "여름철 폭염·산불 위험이 높은 지역이 있다.",
      health: "섬 지역은 의료 시설이 제한적이라 사전 대비가 필요하다.",
      culture: "정교회 성당 방문 시 정숙한 복장을 지킨다.",
      traffic: "섬 지역은 렌터카·스쿠터 이용 시 도로 상태에 주의한다.",
      emergencyContacts:
        "긴급전화 100(경찰)/166(구급), 주그리스 대한민국 대사관 +30-210-698-4080",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
  스위스: {
    country: "스위스",
    categories: {
      security: "치안이 매우 우수하나 관광지 소매치기는 드물게 발생한다.",
      scam: "고가 시계·기념품 판매 관련 과장 광고에 주의한다.",
      law: "산악 지역 지정 트레일 외 이동은 규정을 위반할 수 있다.",
      disaster: "고산 지역 기상 급변, 눈사태 위험 안내를 확인한다.",
      health: "고산병 예방을 위해 고도 적응 시간을 충분히 갖는다.",
      culture: "대중교통 정시 운행 문화를 존중하고 일요일 상점 휴무가 많다.",
      traffic: "등산열차·케이블카 예약 시간을 엄수한다.",
      emergencyContacts:
        "긴급전화 112(통합)/117(경찰), 주스위스 대한민국 대사관 +41-31-356-2444",
    },
    source: "외교부 해외안전여행",
    sourceUrl: "https://www.0404.go.kr",
    checkedAt: "2026-01-05",
    editor: "free_traveler",
  },
};

/**
 * destinations.ts에 게시된 모든 해외 국가와 1:1로 매핑되는지 확인하기 위한
 * 파생 목록이다(REQ-FUNC-046/REQ-NF-027). DATA-VALIDATION-SCRIPT Task가 이
 * 목록과 safetyInfoByCountry의 키 집합을 비교해 커버리지 100%를 강제할 예정이다.
 */
export const publishedOverseasCountries = Array.from(
  new Set(overseasDestinations.map((d) => d.country)),
);
