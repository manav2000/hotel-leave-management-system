# Generated by Django 3.0.7 on 2020-06-16 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warden',
            name='applications',
        ),
    ]
