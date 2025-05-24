from django.apps import AppConfig


class ModelInferConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'model_infer'
