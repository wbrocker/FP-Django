# Generated by Django 4.1.10 on 2023-07-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_activedevices_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activedevices',
            name='name',
            field=models.CharField(blank=True, default='No Name', max_length=100, null=True),
        ),
    ]
