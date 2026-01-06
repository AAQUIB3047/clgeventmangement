# 🎨 React + Django Patterns & Code Examples

Professional patterns for building modern web applications with React + Vite and Django REST.

---

## 📦 React Patterns

### 1. Component with Hooks

**Pattern:**

```jsx
import React, { useState, useEffect, useCallback } from "react";
import "./ComponentName.css";

/**
 * ComponentName - Description
 * @param {object} props - Component props
 * @param {string} props.title - Component title
 * @returns {React.ReactElement} Rendered component
 */
const ComponentName = ({ title, onAction }) => {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch("/api/endpoint");
        const data = await response.json();
        setState(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Memoized callback
  const handleClick = useCallback(() => {
    onAction(state);
  }, [state, onAction]);

  // Render states
  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="component">
      <h2>{title}</h2>
      <button onClick={handleClick}>Action</button>
    </div>
  );
};

export default ComponentName;
```

### 2. Form Handling

**Pattern:**

```jsx
import { useForm } from "../hooks/useCustom";

const FormComponent = ({ onSubmit }) => {
  const { values, errors, handleChange, handleSubmit, isSubmitting } = useForm(
    { email: "", password: "" },
    async (values) => {
      // Validation
      if (!values.email) throw new Error("Email required");
      if (!values.password) throw new Error("Password required");

      // Submit
      await onSubmit(values);
    }
  );

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={values.email}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          name="password"
          value={values.password}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
};

export default FormComponent;
```

### 3. List with Filters

**Pattern:**

```jsx
import { useState, useEffect } from "react";
import { api } from "../utils/helpers";

const ListComponent = () => {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  // Fetch items when filter changes
  useEffect(() => {
    const fetchItems = async () => {
      const params = new URLSearchParams({
        filter,
        search,
      });
      const data = await api.get(`/api/items/?${params}`);
      setItems(data);
    };

    fetchItems();
  }, [filter, search]);

  // Filter locally (if needed)
  const filtered = items.filter((item) =>
    item.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="filters">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      <div className="items-list">
        {filtered.map((item) => (
          <div key={item.id} className="item">
            <h3>{item.name}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ListComponent;
```

### 4. Modal Component

**Pattern:**

```jsx
import React, { useEffect } from "react";
import "./Modal.css";

const Modal = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    // Handle escape key
    const handleEscape = (e) => {
      if (e.key === "Escape") onClose();
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
```

### 5. Protected Route

**Pattern:**

```jsx
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ isAuthenticated, user, requiredRole, children }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/" />;
  }

  return children;
};

// Usage
<Routes>
  <Route
    path="/admin"
    element={
      <ProtectedRoute isAuthenticated={isAuth} user={user} requiredRole="admin">
        <AdminDashboard />
      </ProtectedRoute>
    }
  />
</Routes>;
```

---

## 🐍 Django Patterns

### 1. ViewSet with Custom Actions

**Pattern:**

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD and custom actions for Items

    Actions:
        GET    /items/             - List all items
        POST   /items/             - Create item
        GET    /items/{id}/        - Get item detail
        PUT    /items/{id}/        - Update item
        DELETE /items/{id}/        - Delete item
        GET    /items/bulk-action/ - Custom action
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Override permissions for specific actions"""
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter queryset based on user"""
        user = self.request.user
        if user.is_staff:
            return Item.objects.all()
        return Item.objects.filter(owner=user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently created items"""
        items = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate an item"""
        item = self.get_object()
        item.is_active = True
        item.save()
        return Response({'status': 'Item activated'})

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def bulk_action(self, request):
        """Perform bulk action"""
        action_type = request.data.get('action')
        ids = request.data.get('ids', [])

        items = self.get_queryset().filter(id__in=ids)

        if action_type == 'activate':
            items.update(is_active=True)
        elif action_type == 'deactivate':
            items.update(is_active=False)

        return Response({'count': items.count()})
```

### 2. Serializer with Validation

**Pattern:**

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    """
    Serialize Item model with validation
    """

    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'owner', 'owner_name',
                  'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Validate title field"""
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        return value

    def validate(self, data):
        """Cross-field validation"""
        if data.get('title') == data.get('description'):
            raise serializers.ValidationError(
                "Title and description cannot be the same"
            )
        return data

    def create(self, validated_data):
        """Set owner to current user on create"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
```

### 3. Model with Methods

**Pattern:**

```python
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    """Item model with useful methods"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get URL for item detail page"""
        return f'/items/{self.id}/'

    @property
    def is_recent(self):
        """Check if item was created recently (within 7 days)"""
        from datetime import timedelta
        from django.utils import timezone
        return self.created_at > timezone.now() - timedelta(days=7)

    def activate(self):
        """Activate item"""
        self.is_active = True
        self.save()

    def deactivate(self):
        """Deactivate item"""
        self.is_active = False
        self.save()
```

### 4. Custom Permission

**Pattern:**

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Allow access only to object owner"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    """Allow write access only to admin"""

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class IsBranchCoordinator(BasePermission):
    """Allow access only to branch coordinators"""

    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                request.user.role == 'coordinator')
```

### 5. Filter Backend

**Pattern:**

```python
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    # Usage:
    # GET /items/?search=python
    # GET /items/?ordering=-created_at
    # GET /items/?search=python&ordering=title
```

---

## 🔀 Integration Patterns

### Frontend Consuming Backend API

**Pattern:**

```jsx
// Frontend: src/services/api.js
export const itemsService = {
  async getAll(filters = {}) {
    const params = new URLSearchParams(filters);
    return api.get(`/api/items/?${params}`);
  },

  async getById(id) {
    return api.get(`/api/items/${id}/`);
  },

  async create(data) {
    return api.post("/api/items/", data);
  },

  async update(id, data) {
    return api.put(`/api/items/${id}/`, data);
  },

  async delete(id) {
    return api.delete(`/api/items/${id}/`);
  },

  async bulkAction(action, ids) {
    return api.post("/api/items/bulk-action/", { action, ids });
  },
};
```

**Backend Response:**

```python
# Backend: Return consistent response format
{
  "count": 100,
  "next": "http://api.example.com/items/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Item 1",
      "description": "Description",
      "owner_name": "John Doe",
      "is_active": true,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

---

## 🎯 Complete Example: Event Management

### Backend Model

```python
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

### Backend Serializer

```python
class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.get_full_name')
    registered_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location',
                  'capacity', 'organizer', 'organizer_name',
                  'registered_count', 'created_at']

    def get_registered_count(self, obj):
        return obj.registrations.count()
```

### Backend ViewSet

```python
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

### Frontend Component

```jsx
import { useApi } from "../hooks/useCustom";
import { eventsService } from "../services/api";
import EventCard from "../components/EventCard";

function EventsList() {
  const { data: events, loading, error, refetch } = useApi("/api/events/");
  const [filter, setFilter] = useState("");

  const filtered =
    events?.filter((e) =>
      e.title.toLowerCase().includes(filter.toLowerCase())
    ) || [];

  return (
    <div>
      <input
        type="text"
        placeholder="Search events..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />

      {loading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}

      <div className="events-grid">
        {filtered.map((event) => (
          <EventCard key={event.id} event={event} />
        ))}
      </div>

      <button onClick={refetch}>Refresh</button>
    </div>
  );
}

export default EventsList;
```

---

## ✅ Summary

| Pattern       | Frontend           | Backend               |
| ------------- | ------------------ | --------------------- |
| **API Calls** | `api` helper       | Consistent responses  |
| **Forms**     | `useForm` hook     | Serializer validation |
| **Lists**     | Filtering & search | Filter backends       |
| **Auth**      | Protected routes   | Permission classes    |
| **State**     | Custom hooks       | Model methods         |
| **Errors**    | Error boundaries   | Exception handlers    |
| **Loading**   | Loading states     | Long operations       |

All patterns follow industry standards and are production-ready!
