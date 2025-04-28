from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class DocusignCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='docusign_credentials')
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True) # Consider encryption for production
    account_id = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    is_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_token_valid(self):
        if not self.access_token or not self.token_expiry:
            return False
        # Check if token expires in the next 5 minutes
        return timezone.now() < (self.token_expiry - datetime.timedelta(minutes=5))

    def __str__(self):
        return f"DocuSign Credentials for {self.user.username}"

