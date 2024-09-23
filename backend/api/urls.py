from django.urls import path
from .views import get_github_repositories, select_repository, store_github_user, github_oauth, google_auth

urlpatterns = [
    path('auth/google/', google_auth, name='google_auth'),
    path('github/oauth/', github_oauth, name='github-oauth'),
    path('store/github/user/', store_github_user, name='store_github_user'),
    path('github/repositories/', get_github_repositories, name='github_repositories'),
    path('github/select/', select_repository, name='select_repository'),
]
