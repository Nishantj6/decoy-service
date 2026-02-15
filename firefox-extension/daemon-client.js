/**
 * Daemon Client Bridge for Firefox Extension
 *
 * IMPORTANT: Due to Firefox browser sandbox limitations, this extension cannot
 * directly access Unix domain sockets. As a workaround, it communicates with
 * the daemon via an HTTP API fallback.
 *
 * REQUIREMENT: You must run BOTH processes for the extension to work:
 *   1. daemon.py - Background service (Unix socket IPC)
 *   2. api_server.py - HTTP bridge for browser extension (port 9999)
 *
 * Setup:
 *   python3 daemon.py &           # Start daemon
 *   python3 api_server.py &       # Start HTTP bridge
 *
 * Future improvements could use Firefox Native Messaging API or WebSocket bridge.
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
    async sendCommand(command) {
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error(`Daemon command timeout: ${command}`));
            }, this.timeout);

            // WORKAROUND: Use HTTP bridge because Firefox cannot access Unix sockets
            // This requires api_server.py to be running alongside daemon.py
            // Firefox sandbox prevents direct Unix socket access from extensions
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
