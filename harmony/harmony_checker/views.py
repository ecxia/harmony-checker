from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.views.static import serve
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, views as auth_views
from django.contrib.auth.decorators import login_required

from .forms import ScoreForm, AuthFormWithSubmit
from .models import Score, Result
from . import voiceleading

import music21 as m21
import os

# Create your views here.

def index(request):
    user = get_user(request)
    if request.method == 'POST':
        score_form = ScoreForm(request.POST, request.FILES)
        new_score = score_form.save()
        if user.is_authenticated:
            new_score.user = user
        new_score.score_display_name = os.path.basename(new_score.score.name)
        new_score.save()
        fname = str.format('{0}/{1}', settings.MEDIA_ROOT, new_score.score.url)
        stream = m21.converter.parse(fname)
        end_height = 1
        for test in new_score.tests.all():
            test_failures = getattr(voiceleading, test.func)(
                stream,
                chordified_stream=stream.chordify(),
            )
            r = Result(score=new_score,test=test)
            r.passed = (len(test_failures) == 0)
            r.save()
            stream, end_height = voiceleading.annotate_stream(test_failures, stream, end_height)
            output_path = os.path.join("{}_checked.xml".format(fname[:-4]))
            stream.write(
                "musicxml", output_path
            )
            with open(output_path) as fp:
                contents = File(fp)
                new_score.checked_score.save(output_path, contents)
            new_score.checked_score_display_name = f"{new_score.score_display_name[:-4]}_checked.xml"
            new_score.save()
        return HttpResponseRedirect(
            reverse('harmony_checker:checked', args=(new_score.id,))
        )
    else:
        score_form = ScoreForm()

    return render(
        request, 
        'harmony_checker/index.html', 
        {'score_form': score_form, 'user': user, 'title': "Check Harmony"}
    )

def checked(request, score_id):
    user = get_user(request)
    score = get_object_or_404(Score, pk=score_id)
    results = Result.objects.filter(score=score_id)

    #generate checked score display name
    return render(
        request, 
        'harmony_checker/checked.html',
        {
            'score': score, 
            'results': results, 
            'user': user,
            'title': 'Results'
        }
    )


def checked_score(request, score_id):
    score = get_object_or_404(Score, pk=score_id)
    response = HttpResponse(score.checked_score, content_type='application/xml')
    response['Content-Disposition'] = f"attachment; filename={score.checked_score_display_name}"
    return response


def score(request, score_id):
    score = get_object_or_404(Score, pk=score_id)
    response = HttpResponse(score.score, content_type='application/xml')
    response['Content-Disposition'] = f"attachment; filename={score.score_display_name}"
    return response

@login_required
def profile(request):
    user = get_user(request)
    scores = Score.objects.filter(user=user).order_by('-upload_date')
    return render(
        request,
        'harmony_checker/profile.html',
        {
            'user': user, 
            'scores': scores,
            'title': "User Profile"
        }
    )