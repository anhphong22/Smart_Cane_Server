/**
 * Smart Cane GPS Tracker - Frontend Application with Auth & Smart Features
 * Modern JavaScript with ES6+ features
 */

// Application State
const AppState = {
    map: null,
    marker: null,
    deviceId: 'SmartCane01',
    initialPosition: [10.7769, 106.7009],
    autoRefreshInterval: null,
    refreshRate: 30000, // 30 seconds
    activityLog: [],
    maxLogEntries: 20,
    auth: {
        token: localStorage.getItem('access_token'),
        user: JSON.parse(localStorage.getItem('user') || 'null')
    },
    geofences: [],
    routeHistory: [],
    routePlaybackInterval: null
};

// DOM Elements Cache
const DOM = {
    statusIndicator: document.getElementById('status-indicator'),
    statusText: document.getElementById('status-text'),
    syncStatus: document.getElementById('sync-status'),
    syncAnimation: document.getElementById('sync-animation'),
    progressBar: document.getElementById('data-progress-bar'),
    latValue: document.getElementById('latitude-value'),
    lonValue: document.getElementById('longitude-value'),
    timeValue: document.getElementById('time-value'),
    trackButton: document.getElementById('track-button'),
    activityLog: document.getElementById('activity-log'),
    userDisplay: document.getElementById('user-display'),
    logoutBtn: document.getElementById('logout-btn')
};

/**
 * Check authentication
 */
function checkAuth() {
    if (!AppState.auth.token) {
        window.location.href = '/login';
        return false;
    }
    
    // Display user info
    if (DOM.userDisplay && AppState.auth.user) {
        DOM.userDisplay.textContent = AppState.auth.user.username || 'User';
    }
    
    return true;
}

/**
 * Make authenticated API request
 */
async function authFetch(url, options = {}) {
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${AppState.auth.token}`
    };
    
    const response = await fetch(url, { ...options, headers });
    
    if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        throw new Error('Unauthorized');
    }
    
    return response;
}

/**
 * Logout function
 */
async function logout() {
    try {
        await authFetch('/auth/logout', { method: 'POST' });
    } catch (error) {
        console.log('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    }
}

/**
 * Initialize the application
 */
function initApp() {
    if (!checkAuth()) return;
    
    initMap();
    startAutoRefresh();
    setupTheme();
    loadGeofences();
    logActivity('Application initialized', 'info');
    console.log('?? Smart Cane GPS Tracker initialized');
}

/**
 * Initialize Leaflet map
 */
function initMap() {
    try {
        // Create map instance
        AppState.map = L.map('map', {
            center: AppState.initialPosition,
            zoom: 13,
            zoomControl: false
        });

        // Add tile layers
        const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        });

        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: '&copy; Esri',
            maxZoom: 19
        });

        // Layer control
        const baseMaps = {
            "Street Map": osmLayer,
            "Satellite": satelliteLayer
        };

        L.control.layers(baseMaps).addTo(AppState.map);
        osmLayer.addTo(AppState.map);

        // Custom zoom control position
        L.control.zoom({ position: 'bottomright' }).addTo(AppState.map);

        // Initial marker
        createInitialMarker();

        // Fetch initial location
        fetchLocationData();

        logActivity('Map initialized successfully', 'success');
    } catch (error) {
        console.error('Error initializing map:', error);
        logActivity(`Map initialization error: ${error.message}`, 'error');
    }
}

/**
 * Create initial marker on map
 */
function createInitialMarker() {
    const initialIcon = L.divIcon({
        html: `<div class="custom-marker initial">??</div>`,
        className: '',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    AppState.marker = L.marker(AppState.initialPosition, { icon: initialIcon })
        .addTo(AppState.map)
        .bindPopup('<div class="popup-content"><strong>Initial Position</strong><br>Waiting for GPS data...</div>');
}

/**
 * Fetch location data from API
 */
async function fetchLocationData(useRealTime = false) {
    updateSyncStatus(true);
    setProgressBar(30);

    try {
        const endpoint = useRealTime
            ? `/api/get_real_gps?deviceId=${AppState.deviceId}`
            : `/api/get_latest_location?deviceId=${AppState.deviceId}`;

        console.log(`?? Fetching data from: ${endpoint}`);
        logActivity(`Fetching GPS data ${useRealTime ? '(real-time)' : ''}...`, 'info');

        const response = await fetch(endpoint, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        });

        setProgressBar(70);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data && typeof data.latitude === 'number' && typeof data.longitude === 'number') {
            updateUI(data, useRealTime);
            setProgressBar(100);
            logActivity(`GPS data updated: ${data.latitude.toFixed(6)}, ${data.longitude.toFixed(6)}`, 'success');
            
            // Check geofences
            checkGeofences(data.latitude, data.longitude);
        } else {
            throw new Error('Invalid data received from server');
        }
    } catch (error) {
        console.error('? Fetch error:', error);
        showErrorUI(error.message);
        logActivity(`Error: ${error.message}`, 'error');
    } finally {
        updateSyncStatus(false);
    }
}

/**
 * Update UI with location data
 */
function updateUI(data, isRealTime = false) {
    try {
        const { latitude, longitude, timestamp_server, source } = data;
        const newPosition = [latitude, longitude];
        const timestamp = new Date(timestamp_server);

        if (isNaN(timestamp.getTime())) {
            throw new Error('Invalid timestamp from server');
        }

        // Format timestamp
        const dateTimeString = new Intl.DateTimeFormat('vi-VN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZone: 'Asia/Ho_Chi_Minh'
        }).format(timestamp);

        // Update text values
        DOM.latValue.textContent = latitude.toFixed(6);
        DOM.lonValue.textContent = longitude.toFixed(6);
        DOM.timeValue.textContent = dateTimeString;

        // Update status
        DOM.statusIndicator.className = 'status-dot online';

        if (isRealTime) {
            DOM.statusText.textContent = 'Real-time GPS';
            DOM.syncStatus.textContent = '?? Live Data';
        } else {
            DOM.statusText.textContent = 'Online';
            DOM.syncStatus.textContent = '?? Auto Sync';
        }

        // Update marker
        updateMarker(newPosition, {
            latitude,
            longitude,
            dateTimeString,
            source,
            isRealTime
        });

        console.log(`? UI updated: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`);
    } catch (error) {
        console.error('Error updating UI:', error);
        showErrorUI(error.message);
    }
}

/**
 * Update map marker
 */
function updateMarker(position, info) {
    const { latitude, longitude, dateTimeString, source, isRealTime } = info;

    // Create custom marker icon
    const markerIcon = isRealTime ? '??' : '??';
    const customIcon = L.divIcon({
        html: `<div class="custom-marker" style="font-size: 28px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">${markerIcon}</div>`,
        className: '',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    // Popup content
    const popupContent = `
        <div class="popup-content">
            <div class="popup-title">${isRealTime ? '?? Live GPS' : '?? GPS Location'}</div>
            <div class="popup-time">${dateTimeString}</div>
            <div class="popup-coords">
                <div>Lat: ${latitude.toFixed(6)}</div>
                <div>Lon: ${longitude.toFixed(6)}</div>
            </div>
            <div class="popup-source">Source: ${source}</div>
        </div>
    `;

    if (AppState.marker) {
        AppState.marker.setLatLng(position)
            .setIcon(customIcon)
            .setPopupContent(popupContent)
            .openPopup();
    } else {
        AppState.marker = L.marker(position, { icon: customIcon })
            .addTo(AppState.map)
            .bindPopup(popupContent)
            .openPopup();
    }

    // Pan/zoom to marker
    if (AppState.map.getZoom() < 16 || !AppState.map.getBounds().contains(position)) {
        AppState.map.setView(position, 17, { animate: true });
    } else {
        AppState.map.panTo(position, { animate: true });
    }
}

/**
 * Show error state in UI
 */
function showErrorUI(message) {
    DOM.latValue.textContent = 'N/A';
    DOM.lonValue.textContent = 'N/A';
    DOM.timeValue.textContent = 'N/A';
    DOM.statusIndicator.className = 'status-dot error';
    DOM.statusText.textContent = 'Error';
    DOM.syncStatus.textContent = '? Sync Error';
    setProgressBar(0);
    console.error('Error:', message);
}

/**
 * Manual fetch location (button click)
 */
async function fetchLocationDataManual() {
    const originalText = DOM.trackButton.querySelector('.btn-text').textContent;
    DOM.trackButton.querySelector('.btn-text').textContent = 'Fetching GPS...';
    DOM.trackButton.disabled = true;
    setProgressBar(10);

    try {
        await fetchLocationData(true); // Use real-time GPS
    } finally {
        DOM.trackButton.querySelector('.btn-text').textContent = originalText;
        DOM.trackButton.disabled = false;
    }
}

/**
 * Set progress bar width
 */
function setProgressBar(percentage) {
    if (DOM.progressBar) {
        DOM.progressBar.style.width = `${percentage}%`;
    }
}

/**
 * Update sync status animation
 */
function updateSyncStatus(syncing) {
    if (DOM.syncAnimation) {
        if (syncing) {
            DOM.syncAnimation.classList.add('active');
        } else {
            setTimeout(() => {
                DOM.syncAnimation.classList.remove('active');
            }, 500);
        }
    }
}

/**
 * Start auto-refresh
 */
function startAutoRefresh() {
    // Clear existing interval
    if (AppState.autoRefreshInterval) {
        clearInterval(AppState.autoRefreshInterval);
    }

    // Start new interval
    AppState.autoRefreshInterval = setInterval(() => {
        fetchLocationData(false);
    }, AppState.refreshRate);

    logActivity(`Auto-refresh started (${AppState.refreshRate / 1000}s interval)`, 'info');
    console.log(`? Auto-refresh set to ${AppState.refreshRate / 1000} seconds`);
}

/**
 * Center map on marker
 */
function centerMap() {
    if (AppState.marker) {
        const position = AppState.marker.getLatLng();
        AppState.map.setView(position, 17, { animate: true });
        logActivity('Map centered on marker', 'info');
    }
}

/**
 * Toggle fullscreen
 */
function toggleFullscreen() {
    const mapPanel = document.querySelector('.map-panel');
    
    if (!document.fullscreenElement) {
        mapPanel.requestFullscreen().catch(err => {
            console.error('Error attempting to enable fullscreen:', err);
        });
        logActivity('Entered fullscreen mode', 'info');
    } else {
        document.exitFullscreen();
        logActivity('Exited fullscreen mode', 'info');
    }
}

/**
 * Log activity to activity log panel
 */
function logActivity(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString('vi-VN');
    
    // Add to state
    AppState.activityLog.unshift({ message, type, timestamp });
    
    // Keep only max entries
    if (AppState.activityLog.length > AppState.maxLogEntries) {
        AppState.activityLog.pop();
    }

    // Update DOM
    updateActivityLogDOM();
}

/**
 * Update activity log in DOM
 */
function updateActivityLogDOM() {
    if (!DOM.activityLog) return;

    DOM.activityLog.innerHTML = AppState.activityLog
        .map(log => `
            <div class="activity-item ${log.type}">
                <span class="activity-time">[${log.timestamp}]</span>
                ${log.message}
            </div>
        `)
        .join('');
}

/**
 * Clear activity log
 */
function clearActivityLog() {
    AppState.activityLog = [];
    updateActivityLogDOM();
    logActivity('Activity log cleared', 'info');
}

/**
 * Setup theme toggle
 */
function setupTheme() {
    // Check saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

/**
 * Toggle theme
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    logActivity(`Theme changed to ${newTheme} mode`, 'info');
}

// ============= SMART FEATURES =============

/**
 * Load geofences for current user
 */
async function loadGeofences() {
    try {
        const response = await authFetch('/geofences');
        if (response.ok) {
            AppState.geofences = await response.json();
            displayGeofences();
            logActivity(`Loaded ${AppState.geofences.length} geofences`, 'info');
        }
    } catch (error) {
        console.error('Error loading geofences:', error);
    }
}

/**
 * Display geofences on map
 */
function displayGeofences() {
    // Clear existing geofence layers
    AppState.map.eachLayer(layer => {
        if (layer instanceof L.Circle && layer.options.className === 'geofence') {
            AppState.map.removeLayer(layer);
        }
    });

    // Add geofence circles
    AppState.geofences.forEach(geofence => {
        L.circle([geofence.latitude, geofence.longitude], {
            radius: geofence.radius,
            color: '#3b82f6',
            fillColor: '#3b82f6',
            fillOpacity: 0.1,
            className: 'geofence'
        }).bindPopup(`
            <strong>${geofence.name}</strong><br>
            Radius: ${geofence.radius}m<br>
            <button onclick="deleteGeofence(${geofence.id})">Delete</button>
        `).addTo(AppState.map);
    });
}

/**
 * Check if location breaches geofences
 */
async function checkGeofences(latitude, longitude) {
    if (AppState.geofences.length === 0) return;

    try {
        const response = await authFetch('/geofences/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude, longitude })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.alerts_triggered > 0) {
                data.alerts.forEach(alert => {
                    logActivity(`?? Geofence Alert: ${alert.alert_type} ${alert.geofence_name}`, 'error');
                });
            }
        }
    } catch (error) {
        console.error('Error checking geofences:', error);
    }
}

/**
 * Show route history on map
 */
async function showRouteHistory() {
    try {
        const hours = document.getElementById('route-hours')?.value || 24;
        const response = await authFetch(`/route-history?hours=${hours}`);
        
        if (response.ok) {
            const data = await response.json();
            displayRouteOnMap(data.route_points);
            displayRouteAnalytics(data.analytics);
            logActivity(`Loaded route with ${data.route_points.length} points`, 'success');
        }
    } catch (error) {
        console.error('Error loading route history:', error);
        logActivity('Failed to load route history', 'error');
    }
}

/**
 * Display route on map
 */
function displayRouteOnMap(routePoints) {
    if (!routePoints || routePoints.length === 0) return;

    // Remove existing route
    AppState.map.eachLayer(layer => {
        if (layer instanceof L.Polyline && layer.options.className === 'route-line') {
            AppState.map.removeLayer(layer);
        }
    });

    // Create polyline
    const latLngs = routePoints.map(p => [p.latitude, p.longitude]);
    L.polyline(latLngs, {
        color: '#ef4444',
        weight: 3,
        opacity: 0.7,
        className: 'route-line'
    }).addTo(AppState.map);

    // Fit map to route bounds
    const bounds = L.latLngBounds(latLngs);
    AppState.map.fitBounds(bounds, { padding: [50, 50] });
}

/**
 * Display route analytics
 */
function displayRouteAnalytics(analytics) {
    const analyticsDiv = document.getElementById('route-analytics');
    if (!analyticsDiv) return;

    analyticsDiv.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-item">
                <span class="analytics-label">Distance</span>
                <span class="analytics-value">${analytics.total_distance_km} km</span>
            </div>
            <div class="analytics-item">
                <span class="analytics-label">Duration</span>
                <span class="analytics-value">${analytics.duration_minutes} min</span>
            </div>
            <div class="analytics-item">
                <span class="analytics-label">Avg Speed</span>
                <span class="analytics-value">${analytics.average_speed} km/h</span>
            </div>
            <div class="analytics-item">
                <span class="analytics-label">Points</span>
                <span class="analytics-value">${analytics.total_points}</span>
            </div>
        </div>
    `;
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (AppState.autoRefreshInterval) {
        clearInterval(AppState.autoRefreshInterval);
    }
});

// Export functions for use in HTML onclick handlers
window.fetchLocationDataManual = fetchLocationDataManual;
window.centerMap = centerMap;
window.toggleFullscreen = toggleFullscreen;
window.clearActivityLog = clearActivityLog;
window.toggleTheme = toggleTheme;
window.logout = logout;
window.showRouteHistory = showRouteHistory;
