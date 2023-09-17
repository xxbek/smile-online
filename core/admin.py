# -*- coding: utf-8 -*-
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from core.models import Question, Quest, Questionnaire, Answer, Keyword


class QuestionAdminInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Question
    fk_name = 'quest'
    extra = 0


class QuestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [QuestionAdminInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'questionnaire'
    extra = 0
    can_delete = False


class QuestionnaireAdmin(admin.ModelAdmin):
    fields = ('fio', 'dob', 'phone_number', 'eula_is_accepted', 'quest', 'slug', 'added_at', 'keywords', 'can_edit', 'last_send_file_date', 'last_send_keywords_date')
    readonly_fields = ('added_at',)
    list_display = ('fio', 'dob', 'phone_number', 'eula_is_accepted', 'added_at', 'slug', 'get_cur_question_number', 'quest', 'can_edit', 'last_send_file_date', 'last_send_keywords_date')
    list_filter = ('added_at', 'quest', 'keywords', 'can_edit', 'eula_is_accepted')
    search_fields = ('fio',)
    inlines = [AnswerInline]

    change_form_template = "admin/change_admin_models.html"


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('quest', 'name',)
    list_filter = ('quest',)
    search_fields = ('name',)


admin.site.register(Quest, QuestAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Keyword, KeywordAdmin)
