from django.contrib import admin
from .models import Medicos, Especialidades, Turnos, Usuarios, Horario_medicos, Citas,Departamentos,Ubicaciones

# Register your models here.

admin.site.register(Medicos)
admin.site.register(Departamentos)
admin.site.register(Especialidades)
admin.site.register(Ubicaciones)
admin.site.register(Horario_medicos)
admin.site.register(Usuarios)
admin.site.register(Citas)
admin.site.register(Turnos)