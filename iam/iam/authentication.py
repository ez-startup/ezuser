from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the username is an email or phone number
        if isinstance(username, str) and '@' in username:
            kwargs['email'] = username
        elif isinstance(username, str) and username.isdigit():
            kwargs['primary_phone'] = username
        else:
            kwargs['username'] = username
        
        try:
            user = User.objects.get(**kwargs)
            if password is not None and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
