# 🚢 Quick Start Guide

## Step-by-Step Instructions

### 1. Prerequisites
- ✅ Python 3.7+ installed ([Download here](https://www.python.org/downloads/))
- ✅ Sailaway 3 running with NMEA TCP feed enabled
- ✅ Windy GPS from TCP plugin installed ([Get it here](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP))

### 2. Launch the Bridge

**Option A: Double-click `run_bridge.bat`**

**Option B: Run from command line**
```bash
python sailaway_to_windy.py
```

### 3. Configure Connection

The GUI will open with default settings:
- **IP Address**: `127.0.0.1` (change if Sailaway is on another computer)
- **Port**: `10110` (default Sailaway NMEA port)

### 4. Start the Connection

Click the **"Start Bridge"** button

You should see:
- ✅ Status changes to "Connected" (green)
- ✅ Activity log shows connection messages
- ✅ GPS data appears in the log (updates every 2 seconds)

### 5. Open Windy

1. Go to [Windy.com](https://www.windy.com/)
2. Open the GPS from TCP plugin
3. Click "Update Windy" or refresh
4. Your boat should appear on the map with a red arrow! 🎉
5. The arrow rotates to show your heading as you change course

### 6. Enjoy!

Your boat's position updates every 2 seconds on the Windy map, with smooth heading changes as you sail in Sailaway 3.

---

## Troubleshooting Quick Fixes

### ❌ "Connection refused" error
- Make sure Sailaway 3 is running
- Check that NMEA output is enabled in Sailaway settings
- Verify the port number (default: 10110)

### ❌ "Port already in use" error
- Another application is using port 5000
- Close any other programs that might use this port
- Or modify the bridge code to use a different port

### ❌ Windy shows "No data received"
- Ensure the bridge shows "Connected" status
- Check that GPS data is appearing in the activity log
- Refresh the Windy plugin
- Make sure you're sailing (not in port) so GPS data is available

### ❌ Python not found
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

---

## Visual Guide

```
┌──────────────────────────────────────────────┐
│  Sailaway to Windy GPS Bridge                │
├──────────────────────────────────────────────┤
│                                               │
│  Sailaway Connection Settings                │
│  ┌─────────────────────────────────────────┐ │
│  │ IP Address: 127.0.0.1    Port: 10110   │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  [ Start Bridge ]  [ Stop Bridge ]  [ Clear ]│
│                                               │
│  Status: ● Connected                         │
│  Windy plugin: http://localhost:5000/gps-data│
│                                               │
│  Activity Log                                │
│  ┌─────────────────────────────────────────┐ │
│  │ [12:34:56] ✓ Connected to Sailaway      │ │
│  │ [12:34:57] ✓ HTTP server started        │ │
│  │ [12:34:58] GPS: $GPGLL,1938.9841,N,...  │ │
│  └─────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

---

## Need More Help?

Check the full documentation:
- 📖 [README.md](README.md) - Complete documentation
- ⚙️ [CONFIGURATION.md](CONFIGURATION.md) - Advanced configuration options

Happy sailing! ⛵
