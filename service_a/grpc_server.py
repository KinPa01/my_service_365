import grpc
from concurrent import futures
import time
from datetime import datetime
import sys
import os

# Add the proto directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

import user_pb2
import user_pb2_grpc


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    """Implementation of UserService"""
    
    def __init__(self):
        # In-memory storage for users
        self.users = {}
        self.next_user_id = 1
        
        # Add some sample users
        self._add_sample_users()
    
    def _add_sample_users(self):
        """Add sample users for testing"""
        sample_users = [
            {"name": "John Doe", "email": "john@example.com", "age": 30},
            {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
            {"name": "Bob Johnson", "email": "bob@example.com", "age": 35},
        ]
        
        for user_data in sample_users:
            self.users[self.next_user_id] = {
                "user_id": self.next_user_id,
                "name": user_data["name"],
                "email": user_data["email"],
                "age": user_data["age"],
                "created_at": datetime.now().isoformat()
            }
            self.next_user_id += 1
    
    def GetUser(self, request, context):
        """Get user by ID"""
        user_id = request.user_id
        
        if user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User with ID {user_id} not found')
            return user_pb2.UserResponse()
        
        user = self.users[user_id]
        return user_pb2.UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            age=user["age"],
            created_at=user["created_at"]
        )
    
    def CreateUser(self, request, context):
        """Create a new user"""
        user_id = self.next_user_id
        self.next_user_id += 1
        
        user = {
            "user_id": user_id,
            "name": request.name,
            "email": request.email,
            "age": request.age,
            "created_at": datetime.now().isoformat()
        }
        
        self.users[user_id] = user
        
        return user_pb2.UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            age=user["age"],
            created_at=user["created_at"]
        )
    
    def ListUsers(self, request, context):
        """List all users"""
        users = []
        for user in self.users.values():
            users.append(user_pb2.UserResponse(
                user_id=user["user_id"],
                name=user["name"],
                email=user["email"],
                age=user["age"],
                created_at=user["created_at"]
            ))
        
        return user_pb2.UserListResponse(users=users)


def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    
    port = '50051'
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f'🚀 gRPC Server started on port {port}')
    print(f'📡 Listening for requests...')
    
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        print('\n⏹️  Server stopped')
        server.stop(0)


if __name__ == '__main__':
    serve()
