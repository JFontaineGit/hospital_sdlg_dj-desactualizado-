from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Tipo de campo automatico para las claves primarias de los modelos.
    name = 'blog'
