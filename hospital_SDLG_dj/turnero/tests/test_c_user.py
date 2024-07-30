from django.test import TestCase
from django.contrib.auth import get_user_model

class UserCreationTestCase(TestCase):
    #Obtenemos el modelo (UsuarioManager)
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        # Crear un usuario
        self.User.objects.create_user(dni=00000000, nombre='testname', apellido='testlastname', fecha_nacimiento="0000-0-1", email="test@example.com", contraseña='password')
        
        # Verificar que el usuario se ha creado correctamente
        user_count = self.User.objects.count()
        self.assertEqual(user_count, 1)

    def test_create_superuser(self):
        # Crear un superusuario (admin)
        self.User.objects.create_superuser(dni=11111111, nombre='admin', apellido='adminlastname', fecha_nacimiento="0000-0-1", email="admin@example.com", contraseña='password')
        
        # Verificar que el superusuario se ha creado correctamente
        superuser_count = self.User.objects.filter(is_superuser=True).count()
        self.assertEqual(superuser_count, 1)