# 📦 Sailaway to Windy GPS Bridge - Standalone Version

## What's Included

The **SailawayWindyBridge.exe** is a standalone executable that contains everything needed to run the GPS bridge. No Python installation required!

## For End Users (Simple Instructions)

### Download & Run
1. Download `SailawayWindyBridge.exe`
2. Double-click to run
3. Enter your Sailaway connection details:
   - IP Address: `localhost` (or your Sailaway server IP)
   - Port: `5555` (or your configured port)
4. Click "Start Bridge"
5. Open Windy with the GPS plugin - your boat appears!

### System Requirements
- Windows 10/11 
  - **ARM64 version**: Works on ARM64 Windows (Surface Pro X, etc.)
  - **x64 version**: Works on standard 64-bit Windows PCs
  - **Note**: The .exe is architecture-specific!
- Sailaway 3 running with NMEA output enabled
- Windy GPS from TCP plugin installed

### ⚠️ Important: Architecture Compatibility

**The current build (`SailawayWindyBridge.exe`) only works on ARM64 Windows systems!**

For most Windows users (Intel/AMD PCs), you'll need an x64 build.

**Solutions:**
1. **Use the Python script** - Works on all systems (requires Python 3.7+)
2. **Build on x64 Windows** - Creates x64 executable for most PCs
3. **Distribute both versions** - ARM64 for Surface Pro X, etc. and x64 for standard PCs

### No Installation Needed!
Just run the .exe file - it's completely portable!

---

## For Developers (Building the Executable)

### Prerequisites
```bash
pip install pyinstaller
```

### Build Instructions

**Option 1: Use the build script (Easy)**
```bash
build_standalone.bat
```

**Option 2: Manual build**
```bash
pyinstaller --onefile --windowed --name "SailawayWindyBridge" sailaway_to_windy.py
```

The executable will be created in the `dist/` folder.

### Build Options Explained

- `--onefile`: Creates a single .exe file (everything bundled)
- `--windowed`: No console window (GUI only)
- `--name`: Custom name for the executable

### Advanced Build (with icon)

If you have an icon file:
```bash
pyinstaller --onefile --windowed --icon=app_icon.ico --name "SailawayWindyBridge" sailaway_to_windy.py
```

### Build Output

```
dist/
└── SailawayWindyBridge.exe    (Standalone executable - ~15-20 MB)
```

### Distribution

Simply share the `SailawayWindyBridge.exe` file. Users can run it directly without any dependencies!

---

## Troubleshooting

### Windows SmartScreen Warning
When first running the .exe, Windows might show a SmartScreen warning because the app isn't code-signed.

**To run anyway:**
1. Click "More info"
2. Click "Run anyway"

This is normal for unsigned executables.

### Antivirus False Positives
Some antivirus software may flag PyInstaller executables as suspicious. This is a known issue with all PyInstaller apps.

**Solutions:**
- Add exception in your antivirus
- Run from the source Python script instead
- Code-sign the executable (requires certificate)

### Build Errors

If the build fails:
1. Make sure PyInstaller is installed: `pip install pyinstaller`
2. Make sure all imports in the Python script are standard library only
3. Check that tkinter is available: `python -m tkinter`

---

## File Sizes

- **Source Python Script**: ~10 KB
- **Standalone Executable**: ~15-20 MB (includes Python interpreter + libraries)

The larger size is normal - it includes everything needed to run!

---

## Updating the App

### For Users
Download the new .exe file and replace the old one.

### For Developers
1. Modify `sailaway_to_windy.py`
2. Run `build_standalone.bat` again
3. Distribute the new .exe from `dist/` folder

---

## Version Info

To add version information to the .exe, create a `version.txt`:

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'Sailaway to Windy GPS Bridge'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'ProductName', u'SailawayWindyBridge'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Then build with:
```bash
pyinstaller --onefile --windowed --version-file=version.txt --name "SailawayWindyBridge" sailaway_to_windy.py
```

---

## Security Notes

- The executable is not code-signed
- Source code is available for inspection
- All network communication stays local (localhost:5000)
- Connects to Sailaway via TCP (configurable)
- No data is sent to external servers

---

## License

Free to use and distribute. Source code available in this repository.

Happy sailing! ⛵
