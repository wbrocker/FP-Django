# Generated by Django 4.1.10 on 2023-08-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0008_remove_alarmconfig_alarm_objects'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarmconfig',
            name='alarm_objects',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='detectionobjects',
            name='alarm_on_object',
            field=models.BooleanField(default=False),
        ),
    ]
