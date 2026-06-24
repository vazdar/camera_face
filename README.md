# 📸 Hệ thống điểm danh nhận diện khuôn mặt

Hệ thống điểm danh tự động sử dụng **ESP32-CAM** để chụp ảnh và gửi lên **Flask server** để nhận diện khuôn mặt bằng thư viện `face_recognition`.

---

## 🗂️ Cấu trúc dự án

```
project/
├── face_demo.py          # Flask server chính
├── datasheet.csv         # File lưu dữ liệu điểm danh
├── dataset/              # Ảnh khuôn mặt dùng để train
│   ├── Nguyen_Van_A/
│   │   ├── 1.jpg
│   │   └── 2.jpg
│   └── Tran_Thi_B/
│       └── 1.jpg
└── face_demo.ino         # Code Arduino cho ESP32-CAM
```

---

## ⚙️ Yêu cầu hệ thống

### Phần cứng

- Board **AI Thinker ESP32-CAM**
- Cáp USB-to-TTL (để nạp code)
- Máy tính chạy Python 3.10+

### Phần mềm — Python

```bash
pip install flask opencv-python face_recognition
```

### Phần mềm — Arduino IDE

- Board: `AI Thinker ESP32-CAM`
- Thư viện: `WiFi`, `esp_camera`

---

## 🚀 Hướng dẫn cài đặt

### 1. Chuẩn bị dataset

Tạo thư mục `dataset/` và thêm ảnh khuôn mặt theo cấu trúc:

```
dataset/
└── <Tên_người>/
    └── anh1.jpg   (tối thiểu 1 ảnh, rõ mặt, đủ sáng)
```

### 2. Chạy Flask server

```bash
python face_demo.py
```

Server sẽ khởi động tại `http://0.0.0.0:5000`.

### 3. Mở port Firewall (Windows)

Chạy PowerShell với quyền **Admin**:

```powershell
netsh advfirewall firewall add rule name="Flask ESP32" dir=in action=allow protocol=TCP localport=5000
```

### 4. Nạp code lên ESP32-CAM

Mở `face_demo.ino` trong Arduino IDE, chỉnh thông tin WiFi:

```cpp
WiFi.begin("TEN_WIFI", "MAT_KHAU");
```

Chỉnh IP máy tính (kiểm tra bằng `ipconfig`):

```cpp
client.connect("192.168.x.xxx", 5000)
```

Nạp code và reset board.

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/upload` | Nhận ảnh JPEG từ ESP32, nhận diện và ghi điểm danh |
| `GET` | `/attendance` | Xem danh sách điểm danh dạng HTML |

### POST `/upload`

- **Content-Type:** `image/jpeg`
- **Body:** Raw JPEG binary
- **Response:** Tên người được nhận diện, hoặc `UNKNOWN`

---

## 🔄 Luồng hoạt động

```
ESP32-CAM
  └─► Chụp ảnh mỗi 3 giây
      └─► Gửi HTTP POST đến Flask /upload
          └─► Flask nhận diện khuôn mặt
              ├─► Khớp → ghi vào datasheet.csv
              └─► Không khớp → bỏ qua (UNKNOWN)
```

---

## 📋 Định dạng datasheet.csv

```csv
Nguyen_Van_A,2026-06-24 07:52:11
Tran_Thi_B,2026-06-24 08:05:33
```

Mỗi người chỉ được ghi **một lần duy nhất** trong ngày.

---

## 🐛 Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|----------|
| `Flask Fail` | Firewall chặn port 5000 | Chạy lệnh `netsh` ở bước 3 |
| `Flask Fail` | Sai IP máy tính | Kiểm tra lại bằng `ipconfig` |
| `CAMERA FAIL` | Lỗi khởi tạo camera | Kiểm tra nguồn 5V, reset lại board |
| `CAPTURE FAIL` | Camera trả về null | Giảm `jpeg_quality` hoặc `frame_size` |
| Nhận diện sai | Dataset ít ảnh | Thêm ảnh từ nhiều góc độ, ánh sáng khác nhau |
| Nhận diện sai | Ngưỡng distance quá cao | Giảm `min_distance < 0.6` xuống `0.5` |

---

## 📌 Ghi chú

- ESP32-CAM chỉ hỗ trợ WiFi **2.4GHz**, không kết nối được 5GHz.
- Flask server và ESP32-CAM phải **cùng mạng LAN**.
- Nên dùng ảnh dataset chụp trong điều kiện ánh sáng tương tự môi trường thực tế.
- Đây là môi trường **development** — không dùng trực tiếp cho production.

---

## 👤 Tác giả

Dự án IoT nhận diện khuôn mặt — ESP32-CAM + Python Flask + face_recognition.
