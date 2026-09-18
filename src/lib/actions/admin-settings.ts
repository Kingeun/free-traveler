// API-ADMIN-SETTINGS: 외부 URL 허용목록 설정 Server Action
// 항공·숙소 외부 URL을 HTTPS·허용목록 도메인으로만 제한 저장 (REQ-FUNC-077)

'use server';

import { z } from 'zod';
import { createClient } from '@supabase/supabase-js';
import { getProfile } from '@/lib/supabase/queries';

// ============================================================================
// Constants & Validation
// ============================================================================

const ALLOWED_DOMAINS: Record<string, string[]> = {
  flight: ['google.com', 'www.google.com', 'flights.google.com', 'kayak.com', 'skyscanner.com'],
  hotel: ['booking.com', 'www.booking.com', 'airbnb.com', 'www.airbnb.com', 'tripadvisor.com'],
};

const UpdateUrlSettingSchema = z.object({
  key: z.enum(['flight', 'hotel']),
  url: z.string().url('Valid URL required').refine((url) => url.startsWith('https://'), {
    message: 'Only HTTPS URLs are allowed',
  }),
});

type UpdateUrlSettingInput = z.infer<typeof UpdateUrlSettingSchema>;

// ============================================================================
// Utility Functions
// ============================================================================

function isUrlDomainAllowed(url: string, key: 'flight' | 'hotel'): boolean {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname.toLowerCase();
    const allowedDomains = ALLOWED_DOMAINS[key];

    // Check exact match or wildcard subdomain match
    return allowedDomains.some((domain) => hostname === domain || hostname.endsWith(`.${domain}`));
  } catch {
    return false;
  }
}

async function isCurrentUserAdmin(): Promise<boolean> {
  const { auth } = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await auth.getUser();

  if (!user) return false;

  const profile = await getProfile(user.id);
  return profile?.role === 'admin' || false;
}

// ============================================================================
// Server Actions
// ============================================================================

export async function updateOutboundUrlSetting(input: UpdateUrlSettingInput): Promise<{
  success: boolean;
  error?: string;
}> {
  // 1. Validate input
  const validationResult = UpdateUrlSettingSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid input' };
  }

  const { key, url } = validationResult.data;

  // 2. Check admin authorization
  const isAdmin = await isCurrentUserAdmin();
  if (!isAdmin) {
    return { success: false, error: 'Unauthorized: admin access required' };
  }

  // 3. Validate domain against allowlist
  if (!isUrlDomainAllowed(url, key)) {
    return { success: false, error: `Domain not in allowlist for ${key}` };
  }

  // 4. Reject http:/javascript:/data: schemes (additional safety check)
  if (url.startsWith('http://') || url.startsWith('javascript:') || url.startsWith('data:')) {
    return { success: false, error: 'Unsafe URL scheme' };
  }

  // 5. Update in Supabase
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User session required' };
  }

  const { error } = await supabase.from('outbound_url_settings').upsert(
    {
      key,
      url,
      updated_by: user.id,
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'key' }
  );

  if (error) {
    console.error('Error updating URL setting:', error);
    return { success: false, error: 'Failed to update setting' };
  }

  return { success: true };
}

export async function getOutboundUrlForClient(key: 'flight' | 'hotel'): Promise<string | null> {
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const { data, error } = await supabase
    .from('outbound_url_settings')
    .select('url')
    .eq('key', key)
    .single();

  if (error || !data) {
    console.error('Error fetching URL setting:', error);
    return null;
  }

  return data.url;
}
