from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminDashboardView, EventManagementViewSet

router = DefaultRouter()
router.register(r'events', EventManagementViewSet, basename='event-management')

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('', include(router.urls)),
]
