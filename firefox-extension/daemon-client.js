/**
 * Daemon Client Bridge for Firefox Extension
 * Communicates with decoy_service/daemon_client.py via Python subprocess
 * Provides same interface as HTTP API but uses Unix socket IPC
 */

class DaemonClient {
    constructor() {
        this.connected = false;
        this.timeout = 5000; // 5 second timeout
    }

    /**
     * Send command to daemon and get response
     * Uses Python to communicate via Unix socket
     */
    async sendCommand(command, params = {}) {
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error(`Daemon command timeout: ${command}`));
            }, this.timeout);

            // For now, fall back to HTTP for Firefox native messaging limitations
            // In production, could use subprocess or WebSocket
            const port = 9999;
            const apiUrl = `http://localhost:${port}/api`;

            // Map daemon commands to HTTP endpoints
            let endpoint;
            switch (command) {
                case 'status':
                    endpoint = `${apiUrl}/status`;
                    break;
                case 'start':
                    endpoint = `${apiUrl}/start`;
                    break;
                case 'stop':
                    endpoint = `${apiUrl}/stop`;
                    break;
                case 'activity-log':
                    endpoint = `${apiUrl}/activity-log`;
                    break;
                default:
                    reject(new Error(`Unknown command: ${command}`));
                    return;
            }

            fetch(endpoint)
                .then(response => response.json())
                .then(data => {
                    clearTimeout(timeout);
                    resolve(data);
                })
                .catch(error => {
                    clearTimeout(timeout);
                    reject(error);
                });
        });
    }

    async status() {
        return this.sendCommand('status');
    }

    async start() {
        return this.sendCommand('start');
    }

    async stop() {
        return this.sendCommand('stop');
    }

    async activityLog() {
        return this.sendCommand('activity-log');
    }
}

// Create global client instance
const daemonClient = new DaemonClient();
