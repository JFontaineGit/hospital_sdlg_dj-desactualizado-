from django.contrib.auth.backends import BaseBackend
from .models import Usuarios

class DNIAuthBackend(BaseBackend):
    def authenticate(self, request, dni=None, password=None):
        try:
            usuario = Usuarios.objects.get(dni=dni)
            if usuario.check_password(password):
                return usuario
        except Usuarios.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
