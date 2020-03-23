from django.urls import path

from .views import ApplicationsView

urlpatterns = [
    path('', ApplicationsView.as_view()),
]
