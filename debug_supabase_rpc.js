// Debug script to test Supabase RPC function
// Run this in your browser console on the profile page

async function debugSupabaseRPC() {
  console.log('🔍 Debugging Supabase RPC Function...');
  
  // Get the current Supabase client
  const supabase = window.supabase;
  if (!supabase) {
    console.error('❌ Supabase client not found');
    return;
  }
  
  // Test 1: Check if user is authenticated
  const { data: { session } } = await supabase.auth.getSession();
  console.log('📋 Session:', session ? 'Authenticated' : 'Not authenticated');
  
  if (!session) {
    console.error('❌ User not authenticated');
    return;
  }
  
  // Test 2: Check if the function exists
  try {
    console.log('🔍 Testing if upsert_user_profile function exists...');
    const { data, error } = await supabase.rpc('upsert_user_profile', {
      p_first_name: 'Test',
      p_last_name: 'User',
      p_email: session.user.email,
      p_phone: null,
      p_country: null,
      p_age: null,
      p_profile_picture_url: null
    });
    
    if (error) {
      console.error('❌ RPC Error:', error);
      
      // Check if it's a function not found error
      if (error.message.includes('function') && error.message.includes('does not exist')) {
        console.log('💡 Solution: The SQL script needs to be executed in Supabase');
        console.log('📝 Steps:');
        console.log('1. Go to your Supabase dashboard');
        console.log('2. Navigate to SQL Editor');
        console.log('3. Copy and paste the contents of supabase_fixed_sql.sql');
        console.log('4. Click Run to execute the script');
      }
    } else {
      console.log('✅ RPC Function works!', data);
    }
  } catch (err) {
    console.error('❌ Unexpected error:', err);
  }
  
  // Test 3: Check if user_profiles table exists
  try {
    console.log('🔍 Testing if user_profiles table exists...');
    const { data, error } = await supabase
      .from('user_profiles')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('❌ Table Error:', error);
      if (error.message.includes('relation') && error.message.includes('does not exist')) {
        console.log('💡 Solution: The user_profiles table needs to be created');
        console.log('📝 Run the SQL script in Supabase to create the table');
      }
    } else {
      console.log('✅ user_profiles table exists!');
    }
  } catch (err) {
    console.error('❌ Unexpected table error:', err);
  }
}

// Run the debug function
debugSupabaseRPC();
