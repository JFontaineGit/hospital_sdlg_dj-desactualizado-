from django.urls import path,include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'locations',views.UbicationViewSet)
router.register(r'departments',views.DepartmentViewSet)
router.register(r'specialties',views.SpecialtyViewSet)
router.register(r'doctors',views.DoctorsViewSet)
router.register(r'schedules',views.SchedulesViewSet)
router.register(r'appointments',views.AppointmentsViewSet)
router.register(r'shifts',views.ShiftsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('especialidades-mas-frecuentes/', views.especialidades_mas_frecuentes, name='especialidades_mas_frecuentes')
]