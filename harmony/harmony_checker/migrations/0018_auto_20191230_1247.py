# Generated by Django 2.2.6 on 2019-12-30 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harmony_checker', '0017_auto_20191230_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='func',
            field=models.CharField(max_length=50),
        ),
    ]
