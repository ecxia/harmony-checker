from django.urls import path, include

from . import views

app_name = 'harmony_checker'

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:score_id>/checked/', views.checked, name='checked'),
    path('<uuid:score_id>/checked_score/', views.checked_score, name='checked_score'),
    path('<uuid:score_id>/score/', views.score, name='score'),
]