# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.models import Question, Quest, Questionnaire, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'added_at', 'title', 'quest', 'order', 'answer_options', 'keywords']


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'added_at', 'name']


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'added_at', 'fio', 'dob', 'phone_number', 'eula_is_accepted', 'slug', 'quest', 'keywords',
                  'can_edit']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'questionnaire', 'answer']
