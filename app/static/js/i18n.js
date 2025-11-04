/**
 * Smart Cane GPS Tracker - Internationalization (i18n)
 * Supports: Vietnamese (vi) - Default, English (en)
 */

const translations = {
    vi: {
        // Header & Navigation
        'app.title': 'Gậy Thông Minh GPS',
        'app.subtitle': 'Hệ Thống Giám Sát GPS Thời Gian Thực',
        'theme.toggle': 'Đổi chế độ',
        'user.logout': 'Đăng xuất',
        'language': 'Ngôn ngữ',

        // Login Page
        'login.title': 'Đăng Nhập',
        'login.subtitle': 'Hệ Thống Giám Sát GPS An Toàn',
        'login.username': 'Tên đăng nhập',
        'login.password': 'Mật khẩu',
        'login.username.placeholder': 'Nhập tên đăng nhập',
        'login.password.placeholder': 'Nhập mật khẩu',
        'login.button': 'Đăng Nhập',
        'login.logging_in': 'Đang đăng nhập...',
        'login.demo.title': 'Tài Khoản Demo',
        'login.demo.username': 'Tên đăng nhập',
        'login.demo.password': 'Mật khẩu',
        'login.error.default': 'Đăng nhập thất bại. Vui lòng kiểm tra thông tin.',
        'login.error.network': 'Lỗi mạng. Vui lòng thử lại.',
        'login.footer': 'Gậy Thông Minh GPS v2.0 – An Toàn & Hiện Đại',

        // Dashboard Sections
        'dashboard.overview': 'Tổng Quan',
        'dashboard.map': 'Bản Đồ Trực Tiếp',
        'dashboard.device': 'Thiết Bị',
        'dashboard.analytics': 'Phân Tích',
        
        // Menu
        'menu.main': 'Menu Chính',
        'menu.profile': 'Hồ Sơ',
        'menu.preferences': 'Tùy Chọn',
        'menu.logout': 'Đăng Xuất',
        'menu.help': 'Trợ Giúp & Hỗ Trợ',
        'menu.quick_actions': 'Thao Tác Nhanh',

        // Device Status
        'device.status': 'Trạng Thái Thiết Bị',
        'device.status.online': 'Trực tuyến',
        'device.status.offline': 'Ngoại tuyến',
        'device.status.realtime': 'GPS thời gian thực',
        'device.id': 'ID Thiết Bị',
        'device.battery': 'Pin',
        'device.signal': 'Tín hiệu',

        // GPS Information
        'gps.latitude': 'Vĩ độ',
        'gps.longitude': 'Kinh độ',
        'gps.altitude': 'Độ Cao',
        'gps.speed': 'Tốc độ',
        'gps.accuracy': 'Độ Chính Xác',
        'gps.last_update': 'Cập Nhật Lần Cuối',
        'gps.satellites': 'Vệ Tinh',

        // Sync Status
        'sync.auto': 'Tự Động Đồng Bộ',
        'sync.live': 'Dữ Liệu Trực Tiếp',
        'sync.syncing': 'Đang đồng bộ...',
        'sync.last': 'Đồng bộ lần cuối',

        // Buttons & Actions
        'button.get_gps': 'Lấy GPS Thời Gian Thực',
        'button.center_map': 'Căn Giữa Bản Đồ',
        'button.fullscreen': 'Toàn Màn Hình',
        'button.refresh': 'Làm Mới',
        'button.clear': 'Xóa',
        'button.show_route': 'Hiển Thị Tuyến Đường',
        'button.hide_route': 'Ẩn Tuyến Đường',
        'button.export': 'Xuất Dữ Liệu',
        'button.settings': 'Cài Đặt',
        
        // Notifications
        'notifications.title': 'Thông báo',
        'notifications.empty': 'Không có thông báo mới',

        // Activity Log
        'activity.title': 'Nhật Ký Hoạt Động',
        'activity.clear': 'Xóa nhật ký',
        'activity.empty': 'Không có hoạt động nào',
        'activity.initialized': 'Ứng dụng đã khởi tạo',
        'activity.fetching': 'Đang lấy dữ liệu GPS...',
        'activity.updated': 'Vị trí đã cập nhật',
        'activity.error': 'Lỗi khi lấy dữ liệu',

        // Route History
        'route.title': 'Lịch Sử Tuyến Đường',
        'route.period': 'Khoảng Thời Gian',
        'route.last_hour': 'Giờ Qua',
        'route.last_6hours': '6 Giờ Qua',
        'route.last_24hours': '24 Giờ Qua',
        'route.last_week': 'Tuần Qua',
        'route.last_month': 'Tháng Qua',
        'route.distance': 'Quãng Đường',
        'route.duration': 'Thời Gian',
        'route.avg_speed': 'Tốc độ TB',
        'route.points': 'Điểm',
        'route.start': 'Điểm Đầu',
        'route.end': 'Điểm Cuối',
        'route.no_data': 'Không có dữ liệu tuyến đường',

        // Geofencing
        'geofence.title': 'Rào Cản Địa Lý',
        'geofence.create': 'Tạo Rào Cản',
        'geofence.name': 'Tên',
        'geofence.radius': 'Bán Kính (m)',
        'geofence.alert_enter': 'Cảnh báo khi vào',
        'geofence.alert_exit': 'Cảnh báo khi ra',
        'geofence.active': 'Hoạt động',
        'geofence.alerts': 'Cảnh Báo',
        'geofence.alert.entered': 'Đã vào rào cản',
        'geofence.alert.exited': 'Đã rời rào cản',

        // Analytics
        'analytics.title': 'Phân Tích',
        'analytics.today': 'Hôm Nay',
        'analytics.week': 'Tuần Này',
        'analytics.month': 'Tháng Này',
        'analytics.total_distance': 'Tổng Quãng Đường',
        'analytics.total_time': 'Tổng Thời Gian',
        'analytics.avg_speed': 'Tốc độ Trung Bình',
        'analytics.max_speed': 'Tốc độ Tối Đa',
        'analytics.trips': 'Chuyến đi',

        // Map
        'map.title': 'Bản Đồ Vị Trí Trực Tiếp',
        'map.current_location': 'Vị Trí Hiện Tại',
        'map.layers': 'Lớp Bản Đồ',
        'map.layer.street': 'Đường Phố',
        'map.layer.satellite': 'Vệ Tinh',
        'map.loading': 'Đang tải bản đồ...',
        'map.zoom_in': 'Phóng to',
        'map.zoom_out': 'Thu nhỏ',
        'map.live_location': 'Vị Trí Trực Tiếp',
        'map.stored_location': 'Vị Trí Đã Lưu',

        // Units
        'unit.km': 'km',
        'unit.m': 'm',
        'unit.kmh': 'km/h',
        'unit.min': 'phút',
        'unit.hour': 'giờ',
        'unit.day': 'ngày',

        // Time
        'time.just_now': 'Vừa xong',
        'time.seconds_ago': 'giây trước',
        'time.minutes_ago': 'phút trước',
        'time.hours_ago': 'giờ trước',
        'time.days_ago': 'ngày trước',

        // Messages
        'message.success': 'Thành công',
        'message.error': 'Lỗi',
        'message.warning': 'Cảnh báo',
        'message.info': 'Thông tin',
        'message.no_data': 'Không có dữ liệu',
        'message.loading': 'Đang tải...',

        // Quick Stats
        'stats.locations_today': 'Vị Trí Hôm Nay',
        'stats.distance_today': 'Quãng Đường Hôm Nay',
        'stats.active_time': 'Thời Gian Hoạt Động',
        'stats.alerts_today': 'Cảnh Báo Hôm Nay',
        'stats.locations': 'Vị trí',
        'stats.alerts': 'Cảnh báo',

        // Empty States
        'empty.device.title': 'Chưa Có Thiết Bị Kết Nối',
        'empty.device.description': 'Thiết bị GPS chưa được kết nối hoặc chưa gửi dữ liệu. Vui lòng kiểm tra kết nối thiết bị và thử lại.',
        'empty.device.tip': 'Mẹo: Đảm bảo thiết bị đã bật và có kết nối internet.',
        'empty.analytics.title': 'Chưa Có Dữ Liệu Phân Tích',
        'empty.analytics.description': 'Dữ liệu phân tích sẽ xuất hiện khi thiết bị bắt đầu gửi thông tin vị trí. Hãy kiểm tra lại sau.',
        'empty.analytics.feature1': 'Quãng đường di chuyển',
        'empty.analytics.feature2': 'Thời gian hoạt động',
        'empty.analytics.feature3': 'Tốc độ trung bình',
        'empty.analytics.feature4': 'Địa điểm thường xuyên',
        'empty.map.title': 'Chưa có dữ liệu GPS',
        'empty.map.description': 'Để bắt đầu, hãy nhấn nút "Lấy GPS" hoặc đợi đồng bộ tự động.',
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
        'login.footer': 'Smart Cane GPS v2.0 – Secure & Modern',
        
        // Dashboard Sections
        'dashboard.overview': 'Overview',
        'dashboard.map': 'Live Map',
        'dashboard.device': 'Device',
        'dashboard.analytics': 'Analytics',
        
        // Menu
        'menu.main': 'Main Menu',
        'menu.profile': 'Profile',
        'menu.preferences': 'Preferences',
        'menu.logout': 'Logout',
        'menu.help': 'Help & Support',
        'menu.quick_actions': 'Quick Actions',
        
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
        
        // Notifications
        'notifications.title': 'Notifications',
        'notifications.empty': 'No new notifications',
        
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
        'stats.locations': 'Locations',
        'stats.alerts': 'Alerts',
        
        // Map Page
        'map.title': 'Live Map',
        'map.current_location': 'Current Location',
        'map.layers': 'Map Layers',
        'map.layer.street': 'Street',
        'map.layer.satellite': 'Satellite',
        
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
            'vi': 'Tiếng Việt',
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
