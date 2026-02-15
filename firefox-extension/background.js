// Background service worker
let decoyServiceProcess = null;
let serviceRunning = false;

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startService') {
        startDecoyService().then(success => {
            if (success) {
                serviceRunning = true;
                sendResponse({ success: true });
            } else {
                sendResponse({ success: false, error: 'Failed to start service' });
            }
        });
        return true; // Keep message channel open for async response
    } else if (request.action === 'stopService') {
        stopDecoyService().then(success => {
            if (success) {
                serviceRunning = false;
                sendResponse({ success: true });
            } else {
                sendResponse({ success: false, error: 'Failed to stop service' });
            }
        });
        return true; // Keep message channel open for async response
    } else if (request.action === 'getStatus') {
        getServiceStatus().then(status => {
            sendResponse({ running: status.running, stats: status.stats });
        });
        return true; // Keep message channel open for async response
    }
});

function startDecoyService() {
    console.log('🟢 Decoy Service starting...');
    return fetch('http://localhost:9999/api/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service started:', data);
        return data.success === true;
    })
    .catch(error => {
        console.error('Error starting service:', error);
        return false;
    });
}

function stopDecoyService() {
    console.log('🔴 Decoy Service stopping...');
    return fetch('http://localhost:9999/api/stop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service stopped:', data);
        return data.success === true;
    })
    .catch(error => {
        console.error('Error stopping service:', error);
        return false;
    });
}

function getServiceStatus() {
    return fetch('http://localhost:9999/api/status')
    .then(response => response.json())
    .then(data => {
        return {
            running: data.running || false,
            stats: data.stats || {}
        };
    })
    .catch(error => {
        console.error('Error getting status:', error);
        return { running: false, stats: {} };
    });
}

// Periodically sync status with API
setInterval(() => {
    getServiceStatus().then(status => {
        serviceRunning = status.running;
        
        // Send status to all popup instances
        chrome.runtime.sendMessage({
            action: 'statusUpdate',
            running: status.running,
            stats: status.stats
        }).catch(() => {
            // Popup not open, ignore error
        });
    });
}, 2000);
