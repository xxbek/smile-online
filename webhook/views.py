from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from core.models import Questionnaire
from django.views.decorators.http import require_http_methods

from core.utils import render_to_pdf
from smile_online import settings
from webhook.apps import WebhookConfig
from webhook.utils import send_file_to, generate_body


@login_required
@require_http_methods(['POST'])
def send_document(request, *args, **kwargs):
    patient_pk = kwargs.get('patient_pk')
    patient = get_object_or_404(Questionnaire, id=patient_pk)
    quest = patient.quest

    action = request.POST.get('action')
    if action == 'send_document' and patient and quest:
        data = {
            'patient': patient,
            'quest': quest,
            'title': quest.name,
            'STATIC_ROOT': settings.STATIC_ROOT
        }
        file = render_to_pdf('pdf/questionnaire.html', data, 'myPDF')
        body = generate_body(patient, quest)

        if send_file_to(file=file, url=WebhookConfig.webhook_url, body=body):
            patient.update_send_file_date()
            messages.success(request, 'Документ успешно отправлен')
            return redirect(request.META.get('HTTP_REFERER'))

        messages.success(request, 'Ошибка в сервисе Битрикс')
        return redirect(request.META.get('HTTP_REFERER'))

    messages.success(request, f'Документ не найден')
    return redirect(request.META.get('HTTP_REFERER'))
