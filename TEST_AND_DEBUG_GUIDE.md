# Testing & Debugging Guide

## Current Status

### ✅ Working

- Backend: Running on http://127.0.0.1:8000/
- Frontend: Running on http://localhost:3000/
- Database: SQLite (development)
- Authentication: JWT tokens configured

### ⚠️ Issues Found

#### 1. **401 Unauthorized Errors on /api/events/**

**Status:** Non-blocking
**Cause:** Frontend making requests but events endpoint expects some auth
**Evidence:** Backend logs showing 401 errors
**Solution:** Already configured with `AllowAny` permission - should work without auth

#### 2. **No Admin User Created**

**Status:** Blocking for admin features
**Cause:** Database fresh, no superuser created yet
**Solution:** Run migration and create superuser

#### 3. **No Sample Data**

**Status:** Testing issue
**Cause:** Database is empty
**Solution:** Create sample events for testing

---

## Step-by-Step Testing Guide

### Step 1: Setup Database

```bash
# In backend directory
cd college_event_management/backend

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts:
# - Username: admin
# - Email: admin@example.com
# - Password: (set your password)
```

### Step 2: Create Sample Data

```bash
# Use Django shell to add test data
python manage.py shell

# Paste this code:
from django.contrib.auth.models import User
from events.models import Event
from datetime import datetime, timedelta

# Create test user
admin_user = User.objects.get(username='admin')
admin_user.role = 'admin'
admin_user.save()

# Create sample event
Event.objects.create(
    title="Tech Conference 2026",
    description="A great tech conference for all developers",
    date=datetime.now() + timedelta(days=30),
    location="Conference Hall A",
    capacity=100,
    organizer=admin_user,
    status='approved'
)

# Type: exit()
```

### Step 3: Test Backend APIs

#### Test without Authentication

```bash
# Get all events (should work - AllowAny)
curl http://127.0.0.1:8000/api/events/

# Get single event
curl http://127.0.0.1:8000/api/events/1/
```

#### Admin Panel

- Go to: http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Check Events, Users, Registrations

### Step 4: Test Frontend

1. Open http://localhost:3000/
2. Check browser console (F12) for errors
3. Look for events displayed on home page
4. Test navigation between pages
5. Try login functionality

### Step 5: Check Logs

**Backend Issues:**

```bash
# Watch for new requests
# Terminal shows live logs
```

**Frontend Issues:**

```bash
# Open browser DevTools (F12)
# Check Console tab for JavaScript errors
# Check Network tab for API calls
```

---

## Common Issues & Solutions

### Issue: Events not showing on frontend

**Check:**

1. Database has sample data (Run Step 2 above)
2. API endpoint returns data: curl http://127.0.0.1:8000/api/events/
3. Frontend can reach backend (check Network tab in DevTools)

**Fix:**

```bash
# Restart both servers
# Clear browser cache (Ctrl+Shift+Delete)
```

### Issue: Login not working

**Check:**

1. User exists in database
2. Password is correct
3. Token endpoint exists: http://127.0.0.1:8000/api/token/

**Test:**

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"yourpassword"}'
```

### Issue: 401 Unauthorized errors

**Cause:** Missing or invalid token
**Check:**

1. User is authenticated
2. Token is stored in localStorage
3. Token is included in API requests

**Test:**

```bash
# Get token
TOKEN=$(curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"yourpassword"}' | jq -r '.access')

# Use token in request
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/events/
```

### Issue: CORS errors

**Cause:** Frontend and backend origin mismatch
**Check:** Browser Console for CORS error messages
**Fix:** Already configured in Django settings

---

## Testing Checklist

- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Sample data added
- [ ] Can view events on homepage
- [ ] Can login to admin panel
- [ ] Can view admin dashboard
- [ ] Can create/edit/delete events (as admin)
- [ ] Can register for events (as student)
- [ ] Google OAuth working
- [ ] No console errors in browser
- [ ] All API endpoints responding

---

## Next Actions

After completing testing:

1. **Fix any issues found**
2. **Add more test data**
3. **Test all user roles** (admin, organizer, student)
4. **Test edge cases** (full event, expired event, etc.)
5. **Optimize performance** (if needed)
6. **Document any custom features**

---

## Useful Commands

```bash
# Backend shell
python manage.py shell

# Run specific migration
python manage.py migrate events

# Check database
python manage.py dbshell

# Create test data script
python manage.py shell < setup_data.py

# Clear all data (careful!)
python manage.py flush

# Show all users
python manage.py shell -c "from django.contrib.auth.models import User; print([u.username for u in User.objects.all()])"
```

---

## API Endpoints Available

```
GET    /api/events/                    - List all events
POST   /api/events/                    - Create event (admin)
GET    /api/events/{id}/               - Get single event
PUT    /api/events/{id}/               - Update event (admin)
DELETE /api/events/{id}/               - Delete event (admin)

GET    /api/users/                     - List users (admin)
POST   /api/users/                     - Create user

GET    /api/registrations/             - List registrations
POST   /api/registrations/             - Register for event

GET    /api/attendance/                - List attendance
POST   /api/attendance/                - Mark attendance

POST   /api/token/                     - Get JWT token
POST   /api/token/refresh/             - Refresh token
POST   /api/login/google/              - Google OAuth
```

---

## Questions to Test

1. Can anonymous users see approved events?
2. Can logged-in users see all events?
3. Can admin see all events regardless of status?
4. Can students register for events?
5. Can organizers create events?
6. Does token refresh work?
7. Does Google OAuth work?
8. Are attendance records created?

---

## Support

If you encounter errors:

1. Check the terminal output (above)
2. Check browser DevTools (F12)
3. Check Django admin panel
4. Review API responses with curl
5. Check database with Django shell
