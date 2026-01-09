# College Event Management System - API Documentation

## Overview

Complete REST API for managing college events, registrations, attendance, and user management.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All endpoints (except login/register) require JWT authentication:

```
Authorization: Bearer <access_token>
```

---

## 🔐 **Authentication Endpoints**

### 1. User Registration

**POST** `/users/register/`

Register a new student account.

**Request Body:**

```json
{
  "email": "student@college.edu",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "student@college.edu",
    "first_name": "John",
    "role": "student"
  }
}
```

### 2. User Login

**POST** `/users/login/`

Authenticate and receive JWT tokens.

**Request Body:**

```json
{
  "email": "student@college.edu",
  "password": "securepass123"
}
```

**Response (200):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### 3. Get User Profile

**GET** `/users/profile/`

Retrieve authenticated user's profile.

**Response (200):**

```json
{
  "id": 1,
  "email": "student@college.edu",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "phone_number": "+1234567890",
  "department": { ... }
}
```

---

## 📅 **Events Endpoints**

### 1. List All Events

**GET** `/events/`

Get all published events with pagination and filtering.

**Query Parameters:**

- `page`: Page number (default: 1)
- `search`: Search by title or description
- `category`: Filter by category ID
- `ordering`: Order by field (-created_at, title, etc.)

**Response (200):**

```json
{
  "count": 50,
  "next": "http://localhost:8000/api/events/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Tech Summit 2026",
      "description": "Annual tech conference",
      "event_date": "2026-01-20",
      "start_time": "09:00:00",
      "end_time": "17:00:00",
      "venue": { ... },
      "category": { ... },
      "max_capacity": 500,
      "status": "published"
    }
  ]
}
```

### 2. Get Event Details

**GET** `/events/{id}/`

Get detailed information about a specific event.

**Response (200):**

```json
{
  "id": 1,
  "title": "Tech Summit 2026",
  "description": "...",
  "event_date": "2026-01-20",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "venue": {
    "id": 1,
    "venue_name": "Main Auditorium",
    "capacity": 500
  },
  "current_registrations": 150,
  "max_capacity": 500,
  "registration_deadline": "2026-01-19",
  "status": "published"
}
```

### 3. Create Event (Admin Only)

**POST** `/events/`

Create a new event.

**Request Body:**

```json
{
  "title": "Python Workshop",
  "description": "Learn Python programming",
  "event_date": "2026-02-15",
  "start_time": "10:00:00",
  "end_time": "14:00:00",
  "venue": 1,
  "category": 1,
  "department": 1,
  "max_capacity": 100,
  "event_type": "workshop",
  "status": "published"
}
```

**Response (201):** Event object

### 4. Update Event (Admin Only)

**PUT/PATCH** `/events/{id}/`

Update event details.

### 5. Delete Event (Admin Only)

**DELETE** `/events/{id}/`

Delete an event.

---

## 📝 **Registration Endpoints**

### 1. Get My Registrations

**GET** `/registrations/my-registrations/`

Get all registrations for the authenticated user.

**Response (200):**

```json
[
  {
    "id": 1,
    "event": { ... },
    "registered_at": "2026-01-15T10:30:00Z",
    "status": "confirmed"
  }
]
```

### 2. Register for Event

**POST** `/registrations/`

Register for an event.

**Request Body:**

```json
{
  "event": 1
}
```

**Response (201):**

```json
{
  "id": 1,
  "event": { ... },
  "user": { ... },
  "registered_at": "2026-01-15T10:30:00Z",
  "status": "confirmed"
}
```

### 3. Cancel Registration

**DELETE** `/registrations/{id}/`

Cancel a registration.

---

## 📊 **Attendance Endpoints**

### 1. Mark Attendance

**POST** `/attendance/`

Mark attendance for an event.

**Request Body:**

```json
{
  "event": 1,
  "status": "present"
}
```

**Response (201):** Attendance record

### 2. Get Attendance Records

**GET** `/attendance/?event={event_id}`

Get attendance records for an event.

---

## 🎯 **Admin Dashboard Endpoints**

### 1. Dashboard Statistics

**GET** `/admin/dashboard/`

Get dashboard statistics (admin only).

**Response (200):**

```json
{
  "total_events": 25,
  "total_registrations": 500,
  "total_users": 150,
  "upcoming_events": 10
}
```

### 2. Manage Registrations

**GET/PUT** `/admin/registrations/{id}/`

Approve/reject registrations.

---

## 📋 **Venue Endpoints**

### 1. List Venues

**GET** `/venues/`

Get all available venues.

**Response (200):**

```json
[
  {
    "id": 1,
    "venue_name": "Main Auditorium",
    "capacity": 500,
    "facilities": "Projector, Sound System",
    "availability_status": "available"
  }
]
```

---

## 📂 **Category Endpoints**

### 1. List Categories

**GET** `/categories/`

Get all event categories.

**Response (200):**

```json
[
  {
    "id": 1,
    "category_name": "Technical",
    "description": "Technical workshops and seminars"
  }
]
```

---

## ❌ **Error Responses**

### 400 Bad Request

```json
{
  "error": "Invalid input",
  "details": { "field": ["error message"] }
}
```

### 401 Unauthorized

```json
{
  "error": "Invalid email or password"
}
```

### 403 Forbidden

```json
{
  "error": "You do not have permission to access this resource"
}
```

### 404 Not Found

```json
{
  "error": "Event not found"
}
```

### 500 Server Error

```json
{
  "error": "Internal server error"
}
```

---

## 🧪 **Sample cURL Requests**

### Register User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@college.edu",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@college.edu",
    "password": "testpass123"
  }'
```

### Get Events

```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <access_token>"
```

### Register for Event

```bash
curl -X POST http://localhost:8000/api/registrations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"event": 1}'
```

---

## 🔑 **Test Credentials**

- **Admin:** admin@example.com / admin123
- **Faculty:** john.smith@college.edu / faculty123
- **Student:** aaquib@college.edu / student123
- **Organizer:** organizer@college.edu / organizer123

---

## 📱 **Rate Limiting**

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

---

## 📝 **Notes**

- All timestamps are in UTC
- Pagination default: 20 items per page
- Maximum page size: 100 items
- JWT token lifetime: 60 minutes
- Refresh token lifetime: 7 days
