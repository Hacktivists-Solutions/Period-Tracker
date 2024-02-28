from django.contrib import admin

# Register your models here.
# myapp/admin.py

from django.contrib import admin
from .models import MenstrualCycle, PeriodSymptom

# Register MenstrualCycle model
admin.site.register(MenstrualCycle)


# Customize PeriodSymptom model admin
class PeriodSymptomAdmin(admin.ModelAdmin):
    list_display = ['symptom']  


admin.site.register(PeriodSymptom)
