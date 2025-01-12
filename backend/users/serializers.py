from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from .mixins import UserRegisterMixin

class UserRegisterSerializer(UserRegisterMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value
    
    def create(self, validated_data):
        return self.create_user(validated_data)

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        signer = TimestampSigner()
        try:
            email = signer.unsign(value)
        except SignatureExpired:
            raise serializers.ValidationError("Token expired")
        except BadSignature:
            raise serializers.ValidationError("Invalid token")
        return email

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        refresh_token = token
        access_token = token.access_token
        return {'access_token': str(access_token), 'refresh_token': str(refresh_token)}

class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if self.is_email(username):
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials") 

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials") 
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        attrs['user'] = user
        return attrs

    @staticmethod
    def is_email(value):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, value))