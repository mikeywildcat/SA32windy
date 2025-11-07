# 📦 DISTRIBUTION GUIDE

## Quick Distribution Options

### Option 1: Single File (Simplest)
Just share: `dist\SailawayWindyBridge.exe`

Users can double-click and run immediately!

### Option 2: Package with Docs
Create a ZIP file with:
```
SailawayWindyBridge/
├── SailawayWindyBridge.exe
├── README.txt
└── QUICKSTART.md
```

## Creating Distribution Package

### Using PowerShell:
```powershell
# Create a distribution folder
New-Item -ItemType Directory -Force -Path "SailawayWindyBridge_v1.0"

# Copy the exe
Copy-Item "dist\SailawayWindyBridge.exe" "SailawayWindyBridge_v1.0\"

# Copy documentation
Copy-Item "dist\README.txt" "SailawayWindyBridge_v1.0\"
Copy-Item "QUICKSTART.md" "SailawayWindyBridge_v1.0\"

# Create ZIP
Compress-Archive -Path "SailawayWindyBridge_v1.0" -DestinationPath "SailawayWindyBridge_v1.0.zip"
```

### Manual Method:
1. Create a new folder called `SailawayWindyBridge_v1.0`
2. Copy `dist\SailawayWindyBridge.exe` into it
3. Copy `dist\README.txt` into it  
4. Copy `QUICKSTART.md` into it
5. Right-click the folder → "Send to" → "Compressed (zipped) folder"

## File Locations

- **Source Code**: `sailaway_to_windy.py`
- **Standalone Exe**: `dist\SailawayWindyBridge.exe`
- **Build Spec**: `SailawayWindyBridge.spec`
- **Build Files**: `build\` (can be deleted)

## Sharing Methods

### 1. GitHub Release
1. Create a repository
2. Tag a release (e.g., v1.0)
3. Upload `SailawayWindyBridge.exe` as a release asset
4. Users download directly from GitHub

### 2. File Sharing Services
- Google Drive
- Dropbox
- OneDrive
- WeTransfer

### 3. Direct Transfer
- Email (if < 25 MB - you're good!)
- USB drive
- Network share

## What Users Need to Know

### Minimum Info:
1. Download `SailawayWindyBridge.exe`
2. Double-click to run
3. Enter Sailaway connection details
4. Click "Start Bridge"
5. Open Windy

### Full Instructions:
Include `QUICKSTART.md` in your distribution package.

## Version Information

Current build:
- **Version**: 1.0
- **Platform**: Windows ARM64
- **Size**: ~10 MB
- **Python**: 3.12 (embedded)
- **Dependencies**: All included

## Rebuilding

To rebuild after making changes:
```bash
build_standalone.bat
```

Or manually:
```bash
pyinstaller --onefile --windowed --name "SailawayWindyBridge" sailaway_to_windy.py
```

## File Checksums

After building, you can generate checksums for verification:

### PowerShell:
```powershell
Get-FileHash "dist\SailawayWindyBridge.exe" -Algorithm SHA256
```

Include the hash in your distribution for users to verify file integrity.

## Code Signing (Optional)

For professional distribution, consider code signing:
1. Obtain a code signing certificate
2. Use `signtool.exe` to sign the executable
3. Eliminates Windows SmartScreen warnings

**Note**: Code signing certificates cost money ($100-$400/year)

## Support & Updates

When distributing, consider:
- Creating a simple website or GitHub page
- Providing contact method for support
- Announcing updates
- Maintaining a changelog

## Legal Considerations

- The source code is free to use and distribute
- PyInstaller is GPLv2 (allows free and commercial distribution)
- Python stdlib is Python Software Foundation License
- All dependencies are permissively licensed

You can freely distribute this application!

---

## Distribution Checklist

Before sharing:
- [ ] Test the .exe on a clean Windows PC
- [ ] Verify Sailaway connection works
- [ ] Verify Windy plugin receives data
- [ ] Include README or QUICKSTART guide
- [ ] Note Windows SmartScreen warning in docs
- [ ] Provide your contact info for support (optional)

**You're all set to share!** 🚀
