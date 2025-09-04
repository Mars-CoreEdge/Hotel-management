-- ===========================================
-- VERIFICATION SCRIPT FOR SUPABASE SETUP
-- ===========================================

-- Check if tables exist
SELECT 
    'Tables Check' as check_type,
    schemaname,
    tablename,
    tableowner,
    CASE 
        WHEN tablename IN ('user_profiles', 'admin_users') THEN '✅ Found'
        ELSE '❌ Missing'
    END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('user_profiles', 'admin_users')
ORDER BY tablename;

-- Check if functions exist
SELECT 
    'Functions Check' as check_type,
    routine_name,
    routine_type,
    '✅ Found' as status
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_name IN ('update_updated_at_column', 'set_user_email', 'handle_new_user')
ORDER BY routine_name;

-- Check if triggers exist
SELECT 
    'Triggers Check' as check_type,
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation,
    '✅ Found' as status
FROM information_schema.triggers 
WHERE trigger_schema = 'public'
AND event_object_table IN ('user_profiles', 'admin_users', 'users')
ORDER BY event_object_table, trigger_name;

-- Check RLS policies
SELECT 
    'RLS Policies Check' as check_type,
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    '✅ Found' as status
FROM pg_policies 
WHERE schemaname = 'public'
AND tablename IN ('user_profiles', 'admin_users')
ORDER BY tablename, policyname;

-- Check table structure
SELECT 
    'Table Structure Check' as check_type,
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_schema = 'public'
AND table_name IN ('user_profiles', 'admin_users')
ORDER BY table_name, ordinal_position;

-- Test data insertion (this will be rolled back)
BEGIN;

-- Test inserting a user profile
INSERT INTO public.user_profiles (user_id, email, first_name, last_name)
VALUES (
    '00000000-0000-0000-0000-000000000000'::uuid,
    'test@example.com',
    'Test',
    'User'
);

-- Test inserting an admin user
INSERT INTO public.admin_users (user_id, is_admin)
VALUES ('00000000-0000-0000-0000-000000000000'::uuid, false);

-- Check if data was inserted
SELECT 'Data Insertion Test' as check_type, 'user_profiles' as table_name, COUNT(*) as record_count FROM public.user_profiles WHERE user_id = '00000000-0000-0000-0000-000000000000'::uuid
UNION ALL
SELECT 'Data Insertion Test' as check_type, 'admin_users' as table_name, COUNT(*) as record_count FROM public.admin_users WHERE user_id = '00000000-0000-0000-0000-000000000000'::uuid;

-- Rollback test data
ROLLBACK;

-- Final status
SELECT 
    'Setup Status' as check_type,
    CASE 
        WHEN (SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('user_profiles', 'admin_users')) = 2
        AND (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public' AND routine_name IN ('update_updated_at_column', 'set_user_email', 'handle_new_user')) = 3
        THEN '✅ All Good - Setup Complete'
        ELSE '❌ Setup Incomplete - Check individual components'
    END as status;
