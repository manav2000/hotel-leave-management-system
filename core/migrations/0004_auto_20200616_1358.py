# Generated by Django 3.0.7 on 2020-06-16 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200616_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='date_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='applications',
            name='till_date',
            field=models.DateTimeField(),
        ),
    ]
