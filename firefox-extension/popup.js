// Popup script
let serviceStatus = {
    isRunning: false,
    sessionStartTime: null,
    stats: {
        sitesVisited: 0,
        clicksMade: 0,
        searchesPerformed: 0
    }
};

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('toggle-btn');
    const stopBtn = document.getElementById('stop-btn');

    // Load status from storage
    chrome.storage.local.get(['serviceRunning', 'sessionStats'], (result) => {
        serviceStatus.isRunning = result.serviceRunning || false;
        serviceStatus.stats = result.sessionStats || {
            sitesVisited: 0,
            clicksMade: 0,
            searchesPerformed: 0
        };

        updateUI();
    });

    // Toggle button listener
    toggleBtn.addEventListener('click', () => {
        if (!serviceStatus.isRunning) {
            startService();
        }
    });

    // Stop button listener
    stopBtn.addEventListener('click', () => {
        if (serviceStatus.isRunning) {
            stopService();
        }
    });

    // Update UI every second
    setInterval(updateUI, 1000);
});

function startService() {
    // Send message to background script
    chrome.runtime.sendMessage({
        action: 'startService'
    }, (response) => {
        if (response && response.success) {
            serviceStatus.isRunning = true;
            serviceStatus.sessionStartTime = Date.now();
            
            // Save to storage
            chrome.storage.local.set({
                serviceRunning: true,
                sessionStartTime: serviceStatus.sessionStartTime
            });

            showNotification('Decoy Service started!');
            updateUI();
        } else {
            showNotification('Failed to start service', 'error');
        }
    });
}

function stopService() {
    // Send message to background script
    chrome.runtime.sendMessage({
        action: 'stopService'
    }, (response) => {
        if (response && response.success) {
            serviceStatus.isRunning = false;
            
            // Save to storage
            chrome.storage.local.set({
                serviceRunning: false
            });

            showNotification('Decoy Service stopped');
            updateUI();
        } else {
            showNotification('Failed to stop service', 'error');
        }
    });
}

function updateUI() {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const toggleBtn = document.getElementById('toggle-btn');
    const stopBtn = document.getElementById('stop-btn');
    const statStatus = document.getElementById('stat-status');
    const statTime = document.getElementById('stat-time');
    const statVisits = document.getElementById('stat-visits');
    const statClicks = document.getElementById('stat-clicks');
    const statSearches = document.getElementById('stat-searches');

    // Update status indicator
    if (serviceStatus.isRunning) {
        statusIndicator.classList.add('active');
        statusText.textContent = '🟢 Service Running';
        toggleBtn.disabled = true;
        stopBtn.disabled = false;
        statStatus.textContent = 'Active';
    } else {
        statusIndicator.classList.remove('active');
        statusText.textContent = '🔴 Service Inactive';
        toggleBtn.disabled = false;
        stopBtn.disabled = true;
        statStatus.textContent = 'Inactive';
    }

    // Update time
    if (serviceStatus.isRunning && serviceStatus.sessionStartTime) {
        const elapsed = Math.floor((Date.now() - serviceStatus.sessionStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        statTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    // Update stats
    statVisits.textContent = serviceStatus.stats.sitesVisited;
    statClicks.textContent = serviceStatus.stats.clicksMade;
    statSearches.textContent = serviceStatus.stats.searchesPerformed;
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type === 'error' ? 'error' : ''}`;

    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'updateStats') {
        serviceStatus.stats = request.stats;
        
        // Save to storage
        chrome.storage.local.set({
            sessionStats: serviceStatus.stats
        });

        updateUI();
    }
});
