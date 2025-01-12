from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from .tasks import send_verification_email
User = get_user_model()

class UserRegisterMixin:

    def create_user(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        token = self.generate_token(user.email)
        send_verification_email.delay(user.email, token, user.username)
        return user
    
    def generate_token(self, email):
        signer = TimestampSigner()
        token = signer.sign(email)
        return token

class VerifyEmailMixin:

    def verify_email(self, email):
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return user