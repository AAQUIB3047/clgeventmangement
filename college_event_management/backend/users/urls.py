from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='user-profile'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('google-login/', UserViewSet.as_view({'post': 'google_login'}), name='google-login'),
    path('enrollments/', UserViewSet.as_view({'get': 'enrollments'}), name='enrollments'),
]
