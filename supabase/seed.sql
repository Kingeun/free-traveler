-- DB-SEED-BASE: 로컬 개발 및 E2E 테스트용 시드 데이터
--
-- Purpose: TEST-RLS-BASIC과 E2E-MATE-AUTH가 필요로 하는 최소 테스트 데이터
-- (회원 2명 이상, 동행글 1건 이상) 생성.
--
-- 주의: 로컬 supabase start 시에만 실행됨. 프로덕션에는 적용되지 않음.

-- ============================================================================
-- 테스트 사용자 생성 (auth.users)
-- ============================================================================

-- Test User 1: test1@example.com / password123
INSERT INTO auth.users (
  id,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  aud,
  role,
  confirmation_token
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440001',
  'test1@example.com',
  crypt('password123', gen_salt('bf')),
  now(),
  now(),
  now(),
  'authenticated',
  'authenticated_user',
  ''
)
ON CONFLICT (id) DO NOTHING;

-- Test User 2: test2@example.com / password123
INSERT INTO auth.users (
  id,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  aud,
  role,
  confirmation_token
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440002',
  'test2@example.com',
  crypt('password123', gen_salt('bf')),
  now(),
  now(),
  now(),
  'authenticated',
  'authenticated_user',
  ''
)
ON CONFLICT (id) DO NOTHING;

-- Test User 3 (Admin): admin@example.com / password123
INSERT INTO auth.users (
  id,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  aud,
  role,
  confirmation_token
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440003',
  'admin@example.com',
  crypt('password123', gen_salt('bf')),
  now(),
  now(),
  now(),
  'authenticated',
  'authenticated_user',
  ''
)
ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- 사용자 프로필 생성 (profiles)
-- ============================================================================

-- Test User 1 Profile
INSERT INTO public.profiles (
  id,
  nickname,
  age_range,
  gender,
  travel_style,
  is_adult,
  role,
  created_at,
  updated_at
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440001',
  'TestUser1',
  '20s',
  'male',
  'eco',
  false,
  'member',
  now(),
  now()
)
ON CONFLICT (id) DO NOTHING;

-- Test User 2 Profile
INSERT INTO public.profiles (
  id,
  nickname,
  age_range,
  gender,
  travel_style,
  is_adult,
  role,
  created_at,
  updated_at
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440002',
  'TestUser2',
  '30s',
  'female',
  'budget',
  false,
  'member',
  now(),
  now()
)
ON CONFLICT (id) DO NOTHING;

-- Admin User Profile
INSERT INTO public.profiles (
  id,
  nickname,
  age_range,
  gender,
  travel_style,
  is_adult,
  role,
  created_at,
  updated_at
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440003',
  'AdminUser',
  '40s',
  'unspecified',
  'luxury',
  true,
  'admin',
  now(),
  now()
)
ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- 샘플 동행글 생성 (mate_posts)
-- ============================================================================

-- Test Mate Post 1: Open for applications
INSERT INTO public.mate_posts (
  author_id,
  title,
  country,
  region,
  start_date,
  end_date,
  capacity,
  conditions,
  travel_style,
  description,
  safety_consent_at,
  status,
  created_at,
  updated_at
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440001',
  '일본 도쿄 10월 여행 동행자 모집',
  'Japan',
  'Tokyo',
  '2026-10-01',
  '2026-10-10',
  2,
  '성인만 가능, 영어 가능자 우대',
  'eco',
  '도쿄의 주요 명소와 숨은 카페를 함께 여행할 동행자를 찾습니다. 일정 상의 유연성과 서로 다른 관점을 존중할 수 있는 분을 원합니다.',
  now(),
  'OPEN',
  now(),
  now()
)
ON CONFLICT DO NOTHING;

-- Test Mate Post 2: Closed post
INSERT INTO public.mate_posts (
  author_id,
  title,
  country,
  region,
  start_date,
  end_date,
  capacity,
  conditions,
  travel_style,
  description,
  safety_consent_at,
  status,
  created_at,
  updated_at
)
VALUES (
  '550e8400-e29b-41d4-a716-446655440002',
  '뉴욕 9월 여행 (모집 완료)',
  'United States',
  'New York',
  '2026-09-15',
  '2026-09-25',
  3,
  '택시, 대중교통 이용',
  'budget',
  '뉴욕 여행을 함께할 동행자를 찾아 봤습니다. 이제 모집이 완료되었습니다.',
  now(),
  'CLOSED',
  now(),
  now()
)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 동행 신청 생성 (mate_applications) - optional
-- ============================================================================

-- Test application: User 2 applies to Post 1
INSERT INTO public.mate_applications (
  post_id,
  applicant_id,
  message,
  status,
  created_at,
  updated_at
)
SELECT
  mp.id,
  '550e8400-e29b-41d4-a716-446655440002',
  '안녕하세요! 저는 일본 여행을 좋아하고, 환경 보호에 관심이 많습니다. 함께하고 싶습니다.',
  'PENDING',
  now(),
  now()
FROM public.mate_posts mp
WHERE mp.author_id = '550e8400-e29b-41d4-a716-446655440001'
  AND mp.title = '일본 도쿄 10월 여행 동행자 모집'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 외부 링크 설정 (outbound_url_settings) - optional
-- ============================================================================

INSERT INTO public.outbound_url_settings (
  key,
  url,
  updated_by,
  updated_at
)
VALUES
  ('flight', 'https://www.google.com/flights', '550e8400-e29b-41d4-a716-446655440003', now()),
  ('hotel', 'https://www.booking.com', '550e8400-e29b-41d4-a716-446655440003', now())
ON CONFLICT (key) DO NOTHING;
