from django.contrib import admin

# Register your models here.
from .models import Score, Test, Result

admin.site.register(Score)
admin.site.register(Test)
admin.site.register(Result)