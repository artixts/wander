"""
URL configuration for planner app.
"""
from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/destinations/', views.get_destinations, name='get_destinations'),
    path('api/personality-recommendations/', views.personality_recommendations, name='personality_recommendations'),
    path('api/destination-details/<int:xid>/', views.destination_details, name='destination_details'),
    path('save-trip/', views.save_trip, name='save_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
]
