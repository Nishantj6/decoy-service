// Options page script
const defaultSettings = {
    intensity: 'medium',
    interval: 5,
    sessionDuration: 30,
    headless: true,
    rotateAgents: true,
    enableScrolling: true,
    autoStart: false,
    logLevel: 'info',
    categories: ['news', 'tech', 'education', 'entertainment', 'lifestyle']
};

// Load settings
document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.sync.get(defaultSettings, (settings) => {
        document.getElementById('intensity').value = settings.intensity;
        document.getElementById('interval').value = settings.interval;
        updateIntervalValue();
        
        document.getElementById('session-duration').value = settings.sessionDuration;
        updateDurationValue();
        
        document.getElementById('headless').checked = settings.headless;
        document.getElementById('rotate-agents').checked = settings.rotateAgents;
        document.getElementById('enable-scrolling').checked = settings.enableScrolling;
        document.getElementById('auto-start').checked = settings.autoStart;
        document.getElementById('log-level').value = settings.logLevel;

        // Load categories
        settings.categories.forEach(cat => {
            const checkbox = document.getElementById(`cat-${cat}`);
            if (checkbox) checkbox.checked = true;
        });
    });

    // Update slider values in real-time
    document.getElementById('interval').addEventListener('input', updateIntervalValue);
    document.getElementById('session-duration').addEventListener('input', updateDurationValue);

    // Save settings
    document.getElementById('settings-form').addEventListener('submit', (e) => {
        e.preventDefault();
        saveSettings();
    });

    // Reset to defaults
    document.getElementById('settings-form').addEventListener('reset', () => {
        setTimeout(() => {
            chrome.storage.sync.set(defaultSettings);
            showMessage('Settings reset to defaults', 'success');
        }, 100);
    });
});

function updateIntervalValue() {
    const value = document.getElementById('interval').value;
    document.getElementById('interval-value').textContent = `${value}s`;
}

function updateDurationValue() {
    const value = document.getElementById('session-duration').value;
    document.getElementById('duration-value').textContent = `${value}m`;
}

function saveSettings() {
    // Collect selected categories
    const categories = [];
    document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').forEach(cb => {
        categories.push(cb.value);
    });

    const settings = {
        intensity: document.getElementById('intensity').value,
        interval: parseInt(document.getElementById('interval').value),
        sessionDuration: parseInt(document.getElementById('session-duration').value),
        headless: document.getElementById('headless').checked,
        rotateAgents: document.getElementById('rotate-agents').checked,
        enableScrolling: document.getElementById('enable-scrolling').checked,
        autoStart: document.getElementById('auto-start').checked,
        logLevel: document.getElementById('log-level').value,
        categories: categories
    };

    chrome.storage.sync.set(settings, () => {
        showMessage('✓ Settings saved successfully!', 'success');
    });
}

function showMessage(text, type = 'success') {
    const message = document.getElementById('message');
    message.textContent = text;
    message.className = `message ${type}`;

    setTimeout(() => {
        message.classList.add('hidden');
    }, 3000);
}
