# Generated by Django 2.0.5 on 2019-12-16 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocessing', '0005_auto_20191216_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='items',
            name='date_updated',
        ),
    ]
