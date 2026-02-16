/**
 * Daemon Client Bridge for Firefox Extension
 *
 * All commands are routed through the background script, which handles:
 *   1. HTTP communication with daemon on localhost:9999
 *   2. Auto-starting the daemon via Native Messaging if it's offline
 *   3. Retrying after daemon startup
 *
 * The popup never talks to the daemon directly - background.js is the
 * single point of contact, ensuring the daemon is always started when needed.
 */

class DaemonClient {
    /**
     * Start the decoy service.
     * If the daemon isn't running, background.js will auto-start it first.
     */
    async start() {
        return browser.runtime.sendMessage({ action: "startService" });
    }

    /**
     * Stop the decoy service.
     */
    async stop() {
        return browser.runtime.sendMessage({ action: "stopService" });
    }

    /**
     * Get current service status.
     * Returns { running, stats, daemonOnline }
     */
    async status() {
        return browser.runtime.sendMessage({ action: "getStatus" });
    }

    /**
     * Explicitly request daemon to be started via native messaging.
     */
    async ensureDaemon() {
        return browser.runtime.sendMessage({ action: "ensureDaemon" });
    }
}

// Create global client instance
const daemonClient = new DaemonClient();
