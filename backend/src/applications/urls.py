from django.urls import path

from .views import (
    ApplicationView,
    ApplicationListView,
    TestTokenView,
    RefreshApplicationToken
)

urlpatterns = [
    path('test/', TestTokenView.as_view()),
    path('', ApplicationListView.as_view()),
    path('<pk>/', ApplicationView.as_view()),
    path('<pk>/refresh/', RefreshApplicationToken.as_view()),
]
