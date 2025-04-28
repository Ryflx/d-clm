from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import requests
import json
from docgen.models import DocGenConfiguration, DocLauncherTask
from users.models import DocusignCredentials
from users.views import refresh_token

@login_required
def docgen_form(request):
    """DocGen form view for creating documents using DocGen configurations"""
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
    
    # Get DocGen configurations
    configurations = None
    result = None
    result_json = None
    
    if request.method == 'GET':
        # Fetch configurations
        configurations = get_docgen_configurations(credentials)
    
    elif request.method == 'POST':
        # Create DocLauncher task
        config_href = request.POST.get('configuration')
        xml_data = request.POST.get('xml_data')
        
        if not config_href or not xml_data:
            messages.error(request, 'Please select a configuration and provide XML data.')
        else:
            result = create_doc_launcher_task(credentials, config_href, xml_data)
            if result:
                result_json = json.dumps(result, indent=2)
                
                # Save task to database
                config = DocGenConfiguration.objects.filter(href=config_href).first()
                if not config:
                    # Create configuration if it doesn't exist
                    config = DocGenConfiguration.objects.create(
                        name=result.get('Name', 'Unknown Configuration'),
                        href=config_href,
                        account_id=credentials.account_id
                    )
                
                # Create task record
                DocLauncherTask.objects.create(
                    user=request.user,
                    configuration=config,
                    data=xml_data,
                    result_url=result.get('DocLauncherResultUrl'),
                    status=result.get('Status')
                )
                
                messages.success(request, 'DocLauncher task created successfully!')
            else:
                messages.error(request, 'Failed to create DocLauncher task.')
        
        # Fetch configurations again for the form
        configurations = get_docgen_configurations(credentials)
    
    return render(request, 'docgen/docgen_form.html', {
        'configurations': configurations,
        'result': result,
        'result_json': result_json
    })

def get_docgen_configurations(credentials, max_retries=3):
    """Get list of docgen configurations with pagination support"""
    try:
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'Content-Type': 'application/json'
        }

        all_items = []
        next_url = f"https://apiuatna11.springcm.com/v2/{credentials.account_id}/doclauncherconfigurations?limit=100"

        while next_url:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    response = requests.get(next_url, headers=headers)
                    
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
                    
                    if 'Items' in response_data:
                        all_items.extend(response_data['Items'])
                    
                    # Check if there are more pages
                    next_url = response_data.get('Next')
                    
                    break  # Success, exit retry loop
                    
                except requests.exceptions.RequestException:
                    retry_count += 1
                    if retry_count < max_retries:
                        continue
                    else:
                        return None

        # Create final response with all items
        return all_items

    except Exception:
        return None

def create_doc_launcher_task(credentials, config_href, xml_payload, max_retries=3):
    """Create a DocLauncher task using CLM API"""
    try:
        # Prepare the request data
        data = {
            "Data": xml_payload,
            "DataType": "XML",
            "DocLauncherConfiguration": {
                "Href": config_href
            }
        }

        # Prepare headers
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'Content-Type': 'application/json'
        }

        # Make the API call
        endpoint = f"https://apiuatna11.springcm.com/v2/{credentials.account_id}/doclaunchertasks"
        
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=data
                )
                
                # Check if we got a 500 error
                if response.status_code == 500:
                    retry_count += 1
                    if retry_count < max_retries:
                        continue
                    else:
                        return None
                
                try:
                    response_data = response.json()
                    if response.status_code not in [200, 202]:
                        return None
                except ValueError:
                    return None
                
                break  # Success, exit retry loop
                
            except requests.exceptions.RequestException:
                retry_count += 1
                if retry_count < max_retries:
                    continue
                else:
                    return None
            
        response.raise_for_status()
        
        # Add redirect URL for DocLauncher
        if "DocLauncherResultUrl" in response_data:
            try:
                result_url = response_data['DocLauncherResultUrl']
                headers = {
                    'Authorization': f"Bearer {credentials.access_token}",
                    'Accept': 'text/html'
                }
                redirect_response = requests.get(result_url, headers=headers, allow_redirects=True)
                if redirect_response.status_code == 200:
                    response_data['redirect_url'] = redirect_response.url
            except Exception:
                pass
        
        return response_data

    except Exception:
        return None
