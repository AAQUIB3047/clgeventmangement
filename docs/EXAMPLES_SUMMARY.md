# ✨ React + Vite Frontend & Django Backend Examples

Complete examples and best practices for building the College Event Management system.

---

## 📚 What's New

### Frontend Examples Created

1. **Components**

   - ✅ `EventCard.jsx` - Reusable event display component
   - ✅ `Navbar.jsx` - Navigation with auth integration
   - ✅ Comprehensive styling for both

2. **Hooks** (`src/hooks/useCustom.js`)

   - ✅ `useApi` - API calls with loading/error states
   - ✅ `useForm` - Form state management
   - ✅ `useLocalStorage` - Storage persistence
   - ✅ `usePagination` - Pagination logic
   - ✅ `useDebounce` - Debounced values

3. **Services** (`src/services/api.js`)

   - ✅ `eventsService` - Event endpoints
   - ✅ `usersService` - User management
   - ✅ `registrationsService` - Event registrations
   - ✅ `attendanceService` - Attendance tracking
   - ✅ `reportsService` - Analytics & reports
   - ✅ `dashboardService` - Dashboard data
   - ✅ `authService` - Authentication

4. **Utils** (`src/utils/helpers.js`)

   - ✅ `api` - Centralized API requests
   - ✅ `validators` - Input validation functions
   - ✅ `formatters` - Date, currency, text formatting
   - ✅ `storage` - LocalStorage management
   - ✅ `notify` - Notification helpers

5. **Pages**

   - ✅ `Events.jsx` - Events listing with filters
   - ✅ Complete styling & responsiveness

6. **Documentation**
   - ✅ `FRONTEND_EXAMPLES.md` - Comprehensive guide

### Backend Examples Created

1. **Documentation**
   - ✅ `BACKEND_EXAMPLES.md` - Complete backend guide

---

## 🎯 Quick Start Guide

### Frontend

**Setup:**

```bash
cd college_event_management/frontend
npm install
npm run dev
```

**Example: Using useApi Hook**

```jsx
import { useApi } from "../hooks/useCustom";
import { eventsService } from "../services/api";

function EventsList() {
  const { data: events, loading, error } = useApi("/api/events/");

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error</div>;

  return (
    <div>
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}
```

**Example: Using Services**

```jsx
import { eventsService, usersService } from "../services/api";

// Get all events
const events = await eventsService.getAll({ status: "upcoming" });

// Google login
const response = await usersService.googleLogin(token, "CSE");
```

**Example: Validation**

```jsx
import { validators } from "../utils/helpers";

if (!validators.isEmail(email)) {
  setError("Invalid email");
}

if (!validators.isStrongPassword(password)) {
  setError("Password too weak");
}
```

### Backend

**Setup:**

```bash
cd college_event_management/backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Example: API Endpoints**

```bash
# Google Login
POST /api/users/google_login/
{
  "token": "google_jwt_token",
  "branch": "CSE"
}

# Get Enrollments (Admin)
GET /api/users/enrollments/?branch=CSE
Authorization: Bearer access_token

# Get User Profile
GET /api/users/profile/
Authorization: Bearer access_token
```

---

## 📁 File Structure

```
college_event_management/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── EventCard.jsx          ✅ NEW
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── Events.jsx             ✅ NEW
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── ...
│   │   ├── hooks/
│   │   │   └── useCustom.js           ✅ NEW
│   │   ├── services/
│   │   │   └── api.js                 ✅ NEW
│   │   ├── utils/
│   │   │   └── helpers.js             ✅ NEW
│   │   ├── styles/
│   │   │   ├── eventcard.css          ✅ NEW
│   │   │   ├── navbar.css             ✅ NEW
│   │   │   ├── Events.css             ✅ NEW
│   │   │   └── ...
│   │   └── App.jsx
│   ├── FRONTEND_EXAMPLES.md           ✅ NEW
│   └── ...
│
└── backend/
    ├── users/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   └── migrations/
    ├── events/
    ├── registrations/
    ├── attendance/
    ├── reports/
    ├── BACKEND_EXAMPLES.md            ✅ NEW
    ├── manage.py
    ├── requirements.txt
    └── ...
```

---

## 🔥 Key Features Demonstrated

### Frontend

1. **Component Composition**

   - Reusable EventCard component
   - Navbar with responsive design
   - Proper prop drilling and state management

2. **State Management**

   - useApi hook for data fetching
   - useForm hook for form handling
   - useLocalStorage hook for persistence
   - Custom hooks for pagination & debouncing

3. **Styling**

   - CSS variables for theming
   - Responsive design (mobile-first)
   - Dark mode ready
   - Flexbox & Grid layouts

4. **API Integration**

   - Centralized api helper
   - Service layer architecture
   - Error handling & retry logic
   - JWT token management

5. **Validation**
   - Email, password, phone validators
   - Form field validation
   - Real-time error messages

### Backend

1. **Models**

   - Custom User model with Google OAuth
   - StudentEnrollment for attendance tracking
   - Proper relationships & constraints

2. **Serializers**

   - Google authentication serializer
   - User serialization
   - Enrollment data serialization

3. **Views**

   - ViewSet for standard CRUD operations
   - Custom actions (google_login, profile, enrollments)
   - Proper permission classes
   - Error handling

4. **Admin Interface**

   - Custom UserAdmin with filters
   - StudentEnrollmentAdmin
   - Search & filtering capabilities
   - Readonly fields

5. **API Design**
   - RESTful endpoints
   - Proper HTTP methods
   - Standard response format
   - Error handling

---

## 💡 Usage Examples

### Fetch Events

**Frontend:**

```jsx
import { eventsService } from "../services/api";

async function getEvents() {
  const events = await eventsService.getAll({ status: "upcoming" });
  return events;
}
```

**Backend:**

```python
@api_view(['GET'])
def get_events(request):
    status = request.query_params.get('status')
    events = Event.objects.filter(status=status)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
```

### Create Form

**Frontend:**

```jsx
import { useForm } from "../hooks/useCustom";
import { validators } from "../utils/helpers";

function LoginForm() {
  const { values, errors, handleChange, handleSubmit } = useForm(
    { email: "", password: "" },
    async (values) => {
      if (!validators.isEmail(values.email)) {
        throw new Error("Invalid email");
      }
      await authService.login(values.email, values.password);
    }
  );

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" value={values.email} onChange={handleChange} />
      {errors.email && <span>{errors.email}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

### Protect Routes

**Frontend:**

```jsx
<Route
  path="/admin"
  element={
    isAuthenticated && user?.role === "admin" ? (
      <AdminDashboard />
    ) : (
      <Navigate to="/login" />
    )
  }
/>
```

**Backend:**

```python
class EventViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

---

## 🚀 What You Can Build Now

With these examples, you can easily build:

1. ✅ **Event Management System**

   - List, filter, and display events
   - Event details page
   - Event registration

2. ✅ **User Management**

   - Google OAuth login
   - User profile
   - Admin user management

3. ✅ **Attendance Tracking**

   - Enrollment data collection
   - Attendance by branch
   - Attendance reports

4. ✅ **Admin Dashboard**

   - Event statistics
   - User management
   - Enrollment viewing
   - Attendance reports

5. ✅ **Mobile-Responsive UI**
   - Works on all devices
   - Touch-friendly buttons
   - Responsive grid layouts

---

## 📖 Documentation Files

Located in project root and subdirectories:

- `FRONTEND_EXAMPLES.md` - Comprehensive frontend guide
- `BACKEND_EXAMPLES.md` - Comprehensive backend guide
- `QUICK_TEST.md` - Quick testing guide
- `TESTING_GUIDE.md` - Detailed testing procedures
- Previous documentation on Google OAuth implementation

---

## ✅ Next Steps

1. **Review the examples** in respective documentation files
2. **Test the API** using provided examples
3. **Build new pages** using the component patterns
4. **Add new services** following the service architecture
5. **Deploy** to production

---

## 🎓 Learning Resources

**Frontend:**

- React Hooks: https://react.dev/reference/react
- Vite Guide: https://vitejs.dev/guide/
- REST API Client: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

**Backend:**

- Django ORM: https://docs.djangoproject.com/en/stable/topics/db/models/
- DRF Serializers: https://www.django-rest-framework.org/api-guide/serializers/
- DRF ViewSets: https://www.django-rest-framework.org/api-guide/viewsets/

---

## 🎯 Key Takeaways

| Aspect     | Pattern                    | Location                 |
| ---------- | -------------------------- | ------------------------ |
| API Calls  | Centralized `api` helper   | `src/utils/helpers.js`   |
| State Mgmt | Custom hooks               | `src/hooks/useCustom.js` |
| Services   | Layer architecture         | `src/services/api.js`    |
| Components | Reusable & composable      | `src/components/`        |
| Styling    | CSS variables + responsive | `src/styles/`            |
| Backend    | ViewSet + Serializer       | `backend/*/views.py`     |
| Admin      | Custom ModelAdmin          | `backend/*/admin.py`     |
| Models     | Proper relationships       | `backend/*/models.py`    |

---

**Status:** ✅ Ready to Build!

All examples are production-ready and follow industry best practices.
