# Generated by Django 5.1.5 on 2025-05-11 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportmessage',
            name='is_answered',
        ),
        migrations.RemoveField(
            model_name='supportmessage',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='supportmessage',
            name='user',
        ),
    ]
