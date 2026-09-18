// API-BLOCKS-REPORTS: User blocking and report creation/admin management
// REQ-FUNC-039: Block user, REQ-FUNC-040: Unblock user
// REQ-FUNC-041: Create report, REQ-FUNC-042: Admin update report status

'use server';

import { z } from 'zod';
import { createClient } from '@supabase/supabase-js';

// ============================================================================
// Validation Schemas
// ============================================================================

const BlockUserSchema = z.object({
  blocked_id: z.string().uuid('Invalid user ID'),
});

const CreateReportSchema = z.object({
  target_post_id: z.string().uuid('Invalid post ID').optional(),
  target_user_id: z.string().uuid('Invalid user ID').optional(),
  reason_code: z.enum(['SPAM', 'HARASSMENT', 'SCAM', 'INAPPROPRIATE', 'OTHER']),
  description: z.string().max(1000, 'Description too long').optional(),
});

const UpdateReportStatusSchema = z.object({
  report_id: z.string().uuid('Invalid report ID'),
  status: z.enum(['OPEN', 'REVIEWING', 'RESOLVED', 'DISMISSED']),
});

type BlockUserInput = z.infer<typeof BlockUserSchema>;
type CreateReportInput = z.infer<typeof CreateReportSchema>;
type UpdateReportStatusInput = z.infer<typeof UpdateReportStatusSchema>;

// ============================================================================
// Helper Functions
// ============================================================================

async function isCurrentUserAdmin(): Promise<boolean> {
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) return false;

  const { data: profile } = await supabase.from('profiles').select('role').eq('id', user.id).single();

  return profile?.role === 'admin' || false;
}

function validateReportTarget(input: CreateReportInput): boolean {
  // Must have at least one target (post OR user)
  return !!(input.target_post_id || input.target_user_id);
}

// ============================================================================
// Server Actions
// ============================================================================

export async function blockUser(input: BlockUserInput): Promise<{
  success: boolean;
  error?: string;
  block_id?: string;
}> {
  // 1. Validate input
  const validationResult = BlockUserSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid user ID' };
  }

  // 2. Get current user
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User not authenticated' };
  }

  // 3. Prevent self-blocking
  if (user.id === input.blocked_id) {
    return { success: false, error: 'Cannot block yourself' };
  }

  // 4. Create block record
  const { data, error } = await supabase
    .from('user_blocks')
    .insert({
      blocker_id: user.id,
      blocked_id: input.blocked_id,
    })
    .select('id')
    .single();

  if (error) {
    if (error.code === '23505') {
      // Unique constraint violation = already blocked
      return { success: false, error: 'User already blocked' };
    }
    console.error('Block error:', error);
    return { success: false, error: 'Block failed' };
  }

  return { success: true, block_id: data.id };
}

export async function unblockUser(blocked_id: string): Promise<{
  success: boolean;
  error?: string;
}> {
  // 1. Validate input
  if (!blocked_id || blocked_id.length !== 36) {
    return { success: false, error: 'Invalid user ID' };
  }

  // 2. Get current user
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User not authenticated' };
  }

  // 3. Delete block record (RLS ensures only blocker can delete their own blocks)
  const { error } = await supabase.from('user_blocks').delete().eq('blocker_id', user.id).eq('blocked_id', blocked_id);

  if (error) {
    console.error('Unblock error:', error);
    return { success: false, error: 'Unblock failed' };
  }

  return { success: true };
}

export async function createReport(input: CreateReportInput): Promise<{
  success: boolean;
  error?: string;
  report_id?: string;
}> {
  // 1. Validate input
  const validationResult = CreateReportSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid report data' };
  }

  // 2. Validate report target
  if (!validateReportTarget(validationResult.data)) {
    return { success: false, error: 'Must report either a post or a user' };
  }

  // 3. Get current user
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { success: false, error: 'User not authenticated' };
  }

  // 4. Create report (response within 3 seconds per REQ-FUNC-041)
  const { data, error } = await supabase
    .from('reports')
    .insert({
      reporter_id: user.id,
      target_post_id: validationResult.data.target_post_id || null,
      target_user_id: validationResult.data.target_user_id || null,
      reason_code: validationResult.data.reason_code,
      description: validationResult.data.description || null,
      status: 'OPEN',
    })
    .select('id')
    .single();

  if (error) {
    console.error('Report creation error:', error);
    return { success: false, error: 'Report creation failed' };
  }

  return { success: true, report_id: data.id };
}

export async function updateReportStatus(input: UpdateReportStatusInput): Promise<{
  success: boolean;
  error?: string;
}> {
  // 1. Validate input
  const validationResult = UpdateReportStatusSchema.safeParse(input);
  if (!validationResult.success) {
    return { success: false, error: 'Invalid report data' };
  }

  // 2. Check admin authorization (REQ-FUNC-042: admin-only)
  const isAdmin = await isCurrentUserAdmin();
  if (!isAdmin) {
    return { success: false, error: 'Unauthorized: admin access required' };
  }

  // 3. Update report status
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const { error } = await supabase
    .from('reports')
    .update({
      status: validationResult.data.status,
      updated_at: new Date().toISOString(),
    })
    .eq('id', validationResult.data.report_id);

  if (error) {
    console.error('Report update error:', error);
    return { success: false, error: 'Report update failed' };
  }

  return { success: true };
}

export async function getUserBlockList(): Promise<{
  blocked_ids: string[];
  error?: string;
}> {
  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { blocked_ids: [] };
  }

  const { data, error } = await supabase.from('user_blocks').select('blocked_id').eq('blocker_id', user.id);

  if (error) {
    console.error('Block list fetch error:', error);
    return { blocked_ids: [], error: 'Failed to fetch block list' };
  }

  return { blocked_ids: (data || []).map((r) => r.blocked_id) };
}
