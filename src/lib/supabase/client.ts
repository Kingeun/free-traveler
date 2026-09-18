// DB-ACCESS: Supabase 클라이언트 초기화
// 클라이언트 사이드 쿼리/인증용 (Anon Key 사용, Service Role Key는 사용하지 않음)

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
