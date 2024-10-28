from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('sso-login/', views.sso_login_view, name='sso_login'),  # Add the SSO login URL
]
