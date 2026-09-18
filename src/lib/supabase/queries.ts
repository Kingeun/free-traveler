// DB-ACCESS: 타입 안전 Supabase 쿼리 헬퍼
// 모든 응답에서 이메일·전화번호 필드 제외 (REQ-FUNC-033)
// 항공·숙소 폼용 서버 API 없음 (REQ-FUNC-017)

import { supabase } from './client';

// ============================================================================
// Type Definitions (email/phone excluded)
// ============================================================================

export type Profile = {
  id: string;
  nickname: string;
  age_range: '10s' | '20s' | '30s' | '40s' | '50s_plus';
  gender?: 'male' | 'female' | 'unspecified';
  travel_style: string;
  is_adult: boolean;
  role: 'member' | 'admin';
  created_at: string;
  updated_at: string;
};

export type MatePost = {
  id: string;
  author_id: string;
  author?: Profile;
  title: string;
  country: string;
  region?: string;
  start_date: string;
  end_date: string;
  capacity: number;
  conditions?: string;
  travel_style?: string;
  description: string;
  safety_consent_at: string;
  status: 'OPEN' | 'CLOSED' | 'HIDDEN';
  created_at: string;
  updated_at: string;
};

export type MateApplication = {
  id: string;
  post_id: string;
  applicant_id: string;
  applicant?: Profile;
  message: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  created_at: string;
  updated_at: string;
};

export type UserBlock = {
  id: string;
  blocker_id: string;
  blocked_id: string;
  created_at: string;
};

export type Report = {
  id: string;
  reporter_id: string;
  target_post_id?: string;
  target_user_id?: string;
  reason_code: 'SPAM' | 'HARASSMENT' | 'SCAM' | 'INAPPROPRIATE' | 'OTHER';
  description?: string;
  status: 'OPEN' | 'REVIEWING' | 'RESOLVED' | 'DISMISSED';
  created_at: string;
  updated_at: string;
};

export type OutboundUrlSetting = {
  id: string;
  key: 'flight' | 'hotel';
  url: string;
  updated_by?: string;
  updated_at: string;
};

// ============================================================================
// Profile Queries
// ============================================================================

export async function getProfile(userId: string): Promise<Profile | null> {
  const { data, error } = await supabase
    .from('profiles')
    .select('id, nickname, age_range, gender, travel_style, is_adult, role, created_at, updated_at')
    .eq('id', userId)
    .single();

  if (error) {
    console.error('Error fetching profile:', error);
    return null;
  }

  return data as Profile;
}

export async function getProfiles(userIds: string[]): Promise<Map<string, Profile>> {
  const { data, error } = await supabase
    .from('profiles')
    .select('id, nickname, age_range, gender, travel_style, is_adult, role, created_at, updated_at')
    .in('id', userIds);

  if (error) {
    console.error('Error fetching profiles:', error);
    return new Map();
  }

  const map = new Map<string, Profile>();
  (data as Profile[]).forEach((profile) => {
    map.set(profile.id, profile);
  });
  return map;
}

export async function updateProfile(userId: string, updates: Partial<Omit<Profile, 'id' | 'created_at' | 'updated_at'>>): Promise<Profile | null> {
  const { data, error } = await supabase
    .from('profiles')
    .update({ ...updates, updated_at: new Date().toISOString() })
    .eq('id', userId)
    .select('id, nickname, age_range, gender, travel_style, is_adult, role, created_at, updated_at')
    .single();

  if (error) {
    console.error('Error updating profile:', error);
    return null;
  }

  return data as Profile;
}

// ============================================================================
// Mate Posts Queries
// ============================================================================

export async function getMatePostsList(limit: number = 20, offset: number = 0): Promise<MatePost[]> {
  const { data, error } = await supabase
    .from('mate_posts')
    .select(
      `id, author_id, title, country, region, start_date, end_date, capacity,
       conditions, travel_style, description, safety_consent_at, status,
       created_at, updated_at,
       author:author_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .neq('status', 'HIDDEN')
    .order('created_at', { ascending: false })
    .range(offset, offset + limit - 1);

  if (error) {
    console.error('Error fetching mate posts:', error);
    return [];
  }

  return (data || []) as unknown as MatePost[];
}

export async function getMatePost(postId: string): Promise<MatePost | null> {
  const { data, error } = await supabase
    .from('mate_posts')
    .select(
      `id, author_id, title, country, region, start_date, end_date, capacity,
       conditions, travel_style, description, safety_consent_at, status,
       created_at, updated_at,
       author:author_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .eq('id', postId)
    .single();

  if (error) {
    console.error('Error fetching mate post:', error);
    return null;
  }

  return data as unknown as MatePost;
}

export async function getUserMatePostsList(userId: string): Promise<MatePost[]> {
  const { data, error } = await supabase
    .from('mate_posts')
    .select(
      `id, author_id, title, country, region, start_date, end_date, capacity,
       conditions, travel_style, description, safety_consent_at, status,
       created_at, updated_at,
       author:author_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .eq('author_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching user mate posts:', error);
    return [];
  }

  return (data || []) as unknown as MatePost[];
}

export async function createMatePost(post: Omit<MatePost, 'id' | 'created_at' | 'updated_at'>): Promise<MatePost | null> {
  const { data, error } = await supabase
    .from('mate_posts')
    .insert([post])
    .select(
      `id, author_id, title, country, region, start_date, end_date, capacity,
       conditions, travel_style, description, safety_consent_at, status,
       created_at, updated_at,
       author:author_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .single();

  if (error) {
    console.error('Error creating mate post:', error);
    return null;
  }

  return data as unknown as MatePost;
}

export async function updateMatePost(postId: string, updates: Partial<Omit<MatePost, 'id' | 'created_at' | 'updated_at' | 'author'>>): Promise<MatePost | null> {
  const { data, error } = await supabase
    .from('mate_posts')
    .update({ ...updates, updated_at: new Date().toISOString() })
    .eq('id', postId)
    .select(
      `id, author_id, title, country, region, start_date, end_date, capacity,
       conditions, travel_style, description, safety_consent_at, status,
       created_at, updated_at,
       author:author_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .single();

  if (error) {
    console.error('Error updating mate post:', error);
    return null;
  }

  return data as unknown as MatePost;
}

// ============================================================================
// Mate Applications Queries
// ============================================================================

export async function getMateApplicationsList(postId: string): Promise<MateApplication[]> {
  const { data, error } = await supabase
    .from('mate_applications')
    .select(
      `id, post_id, applicant_id, message, status, created_at, updated_at,
       applicant:applicant_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .eq('post_id', postId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching mate applications:', error);
    return [];
  }

  return (data || []) as unknown as MateApplication[];
}

export async function getUserMateApplicationsList(userId: string): Promise<MateApplication[]> {
  const { data, error } = await supabase
    .from('mate_applications')
    .select(
      `id, post_id, applicant_id, message, status, created_at, updated_at,
       applicant:applicant_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .eq('applicant_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching user mate applications:', error);
    return [];
  }

  return (data || []) as unknown as MateApplication[];
}

export async function createMateApplication(application: Omit<MateApplication, 'id' | 'created_at' | 'updated_at' | 'applicant'>): Promise<MateApplication | null> {
  const { data, error } = await supabase
    .from('mate_applications')
    .insert([application])
    .select(
      `id, post_id, applicant_id, message, status, created_at, updated_at,
       applicant:applicant_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .single();

  if (error) {
    console.error('Error creating mate application:', error);
    return null;
  }

  return data as unknown as MateApplication;
}

export async function updateMateApplicationStatus(
  applicationId: string,
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
): Promise<MateApplication | null> {
  const { data, error } = await supabase
    .from('mate_applications')
    .update({ status, updated_at: new Date().toISOString() })
    .eq('id', applicationId)
    .select(
      `id, post_id, applicant_id, message, status, created_at, updated_at,
       applicant:applicant_id(id, nickname, age_range, gender, travel_style, is_adult, role)`
    )
    .single();

  if (error) {
    console.error('Error updating mate application status:', error);
    return null;
  }

  return data as unknown as MateApplication;
}

// ============================================================================
// User Blocks Queries
// ============================================================================

export async function getUserBlockList(userId: string): Promise<string[]> {
  const { data, error } = await supabase
    .from('user_blocks')
    .select('blocked_id')
    .eq('blocker_id', userId);

  if (error) {
    console.error('Error fetching user blocks:', error);
    return [];
  }

  return (data || []).map((item) => item.blocked_id);
}

export async function blockUser(blockerId: string, blockedId: string): Promise<boolean> {
  const { error } = await supabase.from('user_blocks').insert([{ blocker_id: blockerId, blocked_id: blockedId }]);

  if (error) {
    console.error('Error blocking user:', error);
    return false;
  }

  return true;
}

export async function unblockUser(blockerId: string, blockedId: string): Promise<boolean> {
  const { error } = await supabase
    .from('user_blocks')
    .delete()
    .eq('blocker_id', blockerId)
    .eq('blocked_id', blockedId);

  if (error) {
    console.error('Error unblocking user:', error);
    return false;
  }

  return true;
}

// ============================================================================
// Reports Queries
// ============================================================================

export async function createReport(report: Omit<Report, 'id' | 'created_at' | 'updated_at'>): Promise<Report | null> {
  const { data, error } = await supabase
    .from('reports')
    .insert([report])
    .select('id, reporter_id, target_post_id, target_user_id, reason_code, description, status, created_at, updated_at')
    .single();

  if (error) {
    console.error('Error creating report:', error);
    return null;
  }

  return data as Report;
}

export async function getUserReports(userId: string): Promise<Report[]> {
  const { data, error } = await supabase
    .from('reports')
    .select('id, reporter_id, target_post_id, target_user_id, reason_code, description, status, created_at, updated_at')
    .eq('reporter_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching user reports:', error);
    return [];
  }

  return (data || []) as Report[];
}

// ============================================================================
// Outbound URL Settings Queries
// ============================================================================

export async function getOutboundUrlSettings(): Promise<Map<string, string>> {
  const { data, error } = await supabase
    .from('outbound_url_settings')
    .select('key, url');

  if (error) {
    console.error('Error fetching outbound URL settings:', error);
    return new Map();
  }

  const map = new Map<string, string>();
  (data as OutboundUrlSetting[] || []).forEach((item) => {
    map.set(item.key, item.url);
  });
  return map;
}

export async function getOutboundUrl(key: 'flight' | 'hotel'): Promise<string | null> {
  const { data, error } = await supabase
    .from('outbound_url_settings')
    .select('url')
    .eq('key', key)
    .single();

  if (error) {
    console.error('Error fetching outbound URL:', error);
    return null;
  }

  return data?.url || null;
}
