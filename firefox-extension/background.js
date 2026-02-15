// Background service worker
let decoyServiceProcess = null;

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startService') {
        startDecoyService();
    } else if (request.action === 'stopService') {
        stopDecoyService();
    } else if (request.action === 'getStatus') {
        getServiceStatus().then(status => {
            sendResponse({ running: status.running, stats: status.stats });
        });
        return true; // Keep message channel open
    }
});

function startDecoyService() {
    console.log('🟢 Calling API to start service...');
    fetch('http://localhost:9999/api/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service start response:', data);
    })
    .catch(error => {
        console.error('Error starting service:', error);
    });
}

function stopDecoyService() {
    console.log('🔴 Calling API to stop service...');
    fetch('http://localhost:9999/api/stop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service stop response:', data);
    })
    .catch(error => {
        console.error('Error stopping service:', error);
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

// Periodically sync status with API and broadcast to all popups
setInterval(() => {
    getServiceStatus().then(status => {
        // Send status to all popup instances
        chrome.runtime.sendMessage({
            action: 'statusUpdate',
            running: status.running,
            stats: status.stats
        }).catch(() => {
            // Popup not open, that's fine
        });
    });
}, 1000);
