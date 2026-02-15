# How to Share Decoy Service Extension with Friends

## Step 1: Download the Signed Extension

Since you chose **self-distributed (unlisted)** on Mozilla:

1. Go to [Mozilla Add-ons Developer Hub](https://addons.mozilla.org/developers/addons)
2. Find your "Decoy Service" extension
3. Click on the extension name
4. Look for **"Download Signed File"** or go to **"Manage Status & Versions"**
5. Download the signed `.xpi` file (e.g., `decoy-service-1.0.0-signed.xpi`)

**Important:** You must use the SIGNED .xpi file from Mozilla, not the unsigned one you built locally!

## Step 2: Share the File

### Option A: Direct File Sharing (Recommended)
1. Upload the signed `.xpi` file to a file sharing service:
   - **Google Drive** (set to "Anyone with the link can view")
   - **Dropbox**
   - **GitHub Releases** (create a release in your repo)
   - **Your own web server**

2. Share the download link with your friends

### Option B: GitHub Release (Best for Multiple Friends)
```bash
# In your project directory
git tag v1.0.0
git push origin v1.0.0

# Then:
# 1. Go to GitHub repo → Releases → "Create a new release"
# 2. Choose tag v1.0.0
# 3. Title: "Decoy Service v1.0.0"
# 4. Upload the signed .xpi file
# 5. Publish release
# 6. Share the release URL
```

## Step 3: Installation Instructions for Friends

Send your friends these instructions:

---

### 📦 Installing Decoy Service Extension

#### Method 1: Drag & Drop (Easiest)
1. Download the `.xpi` file (link provided by me)
2. Open Firefox
3. Drag the `.xpi` file into the Firefox window
4. Click **"Add"** when prompted
5. Done! The extension is installed

#### Method 2: Manual Installation
1. Download the `.xpi` file
2. Open Firefox and go to `about:addons`
3. Click the gear icon (⚙️) in the top right
4. Select **"Install Add-on From File..."**
5. Browse to the downloaded `.xpi` file
6. Click **"Add"** when prompted

#### Method 3: Direct Link (If you host it)
1. Open Firefox
2. Go to the direct URL of the `.xpi` file
3. Firefox will prompt to install
4. Click **"Add"**

---

## Step 4: Setting Up the Daemon (Required!)

**Important:** The extension alone won't work - they need to run the daemon too!

### Option A: One-Command Setup (Recommended)

Create a simple install script for your friends:

```bash
#!/bin/bash
# install-decoy-daemon.sh

# Clone the repository
git clone https://github.com/YOUR_USERNAME/decoy-service.git
cd decoy-service

# Install Python dependencies
pip3 install selenium

# Install ChromeDriver (for automation)
# macOS:
brew install chromedriver

# Linux:
# sudo apt-get install chromium-chromedriver

# Start the daemon
python3 daemon.py &

echo "✅ Decoy Service daemon is running!"
echo "Now install the Firefox extension and click Start"
```

### Option B: Manual Setup

Send your friends these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/decoy-service.git
   cd decoy-service
   ```

2. **Install dependencies:**
   ```bash
   pip3 install selenium
   brew install chromedriver  # macOS
   # or
   sudo apt-get install chromium-chromedriver  # Linux
   ```

3. **Start the daemon:**
   ```bash
   python3 daemon.py &
   ```

4. **Verify it's running:**
   ```bash
   curl http://localhost:9999/api/health
   # Should return: {"success": true, "status": "healthy"}
   ```

## Step 5: Testing on Friend's Device

### Pre-Installation Checklist
Ask your friend to verify:
- [ ] Firefox version 109.0 or newer
- [ ] Python 3.7 or newer installed (`python3 --version`)
- [ ] Chrome or Chromium browser installed
- [ ] Terminal/command line access

### Installation Test Steps

1. **Install the extension** (from .xpi file)
2. **Start the daemon:**
   ```bash
   cd decoy-service
   python3 daemon.py
   ```

3. **Test the extension:**
   - Click the extension icon in Firefox toolbar
   - Should see "Service Inactive" status
   - Click **"Start Service"**
   - Should change to "Service Running" 🟢
   - Timer should start counting
   - Stats should update (sites visited, clicks, searches)

4. **Check activity log:**
   - Right-click extension → "Options" or click settings in popup
   - Go to "Activity Log" section
   - Should see websites being visited

5. **Verify daemon logs:**
   ```bash
   tail -f ~/.decoy-service/daemon.log
   ```
   - Should see "Visiting: ..." messages

### Common Issues & Solutions

#### Issue 1: "Connection Failed" Error
**Solution:** Daemon not running
```bash
# Check if daemon is running
ps aux | grep daemon.py

# If not running, start it:
cd decoy-service
python3 daemon.py &
```

#### Issue 2: "Service not initialized"
**Solution:** Missing dependencies
```bash
pip3 install selenium
brew install chromedriver  # or apt-get install
```

#### Issue 3: "Permission denied" on macOS
**Solution:** Grant terminal permissions
- System Preferences → Security & Privacy → Privacy
- Grant Full Disk Access to Terminal app
- Or move project out of Documents folder

#### Issue 4: Extension not installing
**Solution:** Use the SIGNED .xpi file from Mozilla, not the unsigned local build

## Step 6: Distributing Updates

When you release a new version:

1. **Update version in manifest.json:**
   ```json
   "version": "1.1.0"
   ```

2. **Build new .xpi:**
   ```bash
   cd firefox-extension
   python3 build-xpi.py
   ```

3. **Upload to Mozilla:**
   - Go to Developer Hub
   - Upload new version
   - Wait for approval

4. **Download signed file** and share with friends

5. Friends can update by installing the new .xpi file (replaces old version)

## Alternative: Listed Add-on (Public Distribution)

If you want AUTOMATIC updates and easier sharing:

1. **Change distribution to "Listed" on Mozilla:**
   - Go to Developer Hub → Your Add-on → Manage Status
   - Change to "Listed on this site"
   - Complete listing information (description, screenshots, etc.)

2. **After approval, you'll get a public URL like:**
   ```
   https://addons.mozilla.org/firefox/addon/decoy-service/
   ```

3. **Share that URL** - friends just click "Add to Firefox"

4. **Automatic updates** - Firefox auto-updates the extension

**Pros:** Easy sharing, automatic updates
**Cons:** Public visibility, longer review process, must follow stricter guidelines

## Recommended Distribution Method

For sharing with friends (not public):

1. ✅ Use **self-distributed (unlisted)** on Mozilla
2. ✅ Host signed .xpi on **GitHub Releases**
3. ✅ Create simple **install script** for daemon setup
4. ✅ Write clear **README** with setup instructions
5. ✅ Test on a clean machine first

---

## Quick Start for Your Friends

Create this as a README for them:

```markdown
# Decoy Service - Quick Start

## What is this?
Privacy tool that generates fake browsing activity to confuse advertisers.

## Installation (5 minutes)

### 1. Install Extension
- Download [decoy-service-1.0.0-signed.xpi](LINK_HERE)
- Drag into Firefox
- Click "Add"

### 2. Install Daemon
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/decoy-service.git
cd decoy-service
pip3 install selenium
brew install chromedriver  # macOS
python3 daemon.py &
\`\`\`

### 3. Start Service
- Click extension icon in Firefox
- Click "Start Service"
- Done! 🎉

## Usage
- **Start:** Click "Start Service" button
- **Stop:** Click "Stop Service" button
- **Settings:** Right-click extension → Options
- **View Activity:** Settings → Activity Log

## Support
Issues? Open ticket at: https://github.com/YOUR_USERNAME/decoy-service/issues
```

---

## Security Note

**Important:** Only share the signed .xpi with people you trust!

The extension requires:
- Running a background daemon (Python script)
- Browser automation permissions
- Network access

Make sure your friends understand what it does before installing.
