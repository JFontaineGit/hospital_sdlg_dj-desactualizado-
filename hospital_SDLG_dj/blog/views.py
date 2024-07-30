from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import models

# Create your views here.
def home_blog(request):
    testimonios = models.Testimonios.objects.all()
    return render(request, 'index.html',{'title':'Blog - Hospital SDLG','testimonios':testimonios})

def atencion_al_paciente(request):
    return render(request, 'atencionalpaciente.html')

def contactos_blog(request):
    return render(request, 'contactos.html')