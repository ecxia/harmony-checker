# Generated by Django 2.2.6 on 2019-11-17 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('harmony_checker', '0004_auto_20191116_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='tests',
        ),
        migrations.AddField(
            model_name='test',
            name='score',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='harmony_checker.Score'),
        ),
    ]
