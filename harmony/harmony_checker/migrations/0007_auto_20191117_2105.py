# Generated by Django 2.2.6 on 2019-11-18 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harmony_checker', '0006_auto_20191117_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='result',
            new_name='passed',
        ),
    ]
