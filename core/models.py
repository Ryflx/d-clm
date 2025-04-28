from django.db import models

class Feature(models.Model):
    """Model to store feature information for the catalog"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    feature_id = models.CharField(max_length=50, unique=True)
    image_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['order']
