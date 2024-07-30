from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Medicos, Especialidades, Departamentos, Citas, Turnos, Horario_medicos, Ubicaciones
from datetime import time, datetime
from test_c_user import UserCreationTestCase

class TestsCases(TestCase):
    def setUp(self):
        #Crear usuario (para Turnos)
        user = UserCreationTestCase.test_create_user()
        
        # Crear ubicaciones
        self.location = Ubicaciones.objects.create(nombre="Sala Superior", descripcion="En la Sala C, subes y giras a la izquierda")
        # Crear departamentos con sus ubicaciones (foreign key de la tabla Ubicaciones)
        self.department = Departamentos.objects.create(nombre="Emergencias", descripcion="Departamento de atención de urgencias y emergencias médicas",ubicacionID=self.location)
        
        
        #Crear especialidades
        self.specialty = Especialidades.objects.create(nombre="Psiquiatria",descripcion="Rama de la medicina dedicada al estudio y tratamiento de enfermedades mentales")
        
        # Crear doctor 
        self.doctor = Medicos.objects.create(nombre="testDoctor", apellido="testLastName", dni=11112222, especialidadID=self.specialty, telefono="3512225566", email="doctor@example.com")

        # Crear horarios
        self.schedules_doctor = Horario_medicos.objects.create(medicoID=self.doctor, día="Martes y Jueves", hora_inicio='14:00', hora_fin='18:00',especialidadID=self.doctor.especialidadID)

        # Crear citas
        self.appointment = Citas.objects.create(medicoID=self.doctor, horarioID=self.schedules, motivo="Problemas para socializar", estado="Pendiente")
        
        #Crear Turnos
        self.shifts = Turnos.objects.create(userID=user, citaID=self.appointment, estado=self.appointment.estado)
    
    def test_shifts_creation(self):
        # Verificar que el turno se ha creado correctamente
        self.assertEqual(Turnos.objects.count(), 1)
        self.assertEqual(self.shifts.userID, self.user)

    def test_specialty_creation(self):
        # Verificar que la especialidad se ha creado correctamente
        self.assertEqual(Especialidades.objects.count(), 1)
        self.assertEqual(self.specialty.nombre, "Psiquiatría")

    def test_doctor_creation(self):
        # Verificar que el doctor se ha creado correctamente
        self.assertEqual(Medicos.objects.count(), 1)
        self.assertEqual(self.doctor.nombre, "testDoctor")
        self.assertEqual(self.doctor.apellido, "testLastName")
        self.assertEqual(self.doctor.especialidadID, self.specialty)

    def test_schedule_creation(self):
        # Verificar que el horario se ha creado correctamente
        self.assertEqual(Horario_medicos.objects.count(), 1)
        self.assertEqual(self.schedules_doctor.medicoID, self.doctor)
        self.assertEqual(self.schedules_doctor.día, "Martes y Jueves")
        self.assertEqual(self.schedules_doctor.hora_inicio, '14:00')
        self.assertEqual(self.schedules_doctor.hora_fin, '18:00')
        self.assertEqual(self.schedules_doctor.especialidadID, self.specialty)

    def test_appointment_creation(self):
        # Verificar que la cita se ha creado correctamente
        self.assertEqual(Citas.objects.count(), 1)
        self.assertEqual(self.appointment.medicoID, self.doctor)
        self.assertEqual(self.appointment.horarioID, self.schedules_doctor)
        self.assertEqual(self.appointment.motivo, "Problemas para socializar")
        self.assertEqual(self.appointment.estado, "Pendiente")