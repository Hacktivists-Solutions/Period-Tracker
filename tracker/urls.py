from django.urls import path

from . import views

urlpatterns = [
    path('record/', views.record_menstrual_cycle, name='record_cycle'),
    path('cycles/', views.get_menstrual_cycles, name='get_cycles'),
    path('filter/', views.filter_menstrual_cycles, name='filter_cycles'),
]
