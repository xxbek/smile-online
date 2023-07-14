from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from core.models import Questionnaire
from django.views.decorators.http import require_http_methods
from webhook.apps import WebhookConfig
from webhook.utils import send_file_to, generate_body


@login_required
@require_http_methods(['POST'])
def send_document(request, *args, **kwargs):
    patient_pk = kwargs.get('patient_pk')
    patient = get_object_or_404(Questionnaire, id=patient_pk)
    quest = patient.quest
    if not request.FILES:
        messages.success(request, f'Документ не прикреплен')
        return redirect('core:one_patient', patient_pk=patient_pk)

    action = request.POST.get('action')
    if action == 'send_document' and patient and quest:
        file = request.FILES['pdf']
        body = generate_body(patient, quest)
        if send_file_to(file=file, url=WebhookConfig.webhook_url, body=body):
            messages.success(request, 'Документ успешно отправлен')
            return redirect('core:one_patient', patient_pk=patient_pk)
        messages.success(request, 'Ошибка в сервисе Битрикс')
        return redirect('core:one_patient', patient_pk=patient_pk)

    messages.success(request, f'Документ не найден')
    return redirect('core:one_patient', patient_pk=patient_pk)
