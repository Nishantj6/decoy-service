// Background service worker
let decoyServiceProcess = null;
let serviceRunning = false;

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startService') {
        if (!serviceRunning) {
            startDecoyService();
            serviceRunning = true;
            sendResponse({ success: true });
        } else {
            sendResponse({ success: false, error: 'Service already running' });
        }
    } else if (request.action === 'stopService') {
        if (serviceRunning) {
            stopDecoyService();
            serviceRunning = false;
            sendResponse({ success: true });
        } else {
            sendResponse({ success: false, error: 'Service not running' });
        }
    } else if (request.action === 'getStatus') {
        sendResponse({ running: serviceRunning });
    }
});

function startDecoyService() {
    // Send message to content script or native messaging
    console.log('🟢 Decoy Service started');
    
    // You would typically:
    // 1. Use native messaging to communicate with Python service
    // 2. Or spawn a child process
    // 3. Or trigger the service via HTTP request
    
    // For now, we'll use a simple HTTP request approach
    // This would require the Python service to expose a REST API
    
    fetch('http://localhost:5000/api/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service started:', data);
    })
    .catch(error => {
        console.error('Error starting service:', error);
    });
}

function stopDecoyService() {
    console.log('🔴 Decoy Service stopped');
    
    fetch('http://localhost:5000/api/stop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Service stopped:', data);
    })
    .catch(error => {
        console.error('Error stopping service:', error);
    });
}

// Simulate activity updates (in real implementation, 
// this would come from the Python service)
setInterval(() => {
    if (serviceRunning) {
        const stats = {
            sitesVisited: Math.floor(Math.random() * 10),
            clicksMade: Math.floor(Math.random() * 50),
            searchesPerformed: Math.floor(Math.random() * 5)
        };

        // Send update to all popup instances
        chrome.runtime.sendMessage({
            action: 'updateStats',
            stats: stats
        }).catch(() => {
            // Popup not open, ignore error
        });
    }
}, 5000);
