# Generated by Django 3.2.15 on 2022-09-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_message_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='action_requested',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
