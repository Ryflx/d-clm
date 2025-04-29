from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Feature
from users.models import DocusignCredentials

@login_required
def home(request):
    """Home view displaying the feature catalog"""
    features = Feature.objects.all()
    
    # Check DocuSign authentication status
    docusign_authenticated = False
    try:
        credentials = DocusignCredentials.objects.get(user=request.user)
        # Consider a feature active if configured and token is valid (or just configured for simplicity)
        # Let's start by just checking if it's configured.
        # We could add credentials.is_token_valid() check later if needed.
        docusign_authenticated = credentials.is_configured
    except DocusignCredentials.DoesNotExist:
        docusign_authenticated = False # Not configured yet
    
    # Map features to their respective URLs and image paths
    feature_data = []
    for feature in features:
        # Determine URL name based on feature_id
        url_name = ''
        if feature.feature_id == 'docgen':
            url_name = 'docgen:docgen_form'
        elif feature.feature_id == 'document_attributes':
            url_name = 'doc_attributes:document_attributes'
        elif feature.feature_id == 'sourcing_login':
            url_name = 'sourcing:sourcing_login'
        elif feature.feature_id == 'settings':
            url_name = 'settings:app_settings'
        
        # Construct image URL
        image_url = f"https://raw.githubusercontent.com/Ryflx/CLM-API-Examples/main/src/image/{feature.image_name}"
        
        feature_data.append({
            'title': feature.title,
            'description': feature.description,
            'is_active': feature.is_active,
            'url_name': url_name,
            'image_url': image_url
        })
    
    return render(request, 'core/home.html', {
        'features': feature_data,
        'docusign_authenticated': docusign_authenticated
    })
