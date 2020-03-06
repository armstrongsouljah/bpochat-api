from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from .models import User
from utils.validation_helpers import (
    validate_password,
)

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    email = serializers.EmailField()
    username = serializers.CharField()

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def validate_password(self, password):
        return validate_password(password)

    def validate_email(self, email):
        """ This function validates the email input by a new user signing up
            It ensures that the email being used for signing up was not already used by another user.
        Args: 
            email(str): This is the email string received from user
        Returns: 
            Returns the validated email
        Raises: 
            ValidationError: 
            - "Email already exists." : for an already existing email
        """

        check_email = User.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def validate_username(self, username):

        check_username = User.objects.filter(username=username)
        if check_username.exists():
            raise serializers.ValidationError("Username already exists.")
        return username

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                "Email is required"
            )
        if password is None:
            raise serializers.ValidationError(
                "Password is required"
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'message': 'Account created successfully'
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def validate(self,data):
        
        email = data.get('email',None)

        if email is None:
            raise serializers.ValidationError("Email is required")
        
        return {
            'email': email
        }

class PasswordResetSerializer(serializers.Serializer):
     password = serializers.CharField(max_length=128, required=True)

     def validate(self,data):
        new_password = data.get('password',None)
        return {
            'password': validate_password(new_password)
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
