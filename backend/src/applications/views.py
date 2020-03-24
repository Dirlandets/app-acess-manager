from django.db.models import QuerySet
from django.shortcuts import redirect
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from api.permissions import TokenIsActivePermission

from .models import Application
from .serializers import ApplicationSerrializer


class ApplicationListView(ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerrializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Return only objects owned by user if not superuser'''
        user = self.request.user
        if not user.is_superuser:
            qs = self.queryset.filter(owner=user)
        else:
            qs = self.queryset
        return qs


class RefreshApplicationToken(APIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerrializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Return only objects owned by user if not superuser'''
        # TODO: Сделать permission для проверки.
        user = self.request.user
        if not user.is_superuser:
            qs = self.queryset.filter(owner=user)
        else:
            qs = self.queryset
        return qs

    def get(self, request, pk):
        try:
            for_refresh = self.get_queryset().get(pk=int(pk))
            for_refresh.refresh_key()
            response = redirect(f'/api/{for_refresh.pk}/')
        except Application.DoesNotExist:
            response = Response({'error': 'You can\'t do that'})
        return response


class TestTokenView(APIView):
    """
    View to test token is valid and worked fine.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerrializer
    permission_classes = [TokenIsActivePermission]

    def get(self, request, format=None):
        token = self.request.headers.get('Token', None)
        app = self.queryset.get(api_key=token)
        serializer = self.serializer_class(app)
        return Response(serializer.data)
