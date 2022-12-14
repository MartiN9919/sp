# Generated by Django 3.2 on 2021-05-25 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelScript',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Данное название будет отображаться в меню выбора анализа', max_length=50, unique=True, verbose_name='Название Скрипта')),
                ('icon', models.CharField(blank=True, choices=[('home_icon', 'HOME'), ('apple_icon', 'APPLE'), ('celery_icon', 'CELERY'), ('car_icon', 'CAR'), ('cat_icon', 'CAT')], default=None, help_text='Данная иконка будет отображаться в меню выбора анализа', max_length=25, null=True, verbose_name='Иконка')),
                ('hint', models.CharField(blank=True, default='', help_text='Ввод текста подсказки, которая будет отображаться в меню выбора анализа', max_length=255, verbose_name='Всплывающая подсказка')),
                ('content', models.TextField(blank=True, default='', help_text='Поле ввода скрипта', verbose_name='Текст скрипта')),
                ('descript', models.TextField(help_text='Введите описание данного объекта', verbose_name='Описание объекта')),
                ('variables', models.TextField(blank=True, default='', help_text='Введите переменные формата (name variables):(type variables)', verbose_name='Переменные')),
                ('enabled', models.BooleanField(default=True, help_text='Включение/отключение скрипта', verbose_name='Состояние')),
                ('type', models.CharField(choices=[('map', 'Карты'), ('report', 'Отчеты')], max_length=20, verbose_name='Тип скрипта')),
            ],
            options={
                'verbose_name': 'Скрипт',
                'verbose_name_plural': 'Скрипты',
                'db_table': 'sys_script',
                'managed': False,
            },
        ),
    ]
