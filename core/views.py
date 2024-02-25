from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from core.forms import QuestionnaireForm
from core.models import Questionnaire, Answer, Keyword, Quest

from core.utils import render_to_pdf
from django.http import HttpResponse

from smile_online import settings
from webhook.utils import get_all_questionnaire_by_patient


@require_http_methods(['GET', 'POST'])
def index(request, template_name='core/index.html'):
    questionnaire_form = QuestionnaireForm(initial={'fio': request.session.get('fio'),
                                                    'dob': request.session.get('dob'),
                                                    'phone_number': request.session.get('phone_number')})
    if request.method == 'POST':
        questionnaire_form = QuestionnaireForm(data=request.POST)
        if questionnaire_form.is_valid():
            questionnaire = questionnaire_form.save()
            if request.session.get('questionnaires') is None:
                request.session['questionnaires'] = []
            request.session['questionnaires'].append(questionnaire.slug)
            request.session['fio'] = request.POST['fio']
            request.session['dob'] = request.POST['dob']
            request.session['phone_number'] = request.POST['phone_number']
            request.session.save()
            return redirect('core:questionnaire', slug=questionnaire.slug)

    your_questionnaires = Questionnaire.objects.filter(slug__in=request.session.get('questionnaires', [])).order_by('-pk')
    context = {
        'title': 'Главная страница',
        'your_questionnaires': your_questionnaires,
        'questionnaire_form': questionnaire_form,
    }
    return render(request, template_name, context=context)


@login_required
@require_http_methods(['GET'])
def patients_page(request, template_name='core/patients.html'):
    patients = Questionnaire.objects.all()
    context = {
        'title': 'Пациенты',
        'patients': patients,
    }
    return render(request, template_name, context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def one_patient_page(request, patient_pk, template_name='core/one_patient.html'):
    patient = get_object_or_404(Questionnaire, id=patient_pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_keyword':
            Keyword.objects.create(name=request.POST['name'], quest=patient.quest)
            return redirect('core:one_patient', patient_pk=patient_pk)
        elif action == 'set_keyword':
            if patient.can_edit:
                keyword = get_object_or_404(Keyword, pk=request.POST['keyword'])
                patient.keywords.add(keyword)
            return redirect('core:one_patient', patient_pk=patient_pk)
        elif action == 'save_patient':
            patient.can_edit = False
            patient.save()
            return redirect('core:one_patient', patient_pk=patient_pk)

    context = {
        'title': 'Анкета «{}»'.format(patient.fio),
        'patient': patient,
        'all_keywords': Keyword.objects.filter(quest=patient.quest),
    }
    return render(request, template_name, context=context)


@require_http_methods(['GET', 'POST'])
def questionnaire_page(request, slug, template_name='core/questionnaire.html'):
    questionnaire = get_object_or_404(Questionnaire, slug=slug)
    next_question = questionnaire.get_next_question()
    if request.method == 'POST':
        Answer.objects.create(question=next_question,
                              questionnaire=questionnaire,
                              answer=request.POST.get('answer', ''))
        if questionnaire.get_next_question() is None:
            questionnaire.update_keywords()
        return redirect('core:questionnaire', slug=questionnaire.slug)

    questionnaire_need_to_fill = []
    # when questionnaire is filled
    if next_question is None:
        your_questionnaires = Questionnaire.objects.filter(slug__in=request.session.get('questionnaires', []))
        all_user_questionnaires_types = set([quest_id.quest.id for quest_id in your_questionnaires])
        for quest_type in Quest.objects.all():
            if quest_type.id not in all_user_questionnaires_types:
                questionnaire_need_to_fill.append(quest_type)

    context = {
        'title': 'Прохождение теста',
        'questionnaire': questionnaire,
        'next_question': next_question,
        'questionnaire_need_to_fill': questionnaire_need_to_fill
    }
    return render(request, template_name, context=context)


@require_http_methods('POST')
def pdf_user_questionnaire(request, patient_pk):
    patient = get_object_or_404(Questionnaire, id=patient_pk)
    quest = patient.quest

    if patient:
        data = {
            'patient': patient,
            'quest': quest,
            'title': quest.name,
            'word_key': [keyword[0].name for keyword in patient.get_keywords_with_answers()],
            'STATIC_ROOT': settings.STATIC_ROOT
        }
        pdf = render_to_pdf('pdf/questionnaire.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    return HttpResponse("Not found")


@require_http_methods('POST')
def pdf_user_keywords(request, patient_pk):
    patient: Questionnaire = get_object_or_404(Questionnaire, id=patient_pk)
    all_questionnaire = get_all_questionnaire_by_patient(patient)
    for questionnaire in all_questionnaire:
        questionnaire.keyword = [keyword[0].name for keyword in questionnaire.get_keywords_with_answers()]
    if patient:
        data = {
            'patient': patient,
            'all_questionnaire': all_questionnaire,
            'STATIC_ROOT': settings.STATIC_ROOT
        }
        pdf = render_to_pdf('pdf/patient_keywords.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    return HttpResponse("Not found")

