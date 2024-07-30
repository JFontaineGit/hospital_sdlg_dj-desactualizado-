from django.shortcuts import render, redirect
from turnero import models as turn_models
from blog import models as blog_models
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import forms


@login_required
def user_panel(request):
    """
    Vista para renderizar el panel de usuario.
    """
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save() 
            return redirect('panel')
    else:
        form = forms.UserProfileForm(instance=request.user)  

    return render(request, 'panel.html', {'form': form, 'MEDIA_URL': settings.MEDIA_URL,})

@login_required
def turnos_list(request):
    if request.method == 'POST':
        turno = request.POST.get('turno')
        print(turno)
        try:
            paciente = turn_models.Usuarios.objects.get(userID=request.user.userID)
            turno = turn_models.Turnos.objects.get(turnoID=turno)
            try:
                turn_models.Turnos.eliminar_registros_antiguos()
                turno.delete()
                return redirect('lista_de_turnos')
            except Exception as err:
                print(err)
                turnos = []
                error_text = "Usted no tiene turnos"
                return render(request, 'turnos.html', {'turnos': turnos, 'error': error_text})
        except Exception as err:
            print(err)
            return redirect('home_blog')
    else:
        """
        Vista para listar los turnos del usuario.
        Si el usuario está autenticado, busca el paciente asociado a ese usuario y luego busca los turnos asociados a ese paciente.
        Si encuentra turnos, los muestra en una plantilla 'turnos.html'. Si no hay turnos, muestra un mensaje de error.
        Si el usuario no está autenticado o si ocurre algún error, redirige a la página de inicio ('home_blog').
        """
        try:
            try:
                paciente = turn_models.Usuarios.objects.get(userID=request.user.userID)
                turn_models.Turnos.eliminar_registros_antiguos()
                turnos = turn_models.Turnos.objects.filter(userID=paciente)
                return render(request, 'turnos.html', {'turnos': turnos})
            except Exception as err:
                print(err)
                error_text = "Usted no tiene turnos"
                return render(request, 'turnos.html', {'turnos': turnos, 'error': error_text})
        except Exception as err:
            print(err)
            return redirect('home_blog')

@login_required
def form_testimonios(request):
    try:
        user = turn_models.Usuarios.objects.get(userID=request.user.userID)
        testimonio_existente = blog_models.Testimonios.objects.filter(usuario=user).exists()
    except Exception as err:
        print(err)
        return redirect('panel')
    if testimonio_existente:
        # Si el usuario ya tiene un testimonio, permitir editar
        if request.method == 'POST':
            contenido = request.POST.get('contenido')
            # Actualizar el testimonio existente
            testimonio = blog_models.Testimonios.objects.get(usuario=user)
            testimonio.contenido = contenido
            testimonio.save()
            return redirect('panel')
        else:
            # Renderizar la vista de edición con el contenido del testimonio existente
            testimonio = blog_models.Testimonios.objects.get(usuario=user)
            return render(request, 'testimonio.html', {'testimonio': testimonio})
    else:
        # Si el usuario no tiene un testimonio, permitir crear uno nuevo
        if request.method == 'POST':
            contenido = request.POST.get('contenido')
            # Crear un nuevo testimonio
            blog_models.Testimonios.objects.create(contenido=contenido, usuario=user)
            return redirect('panel')
        else:
            # Renderizar la vista de creación
            return render(request, 'testimonio.html')
        
@login_required
def editar_perfil(request):
    """
    Vista para renderizar la plantilla para editar los datos del usuario
    """
    return render(request, 'edit_profile.html')