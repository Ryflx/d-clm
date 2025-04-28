from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sourcing.models import SourcingLogin
from settings.models import AppSettings

@login_required
def sourcing_login(request):
    """Sourcing login view for supplier onboarding"""
    # Get app settings for sourcing title
    app_settings = AppSettings.load()
    sourcing_title = app_settings.sourcing_login_title
    
    success = False
    
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')
        supplier_email = request.POST.get('supplier_email')
        supplier_phone = request.POST.get('supplier_phone')
        
        if not supplier_name or not supplier_email:
            messages.error(request, 'Please provide supplier name and email.')
        else:
            # Create sourcing login record
            SourcingLogin.objects.create(
                user=request.user,
                supplier_name=supplier_name,
                supplier_email=supplier_email,
                supplier_phone=supplier_phone
            )
            
            success = True
            messages.success(request, 'Supplier onboarding request submitted successfully!')
    
    return render(request, 'sourcing/sourcing_login.html', {
        'sourcing_title': sourcing_title,
        'success': success
    })
