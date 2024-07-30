from django.urls import path
import user_panel.views as u_p
import turnero.views as turn
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('panel/',u_p.user_panel,name='panel'),
    path('turnos/',u_p.turnos_list,name='lista_de_turnos'),
    path('testimonios/',u_p.form_testimonios,name='testimonios_form'),
    path('edit_profile/',u_p.editar_perfil,name='editar_perfil'),
    path('comprobante/<int:turno_id>/', turn.generar_comprobante, name='generar_comprobante')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)