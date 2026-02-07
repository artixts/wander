"""
Django views for trip planner with personality-based recommendations.
"""
import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import PersonalityProfile, Trip, Favorite
from datetime import datetime
import math


def index(request):
    """Render the main page."""
    return render(request, 'planner/index.html')


def get_session_key(request):
    """Get or create session key for anonymous users."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km using Haversine formula."""
    R = 6371  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def score_destination_for_personality(destination, profile, user_lat, user_lon):
    """
    Score a destination based on personality preferences.
    Returns a score from 0-100.
    """
    score = 50  # Base score
    
    # Get destination properties
    kinds = destination.get('kinds', '').lower()
    name = destination.get('name', '').lower()
    
    # Distance scoring
    if user_lat and user_lon:
        dist_lat = destination.get('point', {}).get('lat', user_lat)
        dist_lon = destination.get('point', {}).get('lon', user_lon)
        distance = calculate_distance(user_lat, user_lon, dist_lat, dist_lon)
        
        if profile.distance_preference == 'nearby':
            if distance < 50:
                score += 20
            elif distance < 100:
                score += 10
            else:
                score -= 10
        elif profile.distance_preference == 'moderate':
            if 50 <= distance <= 200:
                score += 20
            elif distance < 50 or distance > 200:
                score += 5
        else:  # far
            if distance > 200:
                score += 20
            elif distance > 100:
                score += 10
            else:
                score -= 5
    
    # Crowd preference scoring
    if profile.crowd_preference == 'quiet':
        if any(word in kinds for word in ['natural', 'park', 'garden', 'beach', 'trail', 'forest']):
            score += 15
        if any(word in kinds for word in ['museum', 'gallery', 'library']):
            score += 10
        if any(word in kinds for word in ['mall', 'stadium', 'festival', 'market']):
            score -= 15
    elif profile.crowd_preference == 'lively':
        if any(word in kinds for word in ['mall', 'market', 'festival', 'stadium', 'entertainment']):
            score += 15
        if any(word in kinds for word in ['restaurant', 'cafe', 'nightlife', 'shopping']):
            score += 10
        if any(word in kinds for word in ['isolated', 'remote', 'wilderness']):
            score -= 10
    
    # Activity level scoring
    if profile.activity_level == 'relaxed':
        if any(word in kinds for word in ['spa', 'beach', 'garden', 'cafe', 'museum', 'gallery']):
            score += 15
        if any(word in kinds for word in ['hiking', 'climbing', 'sport', 'adventure']):
            score -= 10
    elif profile.activity_level == 'adventurous':
        if any(word in kinds for word in ['hiking', 'climbing', 'sport', 'adventure', 'mountain', 'trail']):
            score += 15
        if any(word in kinds for word in ['water_park', 'zoo', 'amusement']):
            score += 10
        if any(word in kinds for word in ['spa', 'lounge']):
            score -= 5
    
    # Nature lover bonus
    if profile.nature_lover:
        if any(word in kinds for word in ['natural', 'park', 'beach', 'forest', 'mountain', 'lake', 'river']):
            score += 15
    
    # Culture enthusiast bonus
    if profile.culture_enthusiast:
        if any(word in kinds for word in ['museum', 'gallery', 'historic', 'cultural', 'architecture', 'monument']):
            score += 15
        if any(word in kinds for word in ['theatre', 'art', 'heritage']):
            score += 10
    
    # Budget conscious
    if profile.budget_conscious:
        if any(word in kinds for word in ['park', 'beach', 'garden', 'historic', 'monument']):
            score += 10
        if any(word in kinds for word in ['luxury', 'resort', 'spa']):
            score -= 10
    
    return min(100, max(0, score))  # Clamp between 0-100


def get_destinations(request):
    """Get destinations from OpenTripMap API."""
    try:
        lat = float(request.GET.get('lat', 10.5276))  # Default: Kochi, Kerala
        lon = float(request.GET.get('lon', 76.2144))
        radius = int(request.GET.get('radius', 10000))  # 10km default
        
        # OpenTripMap API endpoint
        url = f"https://api.opentripmap.com/0.1/en/places/radius"
        params = {
            'radius': radius,
            'lon': lon,
            'lat': lat,
            'apikey': settings.OPENTRIPMAP_API_KEY,
            'rate': 2,  # Get places rated 2 or higher
            'limit': 50
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Filter and format the results
        destinations = []
        for place in data.get('features', []):
            properties = place.get('properties', {})
            if properties.get('name'):  # Only include named places
                destinations.append({
                    'xid': properties.get('xid'),
                    'name': properties.get('name'),
                    'kinds': properties.get('kinds', ''),
                    'lat': place['geometry']['coordinates'][1],
                    'lon': place['geometry']['coordinates'][0],
                    'dist': properties.get('dist', 0)
                })
        
        return JsonResponse({
            'success': True,
            'destinations': destinations,
            'count': len(destinations)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_mock_recommendations():
    """Return mock destination data for testing."""
    return [
        {
            'xid': 'Q1234567',
            'name': 'Periyar Tiger Reserve',
            'kinds': 'natural,park,nature,wildlife',
            'lat': 9.3723,
            'lon': 76.8148,
            'score': 92,
            'distance': 25000
        },
        {
            'xid': 'Q1234568',
            'name': 'Chinese Fishing Nets',
            'kinds': 'historic,cultural,monument,landmark',
            'lat': 9.9673,
            'lon': 76.2411,
            'score': 88,
            'distance': 10000
        },
        {
            'xid': 'Q1234569',
            'name': 'Kumarakom Bird Sanctuary',
            'kinds': 'natural,park,nature,birds',
            'lat': 9.6125,
            'lon': 76.4062,
            'score': 85,
            'distance': 15000
        },
        {
            'xid': 'Q1234570',
            'name': 'Mattancherry Palace',
            'kinds': 'historic,museum,cultural,heritage',
            'lat': 9.9638,
            'lon': 76.2671,
            'score': 82,
            'distance': 8000
        },
        {
            'xid': 'Q1234571',
            'name': 'Athirapally Falls',
            'kinds': 'natural,waterfall,nature,scenic',
            'lat': 10.2342,
            'lon': 76.5605,
            'score': 79,
            'distance': 35000
        },
        {
            'xid': 'Q1234572',
            'name': 'Jew Town',
            'kinds': 'historic,cultural,market,heritage',
            'lat': 9.9638,
            'lon': 76.2671,
            'score': 75,
            'distance': 8500
        },
        {
            'xid': 'Q1234573',
            'name': 'Bolgatty Palace',
            'kinds': 'historic,palace,cultural,heritage',
            'lat': 9.9712,
            'lon': 76.2354,
            'score': 73,
            'distance': 6000
        },
        {
            'xid': 'Q1234574',
            'name': 'Munnar Tea Gardens',
            'kinds': 'natural,agricultural,scenic,nature',
            'lat': 10.0844,
            'lon': 76.7304,
            'score': 70,
            'distance': 60000
        },
    ]


def personality_recommendations(request):
    """Get personalized recommendations based on personality profile."""
    try:
        # Get personality preferences from request
        crowd = request.GET.get('crowd', 'moderate')
        activity = request.GET.get('activity', 'balanced')
        distance = request.GET.get('distance', 'moderate')
        nature = request.GET.get('nature', 'true').lower() == 'true'
        culture = request.GET.get('culture', 'true').lower() == 'true'
        budget = request.GET.get('budget', 'false').lower() == 'true'
        lat = float(request.GET.get('lat', 10.5276))
        lon = float(request.GET.get('lon', 76.2144))
        
        # Create or update personality profile
        session_key = get_session_key(request)
        profile, created = PersonalityProfile.objects.get_or_create(
            session_key=session_key,
            defaults={
                'crowd_preference': crowd,
                'activity_level': activity,
                'distance_preference': distance,
                'nature_lover': nature,
                'culture_enthusiast': culture,
                'budget_conscious': budget
            }
        )
        
        if not created:
            profile.crowd_preference = crowd
            profile.activity_level = activity
            profile.distance_preference = distance
            profile.nature_lover = nature
            profile.culture_enthusiast = culture
            profile.budget_conscious = budget
            profile.save()
        
        # Determine search radius based on distance preference
        radius_map = {
            'nearby': 20000,      # 20km
            'moderate': 100000,   # 100km
            'far': 300000         # 300km
        }
        radius = radius_map.get(distance, 50000)
        
        # Try to get destinations from OpenTripMap
        try:
            url = f"https://api.opentripmap.com/0.1/en/places/radius"
            params = {
                'radius': radius,
                'lon': lon,
                'lat': lat,
                'apikey': settings.OPENTRIPMAP_API_KEY,
                'limit': 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Score and rank destinations
            scored_destinations = []
            for place in data.get('features', []):
                properties = place.get('properties', {})
                if properties.get('name'):
                    destination = {
                        'xid': properties.get('xid'),
                        'name': properties.get('name'),
                        'kinds': properties.get('kinds', ''),
                        'point': {
                            'lat': place['geometry']['coordinates'][1],
                            'lon': place['geometry']['coordinates'][0]
                        },
                        'dist': properties.get('dist', 0)
                    }
                    
                    score = score_destination_for_personality(destination, profile, lat, lon)
                    destination['personality_score'] = score
                    
                    scored_destinations.append(destination)
            
            # Sort by score and get top 20
            scored_destinations.sort(key=lambda x: x['personality_score'], reverse=True)
            top_destinations = scored_destinations[:20]
            
            # Format for response
            recommendations = []
            for dest in top_destinations:
                recommendations.append({
                    'xid': dest['xid'],
                    'name': dest['name'],
                    'kinds': dest['kinds'],
                    'lat': dest['point']['lat'],
                    'lon': dest['point']['lon'],
                    'score': dest['personality_score'],
                    'distance': dest['dist']
                })
            
            if len(recommendations) > 0:
                return JsonResponse({
                    'success': True,
                    'recommendations': recommendations,
                    'profile': {
                        'crowd': crowd,
                        'activity': activity,
                        'distance': distance,
                        'nature': nature,
                        'culture': culture,
                        'budget': budget
                    }
                })
        
        except Exception as api_error:
            print(f"OpenTripMap API error: {str(api_error)}")
            # Fall through to use mock data
        
        # Use mock data as fallback
        mock_destinations = get_mock_recommendations()
        scored_destinations = []
        
        for dest in mock_destinations:
            score = score_destination_for_personality(dest, profile, lat, lon)
            dest['personality_score'] = score
            scored_destinations.append(dest)
        
        scored_destinations.sort(key=lambda x: x['personality_score'], reverse=True)
        
        recommendations = []
        for dest in scored_destinations[:15]:
            recommendations.append({
                'xid': dest['xid'],
                'name': dest['name'],
                'kinds': dest['kinds'],
                'lat': dest['lat'],
                'lon': dest['lon'],
                'score': dest['personality_score'],
                'distance': dest['distance']
            })
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations,
            'profile': {
                'crowd': crowd,
                'activity': activity,
                'distance': distance,
                'nature': nature,
                'culture': culture,
                'budget': budget
            }
        })
        
    except Exception as e:
        import traceback
        print(f"Error in personality_recommendations: {str(e)}")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def destination_details(request, xid):
    """Get detailed information about a destination."""
    try:
        url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
        params = {
            'apikey': settings.OPENTRIPMAP_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Get weather if coordinates available
        weather_data = None
        if 'point' in data:
            try:
                weather_url = "https://api.openweathermap.org/data/2.5/weather"
                weather_params = {
                    'lat': data['point']['lat'],
                    'lon': data['point']['lon'],
                    'appid': settings.OPENWEATHER_API_KEY,
                    'units': 'metric'
                }
                weather_response = requests.get(weather_url, params=weather_params, timeout=5)
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
            except:
                pass  # Weather is optional
        
        return JsonResponse({
            'success': True,
            'destination': data,
            'weather': weather_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
def save_trip(request):
    """Save a trip to favorites."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_key = get_session_key(request)
            
            trip = Trip.objects.create(
                session_key=session_key,
                destination_name=data.get('name'),
                destination_id=data.get('xid'),
                location_lat=data.get('lat'),
                location_lon=data.get('lon'),
                description=data.get('description', ''),
                category=data.get('kinds', ''),
                notes=data.get('notes', '')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Trip saved successfully!',
                'trip_id': trip.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def my_trips(request):
    """Get user's saved trips."""
    session_key = get_session_key(request)
    trips = Trip.objects.filter(session_key=session_key)
    
    trips_data = []
    for trip in trips:
        trips_data.append({
            'id': trip.id,
            'name': trip.destination_name,
            'lat': trip.location_lat,
            'lon': trip.location_lon,
            'description': trip.description,
            'category': trip.category,
            'notes': trip.notes,
            'created_at': trip.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'success': True,
        'trips': trips_data
    })
