from django.urls import path

from .views import ApplicationView, ApplicationListView

urlpatterns = [
    path('', ApplicationListView.as_view()),
    path('<pk>/', ApplicationView.as_view()),
]
