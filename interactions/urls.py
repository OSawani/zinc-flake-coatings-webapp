from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comment_list, name='comment_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('comments/add/<int:subsection_id>/',
         views.add_comment, name='add_comment'),
    path(
        'comments/edit/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'),
    path('comment/delete/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('favourites/', views.list_favourites, name='favourite_list'),
    path('favourites/add/<str:content_type>/<int:content_id>/',
         views.add_favourite, name='add_favourite'),

    # New paths for section comments
    path('comments/section/add/<int:section_id>/', views.add_comment_to_section, name='add_comment_to_section'),
    path('comments/section/edit/<int:comment_id>/', views.edit_section_comment, name='edit_section_comment'),
    path('comments/section/delete/<int:comment_id>/', views.delete_section_comment, name='delete_section_comment'),
]
