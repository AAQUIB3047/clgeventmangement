# 📚 Frontend Examples & Best Practices

## Overview

This document provides examples and best practices for building React components in the College Event Management system using React + Vite.

---

## 🎯 Component Structure

### Folder Organization

```
frontend/src/
├── components/       # Reusable components
│   ├── EventCard.jsx
│   ├── Navbar.jsx
│   └── ...
├── pages/           # Page components
│   ├── Events.jsx
│   ├── Login.jsx
│   └── ...
├── hooks/           # Custom hooks
│   └── useCustom.js
├── services/        # API services
│   └── api.js
├── utils/           # Utility functions
│   └── helpers.js
├── styles/          # CSS files
│   ├── eventcard.css
│   ├── navbar.css
│   └── ...
└── App.jsx          # Main app component
```

---

## 📦 Example Components

### 1. EventCard Component

**Location:** `src/components/EventCard.jsx`

```jsx
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/eventcard.css';

/**
 * EventCard Component - Displays a single event
 * Props: event (object with id, title, date, location, etc)
 */
const EventCard = ({ event }) => {
  const registrationPercentage = (event.registered / event.capacity) * 100;
  const isFull = event.registered >= event.capacity;

  return <div className="event-card">{/* Card content */}</div>;
};

export default EventCard;
```

**Usage:**

```jsx
<EventCard event={eventData} />
```

### 2. Navbar Component

**Location:** `src/components/Navbar.jsx`

Provides main navigation with user authentication.

**Features:**

- Dynamic links based on auth status
- Mobile responsive hamburger menu
- User profile dropdown
- Logout functionality

---

## 🪝 Custom Hooks

### useApi Hook

**Location:** `src/hooks/useCustom.js`

```jsx
import { useApi } from '../hooks/useCustom';

function EventsPage() {
  const { data, loading, error, refetch } = useApi('/api/events/');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {data.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

### useForm Hook

```jsx
import { useForm } from '../hooks/useCustom';

function LoginForm() {
  const { values, errors, handleChange, handleSubmit, isSubmitting } = useForm(
    { email: '', password: '' },
    async (values) => {
      await authService.login(values.email, values.password);
    }
  );

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" value={values.email} onChange={handleChange} />
      {errors.email && <span>{errors.email}</span>}
      <button disabled={isSubmitting}>{isSubmitting ? 'Logging in...' : 'Login'}</button>
    </form>
  );
}
```

### useLocalStorage Hook

```jsx
import { useLocalStorage } from '../hooks/useCustom';

function UserPreferences() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current theme: {theme}
    </button>
  );
}
```

### usePagination Hook

```jsx
import { usePagination } from '../hooks/useCustom';

function EventsList({ events }) {
  const { currentPage, totalPages, currentItems, nextPage, prevPage } = usePagination(events, 10);

  return (
    <>
      {currentItems.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
      <div>
        Page {currentPage} of {totalPages}
        <button onClick={prevPage}>Prev</button>
        <button onClick={nextPage}>Next</button>
      </div>
    </>
  );
}
```

---

## 🛠️ Utility Functions

### API Helpers

**Location:** `src/utils/helpers.js`

```jsx
import { api } from '../utils/helpers';

// GET request
const events = await api.get('/api/events/');

// POST request
const newEvent = await api.post('/api/events/', {
  title: 'New Event',
  date: '2025-01-15',
});

// PUT request
const updated = await api.put('/api/events/1/', { title: 'Updated' });

// DELETE request
await api.delete('/api/events/1/');
```

### Validators

```jsx
import { validators } from '../utils/helpers';

// Email validation
if (!validators.isEmail(email)) {
  console.log('Invalid email');
}

// Password strength
if (!validators.isStrongPassword(password)) {
  console.log('Password too weak');
}

// Phone number
if (!validators.isPhoneNumber(phone)) {
  console.log('Invalid phone');
}

// Required field
if (!validators.isRequired(name)) {
  console.log('Name is required');
}

// Length validation
if (!validators.minLength(password, 8)) {
  console.log('Password must be at least 8 characters');
}
```

### Formatters

```jsx
import { formatters } from '../utils/helpers';

// Format date
formatters.formatDate('2025-01-15'); // "January 15, 2025"

// Format date and time
formatters.formatDateTime('2025-01-15T14:30:00'); // "Jan 15, 2025, 02:30 PM"

// Format currency
formatters.formatCurrency(1000); // "$1,000.00"

// Truncate text
formatters.truncate('Long text...', 20); // "Long text..."
```

---

## 📡 Services

### Location: `src/services/api.js`

**Events Service:**

```jsx
import { eventsService } from '../services/api';

// Get all events
const events = await eventsService.getAll({ status: 'upcoming' });

// Get single event
const event = await eventsService.getById(1);

// Create event (admin)
await eventsService.create({ title: '...', date: '...' });

// Update event
await eventsService.update(1, { title: 'Updated' });

// Delete event
await eventsService.delete(1);
```

**Users Service:**

```jsx
import { usersService } from '../services/api';

// Get profile
const profile = await usersService.getProfile();

// Update profile
await usersService.updateProfile({ name: 'New Name' });

// Google login
const { access_token, user } = await usersService.googleLogin(token, 'CSE');

// Get enrollments (admin)
const enrollments = await usersService.getEnrollments();
```

**Registrations Service:**

```jsx
import { registrationsService } from '../services/api';

// Get my registrations
const myRegs = await registrationsService.getMyRegistrations();

// Register for event
await registrationsService.register(eventId, { branch: 'CSE' });

// Cancel registration
await registrationsService.cancel(registrationId);
```

---

## 🎨 Styling

### CSS Variables

```css
/* Light theme */
--primary-color: #3b82f6;
--secondary-color: #8b5cf6;
--success-color: #10b981;
--danger-color: #ef4444;
--warning-color: #f59e0b;

--bg-primary: #ffffff;
--bg-secondary: #f3f4f6;
--border-color: #e5e7eb;

--text-primary: #000000;
--text-secondary: #666666;
```

### Responsive Design

```css
/* Mobile first approach */
.component {
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .component {
    padding: 24px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .component {
    padding: 32px;
  }
}
```

---

## 📋 Example Pages

### Events Page

**Location:** `src/pages/Events.jsx`

Features:

- ✅ Event listing with filters
- ✅ Search functionality
- ✅ Status filtering (upcoming, ongoing, completed)
- ✅ Pagination
- ✅ Statistics cards
- ✅ Responsive grid layout

**Usage:**

```jsx
<Route path="/events" element={<Events />} />
```

---

## 🔐 Authentication Flow

```jsx
// 1. Google Login (in Login.jsx)
const response = await usersService.googleLogin(credential, branch);
localStorage.setItem('access_token', response.access_token);
localStorage.setItem('user', JSON.stringify(response.user));

// 2. Protected Routes
<Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />;

// 3. API Calls with Token
// Automatically added by api helper
headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;

// 4. Logout
const handleLogout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  navigate('/login');
};
```

---

## 🚀 Best Practices

### 1. Component Composition

```jsx
// ✅ Good - Reusable components
const EventList = ({ events }) => (
  <div className="event-list">
    {events.map((event) => (
      <EventCard key={event.id} event={event} />
    ))}
  </div>
);

// ❌ Bad - Inline content
const EventList = ({ events }) => (
  <div>
    {events.map((event) => (
      <div key={event.id} className="card">
        {/* Long JSX */}
      </div>
    ))}
  </div>
);
```

### 2. Error Handling

```jsx
// ✅ Good
try {
  const data = await api.get('/endpoint');
  setData(data);
} catch (error) {
  setError(error.message);
  notify.error('Failed to load data');
}

// ❌ Bad
const data = await api.get('/endpoint');
setData(data);
```

### 3. Loading States

```jsx
// ✅ Good
if (loading) return <Spinner />;
if (error) return <ErrorMessage error={error} />;
return <Content data={data} />;

// ❌ Bad
return <Content data={data} />; // No loading/error handling
```

### 4. Memoization

```jsx
// ✅ Good - Prevent unnecessary re-renders
const EventCard = React.memo(({ event }) => <div className="event-card">{/* ... */}</div>);

// ✅ Good - Memoized callbacks
const handleClick = useCallback(() => {
  // handler logic
}, [dependencies]);
```

### 5. Naming Conventions

```jsx
// ✅ Good
- Components: PascalCase (EventCard, UserProfile)
- Functions: camelCase (fetchEvents, handleChange)
- Constants: UPPER_SNAKE_CASE (MAX_ITEMS, API_BASE_URL)
- CSS classes: kebab-case (event-card, user-profile)
```

---

## 📖 References

- **React Docs:** https://react.dev
- **Vite Docs:** https://vitejs.dev
- **React Router:** https://reactrouter.com
- **CSS Best Practices:** https://developer.mozilla.org/en-US/docs/Web/CSS

---

## ✅ Quick Checklist

- [ ] Component properly documented with JSDoc comments
- [ ] Props validation/TypeScript types added
- [ ] Error handling implemented
- [ ] Loading states included
- [ ] Responsive design tested
- [ ] Accessibility considerations (alt text, labels, etc)
- [ ] Performance optimized (memoization, lazy loading)
- [ ] No console errors/warnings
- [ ] Unit tests written (if required)
