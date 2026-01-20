@echo off
echo ========================================
echo Setting up gRPC Services
echo ========================================

echo.
echo [1/2] Generating Python code from proto files for Service A...
cd service_a\proto
py -3.13 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate Service A proto files
    exit /b 1
)
echo ✓ Service A proto files generated successfully
cd ..\..

echo.
echo [2/2] Generating Python code from proto files for Service B...
cd service_b\proto
py -3.13 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate Service B proto files
    exit /b 1
)
echo ✓ Service B proto files generated successfully
cd ..\..

echo.
echo ========================================
echo ✅ Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Run Service A (Server): run_service_a.bat
echo 2. Run Service B (Client): run_service_b.bat
echo.
pause
