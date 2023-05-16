from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from src.constant import MIN_PASSWORD_LENGTH

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    A custom serializer for obtaining authentication tokens.
    Inherits from TokenObtainPairSerializer, which provides a default implementation for obtaining tokens.
    """

    @classmethod
    def get_token(cls, user):
        """
        Adds custom claims to the authentication token.
        """
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for the User model.
    Validates and serializes User instances.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Validates that the email address is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use.')
        return value

    def validate_password(self, value):
        """
        Validates that the password meets the minimum length requirement.
        """
        if len(value) < MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(f'Password must be at least {MIN_PASSWORD_LENGTH} characters.')
        return value

    def create(self, validated_data):
        """
        Creates a new User instance.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
