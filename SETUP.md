# WanderSoul Trip Planner - Quick Setup Guide

## Step-by-Step Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your Free OpenWeatherMap API Key
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key
5. Open `trip_planner/settings.py`
6. Replace `your_openweather_api_key_here` with your actual key

### 3. Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User (Optional)
```bash
python manage.py createsuperuser
# Follow the prompts to create username and password
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Access the Application
Open your web browser and go to:
```
http://localhost:8000
```

## Admin Panel Access
To access the admin panel (after creating superuser):
```
http://localhost:8000/admin
```

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure you're in the virtual environment and all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete db.sqlite3 and run migrations again
```bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: API not returning data
**Solution**: Check your API keys in settings.py and ensure you have internet connection

## File Structure Overview

```
trip_planner/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Full documentation
├── trip_planner/            # Main project folder
│   ├── settings.py         # Configuration & API keys
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
├── planner/                 # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic & API calls
│   ├── urls.py             # App-specific URLs
│   └── admin.py            # Admin panel config
├── templates/               # HTML templates
│   └── planner/
│       └── index.html      # Main page
└── static/                  # Static files
    ├── css/
    │   └── style.css       # All styles
    └── js/
        └── script.js       # All JavaScript
```

## How to Modify

### Change Color Scheme
Edit `static/css/style.css`, find the `:root` section and modify CSS variables:
```css
:root {
    --color-primary: #2c3e50;    /* Main dark color */
    --color-secondary: #8b6f47;  /* Secondary color */
    --color-accent: #d4af37;     /* Accent/highlight color */
    /* ... */
}
```

### Change Default Location
Edit `templates/planner/index.html`, find the latitude/longitude inputs:
```html
<input type="number" id="latitude" placeholder="Latitude" step="0.0001" value="YOUR_LAT">
<input type="number" id="longitude" placeholder="Longitude" step="0.0001" value="YOUR_LON">
```

### Modify Personality Algorithm
Edit `planner/views.py`, find the `score_destination_for_personality` function to adjust scoring logic.

### Add New Personality Traits
1. Add fields to `PersonalityProfile` model in `planner/models.py`
2. Add HTML inputs in `templates/planner/index.html`
3. Update scoring logic in `planner/views.py`
4. Run migrations: `python manage.py makemigrations && python manage.py migrate`

## Next Steps

1. Customize the design to match your brand
2. Add more personality traits
3. Integrate additional APIs (hotels, restaurants, etc.)
4. Implement user authentication
5. Deploy to a production server (Heroku, DigitalOcean, AWS, etc.)

## Need Help?

- Read the full README.md for detailed documentation
- Check Django documentation: https://docs.djangoproject.com/
- Check API documentation:
  - OpenTripMap: https://opentripmap.io/docs
  - OpenWeatherMap: https://openweathermap.org/api
  - Leaflet: https://leafletjs.com/reference.html

Happy coding! 🚀
