from django.urls import path
from webhook import views
from webhook.apps import WebhookConfig

app_name = WebhookConfig.name


urlpatterns = [
    path('pdf/<int:patient_pk>/', views.send_document, name='send_document'),
]
