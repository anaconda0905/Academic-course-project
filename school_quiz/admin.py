from django.contrib import admin

from .models import Quiz, MCQQuestion

# Register your models here.

admin.site.register(Quiz)
admin.site.register(MCQQuestion)
