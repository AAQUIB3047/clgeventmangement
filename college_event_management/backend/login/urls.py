from django.urls import path
from .views import LoginView, LogoutView, GoogleLoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
]
