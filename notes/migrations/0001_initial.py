# Generated by Django 5.1.7 on 2025-03-26 15:23

import django.db.models.deletion
import notes.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название хаба', max_length=255, verbose_name='Название хаба')),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CarLoanCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название центра', max_length=255, verbose_name='Название центра автокредитования')),
                ('hub', models.ForeignKey(help_text='Выберите хаб', on_delete=django.db.models.deletion.CASCADE, to='notes.hub', verbose_name='Хаб')),
            ],
            options={
                'verbose_name': 'Центр автокредитования',
                'verbose_name_plural': 'Центры автокредитования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_loan_center', models.ForeignKey(help_text='Выберите центр автокредитования', on_delete=django.db.models.deletion.CASCADE, to='notes.carloancenter', verbose_name='Центр автокредитования')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pyrus_url', models.CharField(blank=True, help_text='Введите ссылку на Pyrus', max_length=255, null=True, validators=[notes.validators.validate_parus_url], verbose_name='Ссылка на Pyrus')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания записки', verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='Дата обновления записки', verbose_name='Дата обновления')),
                ('appoval_date', models.DateTimeField(blank=True, help_text='Дата утверждения записки', null=True, verbose_name='Дата утверждения')),
                ('subject', models.CharField(help_text='Введите тему записки', max_length=255, verbose_name='Тема записки')),
                ('status', models.CharField(choices=[('DRAFT', 'Черновик'), ('ACTIVE', 'Активна'), ('IN_PROGRESS', 'Действующая')], default='DRAFT', help_text='Выберите статус записки', max_length=20, verbose_name='Статус записки')),
                ('car_loan_center', models.ForeignKey(help_text='Выберите центр автокредитования', on_delete=django.db.models.deletion.CASCADE, to='notes.carloancenter', verbose_name='Центр автокредитования')),
                ('observers', models.ManyToManyField(blank=True, help_text='Выберите наблюдателей', related_name='observers', to='notes.userprofile', verbose_name='Наблюдатели')),
                ('owner', models.ForeignKey(help_text='Выберите пользователя', null=True, on_delete=django.db.models.deletion.SET_NULL, to='notes.userprofile', verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Записка',
                'verbose_name_plural': 'Записки',
                'ordering': ['-created_at'],
            },
        ),
    ]
