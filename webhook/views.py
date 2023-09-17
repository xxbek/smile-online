from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from core.models import Questionnaire
from django.views.decorators.http import require_http_methods

from webhook.hooks import send_questionnaire, send_keywords


@login_required
@require_http_methods(['POST'])
def send_document(request, *args, **kwargs):
    patient_pk = kwargs.get('patient_pk')
    patient: Questionnaire = get_object_or_404(Questionnaire, id=patient_pk)
    quest = patient.quest

    action = request.POST.get('action')
    if patient and quest:
        if action == 'send_questionnaire':
            return send_questionnaire(request, patient, quest)
        elif action == 'send_keywords':
            return send_keywords(request, patient)

    messages.success(request, f'Документ не найден')
    return redirect(request.META.get('HTTP_REFERER'))
