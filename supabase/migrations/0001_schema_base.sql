-- DB-SCHEMA-BASE: 6개 테이블(profiles/mate_posts/mate_applications/user_blocks/
-- reports/outbound_url_settings) 스키마 + 기본 RLS. 여행지·안전정보·대표소개
-- 콘텐츠는 여기 포함하지 않는다(src/data 정적 데이터로만 관리 — REQ-FUNC-008 등).
-- 정확히 6개 테이블로 제한한다(TASKS/TASK-DB-SCHEMA-BASE.md Forbidden 참고).

-- =============================================================================
-- 1. profiles
-- =============================================================================
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  nickname text not null,
  age_range text not null check (
    age_range in ('10s', '20s', '30s', '40s', '50s_plus')
  ),
  gender text check (gender in ('male', 'female', 'unspecified')),
  travel_style text not null,
  is_adult boolean not null default false,
  adult_verified_at timestamptz,
  role text not null default 'member' check (role in ('member', 'admin')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table public.profiles is
  'REQ-FUNC-028: is_adult/adult_verified_at만 저장, 생년월일은 저장하지 않는다.';

-- profiles.role을 참조하는 다른 테이블의 RLS 정책에서 재귀 없이 admin 여부를
-- 확인하기 위한 SECURITY DEFINER 함수 (profiles 자체 RLS를 우회해 읽는다).
create function public.is_admin()
returns boolean
language sql
security definer
set search_path = public
stable
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$$;

alter table public.profiles enable row level security;

-- 닉네임 등은 동행글 작성자 표시에 필요해 로그인 사용자 전체에 공개한다.
-- 이메일 등 민감 컬럼의 select 제외는 DB-ACCESS(별도 Task)의 Query 계층 책임이다.
create policy "profiles_select_authenticated"
  on public.profiles for select
  to authenticated
  using (true);

create policy "profiles_insert_own"
  on public.profiles for insert
  to authenticated
  with check (auth.uid() = id);

create policy "profiles_update_own_or_admin"
  on public.profiles for update
  to authenticated
  using (auth.uid() = id or public.is_admin())
  with check (auth.uid() = id or public.is_admin());

-- =============================================================================
-- 2. mate_posts
-- =============================================================================
create table public.mate_posts (
  id uuid primary key default gen_random_uuid(),
  author_id uuid not null references public.profiles (id) on delete cascade,
  title text not null,
  country text not null,
  region text,
  start_date date not null,
  end_date date not null,
  capacity integer not null check (capacity > 0),
  conditions text,
  travel_style text,
  description text not null,
  -- REQ-FUNC-080: 동행 안전수칙 동의 체크박스의 동의 시각.
  safety_consent_at timestamptz not null,
  status text not null default 'OPEN' check (status in ('OPEN', 'CLOSED', 'HIDDEN')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint mate_posts_date_order check (end_date >= start_date)
);

comment on table public.mate_posts is
  'REQ-FUNC-037: end_date 경과 여부는 배치/트리거 없이 조회 시점 계산으로 CLOSED 판정한다(status 컬럼은 작성자 수동 마감/관리자 HIDDEN 용도).';

alter table public.mate_posts enable row level security;

-- HIDDEN(관리자 숨김) 글은 작성자·admin만 보고, 그 외 글은 로그인 사용자 전체가 본다.
create policy "mate_posts_select_visible_or_owner_or_admin"
  on public.mate_posts for select
  to authenticated
  using (
    status <> 'HIDDEN'
    or author_id = auth.uid()
    or public.is_admin()
  );

create policy "mate_posts_insert_own"
  on public.mate_posts for insert
  to authenticated
  with check (author_id = auth.uid());

create policy "mate_posts_update_own_or_admin"
  on public.mate_posts for update
  to authenticated
  using (author_id = auth.uid() or public.is_admin())
  with check (author_id = auth.uid() or public.is_admin());

create policy "mate_posts_delete_own"
  on public.mate_posts for delete
  to authenticated
  using (author_id = auth.uid());

-- =============================================================================
-- 3. mate_applications
-- =============================================================================
create table public.mate_applications (
  id uuid primary key default gen_random_uuid(),
  post_id uuid not null references public.mate_posts (id) on delete cascade,
  applicant_id uuid not null references public.profiles (id) on delete cascade,
  message text not null check (char_length(message) <= 500),
  status text not null default 'PENDING' check (status in ('PENDING', 'APPROVED', 'REJECTED')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (post_id, applicant_id)
);

alter table public.mate_applications enable row level security;

-- 신청자 본인 또는 그 모집글의 작성자(요청 대상 작성자)만 열람할 수 있다.
create policy "mate_applications_select_applicant_or_post_owner_or_admin"
  on public.mate_applications for select
  to authenticated
  using (
    applicant_id = auth.uid()
    or public.is_admin()
    or exists (
      select 1 from public.mate_posts p
      where p.id = post_id and p.author_id = auth.uid()
    )
  );

create policy "mate_applications_insert_own"
  on public.mate_applications for insert
  to authenticated
  with check (applicant_id = auth.uid());

-- 신청 상태(승인/거절) 변경은 모집글 작성자 또는 admin만 가능하다.
create policy "mate_applications_update_post_owner_or_admin"
  on public.mate_applications for update
  to authenticated
  using (
    public.is_admin()
    or exists (
      select 1 from public.mate_posts p
      where p.id = post_id and p.author_id = auth.uid()
    )
  )
  with check (
    public.is_admin()
    or exists (
      select 1 from public.mate_posts p
      where p.id = post_id and p.author_id = auth.uid()
    )
  );

-- =============================================================================
-- 4. user_blocks
-- =============================================================================
create table public.user_blocks (
  id uuid primary key default gen_random_uuid(),
  blocker_id uuid not null references public.profiles (id) on delete cascade,
  blocked_id uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (blocker_id, blocked_id),
  constraint user_blocks_no_self_block check (blocker_id <> blocked_id)
);

alter table public.user_blocks enable row level security;

-- 차단 목록은 차단을 건 본인만 열람·생성·해제(삭제)할 수 있다.
create policy "user_blocks_select_own"
  on public.user_blocks for select
  to authenticated
  using (blocker_id = auth.uid());

create policy "user_blocks_insert_own"
  on public.user_blocks for insert
  to authenticated
  with check (blocker_id = auth.uid());

create policy "user_blocks_delete_own"
  on public.user_blocks for delete
  to authenticated
  using (blocker_id = auth.uid());

-- =============================================================================
-- 5. reports
-- =============================================================================
create table public.reports (
  id uuid primary key default gen_random_uuid(),
  reporter_id uuid not null references public.profiles (id) on delete cascade,
  target_post_id uuid references public.mate_posts (id) on delete cascade,
  target_user_id uuid references public.profiles (id) on delete cascade,
  reason_code text not null check (
    reason_code in ('SPAM', 'HARASSMENT', 'SCAM', 'INAPPROPRIATE', 'OTHER')
  ),
  description text,
  -- REQ-FUNC-041: OPEN/REVIEWING/RESOLVED/DISMISSED 상태 필터만 제공(우선순위·담당자 없음).
  status text not null default 'OPEN' check (
    status in ('OPEN', 'REVIEWING', 'RESOLVED', 'DISMISSED')
  ),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint reports_has_target check (
    target_post_id is not null or target_user_id is not null
  )
);

alter table public.reports enable row level security;

-- 신고 접수 내역은 신고자 본인과 admin만 볼 수 있다(신고 대상자에게는 노출하지 않는다).
create policy "reports_select_reporter_or_admin"
  on public.reports for select
  to authenticated
  using (reporter_id = auth.uid() or public.is_admin());

create policy "reports_insert_own"
  on public.reports for insert
  to authenticated
  with check (reporter_id = auth.uid());

-- REQ-FUNC-042: 신고 상태 변경(RESOLVED/DISMISSED 전환)은 admin만 가능하다.
create policy "reports_update_admin_only"
  on public.reports for update
  to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- =============================================================================
-- 6. outbound_url_settings
-- =============================================================================
create table public.outbound_url_settings (
  id uuid primary key default gen_random_uuid(),
  key text not null unique check (key in ('flight', 'hotel')),
  -- REQ-FUNC-077: HTTPS·허용목록 내 값만 저장(HTTP/javascript:/data: 거부).
  url text not null check (url ~* '^https://'),
  updated_by uuid references public.profiles (id),
  updated_at timestamptz not null default now()
);

alter table public.outbound_url_settings enable row level security;

-- 여행 도구(SCR-003)는 비로그인 사용자도 사용하므로 설정값은 누구나 읽을 수 있다.
create policy "outbound_url_settings_select_all"
  on public.outbound_url_settings for select
  to anon, authenticated
  using (true);

create policy "outbound_url_settings_write_admin_only"
  on public.outbound_url_settings for all
  to authenticated
  using (public.is_admin())
  with check (public.is_admin());
