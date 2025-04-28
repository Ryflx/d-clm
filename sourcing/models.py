from django.db import models
from django.contrib.auth.models import User

class SourcingLogin(models.Model):
    """Model to store sourcing login information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sourcing_logins')
    supplier_name = models.CharField(max_length=255)
    supplier_email = models.EmailField()
    supplier_phone = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')  # pending, active, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sourcing login for {self.supplier_name}"
        
    class Meta:
        ordering = ['-created_at']
