"""
Daemon Client - Communicates with DecoyDaemon via Unix socket IPC
Replaces HTTP API calls with socket-based communication
"""

import socket
import json
import os
from pathlib import Path

SOCKET_PATH = Path.home() / '.decoy-service' / 'daemon.sock'

class DaemonClient:
    def __init__(self):
        self.socket = None
    
    def connect(self):
        """Connect to daemon socket"""
        if not SOCKET_PATH.exists():
            raise ConnectionError(f"Daemon socket not found at {SOCKET_PATH}. Is daemon running?")
        
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(str(SOCKET_PATH))
    
    def disconnect(self):
        """Close socket connection"""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def send_command(self, command, **kwargs):
        """Send command to daemon and get response"""
        try:
            self.connect()
            
            # Prepare request
            request = {'command': command}
            request.update(kwargs)
            
            # Send request
            request_json = json.dumps(request)
            self.socket.sendall(request_json.encode('utf-8'))
            
            # Receive response
            response_data = b''
            while True:
                try:
                    chunk = self.socket.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk
                except socket.timeout:
                    break
            
            # Parse response
            response = json.loads(response_data.decode('utf-8'))
            return response
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        finally:
            self.disconnect()
    
    def start(self):
        """Start the service"""
        return self.send_command('start')
    
    def stop(self):
        """Stop the service"""
        return self.send_command('stop')
    
    def status(self):
        """Get service status"""
        return self.send_command('status')
    
    def activity_log(self):
        """Get activity log"""
        return self.send_command('activity-log')
    
    def shutdown(self):
        """Shutdown daemon"""
        return self.send_command('shutdown')

if __name__ == '__main__':
    # Test client
    client = DaemonClient()
    print("Testing daemon client...")
    
    print("\n1. Getting status...")
    status = client.status()
    print(json.dumps(status, indent=2))
    
    print("\n2. Starting service...")
    result = client.start()
    print(json.dumps(result, indent=2))
    
    print("\n3. Getting status again...")
    status = client.status()
    print(json.dumps(status, indent=2))
