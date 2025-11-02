/**
 * Smart Cane GPS Tracker - Internationalization (i18n)
 * Supports: Vietnamese (vi) - Default, English (en)
 */

const translations = {
    vi: {
        // Header & Navigation
        'app.title': 'G?y Th?ng Minh GPS',
        'app.subtitle': 'H? Th?ng Gi?m S?t GPS Th?i Gian Th?c',
        'theme.toggle': '??i ch? ??',
        'user.logout': '??ng xu?t',
        'language': 'Ng?n ng?',
        
        // Login Page
        'login.title': '??ng Nh?p',
        'login.subtitle': 'H? Th?ng Gi?m S?t GPS An To?n',
        'login.username': 'T?n ??ng nh?p',
        'login.password': 'M?t kh?u',
        'login.username.placeholder': 'Nh?p t?n ??ng nh?p',
        'login.password.placeholder': 'Nh?p m?t kh?u',
        'login.button': '??ng Nh?p',
        'login.logging_in': '?ang ??ng nh?p...',
        'login.demo.title': 'T?i Kho?n Demo',
        'login.demo.username': 'T?n ??ng nh?p',
        'login.demo.password': 'M?t kh?u',
        'login.error.default': '??ng nh?p th?t b?i. Vui l?ng ki?m tra th?ng tin.',
        'login.error.network': 'L?i m?ng. Vui l?ng th? l?i.',
        'login.footer': 'G?y Th?ng Minh GPS v2.0 ? An To?n & Hi?n ??i',
        
        // Dashboard Sections
        'dashboard.overview': 'T?ng Quan',
        'dashboard.map': 'B?n ?? Tr?c Ti?p',
        'dashboard.device': 'Thi?t B?',
        'dashboard.analytics': 'Ph?n T?ch',
        
        // Device Status
        'device.status': 'Tr?ng Th?i Thi?t B?',
        'device.status.online': 'Tr?c tuy?n',
        'device.status.offline': 'Ngo?i tuy?n',
        'device.status.realtime': 'GPS th?i gian th?c',
        'device.id': 'ID Thi?t B?',
        'device.battery': 'Pin',
        'device.signal': 'T?n hi?u',
        
        // GPS Information
        'gps.latitude': 'V? ??',
        'gps.longitude': 'Kinh ??',
        'gps.altitude': '?? Cao',
        'gps.speed': 'T?c ??',
        'gps.accuracy': '?? Ch?nh X?c',
        'gps.last_update': 'C?p Nh?t L?n Cu?i',
        'gps.satellites': 'V? Tinh',
        
        // Sync Status
        'sync.auto': 'T? ??ng ??ng B?',
        'sync.live': 'D? Li?u Tr?c Ti?p',
        'sync.syncing': '?ang ??ng b?...',
        'sync.last': '??ng b? l?n cu?i',
        
        // Buttons & Actions
        'button.get_gps': 'L?y GPS Th?i Gian Th?c',
        'button.center_map': 'C?n Gi?a B?n ??',
        'button.fullscreen': 'To?n M?n H?nh',
        'button.refresh': 'L?m M?i',
        'button.clear': 'X?a',
        'button.show_route': 'Hi?n Th? Tuy?n ???ng',
        'button.hide_route': '?n Tuy?n ???ng',
        'button.export': 'Xu?t D? Li?u',
        'button.settings': 'C?i ??t',
        
        // Activity Log
        'activity.title': 'Nh?t K? Ho?t ??ng',
        'activity.clear': 'X?a nh?t k?',
        'activity.empty': 'Kh?ng c? ho?t ??ng n?o',
        'activity.initialized': '?ng d?ng ?? kh?i t?o',
        'activity.fetching': '?ang l?y d? li?u GPS...',
        'activity.updated': 'V? tr? ?? c?p nh?t',
        'activity.error': 'L?i khi l?y d? li?u',
        
        // Route History
        'route.title': 'L?ch S? Tuy?n ???ng',
        'route.period': 'Kho?ng Th?i Gian',
        'route.last_hour': 'Gi? Qua',
        'route.last_6hours': '6 Gi? Qua',
        'route.last_24hours': '24 Gi? Qua',
        'route.last_week': 'Tu?n Qua',
        'route.last_month': 'Th?ng Qua',
        'route.distance': 'Qu?ng ???ng',
        'route.duration': 'Th?i Gian',
        'route.avg_speed': 'T?c ?? TB',
        'route.points': '?i?m',
        'route.start': '?i?m ??u',
        'route.end': '?i?m Cu?i',
        'route.no_data': 'Kh?ng c? d? li?u tuy?n ???ng',
        
        // Geofencing
        'geofence.title': 'R?o C?n ??a L?',
        'geofence.create': 'T?o R?o C?n',
        'geofence.name': 'T?n',
        'geofence.radius': 'B?n K?nh (m)',
        'geofence.alert_enter': 'C?nh b?o khi v?o',
        'geofence.alert_exit': 'C?nh b?o khi ra',
        'geofence.active': 'Ho?t ??ng',
        'geofence.alerts': 'C?nh B?o',
        'geofence.alert.entered': '?? v?o r?o c?n',
        'geofence.alert.exited': '?? r?i r?o c?n',
        
        // Analytics
        'analytics.title': 'Ph?n T?ch',
        'analytics.today': 'H?m Nay',
        'analytics.week': 'Tu?n N?y',
        'analytics.month': 'Th?ng N?y',
        'analytics.total_distance': 'T?ng Qu?ng ???ng',
        'analytics.total_time': 'T?ng Th?i Gian',
        'analytics.avg_speed': 'T?c ?? Trung B?nh',
        'analytics.max_speed': 'T?c ?? T?i ?a',
        'analytics.trips': 'Chuy?n ?i',
        
        // Map
        'map.title': 'B?n ?? V? Tr? Tr?c Ti?p',
        'map.loading': '?ang t?i b?n ??...',
        'map.zoom_in': 'Ph?ng to',
        'map.zoom_out': 'Thu nh?',
        'map.live_location': 'V? Tr? Tr?c Ti?p',
        'map.stored_location': 'V? Tr? ?? L?u',
        
        // Units
        'unit.km': 'km',
        'unit.m': 'm',
        'unit.kmh': 'km/h',
        'unit.min': 'ph?t',
        'unit.hour': 'gi?',
        'unit.day': 'ng?y',
        
        // Time
        'time.just_now': 'V?a xong',
        'time.seconds_ago': 'gi?y tr??c',
        'time.minutes_ago': 'ph?t tr??c',
        'time.hours_ago': 'gi? tr??c',
        'time.days_ago': 'ng?y tr??c',
        
        // Messages
        'message.success': 'Th?nh c?ng',
        'message.error': 'L?i',
        'message.warning': 'C?nh b?o',
        'message.info': 'Th?ng tin',
        'message.no_data': 'Kh?ng c? d? li?u',
        'message.loading': '?ang t?i...',
        
        // Quick Stats
        'stats.title': 'Th?ng K? Nhanh',
        'stats.locations_today': 'V? Tr? H?m Nay',
        'stats.distance_today': 'Qu?ng ???ng H?m Nay',
        'stats.active_time': 'Th?i Gian Ho?t ??ng',
        'stats.alerts_today': 'C?nh B?o H?m Nay'
    },
    
    en: {
        // Header & Navigation
        'app.title': 'Smart Cane GPS',
        'app.subtitle': 'Real-time GPS Monitoring System',
        'theme.toggle': 'Toggle theme',
        'user.logout': 'Logout',
        'language': 'Language',
        
        // Login Page
        'login.title': 'Login',
        'login.subtitle': 'Secure GPS Monitoring System',
        'login.username': 'Username',
        'login.password': 'Password',
        'login.username.placeholder': 'Enter your username',
        'login.password.placeholder': 'Enter your password',
        'login.button': 'Login',
        'login.logging_in': 'Logging in...',
        'login.demo.title': 'Demo Credentials',
        'login.demo.username': 'Username',
        'login.demo.password': 'Password',
        'login.error.default': 'Login failed. Please check your credentials.',
        'login.error.network': 'Network error. Please try again.',
        'login.footer': 'Smart Cane GPS v2.0 ? Secure & Modern',
        
        // Dashboard Sections
        'dashboard.overview': 'Overview',
        'dashboard.map': 'Live Map',
        'dashboard.device': 'Device',
        'dashboard.analytics': 'Analytics',
        
        // Device Status
        'device.status': 'Device Status',
        'device.status.online': 'Online',
        'device.status.offline': 'Offline',
        'device.status.realtime': 'Real-time GPS',
        'device.id': 'Device ID',
        'device.battery': 'Battery',
        'device.signal': 'Signal',
        
        // GPS Information
        'gps.latitude': 'Latitude',
        'gps.longitude': 'Longitude',
        'gps.altitude': 'Altitude',
        'gps.speed': 'Speed',
        'gps.accuracy': 'Accuracy',
        'gps.last_update': 'Last Update',
        'gps.satellites': 'Satellites',
        
        // Sync Status
        'sync.auto': 'Auto Sync',
        'sync.live': 'Live Data',
        'sync.syncing': 'Syncing...',
        'sync.last': 'Last sync',
        
        // Buttons & Actions
        'button.get_gps': 'Get Real-time GPS',
        'button.center_map': 'Center Map',
        'button.fullscreen': 'Fullscreen',
        'button.refresh': 'Refresh',
        'button.clear': 'Clear',
        'button.show_route': 'Show Route',
        'button.hide_route': 'Hide Route',
        'button.export': 'Export Data',
        'button.settings': 'Settings',
        
        // Activity Log
        'activity.title': 'Activity Log',
        'activity.clear': 'Clear log',
        'activity.empty': 'No activities',
        'activity.initialized': 'Application initialized',
        'activity.fetching': 'Fetching GPS data...',
        'activity.updated': 'Location updated',
        'activity.error': 'Error fetching data',
        
        // Route History
        'route.title': 'Route History',
        'route.period': 'Time Period',
        'route.last_hour': 'Last Hour',
        'route.last_6hours': 'Last 6 Hours',
        'route.last_24hours': 'Last 24 Hours',
        'route.last_week': 'Last Week',
        'route.last_month': 'Last Month',
        'route.distance': 'Distance',
        'route.duration': 'Duration',
        'route.avg_speed': 'Avg Speed',
        'route.points': 'Points',
        'route.start': 'Start',
        'route.end': 'End',
        'route.no_data': 'No route data available',
        
        // Geofencing
        'geofence.title': 'Geofencing',
        'geofence.create': 'Create Geofence',
        'geofence.name': 'Name',
        'geofence.radius': 'Radius (m)',
        'geofence.alert_enter': 'Alert on entry',
        'geofence.alert_exit': 'Alert on exit',
        'geofence.active': 'Active',
        'geofence.alerts': 'Alerts',
        'geofence.alert.entered': 'Entered geofence',
        'geofence.alert.exited': 'Exited geofence',
        
        // Analytics
        'analytics.title': 'Analytics',
        'analytics.today': 'Today',
        'analytics.week': 'This Week',
        'analytics.month': 'This Month',
        'analytics.total_distance': 'Total Distance',
        'analytics.total_time': 'Total Time',
        'analytics.avg_speed': 'Average Speed',
        'analytics.max_speed': 'Max Speed',
        'analytics.trips': 'Trips',
        
        // Map
        'map.title': 'Live Location Map',
        'map.loading': 'Loading map...',
        'map.zoom_in': 'Zoom in',
        'map.zoom_out': 'Zoom out',
        'map.live_location': 'Live Location',
        'map.stored_location': 'Stored Location',
        
        // Units
        'unit.km': 'km',
        'unit.m': 'm',
        'unit.kmh': 'km/h',
        'unit.min': 'min',
        'unit.hour': 'hr',
        'unit.day': 'day',
        
        // Time
        'time.just_now': 'Just now',
        'time.seconds_ago': 'seconds ago',
        'time.minutes_ago': 'minutes ago',
        'time.hours_ago': 'hours ago',
        'time.days_ago': 'days ago',
        
        // Messages
        'message.success': 'Success',
        'message.error': 'Error',
        'message.warning': 'Warning',
        'message.info': 'Info',
        'message.no_data': 'No data available',
        'message.loading': 'Loading...',
        
        // Quick Stats
        'stats.title': 'Quick Stats',
        'stats.locations_today': 'Locations Today',
        'stats.distance_today': 'Distance Today',
        'stats.active_time': 'Active Time',
        'stats.alerts_today': 'Alerts Today',
        
        // Empty States
        'empty.map.title': 'No GPS Data Available',
        'empty.map.description': 'The map will display location when GPS signal is received from the device.',
        'empty.map.tip': 'Click "Get GPS" button to update location',
        'empty.device.title': 'No Device Connected',
        'empty.device.description': 'GPS device is not connected or hasn\'t sent data yet. Please check device connection and try again.',
        'empty.device.tip': 'Tip: Make sure device is powered on and has internet connection',
        'empty.analytics.title': 'No Analytics Data',
        'empty.analytics.description': 'Analytics data will appear when the device starts sending location information. Please check back later.',
        'empty.analytics.feature1': 'Distance traveled',
        'empty.analytics.feature2': 'Active time',
        'empty.analytics.feature3': 'Average speed',
        'empty.analytics.feature4': 'Frequent locations'
    }
};

// i18n Manager
class I18nManager {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'vi'; // Default to Vietnamese
        this.translations = translations;
    }
    
    /**
     * Get translation for a key
     */
    t(key, params = {}) {
        let translation = this.translations[this.currentLang][key] || key;
        
        // Replace parameters
        Object.keys(params).forEach(param => {
            translation = translation.replace(`{${param}}`, params[param]);
        });
        
        return translation;
    }
    
    /**
     * Change language
     */
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            this.updatePageTranslations();
            return true;
        }
        return false;
    }
    
    /**
     * Get current language
     */
    getLanguage() {
        return this.currentLang;
    }
    
    /**
     * Update all elements with data-i18n attribute
     */
    updatePageTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.placeholder !== undefined) {
                    element.placeholder = translation;
                }
            } else {
                element.textContent = translation;
            }
        });
        
        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
        
        // Update titles
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.t(key);
        });
        
        // Trigger custom event for components that need to update
        window.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { language: this.currentLang } 
        }));
    }
    
    /**
     * Get available languages
     */
    getAvailableLanguages() {
        return Object.keys(this.translations);
    }
    
    /**
     * Get language name
     */
    getLanguageName(code) {
        const names = {
            'vi': 'Ti?ng Vi?t',
            'en': 'English'
        };
        return names[code] || code;
    }
}

// Create global instance
const i18n = new I18nManager();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { i18n, I18nManager };
}
