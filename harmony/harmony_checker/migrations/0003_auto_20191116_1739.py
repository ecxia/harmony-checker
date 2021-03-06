# Generated by Django 2.2.6 on 2019-11-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harmony_checker', '0002_auto_20191116_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(choices=[('get_num_parts', 'Number of Parts'), ('get_missing_notes', 'Missing Notes'), ('get_parts_out_of_range', 'Parts out of Range'), ('get_doubled_leading_tones', 'Doubled Leading Tones'), ('get_omitted_thirds', 'Omitted Thirds'), ('get_overspacing', 'Overspaced Chords'), ('get_melodic_aug_2', 'Melodic Augmented 2nd'), ('get_parallel_fifths', 'Parallel Fifths'), ('get_d5_to_p5', 'Diminished 5th to Perfect 5th'), ('get_hidden_fifths', 'Hidden Fifths'), ('get_hidden_octaves', 'Hidden Octaves'), ('get_crossed_voices', 'Crossed Voices')], max_length=50, unique=True),
        ),
    ]
