from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.views.static import serve
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required

from .forms import ScoreForm
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
        new_score.user = user 
        new_score.save()
        fname = str.format('{0}/{1}', settings.MEDIA_ROOT, new_score.score.url)
        stream = m21.converter.parse(fname)
        end_height = 1
        for test in new_score.tests.all():
            test_failures = getattr(voiceleading, test.name)(
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
        return HttpResponseRedirect(
            reverse('harmony_checker:checked', args=(new_score.id,))
        )

#         if score_form.is_valid():
#             input_score = request.FILES.get('score')
#             data = input_score.read()
#             f = open('temp_score.xml', 'wb+')
#             f.write(data)
#             output_path = check_file('temp_score.xml')
#             f = open(output_path, 'r')
#             output_file = File(f)
#             response = HttpResponse(output_file, content_type='application/xml')
#             response['Content-Disposition'] = 'attachment; filename="annotated_score.xml'
# #             close file? - return in with statement
#            return response
    else:
        score_form = ScoreForm()

    return render(
        request, 
        'harmony_checker/index.html', 
        {'score_form': score_form, 'user': user}
    )

def checked(request, score_id):
    user = get_user(request)
    score = get_object_or_404(Score, pk=score_id)
    results = Result.objects.filter(score=score_id)
    return render(
        request, 
        'harmony_checker/checked.html',
        {'score': score, 'results': results, 'user': user}
    )

@login_required
def profile(request):
    user = get_user(request)
    scores = Score.objects.filter(user=user)
    return render(
        request,
        'harmony_checker/profile.html',
        {
            'user': user, 
            'scores': scores
        }
    )