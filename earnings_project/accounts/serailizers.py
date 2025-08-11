from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
