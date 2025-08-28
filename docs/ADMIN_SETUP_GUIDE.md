# 👑 Admin System Setup Guide

This guide explains how to set up and use the role-based admin system in your Grand Hotel Management System.

## 🏗️ Architecture Overview

The admin system consists of:

1. **Supabase Database Table**: `admin_users` table storing admin status
2. **React Context**: `AuthContext` managing admin state
3. **Conditional Rendering**: Admin-only UI elements
4. **Protected Routes**: Admin-only access to certain features

## 📋 Prerequisites

- Supabase project set up
- Environment variables configured
- React app running

## 🗄️ Database Setup

### Step 1: Create Admin Table

Go to your **Supabase Dashboard → SQL Editor** and run:

```sql
-- Create admin table to store admin status
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON admin_users(user_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_is_admin ON admin_users(is_admin);

-- Enable Row Level Security
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
```

### Step 2: Set Up RLS Policies

```sql
-- Users can only see their own admin status
CREATE POLICY "Users can view own admin status" ON admin_users
    FOR SELECT USING (auth.uid() = user_id);

-- Only super admins can insert/update admin status
CREATE POLICY "Super admins can manage admin status" ON admin_users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM admin_users 
            WHERE user_id = auth.uid() AND is_admin = TRUE
        )
    );
```

### Step 3: Create Helper Functions

```sql
-- Function to automatically create admin record for new users
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO admin_users (user_id, is_admin)
    VALUES (NEW.id, FALSE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create admin record
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Function to check if user is admin
CREATE OR REPLACE FUNCTION is_user_admin(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM admin_users 
        WHERE user_id = user_uuid AND is_admin = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 👤 Setting Up Your First Admin

### Option 1: Using SQL (Recommended)

1. **Create a user account** through your React app
2. **Make them admin** using SQL:

```sql
-- Replace 'user@example.com' with actual email
UPDATE admin_users 
SET is_admin = TRUE 
WHERE user_id = (
    SELECT id FROM auth.users 
    WHERE email = 'user@example.com'
);
```

### Option 2: Using the Setup Script

Run the provided setup script:

```bash
cd scripts
python setup_admin.py
```

Follow the instructions to manually set up the admin user.

## 🔐 How It Works

### 1. User Registration
- When a user signs up, a record is automatically created in `admin_users` table
- Default `is_admin` value is `FALSE`

### 2. Admin Status Check
- `AuthContext` checks admin status from Supabase on login
- Admin status is stored in React state (`isAdmin`)

### 3. Conditional Rendering
- Admin-only UI elements are wrapped with `{isAdmin && (...)}`
- Navigation tabs show/hide based on admin status

### 4. Protected Features
- Administrative Dashboard tab only visible to admins
- Admin functions like user management require admin privileges

## 🎯 Admin Features

### Current Admin Features
- **Administrative Dashboard**: Main admin interface
- **User Management**: View and manage user accounts
- **System Statistics**: View system analytics
- **Database Management**: Database tools and maintenance
- **Security Settings**: Security configuration

### Future Admin Features
- **Role Management**: Create custom user roles
- **Audit Logs**: Track user actions
- **System Monitoring**: Real-time system health
- **Backup Management**: Database backup and restore

## 🚀 Testing the Admin System

### 1. Create Test User
```bash
# Sign up through your React app
# Use any email/password combination
```

### 2. Make User Admin
```sql
-- In Supabase SQL Editor
UPDATE admin_users 
SET is_admin = TRUE 
WHERE user_id = (
    SELECT id FROM auth.users 
    WHERE email = 'your-test-email@example.com'
);
```

### 3. Test Admin Access
- Log in with the admin user
- Navigate to dashboard
- Verify "Administrative Dashboard" tab is visible
- Click on admin features to test functionality

## 🔧 Troubleshooting

### Common Issues

#### 1. Admin Tab Not Visible
**Problem**: Admin tab doesn't show even after setting admin status
**Solution**: 
- Check browser console for errors
- Verify `isAdmin` state in React DevTools
- Ensure Supabase connection is working

#### 2. Permission Denied Errors
**Problem**: Getting permission errors when accessing admin features
**Solution**:
- Verify RLS policies are correctly set
- Check if user is actually marked as admin
- Ensure proper authentication

#### 3. Database Connection Issues
**Problem**: Can't connect to Supabase
**Solution**:
- Verify environment variables
- Check Supabase project status
- Ensure proper CORS configuration

### Debug Commands

```sql
-- Check if user exists
SELECT * FROM auth.users WHERE email = 'user@example.com';

-- Check admin status
SELECT 
    au.email,
    adu.is_admin,
    adu.created_at
FROM auth.users au
JOIN admin_users adu ON au.id = adu.user_id
WHERE au.email = 'user@example.com';

-- List all admin users
SELECT 
    au.email,
    adu.is_admin
FROM auth.users au
JOIN admin_users adu ON au.id = adu.user_id
WHERE adu.is_admin = TRUE;
```

## 📱 Frontend Integration

### AuthContext Usage

```javascript
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { isAdmin, user, loading } = useAuth();
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <div>
      {isAdmin && (
        <div className="admin-only-content">
          <h2>Admin Panel</h2>
          {/* Admin features */}
        </div>
      )}
    </div>
  );
}
```

### Conditional Rendering Examples

```javascript
// Show admin tab only for admins
{isAdmin && (
  <button className="nav-tab">
    <span className="tab-icon">👑</span>
    Administrative Dashboard
  </button>
)}

// Show admin content only for admins
{currentDashboardView === 'admin' && isAdmin && (
  <div className="admin-section">
    {/* Admin dashboard content */}
  </div>
)}
```

## 🔒 Security Considerations

### Row Level Security (RLS)
- Users can only see their own admin status
- Only admins can modify admin permissions
- Database triggers ensure data integrity

### Frontend Security
- Admin status is checked on every page load
- Sensitive admin functions are protected
- UI elements are conditionally rendered

### Best Practices
- Never trust frontend-only security
- Always verify admin status on backend
- Use environment variables for sensitive data
- Regularly audit admin permissions

## 📈 Monitoring and Maintenance

### Regular Tasks
- Monitor admin user list
- Audit admin actions
- Review RLS policies
- Check database performance

### Backup Strategy
- Regular database backups
- Export admin user configurations
- Document admin setup procedures

## 🎉 Conclusion

Your admin system is now set up with:
- ✅ Secure database structure
- ✅ Role-based access control
- ✅ Conditional UI rendering
- ✅ Admin-only features
- ✅ Comprehensive security policies

The system automatically handles new users and provides a scalable foundation for future admin features.

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify Supabase configuration
3. Review browser console for errors
4. Check database permissions and policies

---

**Happy Administering! 👑✨**
