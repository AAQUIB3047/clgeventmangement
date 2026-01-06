# 🔐 Admin Panel Guide - EventHub

## How Admins Access the System

### 1. **Login as Admin**
```
URL: http://localhost:3000/login

Email: admin@example.com (or any admin user email)
Password: (Your admin password)
```

Once logged in with an admin account, you'll see an **"Admin"** link in the navbar.

### 2. **Access Admin Panel**
Click **"Admin"** in the top navigation bar, or visit:
```
URL: http://localhost:3000/admin
```

---

## 📊 Admin Dashboard Features

The admin panel has **3 main sections**:

### **1. Events Management 📊**
#### Create an Event
1. Click **"+ Create Event"** button
2. Fill in the event details:
   - **Event Title** ✓ (Required)
   - **Category** ✓ (Concert, Conference, Sports, Workshop, Festival, Other)
   - **Description** ✓ (Detailed info about the event)
   - **Date** ✓ (Event date)
   - **Time** (Event start time)
   - **Location** ✓ (Venue name)
   - **Price** (In Rupees, leave empty for free)
   - **Available Seats** ✓ (Number of tickets)
   - **Image URL** (Link to event poster/image)

3. Click **"+ Create Event"** to save
4. Success message appears → Event is live!

#### Edit an Event
1. Find the event in the list
2. Click **"✎ Edit"** button
3. Modify any details
4. Click **"✓ Update Event"**
5. Changes are saved instantly

#### Delete an Event
1. Find the event in the list
2. Click **"🗑 Delete"** button
3. Confirm deletion in the popup
4. Event is removed from the system

#### Search Events
- Use the search bar to filter events by **name** or **description**
- Results update in real-time

---

### **2. Users Management 👥**
View all registered users with the following info:
- **User Name** - Full name or email
- **Email** - Contact email
- **Role** - Admin, Organizer, or Student (color-coded)
- **Status** - Active or Inactive

#### Filter Users
- **Search**: Find users by name or email
- **Role Filter**: Show only specific roles (Admins, Organizers, Students)

#### User Badges
- 🔴 **Admin** - Red badge, full system access
- 🟢 **Organizer** - Green badge, can create events
- 🔵 **Student** - Blue badge, regular users

---

### **3. Analytics 📈**
Coming soon! This section will include:
- Event attendance statistics
- Revenue reports
- Popular events
- User engagement metrics

---

## 🛠️ Event Management Details

### Event Status
Each event displays:
- ✓ **Available** - Green badge, tickets are selling
- ✗ **Sold Out** - Red badge, all tickets booked

### Form Validation
- **Required fields** are marked with ✓
- Form won't submit if required fields are empty
- Email validation for image URLs
- Numbers validated for price and seats

### Real-time Updates
- Events appear instantly after creation
- Changes reflect immediately
- No page refresh needed
- Success/error messages appear at the top

---

## 📱 Admin Features on Mobile

The admin panel is fully responsive:
- Single-column layout on mobile
- Touch-friendly buttons
- Collapsible form sections
- Swipe-friendly search and filters

---

## 🔒 Security & Permissions

### Admin-Only Access
- Only users with `role = admin` can access `/admin`
- Non-admins are redirected to home page
- Login required - unauthenticated users redirected to `/login`
- JWT tokens secure all API requests

### What Admins Can Do
✓ Create events
✓ Edit any event
✓ Delete events
✓ View all users
✓ Filter and search
✓ Access analytics

### What Admins Cannot Do (by design)
✗ Edit user roles (requires database access)
✗ Delete user accounts (use Django admin for this)
✗ View booking details (coming soon)

---

## 🔗 Backend API Endpoints Used

The admin panel communicates with these endpoints:

```
GET  /api/events/           → Fetch all events
POST /api/events/           → Create new event
PUT  /api/events/{id}/      → Update event
DELETE /api/events/{id}/    → Delete event

GET /api/users/             → Fetch all users
```

All requests include JWT authentication headers.

---

## ⚡ Quick Actions

### Create Event in 30 Seconds
1. Log in with admin account
2. Click **Admin** → **Events**
3. Click **+ Create Event**
4. Fill: Title, Date, Location, Category, Seats
5. Click **Create Event** ✓

### Find Specific Event
1. Use the search bar
2. Type event name or keyword
3. Results filter automatically

### Change Event Details
1. Find event in list
2. Click **Edit**
3. Change any field
4. Click **Update Event**

---

## 🆘 Troubleshooting

### **Can't see Admin panel?**
- Confirm you're logged in with an admin account
- Check that your user `role = 'admin'` in database
- Try refreshing the page

### **Event creation fails?**
- Check that all required fields are filled (marked with ✓)
- Verify date is in the future
- Ensure available seats > 0
- Check browser console for error details

### **Can't delete event?**
- Confirm you have admin permissions
- Event may have active registrations (can still delete)
- Try refreshing and deleting again

### **Images not showing?**
- Ensure image URL is valid and accessible
- Image URL must start with `http://` or `https://`
- Try a different image URL

---

## 📚 Example Event Creation

**Concert Event Example:**
```
Title: Summer Rock Festival 2025
Category: Concert
Description: Join us for an unforgettable night with top bands 
             performing live. Featuring rock, pop, and indie acts.
Date: 2025-06-15
Time: 18:00
Location: College Amphitheater
Price: 500
Available Seats: 1000
Image: https://example.com/concert.jpg
```

**Workshop Event Example:**
```
Title: Web Development Bootcamp
Category: Workshop
Description: Learn React, Node.js, and databases in 3 days. 
             Hands-on training with industry experts.
Date: 2025-01-20
Time: 09:00
Location: Computer Lab A
Price: 200
Available Seats: 50
Image: https://example.com/workshop.jpg
```

---

## 🎯 Best Practices

1. **Use clear event titles** - Helps users find events
2. **Write detailed descriptions** - Include dates, requirements, schedule
3. **Add images** - Events with images get more bookings
4. **Set realistic pricing** - Price in Rupees (₹)
5. **Update capacity accurately** - Reflects actual venue size
6. **Test on mobile** - Admin panel works everywhere

---

## 📖 Additional Resources

- **Frontend Code**: `/frontend/src/pages/AdminEvents.js`
- **Styling**: `/frontend/src/pages/AdminEvents.css`
- **Backend API**: `http://localhost:8000/api/events/`
- **User Guide**: This document

---

**Last Updated**: December 29, 2025
**Admin Panel Version**: 1.0.0
**Status**: ✅ Fully Functional
