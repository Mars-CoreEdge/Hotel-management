# Authentication System Setup Guide

This guide explains how to set up and use the authentication system for the Grand Hotel Management System, which includes role-based access control with Supabase integration.

## Overview

The authentication system provides:
- User registration and login
- Role-based access control (Admin vs User)
- JWT token management
- Protected routes
- Supabase integration for user management

## Prerequisites

1. **Supabase Account**: You need a Supabase project
2. **Node.js**: Version 16 or higher
3. **Python**: Version 3.8 or higher
4. **FastAPI**: For the backend API

## Backend Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Other existing variables...
```

### 3. Supabase Project Setup

1. Go to [Supabase](https://supabase.com) and create a new project
2. In your project settings, get the following values:
   - Project URL
   - Anon (public) key
   - Service role key (for admin operations)

3. Enable Email Authentication in Authentication > Settings:
   - Enable "Enable email confirmations"
   - Configure SMTP settings if needed

4. Set up Row Level Security (RLS) policies for your tables

### 4. Run the Backend

```bash
cd app
python main.py
```

The API will be available at `http://localhost:8001`

## Frontend Setup

### 1. Install Dependencies

```bash
cd fruit-store-ui
npm install
```

### 2. Environment Variables

Create a `.env` file in the `fruit-store-ui` directory:

```env
REACT_APP_SUPABASE_URL=your-supabase-project-url
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
REACT_APP_API_URL=http://localhost:8001
```

### 3. Run the Frontend

```bash
npm start
```

The app will be available at `http://localhost:3000`

## Authentication Flow

### 1. User Registration

1. Users visit `/signup`
2. Fill in personal information and choose role
3. Account is created in Supabase
4. User receives confirmation email
5. Redirected to login page

### 2. User Login

1. Users visit `/login`
2. Enter email and password
3. Supabase authenticates credentials
4. JWT token is generated and stored
5. User is redirected based on role:
   - Admin → `/admin/dashboard`
   - User → `/user/dashboard`

### 3. Role-Based Access Control

- **Admin Users**: Access to all features including user management, analytics, and system settings
- **Regular Users**: Limited access to personal bookings, profile, and payment history

## API Endpoints

### Authentication Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info
- `POST /auth/password-reset` - Request password reset
- `POST /auth/password-change` - Change password
- `GET /auth/admin-only` - Admin-only endpoint (for testing)

### Protected Endpoints

All other endpoints require authentication. Admin-only endpoints require admin role.

## Frontend Components

### Core Components

1. **AuthContext**: Manages authentication state and provides auth methods
2. **ProtectedRoute**: Handles route protection and role-based access
3. **Login**: User login form
4. **Signup**: User registration form
5. **AdminDashboard**: Admin-specific dashboard
6. **UserDashboard**: User-specific dashboard

### Route Structure

```
/login - Public login page
/signup - Public signup page
/admin/dashboard - Admin dashboard (protected)
/user/dashboard - User dashboard (protected)
/ai-reception - AI reception (authenticated users)
```

## Security Features

1. **JWT Tokens**: Secure token-based authentication
2. **Role-Based Access Control**: Different permissions for different user types
3. **Protected Routes**: Automatic redirection for unauthorized access
4. **Password Validation**: Minimum length and confirmation requirements
5. **Session Management**: Automatic token refresh and logout

## Testing the System

### 1. Create Test Users

1. Visit `/signup` and create an admin user
2. Create a regular user account
3. Test login with both accounts

### 2. Test Role-Based Access

1. Login as admin and verify access to admin dashboard
2. Login as user and verify limited access
3. Try accessing admin routes as a regular user

### 3. Test Protected Routes

1. Try accessing protected routes without authentication
2. Verify proper redirection to login page
3. Test logout functionality

## Troubleshooting

### Common Issues

1. **Supabase Connection Errors**
   - Verify environment variables
   - Check Supabase project status
   - Ensure proper API keys

2. **Authentication Failures**
   - Check user credentials
   - Verify email confirmation
   - Check JWT token expiration

3. **Role Access Issues**
   - Verify user metadata in Supabase
   - Check role assignment during registration
   - Ensure proper token payload

### Debug Mode

Enable debug mode in settings to get detailed error messages:

```env
DEBUG=True
```

## Production Considerations

1. **Environment Variables**: Use proper production values
2. **JWT Secret**: Use a strong, unique secret key
3. **CORS Settings**: Configure allowed origins properly
4. **HTTPS**: Ensure all communications use HTTPS
5. **Rate Limiting**: Implement API rate limiting
6. **Logging**: Set up proper logging and monitoring

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Test with the provided test endpoints
4. Check Supabase project status and logs

## Next Steps

After setting up authentication:
1. Implement password reset functionality
2. Add email verification workflows
3. Set up user profile management
4. Implement audit logging
5. Add multi-factor authentication (optional)
