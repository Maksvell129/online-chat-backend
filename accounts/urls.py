from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

from accounts.views import CustomTokenObtainPairView, RegisterView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterView.as_view(), name='register'),
]
