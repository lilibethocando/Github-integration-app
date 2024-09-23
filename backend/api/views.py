import os
import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model



User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    id_token = request.data.get('id_token')

    if not id_token:
        return Response({'error': 'id_token is required'}, status=status.HTTP_400_BAD_REQUEST)

    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
    if response.status_code != 200:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    user_data = response.json()
    

    email = user_data.get('email')
    name = user_data.get('name')
    google_user_id = user_data.get('sub') 

    if not email:
        return Response({'error': 'Email is required from Google'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(email=email, defaults={'username': name})

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def github_oauth(request):
    print("starting github oauth")
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)

    client_id = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
    client_secret = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
    redirect_uri = "http://localhost:5173/callback"
    django_client_id = os.getenv('DJANGO_CLIENT_ID')
    django_client_secret = os.getenv('DJANGO_CLIENT_SECRET')

    # Step 1: Exchange GitHub code by 'access_token'
    github_token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    github_response = requests.post(github_token_url, headers=headers, data=data)
    github_token_data = github_response.json()

    if 'access_token' not in github_token_data:
        return Response({'error': 'Failed to obtain GitHub token'}, status=status.HTTP_400_BAD_REQUEST)

    github_access_token = github_token_data['access_token']
    
    # Step 2: Convert GitHub token to a Django token
    convert_token_url = "http://127.0.0.1:8000/auth/convert-token"
    convert_token_data = {
        "grant_type": "convert_token",
        "client_id": django_client_id,  
        "client_secret": django_client_secret, 
        "backend": "github",
        "token": github_access_token
    }

    convert_token_response = requests.post(convert_token_url, data=convert_token_data)
    django_token_data = convert_token_response.json()

    if 'access_token' in django_token_data:
        return Response(django_token_data, status=status.HTTP_200_OK)
    else:
        return Response(django_token_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def store_github_user(request):
    """Guarda las credenciales de GitHub del usuario autenticado en la base de datos."""
    print("starting store github user")
    print("Request headers:", request.headers)
    print("User authenticated:", request.user.is_authenticated)
    access_token = request.data.get('access_token')
    github_username = request.data.get('github_username')

    if not access_token or not github_username:
        return Response({'error': 'Missing access token or GitHub username'}, status=400)

    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    user.github_token = access_token
    user.github_username = github_username
    user.save()

    return Response({
        'message': 'GitHub account linked successfully',
        'github_username': github_username
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_github_repositories(request):
    user = request.user
    if not user.github_token:
        return Response({'error': 'GitHub account not linked'}, status=400)

    headers = {
        'Authorization': f'Bearer {user.github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get('https://api.github.com/user/repos', headers=headers)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch repositories'}, status=response.status_code)

    repos = response.json()
    return Response(repos)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_repository(request):
    user = request.user
    if not user.github_token:
        return Response({'error': 'GitHub account not linked'}, status=400)

    repo_name = request.data.get('repoName')
    if not repo_name:
        return Response({'error': 'No repository name provided'}, status=400)

    user.selected_repository = repo_name
    user.save()

    return Response({'message': 'Repository selected successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_github_link(request):
    user = request.user
    return Response({'isLinked': bool(user.github_token)})
