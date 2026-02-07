# WanderSoul - Personality-Based Travel Planner

A sophisticated travel planning website that recommends destinations based on your personality traits. Built with Django, vanilla JavaScript, and powered by real-time data from free APIs.

## ✨ Features

### 🎯 Personality-Based Recommendations
- **Crowd Preference**: Quiet & peaceful, moderate, or lively & bustling
- **Activity Level**: Relaxed & chill, balanced, or adventurous & active
- **Distance Preference**: Nearby (0-50km), moderate (50-200km), or far away (200km+)
- **Interest Filters**: Nature lover, culture enthusiast, budget-conscious options

### 🗺️ Real-Time Data Integration
- **OpenTripMap API**: Discover thousands of destinations worldwide
- **OpenWeatherMap API**: Get current weather conditions for destinations
- **Leaflet Maps**: Interactive map visualization with custom markers
- **Geolocation**: Automatically detect user's location

### 💫 Advanced Functionality
- Smart destination scoring algorithm (0-100 match score)
- Save favorite trips for later
- Detailed destination information with images and Wikipedia extracts
- Interactive map with all recommended destinations
- Responsive design for mobile and desktop

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys**

Edit `trip_planner/settings.py` and add your API keys:

```python
# OpenTripMap API Key (already included, free tier)
OPENTRIPMAP_API_KEY = '5ae2e3f221c38a28845f05b6c82df5e9ec90c17adf95c91cffd05b66'

# OpenWeatherMap API Key (get free at: https://openweathermap.org/api)
OPENWEATHER_API_KEY = 'your_api_key_here'
```

**Getting Free API Keys:**
- **OpenTripMap**: Already provided, no registration needed for basic usage
- **OpenWeatherMap**: Sign up at https://openweathermap.org/api (Free tier: 1000 calls/day)

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser** (optional, for admin access)
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Open your browser**
Navigate to: `http://localhost:8000`

## 📁 Project Structure

```
trip_planner/
├── trip_planner/           # Main Django project
│   ├── settings.py        # Project settings with API keys
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── planner/               # Main app
│   ├── models.py         # Database models (PersonalityProfile, Trip, Favorite)
│   ├── views.py          # View functions with API logic
│   ├── urls.py           # App URL patterns
│   └── admin.py          # Admin configuration
├── templates/
│   └── planner/
│       └── index.html    # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # All CSS styles
│   └── js/
│       └── script.js     # JavaScript functionality
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Design Philosophy

The website features a **classic, elegant design** with:
- Serif typography (Playfair Display + Lora) for sophistication
- Warm color palette (navy blue, gold accents, cream background)
- Smooth animations and transitions
- Professional card-based layouts
- Interactive map integration
- Responsive design for all devices

## 🔧 Technology Stack

### Backend
- **Django 5.0.1**: Web framework
- **Python 3.x**: Programming language
- **SQLite**: Database (default, can switch to PostgreSQL/MySQL)

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with custom variables and animations
- **Vanilla JavaScript**: No frameworks, pure interactivity
- **Leaflet.js**: Interactive maps

### APIs
- **OpenTripMap**: Destination data
- **OpenWeatherMap**: Weather information
- **Geolocation API**: User location detection

## 🧠 How the Personality Algorithm Works

The recommendation engine scores each destination (0-100) based on:

1. **Distance Scoring** (20 points)
   - Calculates km distance using Haversine formula
   - Matches user's distance preference

2. **Crowd Preference** (15 points)
   - Analyzes destination type keywords
   - Quiet: Favors parks, museums, gardens
   - Lively: Favors markets, stadiums, entertainment

3. **Activity Level** (15 points)
   - Relaxed: Spas, cafes, museums
   - Adventurous: Hiking, sports, adventures

4. **Interest Bonuses** (up to 35 points)
   - Nature lover: +15 for natural attractions
   - Culture enthusiast: +15 for cultural sites
   - Budget conscious: +10 for free attractions

5. **Final Ranking**
   - Sorts all destinations by score
   - Returns top 20 matches

## 📊 Database Models

### PersonalityProfile
Stores user travel preferences:
- Crowd preference (quiet/moderate/lively)
- Activity level (relaxed/balanced/adventurous)
- Distance preference (nearby/moderate/far)
- Interest flags (nature/culture/budget)

### Trip
Saved destinations:
- Destination name and ID
- Location coordinates
- Description and category
- User notes
- Save date

### Favorite
Quick favorites list with destination details

## 🌐 API Endpoints

### Frontend Endpoints
- `/` - Main page
- `/my-trips/` - View saved trips

### API Endpoints
- `/api/destinations/?lat=X&lon=Y&radius=Z` - Get nearby destinations
- `/api/personality-recommendations/?params` - Get personalized recommendations
- `/api/destination-details/<xid>/` - Get detailed destination info
- `/save-trip/` - Save a trip (POST)
- `/my-trips/` - Get user's saved trips (GET)

## 🎯 Usage Guide

### For Users

1. **Start on Hero Section**
   - Click "Start Your Journey"

2. **Complete Personality Quiz**
   - Select your crowd preference
   - Choose activity level
   - Set distance preference
   - Check interests
   - Enter or auto-detect location

3. **Get Recommendations**
   - Click "Get Personalized Recommendations"
   - View match scores and destination cards
   - See results on interactive map

4. **Explore Destinations**
   - Click "View Details" for full information
   - Check current weather
   - Read Wikipedia excerpts
   - Save favorites with ❤️ button

5. **Manage Trips**
   - Click "My Trips" to view saved destinations
   - Access saved locations anytime

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Add your domain to `ALLOWED_HOSTS`
- Use environment variables for API keys
- Enable HTTPS in production

## 🚀 Deployment

For production deployment:

1. Update settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Use a production server (Gunicorn/uWSGI)
4. Set up a reverse proxy (Nginx/Apache)
5. Use a production database (PostgreSQL)

## 🤝 Contributing

This is a personal project template. Feel free to:
- Fork and modify
- Add new features
- Improve the algorithm
- Enhance the UI/UX

## 📝 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- **OpenTripMap** for destination data
- **OpenWeatherMap** for weather API
- **Leaflet** for mapping functionality
- **OpenStreetMap** for map tiles
- **Google Fonts** for typography

## 📧 Support

For issues or questions:
1. Check the console for errors
2. Verify API keys are correct
3. Ensure all dependencies are installed
4. Check that migrations are run

## 🎉 Features to Add (Future)

- User authentication and profiles
- Social sharing of trips
- Trip itinerary builder
- Budget calculator
- Photo galleries
- Reviews and ratings
- Multi-language support
- Mobile app version

---

**Built with ❤️ for travelers who want personalized adventures**

Enjoy exploring the world with WanderSoul! 🌍✈️
