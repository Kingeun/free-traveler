// API-AUTH-PROFILE: OAuth callback handler for Supabase Auth
// Handles redirect after OAuth provider login/signup

import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

    try {
      // Exchange code for session
      const { error } = await supabase.auth.exchangeCodeForSession(code);

      if (error) {
        console.error('Session exchange error:', error);
        return NextResponse.redirect(`${requestUrl.origin}/login?error=session_exchange_failed`);
      }

      // Ensure profile exists for OAuth users
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        // Check if profile exists
        const { data: existingProfile } = await supabase
          .from('profiles')
          .select('id')
          .eq('id', user.id)
          .single();

        // Create profile if doesn't exist (for OAuth first-time users)
        if (!existingProfile) {
          await supabase.from('profiles').insert({
            id: user.id,
            nickname: user.email?.split('@')[0] || 'User',
            age_range: '20s',
            gender: 'unspecified',
            travel_style: 'balanced',
            is_adult: false,
            role: 'member',
          });
        }
      }

      // Redirect to travel tools (SCR-003) or dashboard
      return NextResponse.redirect(`${requestUrl.origin}/travel-tools`);
    } catch (error) {
      console.error('Callback error:', error);
      return NextResponse.redirect(`${requestUrl.origin}/login?error=auth_failed`);
    }
  }

  // No code provided
  return NextResponse.redirect(`${requestUrl.origin}/login?error=no_code`);
}
