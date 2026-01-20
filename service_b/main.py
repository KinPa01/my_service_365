"""
Service B - gRPC Client + Web Interface
Main entry point with web UI
"""
from web_server import serve as serve_web

if __name__ == '__main__':
    print('=' * 50)
    print('Starting Service B')
    print('=' * 50)
    
    # Start web server
    serve_web()