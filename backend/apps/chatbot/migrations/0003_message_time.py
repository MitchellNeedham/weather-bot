# Generated by Django 3.2.15 on 2022-09-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_auto_20220914_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]