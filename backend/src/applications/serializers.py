from rest_framework import serializers
from .models import Application


class ApplicationSerrializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['api_key']
