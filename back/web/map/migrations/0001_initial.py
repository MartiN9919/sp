# Generated by Django 2.2.7 on 2020-03-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model_Alerts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=255, verbose_name='Содержание')),
                ('type', models.CharField(choices=[('info', 'информация'), ('warn', 'предупреждение'), ('error', 'ошибка')], default='error', max_length=8, verbose_name='Тип')),
                ('wait', models.PositiveSmallIntegerField(default=0, help_text='0 - не ограничено', verbose_name='Время показа, сек.')),
                ('owner', models.CharField(blank=True, default='', max_length=5, verbose_name='Владелец')),
                ('users', models.CharField(blank=True, default='', max_length=255, verbose_name='Пользователи')),
                ('groups', models.CharField(blank=True, default='', max_length=255, verbose_name='Группы')),
                ('descript', models.CharField(blank=True, default='', max_length=255, verbose_name='Примечание')),
                ('enabled', models.BooleanField(default=True, verbose_name='Доступно')),
            ],
            options={
                'verbose_name': 'уведомление',
                'verbose_name_plural': 'Уведомления',
                'db_table': 'alerts',
                'managed': False,
            },
        ),
    ]
