# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions

from core.models import Question, Quest, Questionnaire, Answer
from core.serializers import QuestionSerializer, QuestSerializer, QuestionnaireSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-added_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all().order_by('-added_at')
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all().order_by('-added_at')
    serializer_class = QuestionnaireSerializer
    permission_classes = [permissions.IsAdminUser]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-pk')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAdminUser]
