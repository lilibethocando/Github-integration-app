import os
import requests
from social_django.utils import psa
from django.conf import settings
from requests.exceptions import HTTPError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from .serializers import SocialSerializer
from .models import GitHubAccount, SelectedRepository
from django.shortcuts import redirect
import logging


User = get_user_model()
google_client_id = os.getenv('GOOGLE_CLIENT_ID')


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    id_token = request.data.get('id_token')

    if not id_token:
        return Response({'error': 'No id_token provided'}, status=400)

    user = request.user
    return Response({'message': 'User authenticated successfully'})


def github_login(request):
    client_id = client_id = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
    redirect_uri = 'http://localhost:8000/api/callback'
    scope = 'repo'  

    github_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
    return redirect(github_url)



@api_view(['GET'])
@permission_classes([AllowAny])
def github_callback(request):
    code = request.GET.get('code')

    if not code:
        return Response({'error': 'No code provided'}, status=400)


    token_url = 'https://github.com/login/oauth/access_token'
    client_id = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
    client_secret = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
    redirect_uri = 'http://localhost:8000/api/callback'

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }

    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch access token from GitHub'}, status=500)

    access_token = response.json().get('access_token')

    if not access_token:
        return Response({'error': 'No access token returned'}, status=500)

    user_data_url = 'https://api.github.com/user'
    user_response = requests.get(user_data_url, headers={'Authorization': f'Bearer {access_token}'})

    if user_response.status_code != 200:
        return Response({'error': 'Failed to fetch user data from GitHub'}, status=500)

    user_data = user_response.json()

    name = user_data.get('name')
    username = user_data.get('login')
    id = user_data.get('id')

    
    user, created = User.objects.get_or_create(username=username, defaults={'name': name, 'id': id})

    github_account, _ = GitHubAccount.objects.get_or_create(
        user=user,
        defaults={
            'access_token': access_token,
            'github_username': username,
            'repositories': user_data.get('repos_url')
        }
    )

    token, _ = Token.objects.get_or_create(user=user) 

    redirect_url = f'http://localhost:5173/dashboard?token={access_token}'  
    return redirect(redirect_url, user.is_authenticated)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @psa()
def get_github_repositories(request):
    """Get the list of GitHub repositories for the authenticated user."""
    user = request.user

    github_info = GitHubAccount.objects.all()
    repos = github_info[0].repositories
    print(repos)
    return Response({'repositories': repos})

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_repository(request):
    """Save a repository selected by the authenticated user."""
    user = request.user

    repo_name = request.data.get('repoName')
    repo_url = request.data.get('repoUrl')

    if not repo_name or not repo_url:
        return Response({'error': 'Repository name or URL not provided'}, status=400)

    github_info = GitHubAccount.objects.all()
    selected_repository, created = SelectedRepository.objects.get_or_create(
        github_account=github_info[0],
        repo_name=repo_name,
        defaults={'repo_url': repo_url}
    )

    if created:
        message = 'Repository selected and saved successfully.'
    else:
        message = 'Repository already exists in database.'

    return Response({'message': message})





