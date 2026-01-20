"""
Service A - Web Interface (Port 8001)
FastAPI web UI for User Service
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import grpc
import sys
import os

# Add proto directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

import user_pb2
import user_pb2_grpc

app = FastAPI(title="Service A - User Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateUserRequest(BaseModel):
    name: str
    email: str
    age: int

def get_user_service_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return user_pb2_grpc.UserServiceStub(channel)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Web UI Homepage"""
    html_content = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service A - User Service</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            h1 {
                color: white;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin-bottom: 20px;
            }
            .card h2 {
                color: #667eea;
                margin-bottom: 15px;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1em;
                font-weight: bold;
                transition: all 0.3s ease;
                margin: 5px;
            }
            button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            input {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            .user-item {
                background: #f9f9f9;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                background: #f5f5f5;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👥 Service A - User Service</h1>
            <p class="subtitle">🌐 http://localhost:8001 | gRPC Port: 50051</p>
            
            <div class="card">
                <h2>📋 รายการ Users</h2>
                <button onclick="listUsers()">🔄 โหลดข้อมูล Users</button>
                <div id="userList" class="result" style="display:none;"></div>
            </div>
            
            <div class="card">
                <h2>➕ สร้าง User ใหม่</h2>
                <input type="text" id="name" placeholder="ชื่อ">
                <input type="email" id="email" placeholder="อีเมล">
                <input type="number" id="age" placeholder="อายุ">
                <button onclick="createUser()">✨ สร้าง User</button>
                <div id="createResult" class="result" style="display:none;"></div>
            </div>
            
            <div class="card">
                <h2>🔍 ค้นหา User ตาม ID</h2>
                <input type="number" id="userId" placeholder="User ID">
                <button onclick="getUser()">🔍 ค้นหา</button>
                <div id="getUserResult" class="result" style="display:none;"></div>
            </div>
        </div>
        
        <script>
            async function listUsers() {
                try {
                    const response = await fetch('/api/users');
                    const data = await response.json();
                    const div = document.getElementById('userList');
                    
                    let html = '<h3>รายการ Users ทั้งหมด:</h3>';
                    if (data.users && data.users.length > 0) {
                        data.users.forEach(user => {
                            html += `
                                <div class="user-item">
                                    <strong>👤 ${user.name}</strong><br>
                                    📧 ${user.email} | 🎂 ${user.age} ปี<br>
                                    🆔 ID: ${user.user_id} | 📅 ${user.created_at}
                                </div>
                            `;
                        });
                    } else {
                        html += '<p>ไม่มี users</p>';
                    }
                    div.innerHTML = html;
                    div.style.display = 'block';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function createUser() {
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const age = parseInt(document.getElementById('age').value);
                
                if (!name || !email || !age) {
                    alert('กรุณากรอกข้อมูลให้ครบถ้วน');
                    return;
                }
                
                try {
                    const response = await fetch('/api/users', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, email, age })
                    });
                    const data = await response.json();
                    const div = document.getElementById('createResult');
                    
                    div.innerHTML = `
                        <strong>✅ สร้าง User สำเร็จ!</strong><br>
                        👤 ${data.name} | 📧 ${data.email} | 🎂 ${data.age} ปี<br>
                        🆔 ID: ${data.user_id}
                    `;
                    div.style.display = 'block';
                    
                    document.getElementById('name').value = '';
                    document.getElementById('email').value = '';
                    document.getElementById('age').value = '';
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function getUser() {
                const userId = document.getElementById('userId').value;
                if (!userId) {
                    alert('กรุณากรอก User ID');
                    return;
                }
                
                try {
                    const response = await fetch(`/api/users/${userId}`);
                    const data = await response.json();
                    const div = document.getElementById('getUserResult');
                    
                    div.innerHTML = `
                        <div class="user-item">
                            <strong>👤 ${data.name}</strong><br>
                            📧 ${data.email} | 🎂 ${data.age} ปี<br>
                            🆔 ID: ${data.user_id} | 📅 ${data.created_at}
                        </div>
                    `;
                    div.style.display = 'block';
                } catch (error) {
                    alert('Error: User not found');
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/users")
async def list_users():
    """Get all users"""
    try:
        stub = get_user_service_stub()
        request = user_pb2.Empty()
        response = stub.ListUsers(request)
        
        users = []
        for user in response.users:
            users.append({
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "created_at": user.created_at
            })
        
        return {"users": users}
    except Exception as e:
        return {"users": [], "error": str(e)}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID"""
    try:
        stub = get_user_service_stub()
        request = user_pb2.UserRequest(user_id=user_id)
        response = stub.GetUser(request)
        
        return {
            "user_id": response.user_id,
            "name": response.name,
            "email": response.email,
            "age": response.age,
            "created_at": response.created_at
        }
    except Exception as e:
        return {"error": "User not found"}

@app.post("/api/users")
async def create_user(user: CreateUserRequest):
    """Create new user"""
    try:
        stub = get_user_service_stub()
        request = user_pb2.CreateUserRequest(
            name=user.name,
            email=user.email,
            age=user.age
        )
        response = stub.CreateUser(request)
        
        return {
            "user_id": response.user_id,
            "name": response.name,
            "email": response.email,
            "age": response.age,
            "created_at": response.created_at
        }
    except Exception as e:
        return {"error": str(e)}

def serve():
    """Start the web server"""
    import uvicorn
    print('🌐 Web Interface starting on http://localhost:8001')
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    serve()
