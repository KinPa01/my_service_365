# My Service 365 - gRPC Services

โปรเจกต์นี้ประกอบด้วย gRPC services สำหรับจัดการข้อมูล User

## 📋 ข้อกำหนดเบื้องต้น

- Python 3.10 หรือสูงกว่า
- Dependencies ที่ระบุใน `requirements.txt`

## 🚀 วิธีการรัน

### ขั้นตอนที่ 1: ติดตั้ง Dependencies (ทำครั้งเดียว)

```bash
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: Generate Proto Files (ทำครั้งเดียว)

**วิธีที่ 1: ใช้ Batch Script (แนะนำ)**
```bash
setup.bat
```

**วิธีที่ 2: Manual**
```bash
# Service A
cd service_a\proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
cd ..\..

# Service B
cd service_b\proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
cd ..\..
```

### ขั้นตอนที่ 3: รัน Services

**รัน Service A (gRPC Server) - Terminal หน้าต่างที่ 1:**
```bash
run_service_a.bat
```
หรือ
```bash
cd service_a
python main.py
```

**รัน Service B (gRPC Client) - Terminal หน้าต่างที่ 2:**
```bash
run_service_b.bat
```
หรือ
```bash
cd service_b
python main.py
```

## 📁 โครงสร้างโปรเจกต์

```
my_service_365/
├── requirements.txt          # Python dependencies
├── setup.bat                 # Script สำหรับ generate proto files
├── run_service_a.bat        # Script สำหรับรัน Service A
├── run_service_b.bat        # Script สำหรับรัน Service B
├── service_a/               # gRPC Server
│   ├── main.py
│   ├── grpc_server.py
│   └── proto/
│       └── user.proto
├── service_b/               # gRPC Client
│   ├── main.py
│   ├── client.py
│   └── proto/
│       └── user.proto
└── service_c/
```

## 🔧 Services

### Service A (gRPC Server)
- **Port:** 50051
- **Functions:**
  - `GetUser` - ดึงข้อมูล user ตาม ID
  - `CreateUser` - สร้าง user ใหม่
  - `ListUsers` - แสดงรายการ users ทั้งหมด

### Service B (gRPC Client)
- เชื่อมต่อกับ Service A
- Demo การใช้งาน gRPC functions ทั้งหมด

## ⚠️ หมายเหตุ

- **ไม่ใช่ FastAPI/Uvicorn:** โปรเจกต์นี้ใช้ gRPC ไม่ใช่ REST API ดังนั้นไม่สามารถใช้คำสั่ง `uvicorn main:app --reload` ได้
- **ต้อง Generate Proto Files:** ก่อนรันครั้งแรก ต้อง compile `.proto` files เป็น Python code ก่อน
- **รัน Server ก่อน:** ต้องรัน Service A (Server) ก่อน จึงจะรัน Service B (Client) ได้

## 🐛 การแก้ปัญหา

### ปัญหา: ModuleNotFoundError: No module named 'user_pb2'
**วิธีแก้:** รัน `setup.bat` เพื่อ generate proto files

### ปัญหา: grpc._channel._InactiveRpcError
**วิธีแก้:** ตรวจสอบว่า Service A (Server) รันอยู่หรือไม่

### ปัญหา: Microsoft Visual C++ 14.0 required
**วิธีแก้:** อัปเดต `requirements.txt` เป็นเวอร์ชันใหม่ที่มี pre-built wheels (ทำไว้แล้ว)
