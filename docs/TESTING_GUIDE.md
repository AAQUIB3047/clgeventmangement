# 🧪 GOOGLE OAUTH TESTING GUIDE

**Date:** December 30, 2025  
**Objective:** Test Google OAuth login and student enrollment system

---

## 📋 Pre-Testing Checklist

- [x] Backend: Django running (port 8000)
- [x] Frontend: Vite running (port 3000)
- [x] Database: Migrations applied
- [x] Code: All components deployed
- [ ] Google Client ID: Get from Google Cloud
- [ ] Frontend .env: Updated with Client ID

---

## 🎯 STEP 1: Get Google OAuth Client ID (5 minutes)

### 1.1 Go to Google Cloud Console

```
Visit: https://console.cloud.google.com
```

### 1.2 Create New Project

```
1. Click "Select a Project" at the top
2. Click "New Project"
3. Name: "College Event Management"
4. Click "Create"
5. Wait for project to be created
```

### 1.3 Enable Google+ API

```
1. Search for "Google+" in search bar
2. Click "Google+ API"
3. Click "Enable"
```

### 1.4 Create OAuth 2.0 Credentials

```
1. Go to "Credentials" in left sidebar
2. Click "Create Credentials"
3. Choose "OAuth 2.0 Client ID"
4. If prompted to create consent screen:
   - Click "Configure Consent Screen"
   - Choose "External"
   - Fill in app name: "College Event"
   - Add your email
   - Add test users (your emails)
   - Save
5. Back to Credentials, click "Create OAuth 2.0 Client ID"
6. Select "Web application"
7. Name: "College Event Web"
```

### 1.5 Configure Redirect URIs

```
Add these URIs to "Authorized redirect URIs":
- http://localhost:3000
- http://localhost:3000/
- http://localhost:3000/login
- http://localhost:3000/callback

(For production, add your domain later)
```

### 1.6 Copy Your Client ID

```
1. Click "Create"
2. Copy the "Client ID" from the modal
3. Keep this safe - you'll need it in Step 2
```

---

## 🔑 STEP 2: Update Frontend Configuration (2 minutes)

### 2.1 Update .env File

```bash
# File: college_event_management/frontend/.env

REACT_APP_GOOGLE_CLIENT_ID=PASTE_YOUR_CLIENT_ID_HERE

# Example (DO NOT USE - get your own):
# REACT_APP_GOOGLE_CLIENT_ID=123456789-abc123xyz789.apps.googleusercontent.com
```

### 2.2 Save and Verify

```bash
# Check that .env is updated
cat college_event_management/frontend/.env
```

Expected output:

```
VITE_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=123456789-abc123xyz789.apps.googleusercontent.com
```

---

## 🚀 STEP 3: Start Development Servers

### 3.1 Backend Server (Already Running ✅)

```bash
# Backend should be running on:
http://localhost:8000
```

### 3.2 Frontend Server (Restart if needed)

```bash
cd college_event_management/frontend
npm run dev

# Expected output:
# ➜  Local:   http://localhost:3000/
# ➜  Network: use --host to expose
```

---

## 🧪 STEP 4: Test Google Login Flow

### 4.1 Open Login Page

```
1. Open browser
2. Go to: http://localhost:3000/login
3. You should see:
   - Standard login form (email/password)
   - "or" divider
   - "Sign in with Google" button
```

### 4.2 Test Google Sign-In

```
1. Click "Sign in with Google" button
2. Google popup should appear
3. Select your Google account
4. Authorize the app when prompted
```

### 4.3 Branch Selection Modal

```
After Google login, you should see:
- Modal asking "Which branch are you from?"
- Dropdown with 7 options:
  ✓ Computer Science & Engineering (CSE)
  ✓ Electronics & Communication (ECE)
  ✓ Electrical & Electronics (EEE)
  ✓ Mechanical Engineering (ME)
  ✓ Civil Engineering (CE)
  ✓ Information Technology (IT)
  ✓ Other

Select: "Computer Science & Engineering (CSE)"
Click: "Confirm & Login"
```

### 4.4 Success Indicators

```
After branch selection, you should be:
✓ Logged in
✓ Redirected to home page
✓ Navbar shows your name
✓ Profile picture visible (from Google)
✓ Access token in localStorage
```

---

## 🔍 STEP 5: Verify Data in Admin

### 5.1 Login to Django Admin

```
1. Go to: http://localhost:8000/admin
2. Login with admin credentials:
   Email: qureshiaaquib1304@gmail.com
   Password: aaquib1304
```

### 5.2 Check Student Enrollments

```
1. In admin, click "Student Enrollments"
2. You should see your enrollment record with:
   ✓ Email: your-google-email@gmail.com
   ✓ Full Name: Your Name
   ✓ Branch: Computer Science & Engineering
   ✓ Created At: Current timestamp
```

### 5.3 Check User Profile

```
1. In admin, click "Users"
2. Find your user entry
3. Verify fields:
   ✓ email: your-google-email@gmail.com
   ✓ first_name: Your First Name
   ✓ last_name: Your Last Name
   ✓ branch: cse
   ✓ google_id: Unique Google ID
   ✓ is_google_user: True (checked)
   ✓ profile_picture: Google picture URL
```

---

## 🔗 STEP 6: Test API Endpoints

### 6.1 Get Your JWT Token

```
From localStorage in browser console:
localStorage.getItem('access_token')
# Copy the full token
```

### 6.2 Test Profile Endpoint

```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Expected Response:
{
  "id": 1,
  "email": "your-email@gmail.com",
  "first_name": "Your",
  "last_name": "Name",
  "branch": "cse",
  "is_google_user": true,
  "enrollment": {
    "email": "your-email@gmail.com",
    "full_name": "Your Name",
    "branch": "cse"
  }
}
```

### 6.3 Test Enrollments Endpoint (Admin)

```bash
curl -X GET http://localhost:8000/api/users/enrollments/ \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"

Expected Response:
{
  "count": 1,
  "enrollments": [
    {
      "id": 1,
      "email": "your-email@gmail.com",
      "full_name": "Your Name",
      "branch": "cse",
      "roll_number": "",
      "created_at": "2025-12-30T10:30:00Z"
    }
  ]
}
```

---

## ✅ STEP 7: Complete Test Checklist

### Frontend Tests

- [ ] Google button visible on login page
- [ ] Google button clickable
- [ ] Google popup appears
- [ ] Can select Google account
- [ ] Branch selection modal appears
- [ ] All 7 branches visible in dropdown
- [ ] Can select branch
- [ ] "Confirm & Login" button works
- [ ] Redirected to home after login
- [ ] Username/profile picture displayed

### Backend Tests

- [ ] User account created in database
- [ ] StudentEnrollment record created
- [ ] Email unique constraint working
- [ ] JWT tokens generated
- [ ] Tokens stored in localStorage
- [ ] Admin can view enrollment
- [ ] API endpoints responding correctly

### Data Tests

- [ ] Email from Google captured correctly
- [ ] Name from Google captured correctly
- [ ] Branch selection saved
- [ ] Timestamps recorded
- [ ] Google profile picture URL stored

### Admin Tests

- [ ] Can access Django admin
- [ ] Student Enrollments visible
- [ ] Can filter by branch
- [ ] Can search by email
- [ ] User profile shows Google info

---

## 🐛 Troubleshooting During Testing

### Issue: Google button not showing

```
Solution:
1. Check browser console for errors (F12)
2. Verify REACT_APP_GOOGLE_CLIENT_ID in .env
3. Check that it's not empty or invalid
4. Restart dev server: npm run dev
5. Clear browser cache: Ctrl+Shift+Delete
```

### Issue: "Invalid Client ID" error

```
Solution:
1. Verify Client ID from Google Console
2. Check for extra spaces in .env
3. Ensure redirect URIs match Google settings
4. Add http://localhost:3000 to redirect URIs
```

### Issue: Google popup doesn't appear

```
Solution:
1. Check browser popup blocker (allow popups)
2. Verify Google+ API is enabled
3. Check OAuth 2.0 consent screen is configured
4. Clear browser cache and cookies
```

### Issue: Branch selector doesn't appear

```
Solution:
1. Check browser console for errors
2. Verify Login.jsx has branch selector code
3. Check that Google login returned user data
4. Restart frontend dev server
```

### Issue: Data not saving to database

```
Solution:
1. Check Django migrations: python manage.py showmigrations users
2. Verify migration is applied: [X] 0002_*
3. Check backend console for errors
4. Verify StudentEnrollment model exists
5. Restart Django server
```

---

## 📊 Expected Results

### Successful Google Login Flow

```
Browser                    Google              Backend
  │                          │                    │
  ├─ Click Google button ─────>                   │
  │                          │                    │
  │ <─ Google popup ─────────┤                    │
  │                          │                    │
  ├─ Select account ─────────>                    │
  │                          │                    │
  │ <─ Auth code ─────────────┤                    │
  │                          │                    │
  ├─ Send token ─────────────────────────────────>
  │                          │                    │
  │ <─ Access + Refresh tokens ────────────────────
  │                          │                    │
  ├─ Show branch selector ──│                    │
  │                          │                    │
  ├─ Select branch ─────────│                    │
  │                          │                    │
  ├─ Confirm & Login ──────────────────────────>
  │                          │                    │
  │ <─ Enrollment created ──────────────────────
  │                          │                    │
  ├─ Redirect to home ──────│                    │
  │                          │                    │
  ✅ LOGGED IN              │                    ✅ DATA SAVED
```

---

## 📝 Test Results Template

```
═══════════════════════════════════════════════════════════
                    TEST RESULTS
═══════════════════════════════════════════════════════════

Date: _______________
Tester: _______________

FRONTEND TESTS
──────────────────────────────────────────────────────────
Google button visible:          [ ] PASS  [ ] FAIL
Google login works:             [ ] PASS  [ ] FAIL
Branch selector appears:        [ ] PASS  [ ] FAIL
Branch selection saves:         [ ] PASS  [ ] FAIL
Redirect after login:           [ ] PASS  [ ] FAIL
Profile picture displays:       [ ] PASS  [ ] FAIL

BACKEND TESTS
──────────────────────────────────────────────────────────
User created in DB:             [ ] PASS  [ ] FAIL
StudentEnrollment created:      [ ] PASS  [ ] FAIL
JWT tokens generated:           [ ] PASS  [ ] FAIL
Email unique enforced:          [ ] PASS  [ ] FAIL
Data persisted correctly:       [ ] PASS  [ ] FAIL

ADMIN TESTS
──────────────────────────────────────────────────────────
Can access admin:               [ ] PASS  [ ] FAIL
Enrollments visible:            [ ] PASS  [ ] FAIL
Can filter by branch:           [ ] PASS  [ ] FAIL
Data displayed correctly:       [ ] PASS  [ ] FAIL

API TESTS
──────────────────────────────────────────────────────────
Profile endpoint works:         [ ] PASS  [ ] FAIL
Enrollments endpoint works:     [ ] PASS  [ ] FAIL
JWT authentication works:       [ ] PASS  [ ] FAIL

OVERALL RESULT
──────────────────────────────────────────────────────────
[ ] ALL TESTS PASSED ✅
[ ] SOME TESTS FAILED ⚠️
[ ] CRITICAL ISSUES ❌

Notes:
_______________________________________________________________
_______________________________________________________________

═══════════════════════════════════════════════════════════
```

---

## 🎉 Success Criteria

```
✅ TESTING COMPLETE when:

1. Google button appears and is clickable
2. Google popup authentication works
3. Branch selection modal shows correctly
4. User can select branch and confirm
5. Redirected to home page after login
6. Student enrollment record created in DB
7. Data visible in Django admin
8. API endpoints return correct data
9. No errors in browser console
10. No errors in Django console
```

---

## 🚀 Next Steps After Testing

If all tests pass:

1. ✅ Google OAuth working
2. ✅ Student enrollment system functional
3. ✅ Admin can view enrollments
4. Ready to build **Attendance Tracking System**

---

## 📞 Need Help?

Check: `GOOGLE_OAUTH_SETUP_GUIDE.md` → Troubleshooting section

---

**Status:** Ready for Testing  
**Date:** December 30, 2025  
**Version:** 1.0
