from django.db import models
from django.contrib.auth.models import User

from . import voiceleading

# Create your models here.

class Test(models.Model):
    TEST_CHOICES = (
        ('get_num_parts', 'Number of Parts'),
        ('get_missing_notes', 'Missing Notes'),
        ('get_parts_out_of_range', 'Parts out of Range'),
        ('get_doubled_leading_tones', 'Doubled Leading Tones'),
        ('get_omitted_thirds', 'Omitted Thirds'),
        ('get_overspacing', 'Overspaced Chords'),
        ('get_melodic_aug_2', 'Melodic Augmented 2nd'),
        ('get_parallel_fifths', 'Parallel Fifths'),
        ('get_d5_to_p5', 'Diminished 5th to Perfect 5th'),
        ('get_hidden_fifths', 'Hidden Fifths'), # narrow to outer voices
        ('get_hidden_octaves', 'Hidden Octaves'), # narrow to outer voices
        ('get_crossed_voices', 'Crossed Voices') # narrow to outer voices
    )

    # use module path + human-readable name and. Don't have to go into source - just add tests via admin interface
    # no eval!
    # how to do - "import module by string name"

    name = models.CharField(max_length = 50, choices=TEST_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Score(models.Model):
    # replace upload_to with some sort of function (incrementer? uuid?)
    score = models.FileField(upload_to='uploads/')
    tests = models.ManyToManyField(Test)
    checked_score = models.FileField(upload_to='checked/',null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.score.name

class Result(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    passed = models.BooleanField(null=True)
    
    def __str__(self):
        return str.format('{0}: {1}', self.score.score.name, self.test.name)