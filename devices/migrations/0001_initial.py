# Generated by Django 4.1.1 on 2023-07-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveCamera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(default='No Name', max_length=100)),
                ('device_description', models.CharField(default='', max_length=255)),
                ('device_location', models.CharField(default='Unknown', max_length=100)),
                ('device_flash', models.BooleanField(default=True)),
                ('device_status', models.BooleanField(default=True)),
                ('device_picinterval', models.IntegerField(default=1000)),
                ('device_ip', models.CharField(default='0.0.0.0', max_length=15)),
                ('device_firmware', models.CharField(default='', max_length=20)),
                ('device_created', models.DateTimeField(auto_now_add=True)),
                ('device_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
