import io

from core.models import Questionnaire
from core.utils import render_to_pdf
from smile_online import settings
from webhook.apps import WebhookConfig
from django.contrib import messages
from django.shortcuts import redirect

from webhook.utils import send_file_to, get_all_questionnaire_by_patient


def send_questionnaire(request, patient, quest):
    data = {
        'patient': patient,
        'quest': quest,
        'title': quest.name,
        'STATIC_ROOT': settings.STATIC_ROOT
    }
    file = render_to_pdf('pdf/questionnaire.html', data)
    body = {
        'fio': patient.fio,
        'birthday': patient.dob,
        'address': patient.slug,
        'mobile': patient.phone_number,
        'number_per': quest.name,
        'date': patient.added_at,
        'word_key': [keyword[0].name for keyword in patient.get_keywords_with_answers()]
    }

    if send_file_to('questionnaire', file=file, url=WebhookConfig.webhook_url, body=body):
        patient.update_send_file_date()
        messages.success(request, 'Анкета успешно отправлена')
        return redirect(request.META.get('HTTP_REFERER'))

    messages.success(request, 'Ошибка в сервисе Битрикс')
    return redirect(request.META.get('HTTP_REFERER'))


def send_keywords(request, patient):
    all_questionnaire = get_all_questionnaire_by_patient(patient)
    for questionnaire in all_questionnaire:
        questionnaire.keyword = [keyword[0].name for keyword in questionnaire.get_keywords_with_answers()]
    data = {
        'patient': patient,
        'all_questionnaire': all_questionnaire,
        'STATIC_ROOT': settings.STATIC_ROOT
    }
    file = render_to_pdf('pdf/patient_keywords.html', data)

    body = {
        'fio': patient.fio,
        'birthday': patient.dob,
        'address': patient.slug,
        'mobile': patient.phone_number,
    }

    if send_file_to('keywords', file=file, url=WebhookConfig.webhook_url, body=body):
        patient.update_send_keywords_date()
        messages.success(request, 'Ключевые слова успешно отправлены')
        return redirect(request.META.get('HTTP_REFERER'))

    messages.success(request, 'Ошибка в сервисе Битрикс')
    return redirect(request.META.get('HTTP_REFERER'))
