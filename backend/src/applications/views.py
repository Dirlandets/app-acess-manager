from django.db.models import QuerySet
from django.views.decorators.http import require_http_methods
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from .models import Application
from .serializers import ApplicationSerrializer


class ApplicationListView(ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerrializer

    def get_queryset(self) -> 'QuerySet[Application]':
        user = self.request.user
        if not user.is_superuser:
            self.queryset = self.queryset.filter(owner=user)
        return self.queryset.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_superuser:
            serializer.save(owner=user)
        else:
            serializer.save()


class ApplicationView(RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerrializer

    def get_queryset(self):
        '''Return only objects owned by user if not superuser'''
        user = self.request.user
        if not user.is_superuser:
            qs = self.queryset.filter(owner=user)
        else:
            qs = self.queryset
        return qs
