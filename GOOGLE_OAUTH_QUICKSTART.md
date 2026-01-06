# Google OAuth Quick Setup (5 Minutes)

## What's New?

✅ Google login button on Login page  
✅ Student enrollment dataset stores email & branch  
✅ Admin can view all enrolled students  
✅ Branch tracking for attendance purposes

---

## Quick Setup

### 1️⃣ Get Google Client ID (2 minutes)

1. Go to: https://console.cloud.google.com
2. Create new project → Name it "College Event"
3. Search "Google+" → Click "Enable"
4. Go to "Credentials" → "Create OAuth 2.0 Client ID"
5. Choose "Web application"
6. Add URIs:
   - `http://localhost:3000`
   - `http://localhost:3000/login`
7. Click "Create" and copy the Client ID

### 2️⃣ Paste Client ID in Frontend (.env)

```bash
# college_event_management/frontend/.env

REACT_APP_GOOGLE_CLIENT_ID=PASTE_YOUR_CLIENT_ID_HERE
```

### 3️⃣ Restart Frontend Server

```bash
cd college_event_management/frontend
npm run dev
```

✅ **Done!** Google login is now active!

---

## Testing Google Login

1. Open http://localhost:3000/login
2. Click "Sign in with Google" button
3. Select your Google account
4. Choose your branch
5. ✅ Logged in! Check the enrollment data in admin panel

---

## View Student Enrollments

### Option A: Django Admin Panel

1. Go to: http://localhost:8000/admin
2. Login with admin account
3. Click "Student Enrollments"
4. See all students with their email and branch

### Option B: API

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/users/enrollments/
```

---

## Database Schema

### New Fields in User Model

- `branch` - Student's branch (CSE, ECE, etc.)
- `google_id` - Google account ID
- `is_google_user` - True if logged in with Google
- `profile_picture` - Google profile picture URL

### New StudentEnrollment Table

```
┌──────────────────────┐
│  StudentEnrollment   │
├──────────────────────┤
│ id                   │
│ email (unique)       │
│ full_name            │
│ branch               │
│ roll_number          │
│ created_at           │
│ updated_at           │
└──────────────────────┘
```

---

## Next: Build Attendance System

Now you have the enrollment data! Next steps:

1. **Admin Dashboard** - View students by branch
2. **Event Attendance** - Mark attendance at events
3. **Reports** - Generate attendance statistics per branch

---

**Status: ✅ Ready to Use**

Questions? See `GOOGLE_OAUTH_SETUP_GUIDE.md` for details.
