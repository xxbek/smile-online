# -*- coding: utf-8 -*-
from django.db import models
from django.utils.crypto import get_random_string


class Question(models.Model):

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']

    added_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True,
    )
    title = models.CharField(
        verbose_name='Текст вопроса', max_length=1000,
    )
    quest = models.ForeignKey(
        to='core.Quest', on_delete=models.CASCADE,
        related_name='questions', verbose_name='Тест',
    )
    order = models.PositiveIntegerField(
        blank=False, null=False, default=0,
    )
    answer_options = models.TextField(
        verbose_name='Варианты ответа (по одному в строке)',
        blank=True, default='Да\nНет',
    )
    keywords = models.ManyToManyField(
        to='core.Keyword',
        related_name='questions',
        blank=True,
        verbose_name='Ключевые слова',
    )

    def __str__(self):
        max_length = 70
        more_s = '...'
        title = str(self.title)
        if len(title) >= max_length:
            title = title[:max_length - len(more_s)] + more_s
        return title

    def get_answer_options(self):
        options = str(self.answer_options).splitlines()
        options = [line.strip() for line in options if line.strip()]
        return options


class Quest(models.Model):

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    added_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True,
    )
    name = models.CharField(
        verbose_name='Название', max_length=200,
    )

    def __str__(self):
        return str(self.name)


class Questionnaire(models.Model):

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'

    added_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True,
    )
    fio = models.CharField(
        verbose_name='ФИО', max_length=200,
    )
    dob = models.CharField(
        verbose_name='Дата рождения', max_length=20,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона', max_length=20,
    )
    eula_is_accepted = models.BooleanField(
        verbose_name='Согласен с правилами сайта',
        help_text='Соглашаюсь с политикой конфиденциальности. '
                  'Подвертждаю, что все ответы, предоставленные мной, достоверны.',
    )
    slug = models.SlugField(
        verbose_name='Уникальный адрес', max_length=32,
        unique=True,
    )
    quest = models.ForeignKey(
        to='core.Quest', on_delete=models.CASCADE,
        related_name='Questionnaires', verbose_name='Анкета',
    )
    keywords = models.ManyToManyField(
        to='core.Keyword',
        related_name='questionnaires',
        blank=True,
        help_text='Ключевые слова для CRM.',
    )
    can_edit = models.BooleanField(
        verbose_name='Можно редактировать',
        blank=True, default=True,
        help_text='Может ли доктор редактировать ключевые слова анкеты?',
    )

    def __str__(self):
        return '{} {}'.format(self.added_at.strftime('%Y-%m-%d'), self.fio)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=32)
        super(Questionnaire, self).save(*args, **kwargs)

    def update_keywords(self):
        if self.get_next_question() is None:
            for keyword in Keyword.objects.filter(quest=self.quest):
                if self.answers.\
                        filter(question__keywords=keyword).\
                        exclude(answer__iexact='Нет').\
                        values_list('question', flat=True):
                    self.keywords.add(keyword)

    def get_cur_question_number(self):
        return self.answers.count()

    get_cur_question_number.short_description = 'Кол-во отвеченных вопросов'

    def get_total_questions(self):
        return self.quest.questions.order_by('pk')

    def get_total_questions_count(self):
        return self.get_total_questions().count()

    def get_next_question(self):
        for question in self.get_total_questions():
            if not self.answers.filter(question=question).exists():
                return question
        return None

    def get_keywords_with_answers(self):
        items = []
        for keyword in self.keywords.all():
            exact_answers = []
            for question in keyword.questions.all():
                exact_answers = self.answers.\
                    filter(question__keywords=keyword).\
                    exclude(answer__iexact='Нет')
            items.append([
                keyword, exact_answers
            ])
        return items


class Answer(models.Model):

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        unique_together = [['question', 'questionnaire']]

    question = models.ForeignKey(
        to='core.Question', on_delete=models.CASCADE,
        related_name='answers', verbose_name='Вопрос',
    )
    questionnaire = models.ForeignKey(
        to='core.Questionnaire', on_delete=models.CASCADE,
        related_name='answers', verbose_name='Данные',
    )
    answer = models.CharField(
        verbose_name='Ответ', max_length=500,
    )

    def __str__(self):
        return self.answer


class Keyword(models.Model):

    class Meta:
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'

    name = models.CharField(
        verbose_name='Название', max_length=100,
    )
    quest = models.ForeignKey(
        to='core.Quest', on_delete=models.CASCADE,
        related_name='keywords', verbose_name='Тест',
    )

    def __str__(self):
        return '{}: {}'.format(self.quest, self.name)
