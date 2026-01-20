import grpc
import sys
import os

# Add the proto directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

import user_pb2
import user_pb2_grpc


class UserServiceClient:
    """Client for UserService gRPC"""
    
    def __init__(self, host='localhost', port='50051'):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            request = user_pb2.UserRequest(user_id=user_id)
            response = self.stub.GetUser(request)
            return response
        except grpc.RpcError as e:
            print(f'❌ Error: {e.details()}')
            return None
    
    def create_user(self, name, email, age):
        """Create a new user"""
        try:
            request = user_pb2.CreateUserRequest(
                name=name,
                email=email,
                age=age
            )
            response = self.stub.CreateUser(request)
            return response
        except grpc.RpcError as e:
            print(f'❌ Error: {e.details()}')
            return None
    
    def list_users(self):
        """List all users"""
        try:
            request = user_pb2.Empty()
            response = self.stub.ListUsers(request)
            return response
        except grpc.RpcError as e:
            print(f'❌ Error: {e.details()}')
            return None
    
    def close(self):
        """Close the gRPC channel"""
        self.channel.close()


def print_user(user):
    """Pretty print user information"""
    print(f'  👤 User ID: {user.user_id}')
    print(f'     Name: {user.name}')
    print(f'     Email: {user.email}')
    print(f'     Age: {user.age}')
    print(f'     Created: {user.created_at}')


def main():
    """Main function to demonstrate client usage"""
    print('=' * 50)
    print('User Service Client (Service B)')
    print('=' * 50)
    
    # Create client
    client = UserServiceClient()
    
    print('\n📋 Listing all users:')
    print('-' * 50)
    response = client.list_users()
    if response:
        for user in response.users:
            print_user(user)
            print()
    
    print('\n➕ Creating a new user:')
    print('-' * 50)
    new_user = client.create_user(
        name='Alice Williams',
        email='alice@example.com',
        age=28
    )
    if new_user:
        print('✅ User created successfully!')
        print_user(new_user)
    
    print('\n🔍 Getting user by ID (user_id=1):')
    print('-' * 50)
    user = client.get_user(1)
    if user:
        print_user(user)
    
    print('\n🔍 Getting non-existent user (user_id=999):')
    print('-' * 50)
    user = client.get_user(999)
    
    print('\n📋 Listing all users after creation:')
    print('-' * 50)
    response = client.list_users()
    if response:
        for user in response.users:
            print_user(user)
            print()
    
    # Close connection
    client.close()
    print('✅ Client connection closed')


if __name__ == '__main__':
    main()
