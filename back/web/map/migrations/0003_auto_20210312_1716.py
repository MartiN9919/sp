# Generated by Django 3.1.7 on 2021-03-12 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20201015_1442'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='model_alerts',
            table='sys_alert',
        ),
    ]
