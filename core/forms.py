# -*- coding: utf-8 -*-
from django import forms

from core.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    eula_is_accepted = forms.BooleanField(label='Соглашаюсь с политикой конфиденциальности. '
                                                'Подвертждаю, что все ответы, предоставленные мной, достоверны.')

    class Meta:
        model = Questionnaire
        fields = ['fio', 'dob', 'phone_number', 'eula_is_accepted', 'quest']
