from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

from os.path import basename

from . import voiceleading

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    func = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.name

class Score(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score = models.FileField(upload_to='uploads/')
    score_display_name = models.CharField(max_length = 50, null=True)
    tests = models.ManyToManyField(Test)
    checked_score = models.FileField(upload_to='checked/',null=True)
    checked_score_display_name = models.CharField(max_length = 50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upload_date = models.DateTimeField('Date Uploaded', default=timezone.now)

    def __str__(self):
        return self.score_display_name

class Result(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    passed = models.BooleanField(null=True)
    
    def __str__(self):
        return str.format('{0}: {1}', self.score.score.name, self.test.name)