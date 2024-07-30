from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import time, timedelta
import os 

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, fecha_nacimiento, email, profile_picture, contraseña=None):
        if not dni:
            raise ValueError('El DNI es obligatorio')

        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            email=self.normalize_email(email),
        )

        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellido, fecha_nacimiento, email, contraseña):
        user = self.create_user(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            email=email,
            contraseña=contraseña,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.    
class Ubicaciones(models.Model):
    ubicacionID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

class Departamentos(models.Model):
    departamentoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    ubicacionID = models.ForeignKey(Ubicaciones,on_delete=models.CASCADE)

class Especialidades(models.Model):
    especialidadID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=255)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE,null=True,blank=True)


class Medicos(models.Model):
    medicoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.dni} {self.especialidadID.nombre}"

class Horario_medicos(models.Model):
    horarioID = models.AutoField(primary_key=True)
    medicoID = models.ForeignKey(Medicos,on_delete=models.CASCADE)
    dia = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.medicoID} {self.hora_inicio} {self.hora_fin}"

class Usuarios(AbstractBaseUser):
    userID = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(blank=True,null=True,unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default='profile_pictures/default.png', null=True, blank=True)
    telefono = models.CharField(blank=True,null=True)
    contraseña = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'fecha_nacimiento', 'email']

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.fecha_nacimiento}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Citas(models.Model):
    citaID = models.AutoField(primary_key=True)
    medicoID = models.ForeignKey(Medicos, on_delete=models.CASCADE)
    horarioID = models.ForeignKey(Horario_medicos, on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE,null=True,blank=True)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.medicoID.nombre} {self.horarioID.hora_inicio} {self.horarioID.hora_fin} {self.departamentoID.nombre} {self.motivo} {self.estado}"
    
class Turnos(models.Model):
    turnoID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    citaID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    estado = models.CharField(max_length=25)
    fecha_created = models.DateTimeField(auto_now=True)
    fecha = models.DateField()

    @classmethod
    def eliminar_registros_antiguos(cls, dias=0):
        """
        Método de clase para eliminar registros creados en la fecha y hora actual o en los últimos días especificados.
        :param dias: Número de días antes de la fecha y hora actual para incluir en la eliminación.
        """
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual - timedelta(days=dias)
        registros_actuales = cls.objects.filter(fecha_created__date=fecha_actual.date(), fecha_created__time=fecha_actual.time())
        if dias > 0:
            registros_actuales = registros_actuales.filter(fecha_created__gte=fecha_limite)
        registros_actuales.delete()
    
    def __str__(self):
        return f"Turno de {self.pacienteID} el día {self.fecha}"