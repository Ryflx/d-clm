from django.db import models
from django.contrib.auth.models import User

class DocumentAttribute(models.Model):
    """Model to store document attribute information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_attributes')
    document_id = models.CharField(max_length=255)
    attribute_data = models.JSONField()  # Store the full attribute response as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Document {self.document_id} attributes"
        
    class Meta:
        ordering = ['-created_at']
