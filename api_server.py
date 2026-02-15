"""
Flask API server for Decoy Service
Provides REST endpoints for the Firefox extension to control the service
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import logging
import sys
import os

# Add decoy_service module to path
sys.path.insert(0, os.path.dirname(__file__))

from decoy_service.decoy_service import DecoyService
from decoy_service.scheduler import DecoyScheduler
from decoy_service.utils import Logger, ConfigManager

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DecoyAPI')

# Global service instance
service = None
service_thread = None
scheduler = None

# Port for the API
API_PORT = 9999

@app.route('/api/start', methods=['POST'])
def start_service():
    """Start the decoy service"""
    global service, service_thread
    
    try:
        if service and service.running:
            return jsonify({'success': False, 'error': 'Service already running'}), 400
        
        # Create new service instance
        service = DecoyService('decoy_service/config')
        
        # Run in separate thread
        service_thread = threading.Thread(target=service.start_session, daemon=True)
        service_thread.start()
        
        logger.info('Decoy service started via API')
        return jsonify({
            'success': True,
            'message': 'Decoy service started',
            'status': 'running'
        }), 200
        
    except Exception as e:
        logger.error(f'Error starting service: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_service():
    """Stop the decoy service"""
    global service
    
    try:
        if service is None or not service.running:
            return jsonify({'success': False, 'error': 'Service not running'}), 400
        
        service.stop_session()
        logger.info('Decoy service stopped via API')
        
        return jsonify({
            'success': True,
            'message': 'Decoy service stopped',
            'status': 'stopped'
        }), 200
        
    except Exception as e:
        logger.error(f'Error stopping service: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current service status"""
    global service
    
    try:
        if service is None:
            return jsonify({
                'running': False,
                'status': 'inactive',
                'stats': {
                    'sitesVisited': 0,
                    'clicksMade': 0,
                    'searchesPerformed': 0
                }
            }), 200
        
        running = service.running if hasattr(service, 'running') else False
        
        # Get statistics
        if running:
            summary = service.tracker.get_summary()
            stats = {
                'sitesVisited': summary.get('websites_visited', 0),
                'clicksMade': summary.get('total_clicks', 0),
                'searchesPerformed': summary.get('search_queries', 0),
                'sessionDurationMinutes': summary.get('session_duration_minutes', 0)
            }
        else:
            stats = {
                'sitesVisited': 0,
                'clicksMade': 0,
                'searchesPerformed': 0,
                'sessionDurationMinutes': 0
            }
        
        return jsonify({
            'running': running,
            'status': 'running' if running else 'stopped',
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting status: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Get or update service configuration"""
    global service
    
    try:
        if request.method == 'GET':
            # Return current configuration
            if service:
                config = service.settings
            else:
                cm = ConfigManager('decoy_service/config')
                config = cm.load_settings()
            
            return jsonify({
                'success': True,
                'config': config
            }), 200
        
        elif request.method == 'POST':
            # Update configuration
            new_config = request.get_json()
            
            if service:
                service.settings.update(new_config)
                logger.info('Service configuration updated via API')
            
            return jsonify({
                'success': True,
                'message': 'Configuration updated'
            }), 200
            
    except Exception as e:
        logger.error(f'Error managing config: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/schedule', methods=['POST'])
def schedule_service():
    """Schedule the service to run at intervals"""
    global scheduler
    
    try:
        data = request.get_json()
        
        if 'interval' not in data or 'duration' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing interval or duration parameter'
            }), 400
        
        interval = int(data.get('interval', 180))  # minutes
        duration = int(data.get('duration', 15))   # minutes
        
        config_manager = ConfigManager('decoy_service/config')
        settings = config_manager.load_settings()
        logger_instance = Logger.setup_logging(settings)
        
        scheduler = DecoyScheduler('decoy_service/config', logger_instance)
        scheduler.schedule_interval(minutes=interval, duration_minutes=duration)
        scheduler.start()
        
        logger.info(f'Service scheduled: every {interval}m for {duration}m')
        
        return jsonify({
            'success': True,
            'message': f'Service scheduled every {interval} minutes',
            'interval': interval,
            'duration': duration
        }), 200
        
    except Exception as e:
        logger.error(f'Error scheduling service: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Decoy Service API',
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f'Server error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f'Starting Decoy Service API on http://localhost:{API_PORT}')
    logger.info('API endpoints:')
    logger.info('  POST   /api/start       - Start the service')
    logger.info('  POST   /api/stop        - Stop the service')
    logger.info('  GET    /api/status      - Get service status')
    logger.info('  GET    /api/config      - Get configuration')
    logger.info('  POST   /api/config      - Update configuration')
    logger.info('  POST   /api/schedule    - Schedule service')
    logger.info('  GET    /api/health      - Health check')
    logger.info('')
    
    app.run(
        host='localhost',
        port=API_PORT,
        debug=False,
        use_reloader=False
    )
