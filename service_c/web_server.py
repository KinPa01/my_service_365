"""
Service C - Web Interface (Port 8003)
FastAPI web UI for Data Service
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import grpc
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

import schema_pb2
import schema_pb2_grpc

app = FastAPI(title="Service C - Data Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataRequest(BaseModel):
    name: str

def get_service_c_stub():
    channel = grpc.insecure_channel('localhost:50052')
    return schema_pb2_grpc.MyServiceStub(channel)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Web UI Homepage"""
    html_content = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service C - Data Service</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                min-height: 100vh;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                max-width: 600px;
                width: 100%;
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
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .card h2 {
                color: #4facfe;
                margin-bottom: 20px;
                text-align: center;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
            }
            input:focus {
                outline: none;
                border-color: #4facfe;
            }
            button {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1.1em;
                font-weight: bold;
                width: 100%;
                transition: all 0.3s ease;
                margin-top: 10px;
            }
            button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
            }
            .result {
                margin-top: 20px;
                padding: 20px;
                border-radius: 8px;
                background: #e3f2fd;
                border-left: 4px solid #4facfe;
                display: none;
            }
            .result.show {
                display: block;
                animation: slideIn 0.3s ease;
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Service C - Data Service</h1>
            <p class="subtitle">🌐 http://localhost:8003 | gRPC Port: 50052</p>
            
            <div class="card">
                <h2>📡 เรียกใช้ Service C</h2>
                <p style="color: #666; margin-bottom: 15px; text-align: center;">
                    กรอกชื่อของคุณเพื่อรับข้อความจาก gRPC Server
                </p>
                <input type="text" id="name" placeholder="ชื่อของคุณ" autofocus>
                <button onclick="callService()">🚀 ส่งคำขอ</button>
                
                <div id="result" class="result"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('name').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    callService();
                }
            });
            
            async function callService() {
                const name = document.getElementById('name').value;
                if (!name) {
                    alert('กรุณากรอกชื่อ');
                    return;
                }
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<p>⏳ กำลังส่งคำขอ...</p>';
                resultDiv.className = 'result show';
                
                try {
                    const response = await fetch('/api/data', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name })
                    });
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <strong>✅ ได้รับข้อความจาก gRPC Server:</strong><br><br>
                        <div style="background: white; padding: 15px; border-radius: 8px; margin-top: 10px;">
                            💬 ${data.message}
                        </div>
                    `;
                } catch (error) {
                    resultDiv.innerHTML = `<strong>❌ Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/api/data")
async def call_service(request: DataRequest):
    """Call Service C gRPC"""
    try:
        stub = get_service_c_stub()
        grpc_request = schema_pb2.RequestMsg(name=request.name)
        response = stub.GetData(grpc_request)
        
        return {"message": response.message}
    except Exception as e:
        return {"error": str(e)}

def serve():
    """Start the web server"""
    import uvicorn
    print('🌐 Web Interface starting on http://localhost:8003')
    uvicorn.run(app, host="0.0.0.0", port=8003)

if __name__ == "__main__":
    serve()
