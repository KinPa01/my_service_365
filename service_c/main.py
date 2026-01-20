"""
Service C - gRPC Server + Web Interface
Main entry point with both gRPC and HTTP server
"""
import threading
import grpc
from concurrent import futures
import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

import schema_pb2, schema_pb2_grpc

class ServiceCHandler(schema_pb2_grpc.MyServiceServicer):
    def GetData(self, request, context):
        print(f"[Server C] รับ gRPC Request จาก: {request.name}")
        return schema_pb2.ReplyMsg(
            message=f"สวัสดี {request.name}, นี่คือข้อมูลจาก Server C (gRPC System)"
        )

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_pb2_grpc.add_MyServiceServicer_to_server(ServiceCHandler(), server)
    server.add_insecure_port('[::]:50052')
    print("🚀 Server C (gRPC) เริ่มทำงานที่ port 50052...")
    server.start()
    try:
        while True: time.sleep(86400)
    except KeyboardInterrupt: server.stop(0)

def serve_web():
    from web_server import serve
    serve()

if __name__ == '__main__':
    print('=' * 50)
    print('Starting Service C')
    print('=' * 50)
    
    # Start gRPC server in a separate thread
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    
    # Start web server in main thread
    serve_web()