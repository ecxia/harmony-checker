import pytest
from django.test import TestCase
from harmony_checker.models import MusicalTest, Score, Result


pytestmark = pytest.mark.django_db


def test_musical_test_creation():
    mt = MusicalTest.objects.create(name="test_test", func="test_func")
    assert mt.__str__() == "test_test"

def test_score_creation():
    s = Score.objects.create(score_display_name="test_display_name")
    assert s.__str__() == "test_display_name"

def test_result_creation():
    mt = MusicalTest.objects.create(name="test_test", func="test_func")
    s = Score.objects.create(score_display_name="test_display_name")
    r = Result.objects.create(score=s, musical_test=mt)
    assert r.__str__() == "test_display_name: test_test"