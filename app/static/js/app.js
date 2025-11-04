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
    routePlaybackInterval: null,
    notifications: [],
    stats: {
        locations: 0,
        alerts: 0
    }
};

// DOM Elements Cache - with null safety
const DOM = {
    get statusIndicator() { return document.getElementById('status-indicator'); },
    get statusText() { return document.getElementById('status-text'); },
    get syncStatus() { return document.getElementById('sync-status'); },
    get syncIcon() { return document.getElementById('sync-icon'); },
    get progressBar() { return document.getElementById('data-progress-bar'); },
    get latValue() { return document.getElementById('latitude-value'); },
    get lonValue() { return document.getElementById('longitude-value'); },
    get timeValue() { return document.getElementById('time-value'); },
    get activityLog() { return document.getElementById('activity-log'); },
    get userDisplay() { return document.getElementById('user-display'); },
    get logoutBtn() { return document.getElementById('logout-btn'); }
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
 * Initialize i18n system
 */
function initI18n() {
    if (typeof i18n === 'undefined') {
        console.warn('i18n not loaded, using fallback');
        return;
    }
    
    const savedLang = i18n.getLanguage();
    document.documentElement.lang = savedLang;
    i18n.updatePageTranslations();
    
    // Listen for language changes
    window.addEventListener('languageChanged', function(e) {
        updateUITranslations();
    });
}

/**
 * Update UI translations dynamically
 */
function updateUITranslations() {
    if (typeof i18n === 'undefined') return;

    // Refresh any dynamic content that needs translation
    if (DOM.statusText && DOM.statusIndicator) {
        // Update status based on current state
        const isOnline = DOM.statusIndicator.classList.contains('online');
        if (isOnline) {
            DOM.statusText.textContent = i18n.t('device.status.online');
        } else {
            DOM.statusText.textContent = i18n.t('device.status.offline');
        }
    }
}

/**
 * Initialize the application
 */
function initApp() {
    if (!checkAuth()) return;
    
    initI18n();
    initMap();
    startAutoRefresh();
    setupTheme();
    loadGeofences();
    initKeyboardShortcuts();
    updateSidebarStats();
    
    const activityMsg = typeof i18n !== 'undefined' ? i18n.t('activity.initialized') : 'Application initialized';
    logActivity(activityMsg, 'info');
    console.log('🚀 Smart Cane GPS Tracker initialized');
}

/**
 * Initialize Leaflet map
 */
function initMap() {
    try {
        // Detect if mobile device
        const isMobile = window.innerWidth <= 768;

        // Create map instance with mobile-optimized settings
        AppState.map = L.map('map', {
            center: AppState.initialPosition,
            zoom: isMobile ? 12 : 13,
            zoomControl: false,
            // Mobile-specific touch settings
            tap: true,
            tapTolerance: 15,
            touchZoom: true,
            scrollWheelZoom: !isMobile, // Disable scroll zoom on mobile to prevent accidental zooming
            doubleClickZoom: true,
            dragging: true,
            zoomAnimation: true,
            fadeAnimation: true,
            markerZoomAnimation: true
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

        // Add mobile-specific event listeners
        if (isMobile) {
            setupMobileMapControls();
        }

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
        html: `<div class="custom-marker initial"><i class="fas fa-map-marker-alt" style="color: #ef4444; font-size: 24px;"></i></div>`,
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

        console.log(`📡 Fetching data from: ${endpoint}`);
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
            
            // Update stats
            AppState.stats.locations++;
            updateSidebarStats();
            
            // Check geofences
            checkGeofences(data.latitude, data.longitude);
        } else {
            throw new Error('Invalid data received from server');
        }
    } catch (error) {
        console.error('❌ Fetch error:', error);
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

        // Update text values with null checks
        if (DOM.latValue) DOM.latValue.textContent = latitude.toFixed(6);
        if (DOM.lonValue) DOM.lonValue.textContent = longitude.toFixed(6);
        if (DOM.timeValue) DOM.timeValue.textContent = dateTimeString;

        // Update status
        if (DOM.statusIndicator) DOM.statusIndicator.className = 'status-dot online';

        if (isRealTime) {
            if (DOM.statusText) DOM.statusText.textContent = typeof i18n !== 'undefined' ? i18n.t('device.status.realtime') : 'Real-time GPS';
            if (DOM.syncStatus) DOM.syncStatus.innerHTML = '<i class="fas fa-signal"></i> ' + (typeof i18n !== 'undefined' ? i18n.t('sync.live') : 'Live Data');
        } else {
            if (DOM.statusText) DOM.statusText.textContent = typeof i18n !== 'undefined' ? i18n.t('device.status.online') : 'Online';
            if (DOM.syncStatus) DOM.syncStatus.innerHTML = '<i class="fas fa-sync-alt"></i> ' + (typeof i18n !== 'undefined' ? i18n.t('sync.auto') : 'Auto Sync');
        }

        // Update marker
        updateMarker(newPosition, {
            latitude,
            longitude,
            dateTimeString,
            source,
            isRealTime
        });

        console.log(`✅ UI updated: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`);
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
    const markerIcon = isRealTime ? 'fa-circle' : 'fa-map-marker-alt';
    const popupIcon = isRealTime ? '<i class="fas fa-broadcast-tower"></i>' : '<i class="fas fa-map-marker-alt"></i>';

    const customIcon = L.divIcon({
        html: `<div class="custom-marker"><i class="fas ${markerIcon}" style="color: #3b82f6; font-size: 28px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));"></i></div>`,
        className: '',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });

    // Popup content
    const popupContent = `
        <div class="popup-content">
            <div class="popup-title">${popupIcon} ${isRealTime ? 'Live GPS' : 'GPS Location'}</div>
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
    if (DOM.latValue) DOM.latValue.textContent = 'N/A';
    if (DOM.lonValue) DOM.lonValue.textContent = 'N/A';
    if (DOM.timeValue) DOM.timeValue.textContent = 'N/A';
    if (DOM.statusIndicator) DOM.statusIndicator.className = 'status-dot error';
    if (DOM.statusText) DOM.statusText.textContent = 'Error';
    if (DOM.syncStatus) DOM.syncStatus.textContent = '❌ Sync Error';
    setProgressBar(0);
    console.error('Error:', message);
}

/**
 * Manual fetch location (button click)
 */
async function fetchLocationDataManual() {
    setProgressBar(10);

    try {
        await fetchLocationData(true); // Use real-time GPS
    } finally {
        setProgressBar(100);
        setTimeout(() => setProgressBar(0), 500);
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
    if (DOM.syncIcon) {
        if (syncing) {
            DOM.syncIcon.style.animation = 'rotate 1s linear infinite';
        } else {
            setTimeout(() => {
                DOM.syncIcon.style.animation = '';
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
    console.log(`⏰ Auto-refresh set to ${AppState.refreshRate / 1000} seconds`);
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
    
    // Update theme icon
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    logActivity(`Theme changed to ${newTheme} mode`, 'info');
}

/**
 * Update sidebar stats
 */
function updateSidebarStats() {
    const sidebarLocations = document.getElementById('sidebar-locations');
    const sidebarAlerts = document.getElementById('sidebar-alerts');
    
    if (sidebarLocations) {
        sidebarLocations.textContent = AppState.stats.locations;
    }
    if (sidebarAlerts) {
        sidebarAlerts.textContent = AppState.stats.alerts;
    }
}

/**
 * Toggle notifications dropdown
 */
function toggleNotifications() {
    const menu = document.getElementById('notification-menu');
    if (!menu) return;
    
    // Close other dropdowns
    closeAllDropdowns(['notification-menu']);
    
    menu.classList.toggle('show');
    
    // Load notifications if opening
    if (menu.classList.contains('show')) {
        loadNotifications();
    }
}

/**
 * Load notifications
 */
function loadNotifications() {
    const notificationList = document.getElementById('notification-list');
    if (!notificationList) return;
    
    if (AppState.notifications.length === 0) {
        notificationList.innerHTML = `
            <div class="notification-empty">
                <i class="fas fa-bell-slash"></i>
                <span data-i18n="notifications.empty">Không có thông báo</span>
            </div>
        `;
        return;
    }
    
    notificationList.innerHTML = AppState.notifications.map(notif => `
        <div class="notification-item">
            <div class="notification-icon ${notif.type}">
                <i class="fas fa-${getNotificationIcon(notif.type)}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-title">${notif.title}</div>
                <div class="notification-message">${notif.message}</div>
                <div class="notification-time">${notif.time}</div>
            </div>
        </div>
    `).join('');
}

/**
 * Get notification icon based on type
 */
function getNotificationIcon(type) {
    const icons = {
        'info': 'info-circle',
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'error': 'times-circle'
    };
    return icons[type] || 'bell';
}

/**
 * Clear notifications
 */
function clearNotifications() {
    AppState.notifications = [];
    loadNotifications();
    document.getElementById('notification-count').textContent = '0';
}

/**
 * Add notification
 */
function addNotification(title, message, type = 'info') {
    const notification = {
        title,
        message,
        type,
        time: new Date().toLocaleTimeString('vi-VN')
    };
    
    AppState.notifications.unshift(notification);
    
    // Update badge
    const badge = document.getElementById('notification-count');
    if (badge) {
        badge.textContent = AppState.notifications.length;
    }
}

/**
 * Toggle search (placeholder for future feature)
 */
function toggleSearch() {
    console.log('Search feature - Coming soon!');
    addNotification('Search', 'Search feature coming soon!', 'info');
}

/**
 * Close all dropdowns except specified
 */
function closeAllDropdowns(except = []) {
    const dropdowns = ['language-menu', 'notification-menu', 'userDropdownMenu'];
    
    dropdowns.forEach(id => {
        if (!except.includes(id)) {
            const menu = document.getElementById(id);
            if (menu) {
                menu.classList.remove('show');
            }
        }
    });
}

/**
 * Initialize keyboard shortcuts
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K: Search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            toggleSearch();
        }
        
        // Ctrl/Cmd + B: Toggle sidebar
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            toggleSidebar();
        }
        
        // Ctrl/Cmd + T: Toggle theme
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
            e.preventDefault();
            toggleTheme();
        }
        
        // Escape: Close dropdowns and sidebar
        if (e.key === 'Escape') {
            closeAllDropdowns();
            const sidebar = document.querySelector('.sidebar-nav');
            if (sidebar && sidebar.classList.contains('open')) {
                toggleSidebar();
            }
        }
    });
    
    console.log('⌨️ Keyboard shortcuts initialized');
    console.log('  Ctrl+K: Search');
    console.log('  Ctrl+B: Toggle Sidebar');
    console.log('  Ctrl+T: Toggle Theme');
    console.log('  Esc: Close menus');
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
                    logActivity(`<i class="fas fa-exclamation-triangle"></i> Geofence Alert: ${alert.alert_type} ${alert.geofence_name}`, 'error');
                });
            }
        }
    } catch (error) {
        console.error('Error checking geofences:', error);
    }
}

/**
 * Setup mobile-specific map controls
 */
function setupMobileMapControls() {
    console.log('📱 Setting up mobile map controls');

    // Disable map dragging when interacting with device info panel on mobile
    const devicePanel = document.querySelector('.device-status-panel');
    if (devicePanel) {
        devicePanel.addEventListener('touchstart', () => {
            AppState.map.dragging.disable();
        });

        devicePanel.addEventListener('touchend', () => {
            setTimeout(() => {
                AppState.map.dragging.enable();
            }, 100);
        });
    }

    // Add double-tap to recenter on mobile
    let lastTap = 0;
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        mapContainer.addEventListener('touchend', (e) => {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;

            if (tapLength < 300 && tapLength > 0) {
                // Double tap detected
                centerMap();
                e.preventDefault();
            }
            lastTap = currentTime;
        });
    }

    // Handle orientation change
    window.addEventListener('orientationchange', () => {
        setTimeout(() => {
            AppState.map.invalidateSize();
            if (AppState.marker) {
                const position = AppState.marker.getLatLng();
                AppState.map.setView(position, AppState.map.getZoom());
            }
        }, 200);
    });

    // Handle window resize for responsive map
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            AppState.map.invalidateSize();
        }, 250);
    });

    logActivity('Mobile map controls enabled', 'info');
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
