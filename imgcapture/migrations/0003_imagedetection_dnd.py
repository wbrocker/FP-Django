# Generated by Django 4.1.10 on 2023-07-28 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgcapture', '0002_imagedetection_detection_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagedetection',
            name='dnd',
            field=models.BooleanField(default=False),
        ),
    ]