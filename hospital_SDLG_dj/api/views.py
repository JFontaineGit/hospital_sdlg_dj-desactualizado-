from rest_framework import viewsets
from .serializer import *
from turnero.models import * 
from django.http import JsonResponse
from django.db.models import Count
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
import base64


class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer
    
class UbicationViewSet(viewsets.ModelViewSet):
    queryset = Ubicaciones.objects.all()
    serializer_class = UbicationSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    serializer_class = DepartmentSerializer

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Especialidades.objects.all()
    serializer_class = SpecialtySerializer

class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = Medicos.objects.all()
    serializer_class = DoctorsSerializer

class SchedulesViewSet(viewsets.ModelViewSet):
    queryset = Horario_medicos.objects.all()
    serializer_class = SchedulesSerializer

class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = AppointmentsSerializer

class ShiftsViewSet(viewsets.ModelViewSet):
    queryset = Turnos.objects.all()
    serializer_class = ShiftsSerializer

def especialidades_mas_frecuentes(request):
    # Obteniendo la cantidad de especialidades que más se repiten en base a los Médicos
    especialidades = Medicos.objects.values('especialidadID__nombre').annotate(total=Count('especialidadID')).order_by('-total')

    # Preparar los datos para el gráfico
    especialidad_nombres = [especialidad['especialidadID__nombre'] for especialidad in especialidades]
    especialidad_totales = [especialidad['total'] for especialidad in especialidades]

    # Creando un gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(especialidad_nombres, especialidad_totales, color='blue')
    plt.xlabel('Especialidad')
    plt.ylabel('Número de Médicos')
    plt.title('Especialidades Más Frecuentes entre los Médicos')
    plt.xticks(rotation=45, ha='right')

    # Guardar el gráfico en un objeto en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Retornar la imagen como respuesta HTTP
    html = f'<html><head><meta charset="UTF-8>"</head><body><h1>Especialidades Más Frecuentes entre los Médicos</h1><img src="data:image/png;base64,{image_base64}" /></body></html>'
    return HttpResponse(html, content_type='text/html')