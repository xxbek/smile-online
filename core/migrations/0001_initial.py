# Generated by Django 3.2.5 on 2021-08-13 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Ключевое слово',
                'verbose_name_plural': 'Ключевые слова',
            },
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Анкета',
                'verbose_name_plural': 'Анкеты',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('fio', models.CharField(max_length=200, verbose_name='ФИО')),
                ('dob', models.CharField(max_length=20, verbose_name='Дата рождения')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('eula_is_accepted', models.BooleanField(help_text='Соглашаюсь с политикой конфиденциальности. Подвертждаю, что все ответы, предоставленные мной, достоверны.', verbose_name='Согласен с правилами сайта')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='Уникальный адрес')),
                ('can_edit', models.BooleanField(blank=True, default=True, help_text='Может ли доктор редактировать ключевые слова анкеты?', verbose_name='Можно редактировать')),
                ('keywords', models.ManyToManyField(blank=True, help_text='Ключевые слова для CRM.', related_name='questionnaires', to='core.Keyword')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Questionnaires', to='core.quest', verbose_name='Анкета')),
            ],
            options={
                'verbose_name': 'Данные',
                'verbose_name_plural': 'Данные',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=1000, verbose_name='Текст вопроса')),
                ('order', models.PositiveIntegerField(default=0)),
                ('answer_options', models.TextField(blank=True, default='Да\nНет', verbose_name='Варианты ответа (по одному в строке)')),
                ('keywords', models.ManyToManyField(blank=True, related_name='questions', to='core.Keyword', verbose_name='Ключевые слова')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.quest', verbose_name='Тест')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='keyword',
            name='quest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='core.quest', verbose_name='Тест'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=500, verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.question', verbose_name='Вопрос')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.questionnaire', verbose_name='Данные')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'unique_together': {('question', 'questionnaire')},
            },
        ),
    ]
