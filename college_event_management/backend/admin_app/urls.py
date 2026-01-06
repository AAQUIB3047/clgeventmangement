from django.urls import path
from .views import AdminDashboardView, ManageUsersView, ManageEventsView

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('users/', ManageUsersView.as_view(), name='manage-users'),
    path('users/<int:pk>/', ManageUsersView.as_view(), name='manage-user-detail'),
    path('events/', ManageEventsView.as_view(), name='manage-events'),
    path('events/<int:pk>/', ManageEventsView.as_view(), name='manage-event-detail'),
]
