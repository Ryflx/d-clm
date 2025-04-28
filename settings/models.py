from django.db import models
from django.contrib.auth.models import User

class AppSettings(models.Model):
    # Using a single instance model pattern for global settings.
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    sourcing_login_title = models.CharField(max_length=100, default="Sourcing System Login")
    # Add other global settings here if needed

    # Ensure only one instance exists (Singleton pattern)
    def save(self, *args, **kwargs):
        self.pk = 1 # Force primary key to 1
        super(AppSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass # Prevent deletion

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Application Settings"

