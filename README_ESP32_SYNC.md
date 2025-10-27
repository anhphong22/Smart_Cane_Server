# ESP32 Smart Cane - Hệ thống đồng bộ dữ liệu

## Tổng quan
Hệ thống này cho phép ESP32 Smart Cane đồng bộ dữ liệu GPS với web interface một cách tự động và liên tục.

## Các file chính

### 1. `esp32_sync.py` - Script đồng bộ chính
- **Chức năng**: Đồng bộ dữ liệu giữa ESP32 và web
- **Cách chạy**: `python esp32_sync.py`
- **Menu options**:
  - Test ESP32 Connection
  - Send Test Location  
  - Full Sync
  - Monitor ESP32 Data
  - Start/Stop Auto Sync
  - Auto Sync Status

### 2. `esp32_auto_sync.py` - Auto sync background
- **Chức năng**: Chạy đồng bộ tự động trong background
- **Cách chạy**: `python esp32_auto_sync.py`
- **Tính năng**: Đồng bộ liên tục mỗi 10 giây

### 3. `start_smart_cane.py` - Khởi động toàn bộ hệ thống
- **Chức năng**: Chạy cả web server và auto sync
- **Cách chạy**: `python start_smart_cane.py`
- **Kết quả**: Web interface tại http://localhost:8080

### 4. `app.py` - Flask web server
- **Chức năng**: Web interface hiển thị dữ liệu GPS
- **Endpoints**:
  - `/api/get_latest_location` - Lấy vị trí mới nhất
  - `/esp32/save_location` - ESP32 gửi dữ liệu
  - `/map` - Giao diện bản đồ

## Cách sử dụng

### Phương pháp 1: Chạy riêng lẻ
```bash
# 1. Chạy web server
cd /Users/thanhhoa/Documents/smart_cane_server
source venv/bin/activate
python app.py

# 2. Chạy auto sync (terminal mới)
cd /Users/thanhhoa/Documents/smart_cane_server
source venv/bin/activate
python esp32_auto_sync.py
```

### Phương pháp 2: Chạy tất cả cùng lúc
```bash
cd /Users/thanhhoa/Documents/smart_cane_server
source venv/bin/activate
python start_smart_cane.py
```

### Phương pháp 3: Chạy manual sync
```bash
cd /Users/thanhhoa/Documents/smart_cane_server
source venv/bin/activate
python esp32_sync.py
# Chọn option 5: Start Auto Sync
```

## Cấu hình

### Thông số ESP32
- **IP**: 10.251.10.194
- **Port**: 8080
- **Device ID**: SmartCane01
- **Sync Interval**: 10 giây

### Web Interface
- **URL**: http://localhost:8080
- **Auto refresh**: 30 giây
- **Real-time sync**: Có

## Tính năng đồng bộ

### Auto Sync
- ✅ Đồng bộ tự động mỗi 10 giây
- ✅ Lưu dữ liệu vào SQLite database
- ✅ Cập nhật web interface real-time
- ✅ Xử lý lỗi kết nối
- ✅ Logging chi tiết

### Manual Sync
- ✅ Test kết nối ESP32
- ✅ Gửi dữ liệu test
- ✅ Monitor dữ liệu real-time
- ✅ Full sync với ESP32

### Web Interface
- ✅ Hiển thị trạng thái đồng bộ
- ✅ Map real-time với GPS data
- ✅ Auto refresh dữ liệu
- ✅ Responsive design

## Troubleshooting

### ESP32 không kết nối được
1. Kiểm tra IP: 10.251.10.194:8080
2. Chạy `python esp32_sync.py` → option 1
3. Kiểm tra network connection

### Web interface không hiển thị
1. Kiểm tra Flask server: http://localhost:8080
2. Kiểm tra database: `database.db`
3. Restart web server

### Auto sync không hoạt động
1. Kiểm tra `python esp32_sync.py` → option 7
2. Restart auto sync
3. Kiểm tra logs

## Dừng hệ thống
- **Ctrl+C** trong terminal để dừng
- Auto sync sẽ tự động dừng khi thoát
- Web server sẽ dừng khi thoát

## Logs và Monitoring
- Console logs hiển thị trạng thái real-time
- Web interface hiển thị trạng thái đồng bộ
- Database lưu tất cả dữ liệu GPS
