from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Feature

@login_required
def home(request):
    """Home view displaying the feature catalog"""
    features = Feature.objects.all()
    
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
    
    return render(request, 'core/home.html', {'features': feature_data})
