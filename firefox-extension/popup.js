// Popup script
let serviceStatus = {
    isRunning: false,
    daemonOnline: false,
    sessionStartTime: null,
    stats: {
        sitesVisited: 0,
        clicksMade: 0,
        searchesPerformed: 0
    }
};

let isStarting = false; // True while daemon + service startup is in progress

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('toggle-btn');
    const stopBtn = document.getElementById('stop-btn');

    // Start fetching live status from background script
    fetchServiceStatus();
    setInterval(fetchServiceStatus, 2000);

    // Start button: handles everything - daemon startup + service start
    toggleBtn.addEventListener('click', () => {
        startService();
    });

    // Stop button
    stopBtn.addEventListener('click', () => {
        stopService();
    });

    // Update UI every second (for timer)
    setInterval(updateUI, 1000);
});

function fetchServiceStatus() {
    daemonClient.status()
        .then(data => {
            const wasRunning = serviceStatus.isRunning;
            serviceStatus.isRunning = data.running || false;
            serviceStatus.daemonOnline = data.daemonOnline !== false;
            serviceStatus.stats = data.stats || {
                sitesVisited: 0,
                clicksMade: 0,
                searchesPerformed: 0
            };

            if (serviceStatus.isRunning && !wasRunning) {
                const durationSeconds = (data.stats?.sessionDurationMinutes || 0) * 60;
                serviceStatus.sessionStartTime = Date.now() - (durationSeconds * 1000);
                isStarting = false;
            } else if (!serviceStatus.isRunning) {
                serviceStatus.sessionStartTime = null;
            }

            updateUI();
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            serviceStatus.daemonOnline = false;
            updateUI();
        });
}

function startService() {
    if (isStarting) return;
    isStarting = true;
    showNotification('Starting service...');
    updateUI();

    daemonClient.start()
        .then(data => {
            if (data.success) {
                serviceStatus.isRunning = true;
                serviceStatus.daemonOnline = true;
                serviceStatus.sessionStartTime = Date.now();
                isStarting = false;
                showNotification('Decoy Service started!');
                fetchServiceStatus();
            } else {
                isStarting = false;
                showNotification('Failed to start: ' + (data.error || 'Unknown error'), 'error');
            }
            updateUI();
        })
        .catch(error => {
            isStarting = false;
            showNotification('Error: ' + error.message, 'error');
            console.error('Error starting service:', error);
            updateUI();
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
                showNotification('Failed to stop: ' + (data.error || 'Unknown error'), 'error');
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
    const toggleText = document.getElementById('toggle-text');
    const stopBtn = document.getElementById('stop-btn');
    const statStatus = document.getElementById('stat-status');
    const statTime = document.getElementById('stat-time');
    const statVisits = document.getElementById('stat-visits');
    const statClicks = document.getElementById('stat-clicks');
    const statSearches = document.getElementById('stat-searches');

    if (isStarting) {
        // Starting state - daemon being launched + service starting
        statusIndicator.classList.remove('active');
        statusIndicator.classList.add('starting');
        statusText.textContent = 'Starting...';
        toggleBtn.disabled = true;
        stopBtn.disabled = true;
        toggleText.textContent = 'Starting...';
        statStatus.textContent = 'Starting';
    } else if (serviceStatus.isRunning) {
        // Running state
        statusIndicator.classList.remove('starting');
        statusIndicator.classList.add('active');
        statusText.textContent = 'Service Running';
        toggleBtn.disabled = true;
        stopBtn.disabled = false;
        toggleText.textContent = 'Start Service';
        statStatus.textContent = 'Active';
    } else {
        // Stopped state - show Start button regardless of daemon status
        statusIndicator.classList.remove('active', 'starting');
        statusText.textContent = 'Service Inactive';
        toggleBtn.disabled = false;
        stopBtn.disabled = true;
        toggleText.textContent = 'Start Service';
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

// Listen for status updates broadcast from background script
browser.runtime.onMessage.addListener((request, _sender, _sendResponse) => {
    if (request.action === 'statusUpdate') {
        serviceStatus.isRunning = request.running;
        serviceStatus.daemonOnline = request.daemonOnline !== false;
        serviceStatus.stats = request.stats || serviceStatus.stats;
        if (!isStarting) {
            updateUI();
        }
    }
});
