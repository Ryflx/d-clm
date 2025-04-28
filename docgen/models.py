from django.db import models
from django.contrib.auth.models import User

class DocGenConfiguration(models.Model):
    """Model to store DocGen configuration information"""
    name = models.CharField(max_length=255)
    href = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)
    account_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class DocLauncherTask(models.Model):
    """Model to store DocLauncher task information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doc_launcher_tasks')
    configuration = models.ForeignKey(DocGenConfiguration, on_delete=models.CASCADE, related_name='tasks')
    data = models.TextField()  # XML payload
    result_url = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Task for {self.configuration.name} by {self.user.username}"
