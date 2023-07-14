from django.apps import AppConfig


class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'
    webhook_url = 'https://sekvid.ru/for_del/smileOnline/web/webhook/main/service'
