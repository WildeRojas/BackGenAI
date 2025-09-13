from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .viewsets.user_register_viewset import (
    UserRegisterViewSet
)
from .viewsets.user_profile_viewset import (
    UserProfileViewSet,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path('registrar/', UserRegisterViewSet.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('profile/', UserProfileViewSet.as_view(), name='user-profile'),
]
