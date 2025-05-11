from django.apps import AppConfig


class NotesConfig(AppConfig):
    """Настройки приложения служебных записок (notes)"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "notes"
    verbose_name = "служебные записки"
