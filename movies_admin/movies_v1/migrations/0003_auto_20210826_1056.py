# Generated by Django 3.1 on 2021-08-26 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies_v1', '0002_auto_20210824_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='indexed',
        ),
        migrations.RemoveField(
            model_name='filmworkgenre',
            name='indexed',
        ),
        migrations.RemoveField(
            model_name='filmworkperson',
            name='indexed',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='indexed',
        ),
        migrations.RemoveField(
            model_name='person',
            name='indexed',
        ),
    ]
