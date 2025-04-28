from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import DocusignCredentials
import requests
import json
import datetime
from docusign_esign import ApiClient

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return render(request, 'users/register.html')

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

@login_required
def docusign_settings(request):
    """DocuSign settings view for configuring API credentials"""
    # Get or create DocuSign credentials for the user
    credentials, created = DocusignCredentials.objects.get_or_create(user=request.user)
    
    # Get auth server from environment or use default
    auth_server = settings.DOCUSIGN_AUTH_SERVER if hasattr(settings, 'DOCUSIGN_AUTH_SERVER') else 'account-d.docusign.com'
    
    if request.method == 'POST':
        # Update credentials
        credentials.client_id = request.POST.get('client_id')
        credentials.client_secret = request.POST.get('client_secret')
        credentials.account_id = request.POST.get('account_id')
        credentials.is_configured = True
        credentials.save()
        
        messages.success(request, 'DocuSign settings saved successfully!')
        return redirect('users:docusign_settings')
    
    return render(request, 'users/docusign_settings.html', {
        'credentials': credentials,
        'auth_server': auth_server
    })

@login_required
def docusign_auth(request):
    """Initiate DocuSign OAuth flow"""
    credentials = DocusignCredentials.objects.get(user=request.user)
    
    if not credentials.is_configured:
        messages.error(request, 'Please configure your DocuSign settings first.')
        return redirect('users:docusign_settings')
    
    # Get auth server from environment or use default
    auth_server = settings.DOCUSIGN_AUTH_SERVER if hasattr(settings, 'DOCUSIGN_AUTH_SERVER') else 'account-d.docusign.com'
    
    # Generate consent URL
    redirect_uri = request.build_absolute_uri(reverse('users:docusign_callback'))
    
    consent_url = (
        f"https://{auth_server}/oauth/auth"
        f"?response_type=code"
        f"&scope=signature%20impersonation%20spring_write%20spring_read"
        f"&client_id={credentials.client_id}"
        f"&redirect_uri={redirect_uri}"
    )
    
    return HttpResponseRedirect(consent_url)

@login_required
def docusign_callback(request):
    """Handle DocuSign OAuth callback"""
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'Authorization code not received from DocuSign.')
        return redirect('users:docusign_settings')
    
    credentials = DocusignCredentials.objects.get(user=request.user)
    
    # Get auth server from environment or use default
    auth_server = settings.DOCUSIGN_AUTH_SERVER if hasattr(settings, 'DOCUSIGN_AUTH_SERVER') else 'account-d.docusign.com'
    
    # Exchange code for token
    redirect_uri = request.build_absolute_uri(reverse('users:docusign_callback'))
    
    try:
        url = f"https://{auth_server}/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'redirect_uri': redirect_uri
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Save token data
        credentials.access_token = token_data['access_token']
        credentials.refresh_token = token_data['refresh_token']
        credentials.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=token_data['expires_in'])
        credentials.save()
        
        messages.success(request, 'Successfully authenticated with DocuSign!')
    except Exception as e:
        messages.error(request, f'Authentication failed: {str(e)}')
    
    return redirect('users:docusign_settings')

def refresh_token(credentials):
    """Refresh DocuSign access token"""
    if not credentials.refresh_token:
        return False
    
    # Get auth server from environment or use default
    auth_server = settings.DOCUSIGN_AUTH_SERVER if hasattr(settings, 'DOCUSIGN_AUTH_SERVER') else 'account-d.docusign.com'
    
    try:
        url = f"https://{auth_server}/oauth/token"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': credentials.refresh_token,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Update token data
        credentials.access_token = token_data['access_token']
        credentials.refresh_token = token_data['refresh_token']
        credentials.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=token_data['expires_in'])
        credentials.save()
        
        return True
    except Exception:
        return False
