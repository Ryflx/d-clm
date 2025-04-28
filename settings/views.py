from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings.models import AppSettings

@login_required
def app_settings(request):
    """Application settings view for customization"""
    # Get or create app settings
    settings = AppSettings.load()
    
    if request.method == 'POST':
        # Update logo if provided
        if 'logo' in request.FILES:
            settings.logo = request.FILES['logo']
        
        # Update sourcing login title
        settings.sourcing_login_title = request.POST.get('sourcing_login_title', 'Sourcing System Login')
        
        # Save settings
        settings.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings:app_settings')
    
    return render(request, 'settings/app_settings.html', {
        'settings': settings
    })
