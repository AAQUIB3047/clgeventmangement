# Quick Start Guide - College Event Management System

## Prerequisites
- Python 3.8+ installed
- Node.js & npm installed
- Git (optional)

---

## 🚀 Starting the Backend Server

### Windows (PowerShell)
```powershell
cd college_event_management\backend
venv\Scripts\python.exe manage.py runserver
```

### Windows (Command Prompt)
```cmd
cd college_event_management\backend
venv\Scripts\python.exe manage.py runserver
```

### Linux/Mac
```bash
cd college_event_management/backend
source venv/bin/activate
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
December 29, 2025 - 22:26:22
Django version 5.1.1, using settings 'event_management.settings'
Starting development server at http://127.0.0.1:8000/
```

✅ Backend running at: **http://localhost:8000**

---

## 🎨 Starting the Frontend Server

### Windows (PowerShell/Command Prompt)
```powershell
cd college_event_management\frontend
npm start
```

### Linux/Mac
```bash
cd college_event_management/frontend
npm start
```

**Expected Output:**
```
On Your Network:    http://192.168.x.x:3000

Local:              http://localhost:3000
```

✅ Frontend running at: **http://localhost:3000**

---

## 🔐 Admin Login Credentials

**Access the admin panel:**

1. Navigate to http://localhost:3000 in your browser
2. Click "Login"
3. Enter credentials:

```
Email:    qureshiaaquib1304@gmail.com
Password: aaquib1304
```

4. Click "Login"
5. You'll be redirected to the Admin Dashboard

---

## 📋 What You Can Do

### As Admin:
- ✅ Create new events
- ✅ Edit existing events
- ✅ Delete events
- ✅ View all users
- ✅ Manage registrations
- ✅ View attendance

### As Regular User:
- ✅ Browse events
- ✅ Register for events
- ✅ View my bookings
- ✅ Access personal dashboard

---

## 📍 Important URLs

| Page | URL | Notes |
|------|-----|-------|
| Home | http://localhost:3000 | Event listing |
| Login | http://localhost:3000/login | User authentication |
| Register | http://localhost:3000/register | New user signup |
| Admin | http://localhost:3000/admin | Admin dashboard |
| Backend API | http://localhost:8000 | REST API |
| Django Admin | http://localhost:8000/admin | Django admin panel |

---

## 🧪 Testing the API

### Check if backend is running:
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "EventHub API is running",
  "endpoints": { ... }
}
```

### Get all events:
```bash
curl http://localhost:8000/api/events/
```

### Login and get JWT token:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"qureshiaaquib1304@gmail.com","password":"aaquib1304"}'
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Error: "Port 8000 already in use"**
```powershell
# Use a different port
python manage.py runserver 8001
```

**Error: "Module not found"**
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "Database locked"**
```powershell
# Delete and reset database
rm db.sqlite3
python manage.py migrate
```

### Frontend Issues

**Error: "npm not found"**
- Install Node.js from https://nodejs.org/
- Restart terminal

**Error: "Module not found"**
```bash
# Reinstall dependencies
rm -r node_modules package-lock.json
npm install
```

**Port 3000 already in use:**
```bash
# Kill the process using port 3000
# Windows: Use Task Manager
# Linux/Mac: lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

---

## 📝 File Structure

```
college_event_management/
├── backend/           ← Django REST API
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   └── venv/
│
├── frontend/          ← React App
│   ├── package.json
│   ├── public/
│   └── src/
│
└── spring_backend/    ← Optional Spring Boot backend
```

---

## 🔄 Common Commands

### Backend
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check system health
python manage.py check

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

### Frontend
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject configuration (⚠️ irreversible)
npm run eject
```

---

## 🚀 Deployment Notes

### Before Going Live:

1. **Backend (Django):**
   - Set `DEBUG = False`
   - Change `SECRET_KEY`
   - Update `ALLOWED_HOSTS`
   - Use PostgreSQL instead of SQLite
   - Set environment variables
   - Use Gunicorn/uWSGI server

2. **Frontend (React):**
   - Build production version: `npm run build`
   - Deploy build folder to hosting
   - Update API URLs to production backend

3. **Security:**
   - Enable HTTPS/SSL
   - Configure CORS properly
   - Set secure cookie flags
   - Enable CSRF protection

---

## ❓ FAQ

**Q: Can I use the same machine for frontend and backend?**  
A: Yes! They run on different ports (8000 and 3000) and can both run simultaneously.

**Q: How do I change the admin password?**  
A: Log in to the Django admin at http://localhost:8000/admin and use "Change password" option.

**Q: Can I add more events?**  
A: Yes! Log in as admin and use the "Create Event" button in the admin panel.

**Q: Is the database persistent?**  
A: Yes, data is stored in `db.sqlite3`. Deleting this file will reset all data.

---

## 📞 Support

If you encounter issues:

1. Check the console for error messages
2. Verify both servers are running
3. Ensure ports 3000 and 8000 are available
4. Try clearing cache (`Ctrl+F5` in browser)
5. Restart both servers

---

**You're all set! Happy event managing! 🎉**

