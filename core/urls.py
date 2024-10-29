from django.urls import path, re_path
from . import views

urlpatterns = [
    #
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    # Catch-all pattern for handling any URL with a 'jwt' query parameter
    path('sso-login/', views.sso_login_view, name='sso_login'),  # Explicit JWT login path
]
