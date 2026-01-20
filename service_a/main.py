"""
Service A - gRPC Server + Web Interface
Main entry point with both gRPC and HTTP server
"""
import threading
from grpc_server import serve as serve_grpc
from web_server import serve as serve_web

if __name__ == '__main__':
    print('=' * 50)
    print('Starting Service A')
    print('=' * 50)
    
    # Start gRPC server in a separate thread
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    
    # Start web server in main thread
    serve_web()