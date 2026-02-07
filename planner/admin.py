"""
Admin configuration for the trip planner.
"""
from django.contrib import admin
from .models import PersonalityProfile, Trip, Favorite


@admin.register(PersonalityProfile)
class PersonalityProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'crowd_preference', 'activity_level', 'distance_preference', 'created_at']
    list_filter = ['crowd_preference', 'activity_level', 'distance_preference', 'nature_lover', 'culture_enthusiast']
    search_fields = ['session_key']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination_name', 'session_key', 'trip_date', 'created_at']
    list_filter = ['trip_date', 'created_at', 'category']
    search_fields = ['destination_name', 'session_key', 'destination_id']
    readonly_fields = ['created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination_name', 'session_key', 'created_at']
    list_filter = ['created_at']
    search_fields = ['destination_name', 'session_key', 'destination_id']
    readonly_fields = ['created_at']
