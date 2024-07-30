from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.staticfiles import finders
from io import BytesIO
from django.templatetags.static import static
from django.conf import settings
from . import models, forms


def generar_comprobante(request, turno_id):
    turno = get_object_or_404(models.Turnos, turnoID=turno_id)
    cita = turno.citaID
    medico = cita.medicoID
    horario = cita.horarioID
    departamento = cita.departamentoID
    usuario = turno.userID

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Encontrar la ruta a los logos
    logo_path = finders.find('IMG/logo.png')
    
    p.drawImage(logo_path, 40, 700, width=80, height=80)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Comprobante de Turno")
    
    p.setFont("Helvetica", 12)
    p.drawString(40, 680, f"Código del Turno: YY-{turno.turnoID}")
    p.drawString(40, 660, f"Paciente: {usuario.nombre} {usuario.apellido}")
    p.drawString(40, 640, f"Médico: {medico.nombre} {medico.apellido}")
    p.drawString(40, 620, f"Horario: {horario.hora_inicio}")
    p.drawString(40, 600, f"Departamento: {departamento.nombre}")
    p.drawString(40, 580, f"Fecha: {turno.fecha}")
    p.drawString(40, 560, f"Motivo: {cita.motivo}")
    p.drawString(40, 540, f"Estado: {turno.estado}")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comprobante_turno_{turno_id}.pdf"'
    return response

@login_required
def form_turnero(request):
    """
    Esta vista maneja la presentación del formulario de turno y el procesamiento de los datos del formulario enviado por el usuario.
    Si la solicitud es un método POST, recopila los datos del formulario, crea un nuevo turno y lo guarda en la base de datos.
    Si el usuario no existe en la base de datos, muestra un mensaje de error.
    Devuelve una redirección a la página de inicio ('home_blog') después de crear el turno con éxito.
    """
    if request.method == 'POST':
        dni_user = request.user.dni
        id_user = request.user.userID
        especialidad = request.POST.get('especialidad')
        medico = request.POST.get('medico')
        motivo = request.POST.get('motivo')
        fecha = request.POST.get('fecha')
        horario_turno = request.POST.get('horario')
        estado = "Pendiente"

        try:
            especialidad = models.Especialidades.objects.get(especialidadID=especialidad)
            medico = models.Medicos.objects.filter(especialidadID = especialidad.especialidadID).first()     
            departamento = especialidad.departamentoID
            paciente = models.Usuarios.objects.get(dni=dni_user)
            horario = models.Horario_medicos.objects.get(horarioID=horario_turno)
        except models.Usuarios.DoesNotExist:
            messages.error(request, 'Usuario no encontrado. Por favor, registre el usuario primero.')
            medicos = models.Medicos.objects.all()
            return render(request, 'formulario.html', {'medicos': medicos, 'error':'No se encontro usuario existente con esta descripcion\n le recomiendo que se registre'})

        cita = models.Citas.objects.create(
            medicoID=medico,
            horarioID=horario,
            departamentoID=departamento,
            motivo=motivo,
            estado=estado,
        )
        
        turno = models.Turnos.objects.create(
            userID = paciente,
            citaID = cita,
            fecha = fecha,
            estado = cita.estado,
            
            
        )
        messages.success(request, 'Turno creado exitosamente.')
        return redirect('home_blog')

    else:
        especialidades = models.Especialidades.objects.all()
        horarios = models.Horario_medicos.objects.all()
        return render(request, 'formulario.html', {'especialidades': especialidades,'horarios':horarios})
        
# Vista para manejar el inicio de sesión del usuario.
def loguin_turnero(request):
    """
    Esta vista maneja el inicio de sesión del usuario.
    Si la solicitud es un método POST, intenta autenticar al usuario utilizando el DNI y la contraseña proporcionados.
    Si la autenticación es exitosa, inicia sesión en el sistema y redirige al usuario a la página de inicio ('home_blog').
    Si la autenticación falla, muestra un mensaje de error.
    Si la solicitud no es un método POST, simplemente muestra el formulario de inicio de sesión.
    """
    if request.method == 'POST':
        dni = request.POST.get('dni')
        password = request.POST.get('password')

        # Autenticar al usuario utilizando el DNI
        user = authenticate(request, dni=dni, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_blog') 
        else:
            return render(request, 'Login.html', {'error': 'Invalid credentials'})
    return render(request, 'Login.html')

# Vista para manejar el registro de un nuevo usuario.
def signup_turnero(request):
    """
    Esta vista maneja el proceso de registro de un nuevo usuario.
    Si la solicitud es un método POST y el formulario es válido, crea un nuevo usuario en la base de datos con la contraseña cifrada
    y lo redirige al formulario de turno.
    Si la solicitud no es un método POST, simplemente muestra el formulario de registro.
    """
    if request.method == 'POST':
        form = forms.RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['contraseña'])
            usuario.save()
            return redirect('form_turnero')
    else:
        form = forms.RegistroUsuarioForm() 
    return render(request, 'SignUp.html')

# Vista para manejar el cierre de sesión del usuario.
def loguot_turnero(request):
    """
    Esta vista maneja el cierre de sesión del usuario.
    Simplemente cierra la sesión del usuario y redirige a la página de inicio ('home_blog').
    """
    logout(request)
    return redirect('home_blog')
