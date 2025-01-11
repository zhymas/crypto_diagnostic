from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail

class UserRegisterSerializer(serializers.ModelSerializer):
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
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        token = self.generate_token(user.email)
        self.send_verification_email(user.email, token)
        return user
    
    def generate_token(self, email):
        signer = TimestampSigner()
        token = signer.sign(email)
        return token

    def send_verification_email(self, email, token):
        subject = 'Verify your email'
        message = f'Click <a href="http://localhost:8000/api/users/verify-email/?token={token}">here</a> to verify your email'
        from_email = 'noreply@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return "Email sent"

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