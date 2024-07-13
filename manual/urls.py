from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_list, name='section_list'),
    path('section/<int:section_id>/', views.section_detail_accordion,
         name='section_detail_accordion'),
    path('intro/', views.intro, name='intro'),
    path('guide/', views.guide, name='guide'),
]