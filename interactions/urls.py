from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comment_list, name='comment_list'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('notifications/', views.notification_list, name='notification_list'),
]
