// Test Supabase Connection and Schema
// Run this in your browser console to test the connection

async function testSupabaseConnection() {
    console.log('🧪 Testing Supabase Connection...');
    
    try {
        // Test 1: Check if Supabase client is available
        if (typeof supabase === 'undefined') {
            console.error('❌ Supabase client not found');
            return;
        }
        console.log('✅ Supabase client found');
        
        // Test 2: Check if user is authenticated
        const { data: { user }, error: userError } = await supabase.auth.getUser();
        if (userError) {
            console.error('❌ Error getting user:', userError);
            return;
        }
        
        if (!user) {
            console.log('⚠️ No user logged in - please log in first');
            return;
        }
        console.log('✅ User authenticated:', user.email);
        
        // Test 3: Check user_profiles table
        console.log('🔍 Testing user_profiles table...');
        const { data: profileData, error: profileError } = await supabase
            .from('user_profiles')
            .select('*')
            .eq('user_id', user.id)
            .maybeSingle();
            
        if (profileError) {
            console.error('❌ Error accessing user_profiles:', profileError);
        } else if (profileData) {
            console.log('✅ User profile found:', profileData);
        } else {
            console.log('⚠️ No user profile found - this might be expected for new users');
        }
        
        // Test 4: Check admin_users table
        console.log('🔍 Testing admin_users table...');
        const { data: adminData, error: adminError } = await supabase
            .from('admin_users')
            .select('*')
            .eq('user_id', user.id)
            .maybeSingle();
            
        if (adminError) {
            console.error('❌ Error accessing admin_users:', adminError);
        } else if (adminData) {
            console.log('✅ Admin status found:', adminData);
        } else {
            console.log('⚠️ No admin status found - this might be expected for new users');
        }
        
        // Test 5: Test profile creation (if no profile exists)
        if (!profileData) {
            console.log('🔧 Creating user profile...');
            const { data: newProfile, error: createError } = await supabase
                .from('user_profiles')
                .insert({
                    user_id: user.id,
                    email: user.email,
                    first_name: user.user_metadata?.first_name || 'User',
                    last_name: user.user_metadata?.last_name || 'Name'
                })
                .select()
                .single();
                
            if (createError) {
                console.error('❌ Error creating profile:', createError);
            } else {
                console.log('✅ Profile created successfully:', newProfile);
            }
        }
        
        // Test 6: Test admin status creation (if no admin record exists)
        if (!adminData) {
            console.log('🔧 Creating admin status...');
            const { data: newAdmin, error: createAdminError } = await supabase
                .from('admin_users')
                .insert({
                    user_id: user.id,
                    is_admin: false
                })
                .select()
                .single();
                
            if (createAdminError) {
                console.error('❌ Error creating admin status:', createAdminError);
            } else {
                console.log('✅ Admin status created successfully:', newAdmin);
            }
        }
        
        console.log('🎉 Supabase connection test completed!');
        
    } catch (error) {
        console.error('❌ Unexpected error:', error);
    }
}

// Run the test
testSupabaseConnection();
