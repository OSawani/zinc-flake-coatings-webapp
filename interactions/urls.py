from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comment_list, name='comment_list'),
    path(
        'comments/edit/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'),
]
