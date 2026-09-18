// API-AUTH-PROFILE: Email auth, signup, profile, adult verification Server Actions
// No birthdate storage - only is_adult flag + verified_at timestamp (REQ-FUNC-028)

'use server';

import { z } from 'zod';
import { createClient } from '@supabase/supabase-js';

// ============================================================================
// Validation Schemas
// ============================================================================

const SignupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  nickname: z.string().min(2, 'Nickname too short').max(50, 'Nickname too long'),
  age_range: z.enum(['10s', '20s', '30s', '40s', '50s_plus']),
  gender: z.enum(['male', 'female', 'unspecified']).optional(),
  travel_style: z.string().min(1, 'Travel style required'),
});

const UpdateProfileSchema = z.object({
  nickname: z.string().min(2).max(50).optional(),
  age_range: z.enum(['10s', '20s', '30s', '40s', '50s_plus']).optional(),
  gender: z.enum(['male', 'female', 'unspecified']).optional(),
  travel_style: z.string().min(1).optional(),
});

const VerifyAdultSchema = z.object({
  year: z.number().int().min(1900).max(new Date().getFullYear() - 18),
  month: z.number().int().min(1).max(12),
  day: z.number().int().min(1).max(31),
});

type SignupInput = z.infer<typeof SignupSchema>;
type UpdateProfileInput = z.infer<typeof UpdateProfileSchema>;
type VerifyAdultInput = z.infer<typeof VerifyAdultSchema>;

// ============================================================================
// Server Actions
// ============================================================================

export async function signupUser(input: SignupInput): Promise<{
  success: boolean;
  error?: string;
  userId?: string;
}> {
  // 1. Validate input
  const validationResult = SignupSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid signup data' };
  }

  const { email, password, nickname, age_range, gender, travel_style } = validationResult.data;

  // 2. Create Supabase client
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  // 3. Sign up user
  const { data: authData, error: authError } = await supabase.auth.signUp({
    email,
    password,
  });

  if (authError || !authData.user) {
    console.error('Signup error:', authError);
    return { success: false, error: authError?.message || 'Signup failed' };
  }

  // 4. Create profile
  const { error: profileError } = await supabase.from('profiles').insert({
    id: authData.user.id,
    nickname,
    age_range,
    gender: gender || 'unspecified',
    travel_style,
    is_adult: false,
    role: 'member',
  });

  if (profileError) {
    console.error('Profile creation error:', profileError);
    // Cleanup: delete user if profile creation fails
    await supabase.auth.admin.deleteUser(authData.user.id).catch(() => {});
    return { success: false, error: 'Profile creation failed' };
  }

  return { success: true, userId: authData.user.id };
}

export async function updateProfile(input: UpdateProfileInput): Promise<{
  success: boolean;
  error?: string;
}> {
  // 1. Validate input
  const validationResult = UpdateProfileSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid profile data' };
  }

  // 2. Get current user
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User not authenticated' };
  }

  // 3. Update profile
  const { error } = await supabase
    .from('profiles')
    .update({
      ...validationResult.data,
      updated_at: new Date().toISOString(),
    })
    .eq('id', user.id);

  if (error) {
    console.error('Profile update error:', error);
    return { success: false, error: 'Profile update failed' };
  }

  return { success: true };
}

export async function verifyAdult(input: VerifyAdultInput): Promise<{
  success: boolean;
  error?: string;
}> {
  // 1. Validate birthdate (must be 18+)
  const validationResult = VerifyAdultSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid birthdate' };
  }

  const { year, month, day } = validationResult.data;
  const birthDate = new Date(year, month - 1, day);
  const now = new Date();
  const age = now.getFullYear() - birthDate.getFullYear();

  if (age < 18 || (age === 18 && now < new Date(now.getFullYear(), birthDate.getMonth(), birthDate.getDate()))) {
    return { success: false, error: 'Must be 18 or older' };
  }

  // 2. Get current user
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User not authenticated' };
  }

  // 3. Set adult flag + verification timestamp (NO birthdate storage)
  const { error } = await supabase
    .from('profiles')
    .update({
      is_adult: true,
      adult_verified_at: new Date().toISOString(),
    })
    .eq('id', user.id);

  if (error) {
    console.error('Adult verification error:', error);
    return { success: false, error: 'Verification failed' };
  }

  return { success: true };
}

export async function getCurrentUser(): Promise<{
  user: {
    id: string;
    email?: string;
    profile?: {
      nickname: string;
      age_range: string;
      is_adult: boolean;
    };
  } | null;
  error?: string;
}> {
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user: authUser },
  } = await supabase.auth.getUser();

  if (!authUser) {
    return { user: null };
  }

  const { data: profile } = await supabase
    .from('profiles')
    .select('nickname, age_range, is_adult')
    .eq('id', authUser.id)
    .single();

  return {
    user: {
      id: authUser.id,
      email: authUser.email,
      profile: profile || undefined,
    },
  };
}
