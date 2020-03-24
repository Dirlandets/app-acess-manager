from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('shema/', get_schema_view()),
    path('', include('applications.urls')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/get_token/', TokenObtainPairView.as_view()),
    path('auth/refresh_token/', TokenRefreshView.as_view()),
]
