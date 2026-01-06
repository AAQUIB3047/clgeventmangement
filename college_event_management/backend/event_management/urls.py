"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint - returns API status"""
    return JsonResponse({
        "status": "ok",
        "message": "EventHub API is running",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth/",
            "users": "/api/users/",
            "events": "/api/events/",
            "registrations": "/api/registrations/",
            "attendance": "/api/attendance/",
            "reports": "/api/reports/",
            "dashboard": "/api/dashboard/",
            "admin": "/api/admin/",
            "admin_panel": "/admin/"
        }
    })

urlpatterns = [
    path('', api_root),  # Root endpoint
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('login.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/admin/', include('admin_app.urls')),
    path('api/users/', include('users.urls')),
    path('api/events/', include('events.urls')),
    path('api/registrations/', include('registrations.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/reports/', include('reports.urls')),
]
