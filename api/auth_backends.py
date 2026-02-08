from django.contrib.auth.models import User
from django.db.models import Q

class EmailBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # On cherche l'utilisateur par son email (dans le champ username du formulaire)
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
