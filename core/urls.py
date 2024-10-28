from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('sso-login/', views.sso_login_view, name='sso_login'),  # Add the SSO login URL
    # Catch-all pattern for handling JWT passed as a query parameter at any URL
    re_path(r'^.*$', views.sso_login_view, name='catch_all_jwt'),
]
