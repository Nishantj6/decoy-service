#!/usr/bin/env python3
"""
Decoy Service Daemon - Unix Socket-based IPC Server
Provides background service without Flask HTTP overhead
Enables auto-start via LaunchAgent (macOS) / systemd (Linux)
"""

import socket
import json
import os
import signal
import sys
import logging
import threading
from pathlib import Path
from typing import Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Setup logging
log_dir = Path.home() / '.decoy-service'
log_dir.mkdir(exist_ok=True, mode=0o700)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'daemon.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('DecoyDaemon')

SOCKET_PATH = log_dir / 'daemon.sock'
HTTP_PORT = 9999  # Port for Firefox extension HTTP bridge


class HTTPBridgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Firefox extension compatibility"""

    daemon_instance = None  # Will be set by DecoyDaemon

    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"HTTP {args[0]}")

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/status':
            response = self.daemon_instance.cmd_status()
            self.send_json_response(response)
        elif parsed_path.path == '/api/activity-log':
            response = self.daemon_instance.cmd_activity_log()
            self.send_json_response(response)
        elif parsed_path.path == '/api/health':
            self.send_json_response({'success': True, 'status': 'healthy'})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/start':
            response = self.daemon_instance.cmd_start()
            self.send_json_response(response)
        elif parsed_path.path == '/api/stop':
            response = self.daemon_instance.cmd_stop()
            self.send_json_response(response)
        else:
            self.send_error(404, "Not Found")

    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


class DecoyDaemon:
    def __init__(self):
        self.running = True
        self.service_active = False
        self.socket = None
        self.client_threads = []
        self.http_server = None
        self.http_thread = None
        
        # Import service here to avoid early dependencies
        try:
            # Import from the decoy_service module directly
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from decoy_service.decoy_service import DecoyService
            # Use correct config path
            config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decoy_service', 'config')
            self.service = DecoyService(config_dir=config_dir)
            logger.info("✅ DecoyService initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load DecoyService: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.service = None
    
    def handle_client(self, conn: socket.socket, addr: str):
        """Handle individual client connection"""
        try:
            logger.debug(f"Client connected: {addr}")
            
            # Receive request
            request_data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                request_data += chunk
                # Check if we have a complete JSON message
                try:
                    request = json.loads(request_data.decode('utf-8'))
                    break
                except json.JSONDecodeError:
                    continue
            
            if not request_data:
                return
            
            try:
                request = json.loads(request_data.decode('utf-8'))
            except json.JSONDecodeError as e:
                response = {'success': False, 'error': f'Invalid JSON: {e}'}
                conn.sendall(json.dumps(response).encode('utf-8'))
                return
            
            # Process command
            response = self.process_command(request)
            
            # Send response
            response_json = json.dumps(response).encode('utf-8')
            conn.sendall(response_json)
            
        except Exception as e:
            logger.error(f"Error handling client: {e}")
            try:
                response = {'success': False, 'error': str(e)}
                conn.sendall(json.dumps(response).encode('utf-8'))
            except:
                pass
        finally:
            conn.close()
    
    def process_command(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming command"""
        command = request.get('command', 'unknown')
        
        if command == 'start':
            return self.cmd_start()
        elif command == 'stop':
            return self.cmd_stop()
        elif command == 'status':
            return self.cmd_status()
        elif command == 'activity-log':
            return self.cmd_activity_log()
        elif command == 'shutdown':
            return self.cmd_shutdown()
        else:
            return {'success': False, 'error': f'Unknown command: {command}'}
    
    def cmd_start(self) -> Dict[str, Any]:
        """Start the automation service"""
        try:
            if not self.service:
                return {'success': False, 'error': 'Service not initialized'}
            
            if self.service_active:
                return {'success': True, 'message': 'Service already running'}
            
            logger.info("Starting Decoy Service")
            # Start service in a separate thread so daemon stays responsive
            service_thread = threading.Thread(
                target=lambda: self.service.start_session(),
                daemon=False
            )
            service_thread.start()
            self.service_active = True
            
            return {'success': True, 'message': 'Service started'}
        except Exception as e:
            logger.error(f"Failed to start service: {e}")
            return {'success': False, 'error': str(e)}
    
    def cmd_stop(self) -> Dict[str, Any]:
        """Stop the automation service"""
        try:
            if not self.service:
                return {'success': False, 'error': 'Service not initialized'}
            
            if not self.service_active:
                return {'success': True, 'message': 'Service already stopped'}
            
            logger.info("Stopping Decoy Service")
            self.service.stop_session()
            self.service_active = False
            
            return {'success': True, 'message': 'Service stopped'}
        except Exception as e:
            logger.error(f"Failed to stop service: {e}")
            return {'success': False, 'error': str(e)}
    
    def cmd_status(self) -> Dict[str, Any]:
        """Get service status - format for Firefox extension compatibility"""
        try:
            if not self.service:
                return {'success': False, 'error': 'Service not initialized'}

            # Format expected by Firefox extension
            response = {
                'success': True,
                'running': self.service_active,
                'stats': {
                    'sitesVisited': 0,
                    'clicksMade': 0,
                    'searchesPerformed': 0,
                    'sessionDurationMinutes': 0
                }
            }

            # Try to get service stats
            try:
                if hasattr(self.service, 'get_status'):
                    service_status = self.service.get_status()
                    if 'stats' in service_status:
                        response['stats'].update(service_status['stats'])
            except:
                pass

            return response
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {'success': False, 'error': str(e)}
    
    def cmd_activity_log(self) -> Dict[str, Any]:
        """Get activity log"""
        try:
            log_file = log_dir / 'service.log'
            if not log_file.exists():
                return {'success': True, 'activities': []}
            
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            activities = []
            for line in lines[-20:]:  # Last 20 activities
                if 'Visited:' in line or 'Searched:' in line:
                    activities.append(line.strip())
            
            return {'success': True, 'activities': activities}
        except Exception as e:
            logger.error(f"Failed to read activity log: {e}")
            return {'success': False, 'error': str(e)}
    
    def cmd_shutdown(self) -> Dict[str, Any]:
        """Shutdown the daemon"""
        logger.info("Shutdown command received")
        self.running = False
        return {'success': True, 'message': 'Daemon shutting down'}
    
    def start(self):
        """Start the daemon server"""
        logger.info(f"Starting Decoy Daemon on {SOCKET_PATH}")

        # Remove old socket if exists
        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

        # Start HTTP bridge for Firefox extension
        self._start_http_bridge()
        
        try:
            # Create Unix socket
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.bind(str(SOCKET_PATH))
            SOCKET_PATH.chmod(0o600)
            self.socket.listen(5)
            
            logger.info(f"Daemon listening on {SOCKET_PATH}")
            
            # Accept connections
            while self.running:
                try:
                    conn, addr = self.socket.accept()
                    # Handle in thread to accept multiple clients
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(conn, addr),
                        daemon=True
                    )
                    client_thread.start()
                    self.client_threads.append(client_thread)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {e}")
        
        except Exception as e:
            logger.error(f"Failed to start daemon: {e}")
            sys.exit(1)
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown"""
        logger.info("Shutting down daemon")

        # Stop HTTP server
        if self.http_server:
            logger.info("Stopping HTTP bridge")
            self.http_server.shutdown()
            self.http_server.server_close()

        if self.socket:
            self.socket.close()

        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

        # Wait for client threads
        for thread in self.client_threads:
            thread.join(timeout=1.0)

        logger.info("Daemon stopped")
    
    def _start_http_bridge(self):
        """Start HTTP server for Firefox extension compatibility"""
        try:
            # Set daemon instance reference for HTTP handler
            HTTPBridgeHandler.daemon_instance = self

            # Create HTTP server
            self.http_server = HTTPServer(('localhost', HTTP_PORT), HTTPBridgeHandler)

            # Run HTTP server in separate thread
            self.http_thread = threading.Thread(
                target=self.http_server.serve_forever,
                daemon=True
            )
            self.http_thread.start()
            logger.info(f"✅ HTTP bridge started on http://localhost:{HTTP_PORT}")
        except Exception as e:
            logger.error(f"⚠️  Failed to start HTTP bridge: {e}")
            logger.error("Firefox extension will not work, but Unix socket is still available")

    def _signal_handler(self, signum, frame):
        """Handle signals"""
        logger.info(f"Received signal {signum}")
        self.running = False


def main():
    # Add project directory to path for proper imports without changing working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    daemon = DecoyDaemon()
    daemon.start()


if __name__ == '__main__':
    main()
