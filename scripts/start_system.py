#!/usr/bin/env python3
"""
Start Script for Grand Hotel Management System
Helps start both backend and frontend servers
"""

import subprocess
import time
import sys
import os
import signal
import threading
from datetime import datetime

def print_status(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    icon = icons.get(status, "ℹ️")
    print(f"[{timestamp}] {icon} {message}")

def check_port_usage(port):
    """Check if a port is in use"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def kill_process_on_port(port):
    """Kill process running on specific port (Windows)"""
    try:
        # Find process using the port
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print_status(f"Killing process {pid} on port {port}", "INFO")
                    subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                    time.sleep(2)
                    return True
    except Exception as e:
        print_status(f"Could not kill process on port {port}: {e}", "WARNING")
    return False

def start_backend():
    """Start the FastAPI backend server"""
    print_status("Starting backend server...", "INFO")
    
    # Check if port 8001 is in use
    if check_port_usage(8001):
        print_status("Port 8001 is in use. Attempting to free it...", "WARNING")
        kill_process_on_port(8001)
        time.sleep(3)
    
    try:
        # Start backend server
        process = subprocess.Popen([sys.executable, 'main.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 bufsize=1,
                                 universal_newlines=True)
        
        print_status("Backend server starting... waiting for initialization", "INFO")
        
        # Monitor backend startup
        startup_timeout = 30  # seconds
        start_time = time.time()
        
        while time.time() - start_time < startup_timeout:
            # Check if backend is responding
            if check_port_usage(8001):
                print_status("Backend server started successfully on http://localhost:8001", "SUCCESS")
                return process
            time.sleep(1)
        
        print_status("Backend server startup timeout", "ERROR")
        process.terminate()
        return None
        
    except Exception as e:
        print_status(f"Failed to start backend server: {e}", "ERROR")
        return None

def start_frontend():
    """Start the React frontend"""
    print_status("Starting frontend...", "INFO")
    
    # Check if frontend directory exists
    frontend_dir = "fruit-store-ui"
    if not os.path.exists(frontend_dir):
        print_status(f"Frontend directory '{frontend_dir}' not found", "ERROR")
        return None
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Check if port 3000 is in use
    port_to_use = 3000
    if check_port_usage(3000):
        print_status("Port 3000 is in use. Will try port 3001...", "WARNING")
        port_to_use = 3001
        
        if check_port_usage(3001):
            print_status("Port 3001 also in use. Attempting to free port 3000...", "WARNING")
            kill_process_on_port(3000)
            time.sleep(3)
            port_to_use = 3000
    
    try:
        # Start frontend
        env = os.environ.copy()
        if port_to_use != 3000:
            env['PORT'] = str(port_to_use)
        
        process = subprocess.Popen(['npm', 'start'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 env=env,
                                 bufsize=1,
                                 universal_newlines=True)
        
        print_status(f"Frontend starting on port {port_to_use}...", "INFO")
        
        # Monitor frontend startup
        startup_timeout = 60  # seconds (npm start takes longer)
        start_time = time.time()
        
        while time.time() - start_time < startup_timeout:
            # Check if frontend is responding
            if check_port_usage(port_to_use):
                print_status(f"Frontend started successfully on http://localhost:{port_to_use}", "SUCCESS")
                return process
            time.sleep(2)
        
        print_status("Frontend startup timeout", "ERROR")
        process.terminate()
        return None
        
    except Exception as e:
        print_status(f"Failed to start frontend: {e}", "ERROR")
        return None
    finally:
        # Return to original directory
        os.chdir("..")

def monitor_process(process, name):
    """Monitor a process and print its output"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                print(f"[{name}] {line.strip()}")
    except:
        pass

def main():
    print("🏨 GRAND HOTEL MANAGEMENT SYSTEM STARTUP")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            print_status("Failed to start backend. Exiting.", "ERROR")
            return
        
        # Wait a bit for backend to fully initialize
        time.sleep(5)
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            print_status("Failed to start frontend. Backend will continue running.", "WARNING")
        
        print("\n" + "=" * 60)
        print_status("🎉 HOTEL MANAGEMENT SYSTEM IS RUNNING!", "SUCCESS")
        print("=" * 60)
        print_status("Backend API: http://localhost:8001", "INFO")
        print_status("API Documentation: http://localhost:8001/docs", "INFO")
        if frontend_process:
            port = 3001 if check_port_usage(3001) and not check_port_usage(3000) else 3000
            print_status(f"Frontend: http://localhost:{port}", "INFO")
        print_status("Press Ctrl+C to stop all servers", "INFO")
        print("=" * 60)
        
        # Monitor processes
        if backend_process:
            backend_thread = threading.Thread(target=monitor_process, args=(backend_process, "BACKEND"))
            backend_thread.daemon = True
            backend_thread.start()
        
        if frontend_process:
            frontend_thread = threading.Thread(target=monitor_process, args=(frontend_process, "FRONTEND"))
            frontend_thread.daemon = True
            frontend_thread.start()
        
        # Wait for processes
        while True:
            if backend_process and backend_process.poll() is not None:
                print_status("Backend process stopped", "WARNING")
                break
            if frontend_process and frontend_process.poll() is not None:
                print_status("Frontend process stopped", "WARNING")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print_status("\nShutting down servers...", "INFO")
    
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
    
    finally:
        # Clean up processes
        if backend_process:
            print_status("Stopping backend server...", "INFO")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process:
            print_status("Stopping frontend server...", "INFO")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print_status("All servers stopped. Goodbye!", "SUCCESS")

if __name__ == "__main__":
    main() 