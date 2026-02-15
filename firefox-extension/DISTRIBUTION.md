# Firefox Extension Distribution Guide

This guide covers how to build, sign, and distribute the Decoy Service Firefox extension.

## Quick Start

```bash
cd firefox-extension
./build-xpi.sh
```

This creates a `.xpi` file in the `dist/` directory ready for signing.

## Mozilla Signing Process

Firefox requires all extensions to be signed by Mozilla before they can be permanently installed. There are two distribution options:

### Option 1: Self-Distributed (Unlisted) - **Recommended**

Best for: Sharing with friends, private distribution, privacy-focused tools

**Advantages:**
- No public review process
- Fast approval (usually automated within minutes)
- You control distribution
- Can update at your own pace
- More privacy (not searchable on AMO)

**Steps:**

1. **Create Mozilla Account**
   - Go to https://addons.mozilla.org
   - Sign up or log in

2. **Submit for Signing**
   - Visit https://addons.mozilla.org/developers/
   - Click "Submit a New Add-on"
   - Choose **"On your own"** (self-distributed/unlisted)
   - Upload your `.xpi` file from `dist/` directory
   - Fill in required fields (minimal for unlisted)

3. **Automated Review**
   - Most unlisted add-ons are auto-approved within minutes
   - Checks for malware, security issues, basic compliance
   - No human review for unlisted add-ons

4. **Download Signed .xpi**
   - Once approved, download the signed `.xpi` file
   - This is what you distribute to friends
   - Store it in your GitHub releases or file hosting

5. **Distribute to Friends**
   - Share the signed `.xpi` file
   - Friends double-click to install (permanent installation)
   - Or drag-and-drop into Firefox
   - Updates require distributing new signed versions

### Option 2: Listed on AMO (Public)

Best for: Public tools, wider distribution, automatic updates

**Advantages:**
- Searchable on addons.mozilla.org
- Automatic updates for users
- Wider reach and discoverability
- Mozilla CDN hosting

**Disadvantages:**
- Human review required (can take days/weeks)
- Must follow strict AMO policies
- Public scrutiny
- Requires ongoing maintenance

**Steps:**

1. Go to https://addons.mozilla.org/developers/
2. Choose **"On this site"** (listed)
3. Submit for review
4. Wait for human review (typically 1-7 days)
5. Once approved, it's publicly available

## Building the Extension

### Manual Build

```bash
cd firefox-extension
mkdir -p dist
zip -r -FS dist/decoy-service-1.0.0.xpi \
  manifest.json \
  background.js \
  daemon-client.js \
  popup.html \
  popup.js \
  popup.css \
  icons/ \
  pages/ \
  -x "*.DS_Store"
```

### Using Build Script

```bash
./build-xpi.sh
```

The script:
- Cleans previous builds
- Copies all necessary files
- Creates versioned `.xpi` package
- Shows next steps for signing

## Version Management

Update version in `manifest.json`:

```json
{
  "version": "1.0.1"
}
```

Then rebuild:

```bash
./build-xpi.sh
```

## Distribution Methods

### GitHub Releases (Recommended)

1. Create a new release on GitHub
2. Upload the signed `.xpi` file
3. Share the release URL with friends

```bash
# Example release URL
https://github.com/Nishantj6/decoy-service/releases/download/v1.0.0/decoy-service-1.0.0.xpi
```

### Direct File Sharing

- Upload to cloud storage (Dropbox, Google Drive)
- Host on your own website
- Share via email/messaging

## Installation for Users

### From Signed .xpi

**Method 1: Double-click**
- Download the `.xpi` file
- Double-click it
- Firefox prompts to install
- Click "Add" to confirm

**Method 2: Drag and Drop**
- Download the `.xpi` file
- Open Firefox
- Drag `.xpi` into Firefox window
- Click "Add" to confirm

**Method 3: Manual Install**
- Type `about:addons` in Firefox
- Click gear icon → "Install Add-on From File"
- Select the `.xpi` file
- Click "Add"

## Updating the Extension

### For Self-Distributed

1. Update version in `manifest.json`
2. Build new `.xpi`: `./build-xpi.sh`
3. Submit new version to Mozilla for signing
4. Distribute new signed `.xpi` to users
5. Users must manually install the update

### For Listed on AMO

1. Update version in `manifest.json`
2. Build new `.xpi`
3. Submit update to AMO
4. After approval, users get automatic updates

## Troubleshooting

### "This add-on could not be installed because it has not been verified"

- The `.xpi` is not signed by Mozilla
- Submit it to addons.mozilla.org for signing
- Or load it temporarily via `about:debugging` for testing

### "This add-on is not compatible with your version of Firefox"

- Check `manifest.json` browser compatibility
- Update Firefox to latest version
- Verify Manifest V3 syntax

### Signing Rejected

Common reasons:
- Minified/obfuscated code without source
- External script loading
- Suspicious network requests
- Invalid permissions

**Fix:**
- Review Mozilla's policies
- Check automated validator messages
- Fix issues and resubmit

## Development Workflow

### Testing (Unsigned)

```bash
# Load temporary extension for testing
1. Open Firefox
2. Go to about:debugging
3. Click "This Firefox"
4. Click "Load Temporary Add-on"
5. Select manifest.json
```

### Release (Signed)

```bash
# Build and sign for distribution
1. ./build-xpi.sh
2. Submit dist/*.xpi to addons.mozilla.org
3. Download signed version
4. Distribute to users
```

## Security Notes

- Always sign extensions before distribution
- Never share your Mozilla API keys
- Keep source code in version control
- Verify signed `.xpi` integrity before sharing
- Use HTTPS for distribution URLs

## Resources

- **Mozilla Developer Hub**: https://extensionworkshop.com/
- **Submission Guide**: https://extensionworkshop.com/documentation/publish/submitting-an-add-on/
- **Signing API**: https://extensionworkshop.com/documentation/develop/web-ext-command-reference/#web-ext-sign
- **Distribution Options**: https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/

## Automated Signing (Advanced)

For frequent updates, use `web-ext` CLI:

```bash
# Install web-ext
npm install -g web-ext

# Get API credentials from addons.mozilla.org
# Tools → API Key Management

# Sign automatically
web-ext sign \
  --api-key=YOUR_API_KEY \
  --api-secret=YOUR_API_SECRET \
  --channel=unlisted
```

This automates the build + sign + download workflow.

## Summary

**For your use case (sharing with friends):**

1. ✅ Build: `./build-xpi.sh`
2. ✅ Sign: Upload to addons.mozilla.org (unlisted)
3. ✅ Distribute: Share signed `.xpi` via GitHub releases
4. ✅ Install: Friends double-click the file

**Estimated time:** 10-15 minutes for first signing, ~5 minutes for updates

The unlisted/self-distributed option is perfect for privacy-focused tools shared with friends!
