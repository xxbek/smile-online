# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from core import views
from core.apps import CoreConfig
from core.viewsets import QuestionViewSet, QuestViewSet, QuestionnaireViewSet, AnswerViewSet


app_name = CoreConfig.name

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'quests', QuestViewSet)
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'answers', AnswerViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.patients_page, name='patients'),
    path('patients/<int:patient_pk>/', views.one_patient_page, name='one_patient'),
    path('q/<slug:slug>/', views.questionnaire_page, name='questionnaire'),
    path('api/', include(router.urls)),
]
