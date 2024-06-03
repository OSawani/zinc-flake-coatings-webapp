from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_list, name='section_list'),
    path('section/<int:section_id>/', views.subsection_list, name='subsection_list'),
    path('subsection/<int:subsection_id>/', views.subsection_detail, name='subsection_detail'),
]