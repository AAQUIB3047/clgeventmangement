# ⚡ QUICK TESTING START

**Backend Status:** ✅ Running on http://localhost:8000  
**Frontend Status:** ⏳ Ready (Start with: `npm run dev`)

---

## 🎯 Do These 3 Things NOW

### 1️⃣ Get Google Client ID (5 minutes)

```
1. Go: https://console.cloud.google.com
2. Create project: "College Event"
3. Enable: Google+ API
4. Create: OAuth 2.0 Web credentials
5. Add redirect URI: http://localhost:3000
6. Copy: Client ID
```

**You'll get something like:**

```
123456789-abc123xyz789.apps.googleusercontent.com
```

---

### 2️⃣ Update Frontend .env (1 minute)

**File:** `college_event_management/frontend/.env`

```env
VITE_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=PASTE_YOUR_CLIENT_ID_HERE
```

**Replace:** `PASTE_YOUR_CLIENT_ID_HERE` with your actual Client ID

---

### 3️⃣ Start Frontend & Test (1 minute)

```bash
cd college_event_management/frontend
npm run dev

# Then open: http://localhost:3000/login
# Click: "Sign in with Google"
# Select: Your Google account
# Choose: Any branch
# ✅ Logged in!
```

---

## ✅ What to Look For

**Success Indicators:**

- ✅ Google button visible on login page
- ✅ Google popup appears when clicked
- ✅ Can select your Google account
- ✅ Branch selection modal appears
- ✅ Can choose branch and confirm
- ✅ Redirected to home page
- ✅ Your name displayed in navbar

---

## 🔍 Verify in Admin

```
1. Go: http://localhost:8000/admin
2. Login with admin account
3. Go: Student Enrollments
4. You should see your enrollment record:
   - Email: your-google-email@gmail.com
   - Name: Your Name
   - Branch: The one you selected
```

---

## 📖 Complete Guide

For detailed testing steps, see: **TESTING_GUIDE.md**

---

## 🚀 You're Set!

Everything is ready. Just:

1. Get Client ID (5 min)
2. Update .env (1 min)
3. Test (5 min)

**Total: 11 minutes to full testing!**

---

**Status:** ✅ Ready to Test
