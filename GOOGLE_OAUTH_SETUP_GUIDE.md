# Google OAuth Integration Guide

## Overview

Your application now supports Google OAuth login with automatic email and branch enrollment tracking. Students can sign in with their Google email and specify their branch for attendance tracking.

## Features Implemented

### 1. **Google Sign-In Button**

- Located on the Login page
- One-click authentication
- Automatically captures user name and profile picture
- Branch selection prompt after first login

### 2. **Student Enrollment Dataset**

- Stores: Email, Full Name, Branch, Roll Number
- Accessible via admin dashboard
- Tracks student enrollment for attendance purposes
- Automatically created on first Google login

### 3. **Backend API Endpoints**

- `POST /api/users/google_login/` - Google OAuth login
- `GET /api/users/enrollments/` - View all student enrollments (admin only)
- `GET /api/users/profile/` - Get current user profile

### 4. **User Model Enhancements**

- `branch` field - Store student branch information
- `google_id` - Google account identifier
- `is_google_user` - Flag for Google authentication
- `profile_picture` - User's Google profile picture URL

---

## Setup Instructions

### Step 1: Get Google OAuth Credentials

1. **Go to Google Cloud Console**

   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Create a New Project**

   - Click "Select a Project" → "New Project"
   - Name it: "College Event Management"
   - Click "Create"

3. **Enable OAuth 2.0**

   - Search for "OAuth 2.0" in the search bar
   - Find "Google OAuth 2.0"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**

   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Web application"
   - Name it: "College Event Management Web"

5. **Configure Authorized URIs**

   - Under "Authorized redirect URIs", add:
     ```
     http://localhost:3000
     http://localhost:3000/
     http://localhost:3000/login
     ```
   - For production, add your domain:
     ```
     https://yourdomain.com
     https://yourdomain.com/login
     ```

6. **Copy Your Client ID**
   - Click "Create"
   - Copy the "Client ID" from the modal

### Step 2: Configure Frontend

1. **Update Frontend .env**

   ```bash
   # college_event_management/frontend/.env
   REACT_APP_GOOGLE_CLIENT_ID=YOUR_COPIED_CLIENT_ID_HERE
   ```

2. **Restart Frontend Development Server**
   ```bash
   cd college_event_management/frontend
   npm run dev
   ```

### Step 3: Configure Backend (Optional)

For enhanced security in production, configure the backend to verify Google tokens:

```bash
# college_event_management/backend/.env
GOOGLE_CLIENT_ID=YOUR_COPIED_CLIENT_ID_HERE
```

**Note:** For development, token verification is skipped. In production, the backend validates tokens with Google.

---

## User Flow

### First Time Google Login

1. User clicks "Sign in with Google" button
2. Google login popup appears
3. User selects their Google account
4. App prompts for branch selection
5. System creates:
   - New User account
   - StudentEnrollment record with email, name, and branch
   - JWT tokens for session

### Subsequent Logins

1. User clicks "Sign in with Google"
2. Instant login (Google remembers the account)
3. No branch selection needed (already in system)

---

## Database Schema

### User Model Fields

| Field             | Type         | Purpose                             |
| ----------------- | ------------ | ----------------------------------- |
| `email`           | EmailField   | Unique email address                |
| `first_name`      | CharField    | User's first name                   |
| `last_name`       | CharField    | User's last name                    |
| `branch`          | CharField    | Student branch (CSE, ECE, etc.)     |
| `google_id`       | CharField    | Unique Google ID                    |
| `is_google_user`  | BooleanField | Authentication method               |
| `profile_picture` | URLField     | Google profile picture              |
| `role`            | CharField    | User role (student/organizer/admin) |

### StudentEnrollment Model (NEW)

| Field         | Type          | Purpose                |
| ------------- | ------------- | ---------------------- |
| `user`        | OneToOneField | Reference to User      |
| `email`       | EmailField    | Student email (unique) |
| `full_name`   | CharField     | Complete name          |
| `branch`      | CharField     | Branch information     |
| `roll_number` | CharField     | Roll number (optional) |
| `created_at`  | DateTimeField | Enrollment timestamp   |
| `updated_at`  | DateTimeField | Last update timestamp  |

---

## Admin Access to Enrollment Data

### Via API

```bash
# Get all student enrollments
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/users/enrollments/
```

Response:

```json
{
  "count": 150,
  "enrollments": [
    {
      "id": 1,
      "email": "student@gmail.com",
      "full_name": "John Doe",
      "branch": "cse",
      "roll_number": "21IT001",
      "created_at": "2025-12-30T10:30:00Z"
    }
  ]
}
```

### Via Django Admin Panel

1. Go to: http://localhost:8000/admin
2. Login with admin credentials
3. Navigate to "Student Enrollments"
4. View/export all student data

---

## Branch Options

The system supports the following branches:

| Code    | Branch Name                    |
| ------- | ------------------------------ |
| `cse`   | Computer Science & Engineering |
| `ece`   | Electronics & Communication    |
| `eee`   | Electrical & Electronics       |
| `me`    | Mechanical Engineering         |
| `ce`    | Civil Engineering              |
| `it`    | Information Technology         |
| `other` | Other                          |

---

## API Examples

### Google Login Endpoint

```javascript
// Frontend Code
POST http://localhost:8000/api/users/google_login/

Request Body:
{
  "token": "google_id_token_from_library",
  "name": "John Doe",
  "email": "john@gmail.com",
  "picture": "https://lh3.googleusercontent.com/...",
  "branch": "cse"
}

Response:
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "email": "john@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "branch": "cse",
    "is_google_user": true,
    "enrollment": {
      "email": "john@gmail.com",
      "full_name": "John Doe",
      "branch": "cse"
    }
  }
}
```

---

## Troubleshooting

### "Sign in with Google button not showing"

- Check if `REACT_APP_GOOGLE_CLIENT_ID` is set in `.env`
- Restart the frontend dev server after changing `.env`
- Ensure the Client ID is correct (no spaces or typos)

### "Invalid Client ID" error

- Verify the Client ID from Google Cloud Console
- Ensure it matches between frontend `.env` and Google settings
- Check that URIs are correctly configured in Google Console

### "User not created" after Google login

- Check Django migrations: `python manage.py migrate`
- Verify the User model has the new fields
- Check backend logs for errors

### Branch not saving

- Ensure the branch value matches one of the valid options
- Check that the StudentEnrollment model exists in database
- Verify migration was applied: `python manage.py showmigrations users`

---

## Security Considerations

### In Development

- Token verification is optional
- Suitable for testing and development

### In Production

1. **Enable Token Verification**

   - Set `GOOGLE_CLIENT_ID` in backend `.env`
   - Backend validates all tokens with Google
   - Prevents token spoofing

2. **HTTPS Required**

   - All OAuth flows must use HTTPS
   - Google Console requires HTTPS URIs

3. **CORS Configuration**

   - Backend allows only your frontend origin
   - Update `ALLOWED_HOSTS` in Django settings

4. **Environment Variables**
   - Never commit `.env` files to git
   - Use `.env.example` for documentation
   - Deploy secrets via CI/CD or config management

---

## Next Steps: Attendance Tracking

The enrollment dataset is now ready for building the attendance system:

1. **Admin Dashboard Feature**

   - View enrolled students filtered by branch
   - Generate attendance reports
   - Export student lists

2. **Event Attendance**

   - Mark attendance for students at events
   - Filter by branch to see who attended
   - Generate per-branch attendance statistics

3. **Student Perspective**
   - View their attendance history
   - See events attended
   - Download attendance certificates

---

## Files Modified/Created

### Backend

- ✅ `users/models.py` - Added branch field and StudentEnrollment model
- ✅ `users/serializers.py` - Added GoogleAuthSerializer
- ✅ `users/views.py` - Added google_login endpoint
- ✅ `users/urls.py` - Added google_login and enrollments routes
- ✅ `users/admin.py` - Enhanced admin interface
- ✅ `users/migrations/0002_*` - Database migration
- ✅ `.env` - Configuration file

### Frontend

- ✅ `src/pages/Login.jsx` - Google sign-in button integration
- ✅ `src/App.jsx` - GoogleOAuthProvider wrapper
- ✅ `src/pages/Auth.css` - Styling for Google button and branch selector
- ✅ `.env` - Environment variables

---

## Support & Debugging

**Enable Debug Mode (Backend)**

```bash
# In django settings
DEBUG = True
```

**Check Migration Status**

```bash
cd college_event_management/backend
python manage.py showmigrations users
```

**View API Responses**

```bash
# Frontend console (F12 → Console)
localStorage.getItem('access_token')
localStorage.getItem('user')
```

---

**Setup Status: ✅ COMPLETE**

Your Google OAuth integration is ready! Users can now:

- Sign in with Google email
- Automatically enroll with their branch
- Be tracked for event attendance
