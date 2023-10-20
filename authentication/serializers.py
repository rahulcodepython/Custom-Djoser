from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings
import random

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_staff", "is_active", "is_superuser", "password")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.AUTH_CONFIG['LOGIN_FIELD'],
            'password'
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.username = validated_data['email'].split(
            '@')[0] + str(random.randint(1000, 9999))

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_staff", "is_active", "is_superuser",
                   "password", settings.AUTH_CONFIG['LOGIN_FIELD'], "id")

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
