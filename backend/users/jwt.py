from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone

class CustomRefreshToken(RefreshToken):
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        
        self.payload['custom_field'] = 'test_field'
        self.payload['user_id'] = user.id
        self.payload['email'] = user.email
        self.payload['exp'] = timezone.now() + timedelta(days=1)

    def get_payload(self):
        return self.payload