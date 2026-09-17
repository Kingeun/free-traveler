import { test, expect, type Page } from "@playwright/test";

// Free Traveler Playwright Chromium Smoke - 로그인이 필요 없는 공개 흐름만 다룬다.
// Selector 우선순위: role > label > test id. 텍스트 위치·CSS 구조에 의존하지 않는다.
// 외부 사이트(항공/숙소)는 실제로 이동해 내용을 검사하지 않는다 - 새 탭 URL과
// 페이지에 남은 안내 문구/href만 확인하고 새 탭은 곧바로 닫는다.

const NAV_LINKS = ["여행지", "여행 도구", "동행", "대표소개"];

async function openExternalTab(page: Page, triggerTestId: string) {
  const [popup] = await Promise.all([
    page.context().waitForEvent("page"),
    page.getByTestId(triggerTestId).click(),
  ]);
  await popup
    .waitForLoadState("domcontentloaded", { timeout: 15_000 })
    .catch(() => {
      // 실제 외부 사이트 콘텐츠는 검사하지 않는다 - URL 확인 전 로드가 끝나지 않아도 무방하다.
    });
  return popup;
}

test.describe("E2E-001: 메인 페이지의 추천 여행지와 주요 CTA", () => {
  test("국내/해외 추천 여행지가 보이고 상세 Drawer와 전역 CTA가 동작한다", async ({
    page,
  }) => {
    await page.goto("/");

    // 주요 CTA: 전역 Header nav 4개.
    for (const name of NAV_LINKS) {
      await expect(page.getByRole("link", { name })).toBeVisible();
    }

    // 추천 여행지: 국내+해외 합쳐 최소 12개(6+6) Card.
    const destinationCards = page.getByTestId("destination-card");
    await expect(destinationCards.first()).toBeVisible();
    expect(await destinationCards.count()).toBeGreaterThanOrEqual(12);

    // Card 선택 시 같은 화면 위 상세 Drawer가 열린다(별도 Page로 이동하지 않음).
    await destinationCards.first().click();
    await expect(page.getByTestId("destination-drawer")).toBeVisible();
  });
});

test.describe("E2E-002: 대표 소개의 free_traveler, 50+ Trips, 30+ Countries", () => {
  test("대표 소개 페이지에 고정 지표 문구가 표시된다", async ({ page }) => {
    await page.goto("/about");

    await expect(
      page.getByText("free_traveler", { exact: false }).first(),
    ).toBeVisible();
    await expect(page.getByText("50+ Trips", { exact: false })).toBeVisible();
    await expect(
      page.getByText("30+ Countries", { exact: false }),
    ).toBeVisible();
  });
});

test.describe("E2E-003: 여행 도구의 항공 외부 이동 안내와 href", () => {
  test("항공 조건 입력 후 비전달 고지와 외부 이동 새 탭 URL을 확인한다", async ({
    page,
  }) => {
    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "항공편 찾기" }).click();

    const flightForm = page.getByTestId("flight-form");
    await flightForm
      .getByLabel("국가")
      .selectOption({ index: 1 })
      .catch(async () => {
        // select가 아니라 combobox/버튼형일 수 있으므로 role 기반으로 한 번 더 시도한다.
        await flightForm.getByLabel("국가").click();
      });
    await flightForm
      .getByLabel("지역")
      .fill("테스트 지역")
      .catch(() => undefined);
    await flightForm.getByLabel("출발일").fill(futureDate(7));
    await flightForm.getByLabel("귀국일").fill(futureDate(10));

    await expect(
      page.getByText("입력값은 외부 사이트로 전달되지 않습니다", {
        exact: false,
      }),
    ).toBeVisible();

    const popup = await openExternalTab(page, "flight-open-external");
    expect(popup.url()).toContain("google.com/travel/flights");
    await popup.close();
  });
});

test.describe("E2E-004: 여행 도구의 숙소 외부 이동 안내와 href", () => {
  test("숙소 조건 입력 후 비전달 고지와 외부 이동 새 탭 URL을 확인한다", async ({
    page,
  }) => {
    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "숙소 찾기" }).click();

    const hotelForm = page.getByTestId("hotel-form");
    await hotelForm
      .getByLabel("국가")
      .selectOption({ index: 1 })
      .catch(async () => {
        await hotelForm.getByLabel("국가").click();
      });
    await hotelForm
      .getByLabel("지역")
      .fill("테스트 지역")
      .catch(() => undefined);
    await hotelForm.getByLabel("체크인").fill(futureDate(7));
    await hotelForm.getByLabel("체크아웃").fill(futureDate(9));

    await expect(
      page.getByText("입력값은 외부 사이트로 전달되지 않습니다", {
        exact: false,
      }),
    ).toBeVisible();

    const popup = await openExternalTab(page, "hotel-open-external");
    expect(popup.url()).toContain("booking.com");
    await popup.close();
  });
});

test.describe("E2E-005: 비로그인 동행글 작성의 로그인 안내", () => {
  test("로그인하지 않은 상태로 동행 구하기 탭을 열면 작성 Form 대신 로그인 안내가 보인다", async ({
    page,
  }) => {
    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "동행 구하기" }).click();

    await expect(page.getByRole("heading", { name: /로그인/ })).toBeVisible();
    await expect(page.getByRole("link", { name: /로그인/ })).toBeVisible();

    // 작성 Form은 렌더링되지 않는다(빈 화면이 아니라 로그인 안내로 대체).
    await expect(page.getByLabel("제목")).toHaveCount(0);
  });
});

function futureDate(daysFromNow: number): string {
  const d = new Date();
  d.setDate(d.getDate() + daysFromNow);
  return d.toISOString().slice(0, 10);
}
