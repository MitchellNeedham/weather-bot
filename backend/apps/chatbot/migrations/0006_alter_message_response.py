# Generated by Django 3.2.15 on 2022-09-15 13:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_conversation_location_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='response',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
        ),
    ]
