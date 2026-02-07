"""
Django models for the trip planner.
"""
from django.db import models
from django.contrib.auth.models import User

class PersonalityProfile(models.Model):
    """Stores user personality preferences for travel."""
    CROWD_CHOICES = [
        ('quiet', 'Quiet & Peaceful'),
        ('moderate', 'Moderate'),
        ('lively', 'Lively & Crowded'),
    ]
    
    ACTIVITY_CHOICES = [
        ('relaxed', 'Relaxed & Chill'),
        ('balanced', 'Balanced'),
        ('adventurous', 'Adventurous & Active'),
    ]
    
    DISTANCE_CHOICES = [
        ('nearby', 'Nearby (0-50 km)'),
        ('moderate', 'Moderate (50-200 km)'),
        ('far', 'Far Away (200+ km)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    crowd_preference = models.CharField(max_length=20, choices=CROWD_CHOICES, default='moderate')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='balanced')
    distance_preference = models.CharField(max_length=20, choices=DISTANCE_CHOICES, default='moderate')
    budget_conscious = models.BooleanField(default=False)
    nature_lover = models.BooleanField(default=True)
    culture_enthusiast = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.crowd_preference}-{self.activity_level}-{self.distance_preference}"


class Trip(models.Model):
    """Stores saved trips."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    destination_name = models.CharField(max_length=255)
    destination_id = models.CharField(max_length=100)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(null=True, blank=True)
    trip_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.destination_name} - {self.trip_date}"


class Favorite(models.Model):
    """Stores favorite destinations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    destination_name = models.CharField(max_length=255)
    destination_id = models.CharField(max_length=100)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['session_key', 'destination_id']
    
    def __str__(self):
        return self.destination_name
