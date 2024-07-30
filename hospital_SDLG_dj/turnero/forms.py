# myapp/forms.py
from django import forms
from django.utils import timezone
from . import models

class TurnoForm(forms.ModelForm):
    fecha = forms.DateField(required=True)
    class Meta:
        model = models.Turnos
        fields = ['userID','citaID','fecha','estado']

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now():
            raise forms.ValidationError("La fecha del turno no puede ser en el pasado.")
        return fecha

class RegistroUsuarioForm(forms.ModelForm):
    dni = forms.CharField(max_length=100, required=True)
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    fecha_nacimiento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    contraseña = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = models.Usuarios
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'email', 'profile_picture', 'contraseña']
        
        widgets = {
            'profile_picture': forms.HiddenInput(),
        }