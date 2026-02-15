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

    // Start fetching live status from API
    fetchServiceStatus();
    setInterval(fetchServiceStatus, 1000);

    // Toggle button listener
    toggleBtn.addEventListener('click', () => {
        startService();
    });

    // Stop button listener
    stopBtn.addEventListener('click', () => {
        stopService();
    });

    // Update UI every second
    setInterval(updateUI, 1000);
});

function fetchServiceStatus() {
    // Get real status from daemon via IPC client
    daemonClient.status()
        .then(data => {
            serviceStatus.isRunning = data.running || false;
            serviceStatus.stats = data.stats || {
                sitesVisited: 0,
                clicksMade: 0,
                searchesPerformed: 0
            };
            
            // Use actual session duration from API instead of local tracking
            if (serviceStatus.isRunning && data.stats && data.stats.sessionDurationMinutes !== undefined) {
                // Calculate start time from duration
                const durationSeconds = (data.stats.sessionDurationMinutes || 0) * 60;
                serviceStatus.sessionStartTime = Date.now() - (durationSeconds * 1000);
            } else if (!serviceStatus.isRunning) {
                serviceStatus.sessionStartTime = null;
            }
            
            updateUI();
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

function startService() {
    showNotification('Starting service...');
    
    daemonClient.start()
        .then(data => {
            if (data.success) {
                serviceStatus.isRunning = true;
                serviceStatus.sessionStartTime = Date.now();
                showNotification('Decoy Service started!');
                fetchServiceStatus();
            } else {
                showNotification('Failed to start service: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            showNotification('Error: ' + error.message, 'error');
            console.error('Error starting service:', error);
        });
}

function stopService() {
    showNotification('Stopping service...');
    
    daemonClient.stop()
        .then(data => {
            if (data.success) {
                serviceStatus.isRunning = false;
                serviceStatus.sessionStartTime = null;
                showNotification('Decoy Service stopped');
                fetchServiceStatus();
            } else {
                showNotification('Failed to stop service: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            showNotification('Error: ' + error.message, 'error');
            console.error('Error stopping service:', error);
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
    if (request.action === 'statusUpdate') {
        serviceStatus.isRunning = request.running;
        serviceStatus.stats = request.stats || serviceStatus.stats;
        updateUI();
    }
});
