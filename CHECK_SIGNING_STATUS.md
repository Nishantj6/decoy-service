# How to Check if Your Extension is Signed

## Method 1: Mozilla Developer Hub (Recommended)

1. **Go to your developer dashboard:**
   ```
   https://addons.mozilla.org/developers/addons
   ```

2. **Find your "Decoy Service" extension**

3. **Check the status indicators:**

   ### ✅ Signed and Approved
   - Status shows: **"Approved"** or **"Public"**
   - You'll see: "This version is signed"
   - You can download the signed file

   ### ⏳ Pending Review
   - Status shows: **"Awaiting Review"**
   - You'll see: "This version is being reviewed"
   - Cannot download signed file yet (wait for approval)

   ### ❌ Not Signed
   - Status shows: **"Incomplete"** or **"Rejected"**
   - You'll see: "This version needs to be submitted"
   - Need to submit or fix issues

4. **Download signed file:**
   - Click on your extension name
   - Go to "Manage Status & Versions"
   - Look for **"Download Signed File"** button
   - If button exists → Extension is signed ✅
   - If no button → Not signed yet ❌

---

## Method 2: Check File Name

### Signed File Naming
Mozilla adds specific patterns to signed files:

**Unsigned (your build):**
```
decoy-service-1.0.0.xpi
```

**Signed by Mozilla:**
```
decoy_service-1.0.0-an+fx.xpi
decoy_service-1.0.0.xpi
```

**Key indicators:**
- May contain `-an+fx` (means "Approved, Not listed, for Firefox")
- Often uses underscores instead of hyphens
- Different naming from your original build

**If you see your exact original filename → probably NOT signed**

---

## Method 3: Check in Firefox

### After Installing the Extension:

1. **Open Firefox Extensions page:**
   ```
   about:addons
   ```

2. **Find "Decoy Service"**

3. **Check details:**
   - Click on the extension
   - Look at the bottom of the details panel

   ### ✅ Signed Extension Shows:
   ```
   Verified by: Mozilla
   ```
   or
   ```
   Add-on ID: decoy-service@nishantj6.github.io
   Verified: ✓
   ```

   ### ❌ Unsigned Shows:
   ```
   This extension is not signed
   ```
   or
   ```
   Could not be verified for use in Firefox
   ```

---

## Method 4: Inspect XPI File Contents

### Advanced Check (for nerds):

1. **Rename .xpi to .zip:**
   ```bash
   cp decoy-service-1.0.0.xpi decoy-service.zip
   ```

2. **Extract it:**
   ```bash
   unzip decoy-service.zip -d extracted/
   ```

3. **Check for Mozilla signature files:**
   ```bash
   ls -la extracted/META-INF/
   ```

   **Signed extension contains:**
   ```
   META-INF/
   ├── cose.manifest
   ├── cose.sig
   └── manifest.mf
   ```

   **Unsigned extension:**
   - No `META-INF` folder
   - Or empty `META-INF` folder

4. **Quick command:**
   ```bash
   unzip -l decoy-service-1.0.0.xpi | grep META-INF
   ```

   **If output shows META-INF files → Signed ✅**
   **If no output → Unsigned ❌**

---

## Method 5: Try Installing in Regular Firefox

### The Definitive Test:

**Unsigned extensions:**
- Cannot be installed in regular Firefox Release
- Only work in Developer Edition or Nightly
- Show error: "This add-on could not be installed because it appears to be corrupt"

**Signed extensions:**
- Install normally in any Firefox version
- No warnings or errors
- Work immediately after installation

### Test Steps:
1. Open **regular Firefox** (not Developer Edition)
2. Drag your .xpi file into Firefox
3. **Results:**
   - ✅ Prompts to install → **Signed**
   - ❌ Shows corruption error → **Not signed**

---

## Quick Status Check Script

Run this to check your extension status:

```bash
#!/bin/bash
# check-extension-signing.sh

XPI_FILE="$1"

if [ -z "$XPI_FILE" ]; then
    echo "Usage: ./check-extension-signing.sh <path-to-xpi-file>"
    exit 1
fi

if [ ! -f "$XPI_FILE" ]; then
    echo "❌ File not found: $XPI_FILE"
    exit 1
fi

echo "🔍 Checking signing status of: $XPI_FILE"
echo ""

# Check for META-INF
if unzip -l "$XPI_FILE" 2>/dev/null | grep -q "META-INF"; then
    echo "✅ SIGNED - Contains Mozilla signature files"
    echo ""
    echo "META-INF contents:"
    unzip -l "$XPI_FILE" | grep META-INF
else
    echo "❌ NOT SIGNED - No signature files found"
    echo ""
    echo "This is your local build. You need to:"
    echo "1. Upload to https://addons.mozilla.org/developers/"
    echo "2. Wait for approval"
    echo "3. Download the signed version"
fi

echo ""
echo "File size: $(ls -lh "$XPI_FILE" | awk '{print $5}')"
echo "File name: $(basename "$XPI_FILE")"
```

**Usage:**
```bash
chmod +x check-extension-signing.sh
./check-extension-signing.sh firefox-extension/dist/decoy-service-1.0.0.xpi
```

---

## What to Do If Not Signed

### Step 1: Check Submission Status
- Go to https://addons.mozilla.org/developers/addons
- Check if you submitted the extension
- Look at review status

### Step 2: Wait for Review
**Self-distributed (unlisted):**
- Usually approved in **minutes to hours**
- Automated checks only
- Very fast

**Listed on AMO:**
- Can take **1-7 days**
- Manual human review
- Stricter guidelines

### Step 3: Check for Issues
If rejected or pending long:
- Check your email for Mozilla notifications
- Look at developer dashboard for messages
- Common issues:
  - Minified code (must submit source)
  - Security issues
  - Missing permissions explanations

### Step 4: Download Signed File
Once approved:
- Dashboard shows "Download Signed File"
- Download it
- This is what you share with friends

---

## Testing Your Current Extension

**Quick test right now:**

```bash
# Check if you have a signed version
cd firefox-extension/dist/

# Look for any .xpi files
ls -lh *.xpi

# Check each one
for xpi in *.xpi; do
    echo "Checking: $xpi"
    if unzip -l "$xpi" 2>/dev/null | grep -q META-INF; then
        echo "  ✅ SIGNED"
    else
        echo "  ❌ NOT SIGNED (local build)"
    fi
    echo ""
done
```

---

## Summary

| Method | Speed | Reliability | When to Use |
|--------|-------|-------------|-------------|
| Developer Hub | Instant | ✅ 100% | First check |
| File name | Instant | ⚠️ 60% | Quick guess |
| Firefox details | Fast | ✅ 100% | After install |
| XPI contents | Fast | ✅ 100% | Technical verification |
| Install test | Fast | ✅ 100% | Final confirmation |

**Recommended workflow:**
1. Check Developer Hub first
2. If shows "Approved", download signed file
3. Verify by checking META-INF in the downloaded file
4. Test install in regular Firefox

**You need the SIGNED version to share with friends!**
