// Background script - handles daemon communication
var API_BASE = "http://localhost:9999/api";

/**
 * HTTP request to daemon API with retry.
 * The daemon auto-starts on boot via LaunchAgent, so it should always be up.
 * Retries a few times to handle the case where daemon is still starting.
 */
function apiRequest(path, method, retries) {
    method = method || "GET";
    retries = retries || 0;
    var url = API_BASE + path;

    return fetch(url, { method: method })
        .then(function(resp) { return resp.json(); })
        .catch(function(err) {
            if (retries > 0) {
                return new Promise(function(resolve) {
                    setTimeout(resolve, 1500);
                }).then(function() {
                    return apiRequest(path, method, retries - 1);
                });
            }
            throw err;
        });
}

// ---- Message handler from popup ----

browser.runtime.onMessage.addListener(function(request, _sender, sendResponse) {
    if (request.action === "startService") {
        // Retry a few times in case daemon is still booting
        apiRequest("/start", "POST", 3)
            .then(function(data) { sendResponse({ success: true, data: data }); })
            .catch(function(err) { sendResponse({ success: false, error: "Daemon offline. Run setup-daemon.sh to fix." }); });
        return true;
    }

    if (request.action === "stopService") {
        apiRequest("/stop", "POST")
            .then(function(data) { sendResponse({ success: true, data: data }); })
            .catch(function(err) { sendResponse({ success: false, error: err.message }); });
        return true;
    }

    if (request.action === "getStatus") {
        apiRequest("/status", "GET")
            .then(function(data) {
                sendResponse({
                    running: data.running || false,
                    stats: data.stats || {},
                    daemonOnline: true
                });
            })
            .catch(function() {
                sendResponse({
                    running: false,
                    stats: {},
                    daemonOnline: false
                });
            });
        return true;
    }
});

// ---- Periodic status sync ----

setInterval(function() {
    apiRequest("/status", "GET")
        .then(function(data) {
            return { running: data.running || false, stats: data.stats || {}, daemonOnline: true };
        })
        .catch(function() {
            return { running: false, stats: {}, daemonOnline: false };
        })
        .then(function(status) {
            browser.runtime.sendMessage({
                action: "statusUpdate",
                running: status.running,
                stats: status.stats,
                daemonOnline: status.daemonOnline
            }).catch(function() {});
        });
}, 2000);
