from rest_framework import serializers
from .models import User
from datetime import datetime

class UserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)

class TimeSerializer(serializers.Serializer):
    now = serializers.DateTimeField()

class StatsSerializer(serializers.Serializer):
    user = serializers.CharField()
    open_count = serializers.IntegerField()