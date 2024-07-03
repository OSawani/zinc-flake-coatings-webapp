from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_list, name='section_list'),
    path('section/<int:section_id>/', views.section_detail_accordion,
         name='section_detail_accordion'),
    #path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('section/<int:section_id>/subsections/', views.subsection_list, name='subsection_list'),
    path('subsection/<int:subsection_id>/', views.subsection_detail, name='subsection_detail'),
    path('intro/', views.intro, name='intro'),
    path('guide/', views.guide, name='guide'),
]