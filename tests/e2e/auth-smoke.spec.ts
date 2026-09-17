import { test, expect, type Page } from "@playwright/test";

// Free Traveler Playwright Chromium Smoke - 로그인이 필요한 흐름의 골격.
// Supabase 테스트 계정 자격증명(E2E_AUTH_EMAIL/E2E_AUTH_PASSWORD)이 없는
// 환경(예: Secret이 없는 CI)에서는 이 파일 전체를 명시적으로 skip한다 -
// public-smoke.spec.ts는 이 조건과 무관하게 항상 실행된다.
const AUTH_EMAIL = process.env.E2E_AUTH_EMAIL;
const AUTH_PASSWORD = process.env.E2E_AUTH_PASSWORD;
const hasAuthEnv = Boolean(AUTH_EMAIL && AUTH_PASSWORD);

async function loginAsTestUser(page: Page) {
  await page.goto("/account");
  await page.getByLabel("이메일").fill(AUTH_EMAIL as string);
  await page.getByLabel("비밀번호").fill(AUTH_PASSWORD as string);
  await page.getByRole("button", { name: "로그인" }).click();
  await expect(page.getByTestId("account-profile")).toBeVisible();
}

test.describe("E2E-006~007: 인증이 필요한 동행 흐름(골격)", () => {
  test.skip(
    !hasAuthEnv,
    "E2E_AUTH_EMAIL/E2E_AUTH_PASSWORD가 없어 인증 Smoke를 건너뜁니다",
  );

  test("E2E-006: 로그인 사용자의 동행글 작성과 목록·상세 확인", async ({
    page,
  }) => {
    await loginAsTestUser(page);

    const title = `E2E-006 테스트 동행글 ${Date.now()}`;

    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "동행 구하기" }).click();

    const writeForm = page.getByTestId("mate-write-form");
    await writeForm.getByLabel("제목").fill(title);
    await writeForm
      .getByLabel("국가")
      .selectOption({ index: 1 })
      .catch(() => undefined);
    await writeForm
      .getByLabel("지역")
      .fill("테스트 지역")
      .catch(() => undefined);
    await writeForm.getByLabel("시작일").fill(futureDate(14));
    await writeForm.getByLabel("종료일").fill(futureDate(17));
    await writeForm.getByLabel("안전수칙에 동의합니다").check();
    await writeForm.getByRole("button", { name: "작성 완료" }).click();

    await page.goto("/mates");
    await expect(page.getByRole("heading", { name: title })).toBeVisible();
    await page.getByRole("heading", { name: title }).click();
    await expect(page.getByTestId("mate-detail-panel")).toBeVisible();
    await expect(
      page.getByTestId("mate-detail-panel").getByText(title),
    ).toBeVisible();
  });

  test("E2E-007: 동행글 신청과 계정 화면의 내 활동 확인", async ({ page }) => {
    await loginAsTestUser(page);

    await page.goto("/mates");
    const firstPost = page.getByTestId("mate-post-card").first();
    await expect(firstPost).toBeVisible();
    await firstPost.click();

    const applyForm = page.getByTestId("mate-apply-form");
    await applyForm
      .getByLabel("참가 메시지")
      .fill("E2E-007 테스트 참가 요청입니다.");
    await applyForm.getByRole("button", { name: "참가 요청" }).click();
    await expect(page.getByText("접수", { exact: false })).toBeVisible();

    await page.goto("/account");
    await expect(page.getByTestId("my-activity-applications")).toBeVisible();
  });
});

function futureDate(daysFromNow: number): string {
  const d = new Date();
  d.setDate(d.getDate() + daysFromNow);
  return d.toISOString().slice(0, 10);
}
