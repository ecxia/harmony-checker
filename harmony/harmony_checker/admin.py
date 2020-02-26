from django.contrib import admin

# Register your models here.
from .models import Score, MusicalTest, Result

admin.site.register(Score)
admin.site.register(MusicalTest)
admin.site.register(Result)