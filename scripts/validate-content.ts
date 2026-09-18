// DATA-VALIDATION-SCRIPT: src/data의 정적 콘텐츠(여행지/안전정보/대표 소개)가
// 게시 최소 기준을 만족하는지 build 전에 검사한다(REQ-FUNC-008/046/074,
// REQ-NF-026/027). 실패하면 non-zero exit code로 종료해 build를 중단시킨다.
//
// 참고(보고 필요 - 이 Task 범위에서 해결하지 않음): docs/PROJECT_SCOPE.md의
// REQ-FUNC-052("scope_type/scope_text 필드를 지역 경보 게시 시 필수화")는 이
// Task의 Requirement Ref에 포함되어 있으나, DATA-SAFETY(TASKS/TASK-DATA-SAFETY.md)
// 는 국가 단위 안전정보만 정의하고 지역(sub-national) 경보 개념이나
// scope_type/scope_text 필드를 두지 않았다 — DATA-SAFETY 쪽 Requirement Ref
// 목록에도 REQ-FUNC-052가 없다. 존재하지 않는 필드를 검증할 수는 없으므로 이
// 스크립트는 REQ-FUNC-052 검사를 생략한다. 데이터 모델에 지역 경보가 추가되면
// 이 스크립트도 함께 갱신해야 한다.

import {
  destinations,
  domesticDestinations,
  overseasDestinations,
  type Destination,
} from "../src/data/destinations";
import {
  safetyInfoByCountry,
  publishedOverseasCountries,
} from "../src/data/safety";
import {
  representativeStats,
  timeline,
  visitedCountries,
  gallery,
  memorableDestinations,
} from "../src/data/representative";

const MIN_DOMESTIC = 10;
const MIN_OVERSEAS_COUNTRIES = 15;
const MIN_OVERSEAS_CITIES = 30;
const MIN_ATTRACTIONS = 5;
const MIN_FOOD = 3;
const MIN_ETIQUETTE = 3;
const MIN_STATS_TRIPS = 50;
const MIN_STATS_COUNTRIES = 30;
const MIN_TIMELINE = 6;
const MIN_VISITED_COUNTRIES = 30;
const MIN_GALLERY = 8;
const MIN_MEMORABLE_DESTINATIONS = 4;

const errors: string[] = [];

function fail(message: string) {
  errors.push(message);
}

function validateDestination(d: Destination) {
  const label = `destinations.ts[${d.id}]`;
  if (!d.intro) fail(`${label}: intro가 비어 있다.`);
  if (d.attractions.length < MIN_ATTRACTIONS) {
    fail(
      `${label}: attractions ${d.attractions.length}개 (최소 ${MIN_ATTRACTIONS}개 필요).`,
    );
  }
  if (d.itinerary.oneDay.length === 0)
    fail(`${label}: itinerary.oneDay가 비어 있다.`);
  if (d.itinerary.threeDay.length === 0) {
    fail(`${label}: itinerary.threeDay가 비어 있다.`);
  }
  if (!d.budget) fail(`${label}: budget이 비어 있다.`);
  if (!d.transport) fail(`${label}: transport가 비어 있다.`);
  if (d.food.length < MIN_FOOD) {
    fail(`${label}: food ${d.food.length}개 (최소 ${MIN_FOOD}개 필요).`);
  }
  if (d.etiquette.length < MIN_ETIQUETTE) {
    fail(
      `${label}: etiquette ${d.etiquette.length}개 (최소 ${MIN_ETIQUETTE}개 필요).`,
    );
  }
  if (!d.source) fail(`${label}: source가 비어 있다.`);
  if (!d.updatedAt) fail(`${label}: updatedAt이 비어 있다.`);
}

function validateDestinations() {
  if (domesticDestinations.length < MIN_DOMESTIC) {
    fail(
      `destinations.ts: 국내 여행지 ${domesticDestinations.length}개 (최소 ${MIN_DOMESTIC}개 필요).`,
    );
  }

  const overseasCountries = new Set(overseasDestinations.map((d) => d.country));
  if (overseasCountries.size < MIN_OVERSEAS_COUNTRIES) {
    fail(
      `destinations.ts: 해외 국가 ${overseasCountries.size}개 (최소 ${MIN_OVERSEAS_COUNTRIES}개국 필요).`,
    );
  }
  if (overseasDestinations.length < MIN_OVERSEAS_CITIES) {
    fail(
      `destinations.ts: 해외 도시 ${overseasDestinations.length}개 (최소 ${MIN_OVERSEAS_CITIES}개 필요).`,
    );
  }

  const seenIds = new Set<string>();
  for (const d of destinations) {
    if (seenIds.has(d.id)) fail(`destinations.ts: id "${d.id}" 중복.`);
    seenIds.add(d.id);
    validateDestination(d);
  }
}

function validateSafety() {
  const requiredCategories: Array<
    keyof (typeof safetyInfoByCountry)[string]["categories"]
  > = [
    "security",
    "scam",
    "law",
    "traffic",
    "disaster",
    "health",
    "culture",
    "emergencyContacts",
  ];

  for (const country of publishedOverseasCountries) {
    const record = safetyInfoByCountry[country];
    if (!record) {
      fail(`safety.ts: 게시된 해외 국가 "${country}"에 대한 안전정보가 없다.`);
      continue;
    }
    for (const category of requiredCategories) {
      if (!record.categories[category]) {
        fail(`safety.ts[${country}]: categories.${category}가 비어 있다.`);
      }
    }
    if (!record.source) fail(`safety.ts[${country}]: source가 비어 있다.`);
    if (!record.sourceUrl)
      fail(`safety.ts[${country}]: sourceUrl이 비어 있다.`);
    if (!record.checkedAt)
      fail(`safety.ts[${country}]: checkedAt이 비어 있다.`);
    if (!record.editor) fail(`safety.ts[${country}]: editor가 비어 있다.`);
  }

  // safety.ts에만 있고 실제로는 게시되지 않은 국가(고아 레코드)가 있으면 1:1이 아니다.
  const publishedSet = new Set(publishedOverseasCountries);
  for (const country of Object.keys(safetyInfoByCountry)) {
    if (!publishedSet.has(country)) {
      fail(
        `safety.ts[${country}]: destinations.ts에 게시되지 않은 국가의 안전정보 레코드(고아 레코드)가 있다.`,
      );
    }
  }
}

function validateRepresentative() {
  if (representativeStats.trips < MIN_STATS_TRIPS) {
    fail(
      `representative.ts: trips ${representativeStats.trips} (최소 ${MIN_STATS_TRIPS} 필요).`,
    );
  }
  if (representativeStats.countries < MIN_STATS_COUNTRIES) {
    fail(
      `representative.ts: countries ${representativeStats.countries} (최소 ${MIN_STATS_COUNTRIES} 필요).`,
    );
  }
  if (timeline.length < MIN_TIMELINE) {
    fail(
      `representative.ts: timeline ${timeline.length}개 (최소 ${MIN_TIMELINE}개 필요).`,
    );
  }
  if (visitedCountries.length < MIN_VISITED_COUNTRIES) {
    fail(
      `representative.ts: visitedCountries ${visitedCountries.length}개 (최소 ${MIN_VISITED_COUNTRIES}개 필요).`,
    );
  }
  if (gallery.length < MIN_GALLERY) {
    fail(
      `representative.ts: gallery ${gallery.length}장 (최소 ${MIN_GALLERY}장 필요).`,
    );
  }
  if (memorableDestinations.length < MIN_MEMORABLE_DESTINATIONS) {
    fail(
      `representative.ts: memorableDestinations ${memorableDestinations.length}개 (최소 ${MIN_MEMORABLE_DESTINATIONS}개 필요).`,
    );
  }
}

function main() {
  validateDestinations();
  validateSafety();
  validateRepresentative();

  if (errors.length > 0) {
    console.error("CONTENT_VALIDATION_FAIL");
    for (const message of errors) {
      console.error(`- ${message}`);
    }
    process.exit(1);
  }

  console.log("CONTENT_VALIDATION_PASS");
}

main();
