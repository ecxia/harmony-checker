# Generated by Django 2.2.6 on 2019-11-16 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harmony_checker', '0003_auto_20191116_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='result',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Result',
        ),
    ]
