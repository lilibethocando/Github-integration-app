from django.urls import path
from .views import (
    google_auth,
    github_login,
    github_callback,
    get_github_repositories,
    select_repository
)

urlpatterns = [
    path('auth/google-oauth2/', google_auth, name='google_auth'), 
    path('github/login/', github_login, name='github_login'), 
    path('callback/', github_callback, name='github_callback'), 
    path('github/repositories/', get_github_repositories, name='github_repositories'),
    path('github/select/repositories/', select_repository, name='select_repository'),
]
