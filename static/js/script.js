// Global variables
let map;
let markers = [];
let currentDestinations = [];

// Smooth scroll to personality section
function scrollToPersonality() {
    document.getElementById('personality').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// Get current geolocation
function getCurrentLocation() {
    if (navigator.geolocation) {
        const loading = document.getElementById('loading');
        loading.style.display = 'flex';
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                document.getElementById('latitude').value = position.coords.latitude.toFixed(4);
                document.getElementById('longitude').value = position.coords.longitude.toFixed(4);
                loading.style.display = 'none';
                showNotification('Location obtained successfully!', 'success');
            },
            (error) => {
                loading.style.display = 'none';
                showNotification('Unable to get location. Using default.', 'error');
                console.error('Geolocation error:', error);
            }
        );
    } else {
        showNotification('Geolocation is not supported by your browser.', 'error');
    }
}

// Get personality-based recommendations
async function getRecommendations() {
    const loading = document.getElementById('loading');
    loading.style.display = 'flex';
    
    // Gather personality data
    const crowd = document.querySelector('input[name="crowd"]:checked').value;
    const activity = document.querySelector('input[name="activity"]:checked').value;
    const distance = document.querySelector('input[name="distance"]:checked').value;
    const nature = document.getElementById('nature').checked;
    const culture = document.getElementById('culture').checked;
    const budget = document.getElementById('budget').checked;
    const lat = parseFloat(document.getElementById('latitude').value);
    const lon = parseFloat(document.getElementById('longitude').value);
    
    try {
        const response = await fetch(`/api/personality-recommendations/?crowd=${crowd}&activity=${activity}&distance=${distance}&nature=${nature}&culture=${culture}&budget=${budget}&lat=${lat}&lon=${lon}`);
        const data = await response.json();
        
        if (data.success) {
            currentDestinations = data.recommendations;
            displayResults(data.recommendations, data.profile);
            
            // Scroll to results
            setTimeout(() => {
                document.getElementById('results').scrollIntoView({ 
                    behavior: 'smooth' 
                });
            }, 300);
        } else {
            showNotification('Error getting recommendations: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to get recommendations. Please try again.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display results
function displayResults(destinations, profile) {
    const resultsSection = document.getElementById('results');
    const resultsGrid = document.getElementById('resultsGrid');
    const personalitySummary = document.getElementById('personality-summary');
    
    // Show personality summary
    personalitySummary.innerHTML = `
        <div class="personality-badge">👥 ${formatPreference(profile.crowd)}</div>
        <div class="personality-badge">⚡ ${formatPreference(profile.activity)}</div>
        <div class="personality-badge">📍 ${formatPreference(profile.distance)}</div>
        ${profile.nature ? '<div class="personality-badge">🌿 Nature Lover</div>' : ''}
        ${profile.culture ? '<div class="personality-badge">🏛️ Culture Enthusiast</div>' : ''}
        ${profile.budget ? '<div class="personality-badge">💰 Budget Conscious</div>' : ''}
    `;
    
    // Display destination cards
    resultsGrid.innerHTML = '';
    
    if (destinations.length === 0) {
        resultsGrid.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No destinations found. Try adjusting your preferences.</p>';
        resultsSection.style.display = 'block';
        return;
    }
    
    destinations.forEach(dest => {
        const card = createDestinationCard(dest);
        resultsGrid.appendChild(card);
    });
    
    resultsSection.style.display = 'block';
    
    // Initialize map
    initializeMap(destinations);
}

// Format preference text
function formatPreference(value) {
    const map = {
        'quiet': 'Quiet & Peaceful',
        'moderate': 'Moderate',
        'lively': 'Lively & Bustling',
        'relaxed': 'Relaxed & Chill',
        'balanced': 'Balanced',
        'adventurous': 'Adventurous',
        'nearby': 'Nearby',
        'far': 'Far Away'
    };
    return map[value] || value;
}

// Create destination card
function createDestinationCard(dest) {
    const card = document.createElement('div');
    card.className = 'destination-card';
    card.style.animation = 'fadeInUp 0.6s ease-out';
    
    const category = formatCategory(dest.kinds);
    const scoreColor = getScoreColor(dest.score);
    const distanceKm = (dest.distance / 1000).toFixed(1);
    
    card.innerHTML = `
        <div class="destination-header">
            <h3 class="destination-name">${dest.name}</h3>
            <p class="destination-category">${category}</p>
        </div>
        <div class="destination-body">
            <span class="score-badge" style="background: ${scoreColor};">
                Match Score: ${Math.round(dest.score)}%
            </span>
            <p class="destination-distance">📍 ${distanceKm} km away</p>
            <div class="destination-actions">
                <button class="btn-view" onclick="viewDestinationDetails('${dest.xid}')">
                    View Details
                </button>
                <button class="btn-save" onclick="saveTrip('${dest.xid}', '${dest.name.replace(/'/g, "\\'")}', ${dest.lat}, ${dest.lon}, '${category}')">
                    ❤️ Save
                </button>
            </div>
        </div>
    `;
    
    return card;
}

// Format category from kinds
function formatCategory(kinds) {
    if (!kinds) return 'Attraction';
    
    const kindsList = kinds.split(',');
    const categoryMap = {
        'natural': '🌿 Natural',
        'cultural': '🏛️ Cultural',
        'religion': '⛪ Religious',
        'architecture': '🏛️ Architecture',
        'historic': '📜 Historic',
        'museums': '🖼️ Museum',
        'sport': '⚽ Sports',
        'tourist_facilities': '🏨 Tourist Facility',
        'interesting_places': '⭐ Interesting Place',
        'other': '📍 Attraction'
    };
    
    for (const [key, value] of Object.entries(categoryMap)) {
        if (kindsList.some(k => k.includes(key))) {
            return value;
        }
    }
    
    return '📍 Attraction';
}

// Get color based on score
function getScoreColor(score) {
    if (score >= 80) return 'linear-gradient(135deg, #2ecc71, #27ae60)';
    if (score >= 60) return 'linear-gradient(135deg, #f39c12, #d68910)';
    return 'linear-gradient(135deg, #95a5a6, #7f8c8d)';
}

// View destination details
async function viewDestinationDetails(xid) {
    const loading = document.getElementById('loading');
    loading.style.display = 'flex';
    
    try {
        const response = await fetch(`/api/destination-details/${xid}/`);
        const data = await response.json();
        
        if (data.success) {
            displayDestinationModal(data.destination, data.weather);
        } else {
            showNotification('Error loading details: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load destination details.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display destination modal
function displayDestinationModal(destination, weather) {
    const modal = document.getElementById('detailModal');
    const modalContent = document.getElementById('modalContent');
    
    let weatherHTML = '';
    if (weather) {
        weatherHTML = `
            <div class="weather-section" style="background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                <h3 style="margin-bottom: 1rem;">☀️ Current Weather</h3>
                <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <p style="font-size: 2rem; margin: 0;">${Math.round(weather.main.temp)}°C</p>
                        <p style="margin: 0; opacity: 0.9;">${weather.weather[0].description}</p>
                    </div>
                    <div>
                        <p>💧 Humidity: ${weather.main.humidity}%</p>
                        <p>🌪️ Wind: ${weather.wind.speed} m/s</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    const imageURL = destination.preview?.source || destination.image || 'https://via.placeholder.com/800x400?text=No+Image+Available';
    
    modalContent.innerHTML = `
        <div style="position: relative;">
            <img src="${imageURL}" alt="${destination.name}" 
                 style="width: 100%; height: 400px; object-fit: cover; border-radius: 20px 20px 0 0;"
                 onerror="this.src='https://via.placeholder.com/800x400?text=No+Image+Available'">
        </div>
        <div style="padding: 2rem;">
            <h2 style="font-family: var(--font-display); font-size: 2.5rem; color: var(--color-primary); margin-bottom: 1rem;">
                ${destination.name}
            </h2>
            
            ${destination.wikipedia_extracts?.text ? `
                <div style="margin-bottom: 1.5rem;">
                    <h3 style="color: var(--color-secondary); margin-bottom: 0.5rem;">About</h3>
                    <p style="line-height: 1.8;">${destination.wikipedia_extracts.text.substring(0, 500)}...</p>
                </div>
            ` : ''}
            
            ${destination.address?.city || destination.address?.state ? `
                <p style="color: var(--color-secondary); margin-bottom: 1rem;">
                    📍 ${destination.address.city || ''} ${destination.address.state || ''}
                </p>
            ` : ''}
            
            ${destination.kinds ? `
                <p style="margin-bottom: 1rem;">
                    <strong>Categories:</strong> ${destination.kinds.replace(/_/g, ' ').split(',').slice(0, 5).join(', ')}
                </p>
            ` : ''}
            
            ${weatherHTML}
            
            ${destination.wikipedia ? `
                <div style="margin-top: 1.5rem;">
                    <a href="${destination.wikipedia}" target="_blank" 
                       style="display: inline-block; background: var(--color-accent); color: var(--color-dark); 
                              padding: 1rem 2rem; border-radius: 10px; text-decoration: none; font-weight: 600;">
                        📖 Read More on Wikipedia
                    </a>
                </div>
            ` : ''}
        </div>
    `;
    
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('detailModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('detailModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Save trip
async function saveTrip(xid, name, lat, lon, category) {
    try {
        const response = await fetch('/save-trip/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                xid: xid,
                name: name,
                lat: lat,
                lon: lon,
                kinds: category
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Trip saved successfully! ❤️', 'success');
        } else {
            showNotification('Error saving trip: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to save trip.', 'error');
    }
}

// Show my trips
async function showMyTrips() {
    const loading = document.getElementById('loading');
    loading.style.display = 'flex';
    
    try {
        const response = await fetch('/my-trips/');
        const data = await response.json();
        
        if (data.success) {
            displayMyTrips(data.trips);
        } else {
            showNotification('Error loading trips: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load trips.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display my trips
function displayMyTrips(trips) {
    const section = document.getElementById('myTripsSection');
    const tripsList = document.getElementById('tripsList');
    
    if (trips.length === 0) {
        tripsList.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; color: white; padding: 4rem;">
                <p style="font-size: 1.5rem; margin-bottom: 1rem;">No saved trips yet!</p>
                <p style="opacity: 0.8;">Start exploring and save your favorite destinations.</p>
            </div>
        `;
    } else {
        tripsList.innerHTML = '';
        
        trips.forEach(trip => {
            const tripCard = document.createElement('div');
            tripCard.className = 'destination-card';
            tripCard.style.animation = 'fadeInUp 0.5s ease-out';
            
            tripCard.innerHTML = `
                <div class="destination-header">
                    <h3 class="destination-name">${trip.name}</h3>
                    <p class="destination-category">${trip.category}</p>
                </div>
                <div class="destination-body">
                    <p style="color: var(--color-secondary); margin-bottom: 0.5rem;">
                        Saved on ${trip.created_at}
                    </p>
                    ${trip.notes ? `<p style="font-style: italic; margin-top: 1rem;">${trip.notes}</p>` : ''}
                    <button class="btn-view" style="margin-top: 1rem; width: 100%;" 
                            onclick="window.open('https://www.google.com/maps?q=${trip.lat},${trip.lon}', '_blank')">
                        📍 View on Map
                    </button>
                </div>
            `;
            
            tripsList.appendChild(tripCard);
        });
    }
    
    section.style.display = 'block';
}

// Close my trips
function closeMyTrips() {
    document.getElementById('myTripsSection').style.display = 'none';
}

// Initialize map
function initializeMap(destinations) {
    const mapSection = document.getElementById('map-section');
    mapSection.style.display = 'block';
    
    // Clear existing map
    if (map) {
        map.remove();
    }
    
    // Get center coordinates
    const centerLat = parseFloat(document.getElementById('latitude').value);
    const centerLon = parseFloat(document.getElementById('longitude').value);
    
    // Create map
    map = L.map('map').setView([centerLat, centerLon], 10);
    
    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
    }).addTo(map);
    
    // Add user location marker
    L.marker([centerLat, centerLon], {
        icon: L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41]
        })
    }).addTo(map).bindPopup('<b>Your Location</b>');
    
    // Add destination markers
    destinations.forEach(dest => {
        const marker = L.marker([dest.lat, dest.lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41]
            })
        }).addTo(map);
        
        marker.bindPopup(`
            <div style="font-family: var(--font-body);">
                <h4 style="margin: 0 0 0.5rem 0;">${dest.name}</h4>
                <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem;">Match: ${Math.round(dest.score)}%</p>
                <button onclick="viewDestinationDetails('${dest.xid}')" 
                        style="background: var(--color-accent); border: none; padding: 0.5rem 1rem; 
                               border-radius: 5px; cursor: pointer; font-weight: 600;">
                    View Details
                </button>
            </div>
        `);
        
        markers.push(marker);
    });
    
    // Fit bounds to show all markers
    if (destinations.length > 0) {
        const bounds = L.latLngBounds(destinations.map(d => [d.lat, d.lon]));
        map.fitBounds(bounds, { padding: [50, 50] });
    }
    
    // Scroll to map
    setTimeout(() => {
        mapSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 500);
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10001;
        font-family: var(--font-body);
        font-weight: 600;
        animation: slideInRight 0.4s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.4s ease-out';
        setTimeout(() => notification.remove(), 400);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('WanderSoul Trip Planner initialized!');
});
