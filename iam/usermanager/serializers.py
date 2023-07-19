from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group # import django.contrib.auth.models as models
from .models import *
from django.contrib.auth import models
from django.db.models import fields
from rest_framework.exceptions import ValidationError
from .models import User
from django.db.models import Q


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation']

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.EmailField()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )
        


class CreateOAuthUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class OAutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = '__all__'



User = get_user_model()

class UserLoginSerializer(serializers.ModelSerializer):
    login_identifier = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'login_identifier',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        login_identifier = data.get('login_identifier')
        password = data.get('password')

        user = User.objects.filter(
            Q(username=login_identifier) | Q(email=login_identifier) | Q(primary_phone=login_identifier)
        ).first()

        if user is None:
            raise serializers.ValidationError('Invalid login credentials.')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')

        data['user'] = user
        return data

