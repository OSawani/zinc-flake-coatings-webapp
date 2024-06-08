from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/add/<int:subsection_id>/',
         views.add_comment, name='add_comment'),
    path(
        'comments/edit/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'),
    path('comment/delete/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]
