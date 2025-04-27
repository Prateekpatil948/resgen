from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User
import json

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=20)
    linkedin_id = models.URLField(blank=True, null=True)
    summary = models.TextField()
    
    # Additional Information
    skills = models.TextField()
    certifications = models.TextField(blank=True, null=True)
    
    
    # JSON fields
    education = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    projects = models.JSONField(default=list)

    template_choice = models.CharField(max_length=1, default='1')
    
    # New fields for resume scoring
    score = models.FloatField(null=True, blank=True)
    last_analyzed = models.DateTimeField(null=True, blank=True)
    score_metrics = models.JSONField(default=dict, blank=True)  # Stores detailed metrics
    feedback = models.TextField(blank=True, null=True)  # Stores analysis feedback
    ai_suggestions = models.JSONField(default=list, blank=True)  # Stores AI editing suggestions
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def ai_suggestions_for_edit(self):
        """Helper property to ensure consistent return format"""
        if isinstance(self.ai_suggestions, str):
            try:
                return json.loads(self.ai_suggestions)
            except json.JSONDecodeError:
                return []
        return self.ai_suggestions or []