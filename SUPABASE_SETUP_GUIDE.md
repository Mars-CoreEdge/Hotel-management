# 🏨 Supabase Database Setup Guide

This guide will help you set up the complete database schema for the Hotel Management System with proper user profiles and admin management.

## 📋 Prerequisites

- Supabase project created
- Database access (SQL Editor or Dashboard)
- Frontend application running

## 🚀 Quick Setup (Recommended)

### Step 1: Run the Complete Schema
1. Go to your Supabase Dashboard
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `supabase_complete_schema.sql`
4. Click **Run** to execute the entire schema

### Step 2: Verify Setup
1. Run the contents of `verify_supabase_setup.sql`
2. Check that all components show "✅ Found" status

## 🔧 Step-by-Step Setup (Alternative)

If you prefer to run commands individually:

1. **Create Functions**: Run the function creation queries from `supabase_setup_step_by_step.sql`
2. **Create Tables**: Run the table creation queries
3. **Create Indexes**: Run the index creation queries
4. **Create Triggers**: Run the trigger creation queries
5. **Enable RLS**: Run the RLS enablement queries
6. **Create Policies**: Run the policy creation queries
7. **Grant Permissions**: Run the permission grants

## 📊 Database Schema Overview

### Tables Created

#### 1. `user_profiles`
- Stores user profile information
- Automatically linked to `auth.users`
- Includes: name, email, phone, country, age, profile picture
- Has proper constraints and validation

#### 2. `admin_users`
- Manages admin privileges
- Links to `auth.users` via `user_id`
- Default `is_admin` is `false`
- Unique constraint on `user_id`

### Functions Created

#### 1. `update_updated_at_column()`
- Automatically updates `updated_at` timestamp
- Used by both tables

#### 2. `set_user_email()`
- Automatically sets email from `auth.users`
- Ensures data consistency

#### 3. `handle_new_user()`
- Automatically creates profile and admin records
- Triggered when new user signs up
- Creates both `user_profiles` and `admin_users` entries

### Triggers Created

#### User Profiles
- `set_user_profiles_email`: Sets email from auth.users
- `update_user_profiles_updated_at`: Updates timestamp on changes

#### Admin Users
- `update_admin_users_updated_at`: Updates timestamp on changes

#### Auth Users
- `on_auth_user_created`: Creates profile and admin records on signup

### Row Level Security (RLS)

#### User Profiles Policies
- Users can view/update their own profile
- Admins can view/update all profiles

#### Admin Users Policies
- Users can view their own admin status
- Admins can view all admin statuses

## 🔐 Admin Setup

### Making the First User Admin

1. **Sign up** a new user through the frontend
2. **Go to the dashboard** (you'll see access denied page)
3. **Click "Set Admin Status"** button
4. **Refresh the page** - you should now see the dashboard

### Making Additional Users Admin

1. **Login as an existing admin**
2. **Go to the dashboard**
3. **Use the admin management features** (if implemented)

## 🧪 Testing the Setup

### 1. Test User Signup
1. Sign up a new user
2. Check if profile is created automatically
3. Verify admin status is set to false

### 2. Test Profile Access
1. Login as the user
2. Check if profile data is displayed correctly
3. Verify profile picture and name show in navbar

### 3. Test Admin Access
1. Set admin status for a user
2. Verify dashboard access is granted
3. Check if admin features are available

## 🐛 Troubleshooting

### Common Issues

#### 1. "Table doesn't exist" Error
- **Solution**: Run the complete schema setup
- **Check**: Verify tables exist in Supabase dashboard

#### 2. "Permission denied" Error
- **Solution**: Check RLS policies are created
- **Check**: Verify user is authenticated

#### 3. "Function doesn't exist" Error
- **Solution**: Run the function creation queries
- **Check**: Verify functions exist in Supabase

#### 4. Profile not created on signup
- **Solution**: Check if `handle_new_user` trigger exists
- **Check**: Verify trigger is active on `auth.users`

#### 5. Admin status not working
- **Solution**: Check if `admin_users` table exists
- **Check**: Verify RLS policies allow access

### Debug Steps

1. **Check Tables**: Run verification queries
2. **Check Functions**: Verify all functions exist
3. **Check Triggers**: Ensure triggers are active
4. **Check RLS**: Verify policies are created
5. **Check Data**: Look for test data in tables

## 📝 Frontend Integration

The frontend is already configured to work with this schema:

- **Profile Fetching**: Uses `user_profiles` table
- **Admin Check**: Uses `admin_users` table
- **Authentication**: Integrated with Supabase Auth
- **Error Handling**: Proper error handling for missing data

## 🔄 Maintenance

### Regular Checks
- Monitor table sizes
- Check for orphaned records
- Verify RLS policies are working
- Test admin functionality

### Updates
- Backup before schema changes
- Test changes in development first
- Update frontend code if needed
- Verify all functionality works

## 📞 Support

If you encounter issues:

1. **Check the verification script** results
2. **Review the error messages** carefully
3. **Check Supabase logs** for detailed errors
4. **Verify your Supabase project** is active
5. **Test with a fresh user** account

---

## ✅ Success Checklist

- [ ] All tables created successfully
- [ ] All functions created successfully
- [ ] All triggers created successfully
- [ ] RLS policies created successfully
- [ ] User signup creates profile automatically
- [ ] Admin status can be set and checked
- [ ] Dashboard access works for admins
- [ ] Profile data displays correctly
- [ ] All verification queries pass

Once all items are checked, your Supabase database is fully set up and ready for use! 🎉
