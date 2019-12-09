from django.urls import path, include

from . import views

app_name = 'harmony_checker'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:score_id>/checked', views.checked, name='checked'),
]