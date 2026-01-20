"""
Service B - Web Interface (Port 8002)
FastAPI web UI for gRPC Client Demo
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import grpc
import sys
import os

# Add proto directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

import user_pb2
import user_pb2_grpc

app = FastAPI(title="Service B - gRPC Client", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        <title>Service B - gRPC Client</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
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
                color: #f5576c;
                margin-bottom: 15px;
            }
            button {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
                box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
            }
            .user-item {
                background: #f9f9f9;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #f5576c;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                background: #f5f5f5;
            }
            .info {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #2196f3;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔌 Service B - gRPC Client</h1>
            <p class="subtitle">🌐 http://localhost:8002 | เชื่อมต่อกับ Service A (Port 50051)</p>
            
            <div class="info">
                <strong>ℹ️ Service B คือ gRPC Client</strong><br>
                เชื่อมต่อกับ Service A เพื่อทดสอบการทำงานของ gRPC
            </div>
            
            <div class="card">
                <h2>🧪 ทดสอบ gRPC Functions</h2>
                <button onclick="testAllFunctions()">▶️ รันการทดสอบทั้งหมด</button>
                <div id="testResult" class="result" style="display:none;"></div>
            </div>
            
            <div class="card">
                <h2>📊 ดูข้อมูล Users จาก Service A</h2>
                <button onclick="viewUsers()">👥 แสดงรายการ Users</button>
                <div id="userList" class="result" style="display:none;"></div>
            </div>
        </div>
        
        <script>
            async function testAllFunctions() {
                const div = document.getElementById('testResult');
                div.innerHTML = '<p>⏳ กำลังทดสอบ...</p>';
                div.style.display = 'block';
                
                try {
                    const response = await fetch('/api/test');
                    const data = await response.json();
                    
                    let html = '<h3>✅ ผลการทดสอบ gRPC:</h3>';
                    html += '<div class="user-item">' + data.message + '</div>';
                    
                    div.innerHTML = html;
                } catch (error) {
                    div.innerHTML = '<p style="color: red;">❌ Error: ' + error.message + '</p>';
                }
            }
            
            async function viewUsers() {
                const div = document.getElementById('userList');
                div.innerHTML = '<p>⏳ กำลังโหลด...</p>';
                div.style.display = 'block';
                
                try {
                    const response = await fetch('/api/users');
                    const data = await response.json();
                    
                    let html = '<h3>รายการ Users จาก Service A:</h3>';
                    if (data.users && data.users.length > 0) {
                        data.users.forEach(user => {
                            html += `
                                <div class="user-item">
                                    <strong>👤 ${user.name}</strong><br>
                                    📧 ${user.email} | 🎂 ${user.age} ปี<br>
                                    🆔 ID: ${user.user_id}
                                </div>
                            `;
                        });
                    } else {
                        html += '<p>ไม่มี users</p>';
                    }
                    div.innerHTML = html;
                } catch (error) {
                    div.innerHTML = '<p style="color: red;">❌ Error: ' + error.message + '</p>';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/test")
async def test_grpc():
    """Test gRPC connection"""
    try:
        stub = get_user_service_stub()
        request = user_pb2.Empty()
        response = stub.ListUsers(request)
        
        return {
            "status": "success",
            "message": f"✅ เชื่อมต่อ Service A สำเร็จ! พบ {len(response.users)} users"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ ไม่สามารถเชื่อมต่อ Service A: {str(e)}"
        }

@app.get("/api/users")
async def list_users():
    """Get all users from Service A"""
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

def serve():
    """Start the web server"""
    import uvicorn
    print('🌐 Web Interface starting on http://localhost:8002')
    uvicorn.run(app, host="0.0.0.0", port=8002)

if __name__ == "__main__":
    serve()
