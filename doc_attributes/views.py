from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import json
from doc_attributes.models import DocumentAttribute
from users.models import DocusignCredentials
from users.views import refresh_token

@login_required
def document_attributes(request):
    """Document attributes view for retrieving and viewing document attributes"""
    # Check if user has DocuSign credentials
    try:
        credentials = DocusignCredentials.objects.get(user=request.user)
        if not credentials.is_configured:
            messages.error(request, 'Please configure your DocuSign settings first.')
            return redirect('users:docusign_settings')
        
        # Check if token is valid, refresh if needed
        if not credentials.is_token_valid():
            if not refresh_token(credentials):
                messages.error(request, 'Your DocuSign authentication has expired. Please re-authenticate.')
                return redirect('users:docusign_settings')
    except DocusignCredentials.DoesNotExist:
        messages.error(request, 'Please configure your DocuSign settings first.')
        return redirect('users:docusign_settings')
    
    document_attributes = None
    document_attributes_json = None
    
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        
        if not document_id:
            messages.error(request, 'Please enter a Document ID.')
        else:
            # Get document attributes
            document_attributes = get_document_attributes(credentials, document_id)
            
            if document_attributes:
                # Save to database
                DocumentAttribute.objects.create(
                    user=request.user,
                    document_id=document_id,
                    attribute_data=document_attributes
                )
                
                document_attributes_json = json.dumps(document_attributes, indent=2)
                messages.success(request, 'Document attributes retrieved successfully!')
            else:
                messages.error(request, 'Failed to retrieve document attributes.')
    
    return render(request, 'doc_attributes/document_attributes.html', {
        'document_attributes': document_attributes,
        'document_attributes_json': document_attributes_json
    })

def get_document_attributes(credentials, doc_id, max_retries=3):
    """Get document attributes using CLM API"""
    try:
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'Content-Type': 'application/json'
        }
        
        endpoint = f"https://apiuatna11.springcm.com/v2/{credentials.account_id}/documents/{doc_id}?expand=AttributeGroups"
        
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(endpoint, headers=headers)
                
                # Check if we got a 500 error
                if response.status_code == 500:
                    retry_count += 1
                    if retry_count < max_retries:
                        continue
                    else:
                        return None
                
                # For other errors
                if response.status_code != 200:
                    return None
                
                response_data = response.json()
                return response_data
                
            except requests.exceptions.RequestException:
                retry_count += 1
                if retry_count < max_retries:
                    continue
                else:
                    return None

    except Exception:
        return None
