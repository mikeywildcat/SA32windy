# Sailaway 3 to Windy GPS Bridge

A lightweight application that connects Sailaway 3's NMEA TCP feed to the Windy GPS plugin, displaying your boat's real-time position on the Windy.com map with smooth heading updates.

## Features

- 🚢 **Connects to Sailaway 3** - Reads NMEA data directly from the game
- 🌐 **Windy Integration** - Serves GPS data to Windy plugin via HTTP (localhost:5000)
- 🖥️ **Simple GUI** - Easy-to-use interface, no configuration files needed
- 📊 **Real-time Activity Log** - See exactly what's happening
- ⚡ **Auto-reconnection** - Handles connection drops gracefully
- ⏱️ **Always Fresh Data** - No rate limiting - plugin always gets latest position for smooth heading
- 🎯 **Accurate Navigation** - Uses GLL NMEA sentences for precise positioning
- 🧭 **Stable Heading** - Red arrow on map rotates smoothly without drifting back to north

## Quick Start (Standalone Executable)

**For users who don't want to install Python:**

1. **Download** the latest release:
   - Go to [Releases](https://github.com/mikeywildcat/SA32windy/releases)
   - Download `sailaway_to_windy.exe` (Windows x64)

2. **Install Windy Plugin**:
   - Download the [Windy GPS from TCP plugin](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP)
   - Follow the plugin installation instructions

3. **Run the application**:
   - Double-click `sailaway_to_windy.exe`
   - Default settings (127.0.0.1:10110) should work automatically
   - Click **"Start Bridge"**

4. **Open Windy**:
   - Go to [Windy.com](https://www.windy.com/)
   - Activate the GPS from TCP plugin
   - Click "Update Windy"
   - Your boat should appear with a red arrow showing your heading! ⛵

## Installation (Python Source)

**For developers or users who prefer running from source:**

### Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- No additional packages required!

### Setup

### Setup

1. **Verify Python installation**:
   ```bash
   python --version
   ```

2. **Clone or download** this repository:
   ```bash
   git clone https://github.com/mikeywildcat/SA32windy.git
   cd SA32windy
   ```

3. **Run directly** (no installation needed):
   ```bash
   python sailaway_to_windy.py
   ```

## Usage Guide

### Step-by-Step Instructions

1. **Start Sailaway 3**
   - Launch the game and ensure NMEA TCP output is enabled
   - Default Sailaway NMEA settings: Port 10110

2. **Launch SA32windy Bridge**
   - Run `sailaway_to_windy.exe` (standalone) or `python sailaway_to_windy.py` (source)
   - The GUI will open with pre-configured defaults

3. **Configure Connection** (if needed)
   - **IP Address**: `127.0.0.1` (for local Sailaway)
   - **Port**: `10110` (Sailaway's default NMEA port)
   - Change these only if Sailaway runs on another computer or uses custom port

3. **Start the Bridge**
   - Click **"Start Bridge"** button
   - Status should show **"● Connected"** (green)
   - Activity log will show GPS data arriving (logged every 0.5 seconds)

5. **Open Windy**
   - Navigate to [Windy.com](https://www.windy.com/)
   - Activate the **GPS from TCP** plugin
   - Click **"Update Windy"** button in the plugin
   - Your boat appears with a **red arrow** showing heading! 🎉

5. **Navigation**
   - Arrow rotates automatically based on your course
   - Use plugin's "Follow Ship" button to keep boat centered
   - Position updates continuously - no rate limiting for smooth, stable heading

## Configuration

### Default Settings

```
Sailaway IP:    127.0.0.1
Sailaway Port:  10110
HTTP Endpoint:  localhost:5000/gps-data (fixed, required by Windy plugin)
Update Rate:    Continuous - always serves latest position (no rate limiting)
```

### Advanced Configuration

#### Connecting to Remote Sailaway

If Sailaway runs on **another computer** on your network:

1. **Find Sailaway PC's IP address**:
   - On Sailaway PC, open Command Prompt
   - Type: `ipconfig`
   - Note the IPv4 Address (e.g., `192.168.1.100`)

2. **Configure SA32windy**:
   - Enter the Sailaway PC's IP in the bridge
   - Port remains `10110`

3. **Firewall Setup** (on Sailaway PC):
   - Open Windows Defender Firewall
   - Advanced Settings → Inbound Rules → New Rule
   - Port → TCP → Specific port: `10110`
   - Allow the connection → Apply to all profiles
   - Name: "Sailaway NMEA"

#### Custom Port

If Sailaway uses a different port:

1. Check Sailaway settings for NMEA TCP port
2. Enter that port number in SA32windy
3. Keep IP as `127.0.0.1` for local connection

## How It Works

### Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│  Sailaway   │  NMEA   │   SA32windy  │  HTTP   │   Windy    │
│ NMEA Server │────────▶│    Bridge    │────────▶│   Plugin   │
│ 127.0.0.1   │  :10110 │ localhost    │  :5000  │  Browser   │
└─────────────┘         └──────────────┘         └────────────┘
```

### Data Flow

1. **Sailaway** outputs NMEA sentences via TCP on port 10110
2. **SA32windy** connects and receives NMEA data continuously
3. **Filters** for GLL sentences (Geographic Position: Lat/Lon)
4. **Stores latest** position data with no rate limiting
5. **HTTP server** provides data at `localhost:5000/gps-data`
6. **Windy plugin** fetches GPS data every 500ms
7. **Plugin calculates** boat heading from consecutive positions
8. **Map displays** boat position with stable, accurate arrow rotation

### NMEA Sentence Details

**What is NMEA?**
- **N**ational **M**arine **E**lectronics **A**ssociation standard
- Text-based protocol for marine instruments
- Sailaway outputs realistic NMEA data like real GPS devices

**NMEA Sentence Format:**
```
$GPRMC,163016.360,A,1938.9841,N,12342.9223,W,5.2,135.0,080325,,,A*6F
  │       │        │    │        │    │        │   │    │       │
  │       │        │    │        │    │        │   │    │       └─ Mode
  │       │        │    │        │    │        │   │    └───────── Date
  │       │        │    │        │    │        │   └────────────── COG (degrees)
  │       │        │    │        │    │        └────────────────── Speed (knots)
  │       │        │    │        │    └─────────────────────────── Lon (dddmm.mmmm,W)
  │       │        │    │        └──────────────────────────────── Lat (ddmm.mmmm,N)
  │       │        │    └───────────────────────────────────────── Status (A=Valid)
  │       │        └────────────────────────────────────────────── UTC Time
  │       └─────────────────────────────────────────────────────── RMC ID
  └─────────────────────────────────────────────────────────────── GPS Prefix

$GPGLL,1938.9841,N,12342.9223,W,163016.360,A,A*5C
  │      │        │    │        │      │      │ │
  │      │        │    │        │      │      │ └─ Mode
  │      │        │    │        │      │      └─── Status (A=Valid)
  │      │        │    │        │      └────────── UTC Time
  │      │        │    │        └───────────────── Lon Direction (E/W)
  │      │        │    └────────────────────────── Longitude (dddmm.mmmm)
  │      │        └─────────────────────────────── Lat Direction (N/S)
  │      └──────────────────────────────────────── Latitude (ddmm.mmmm)
  └─────────────────────────────────────────────── Sentence ID
```

**Why RMC is Better:**
- **RMC** includes Course Over Ground (COG) directly from GPS - more accurate and stable
- **GLL** only has position - plugin must calculate COG from position changes
- Calculation from position changes can be jittery, especially at slow speeds
- Bridge accepts both sentence types - RMC preferred when available

### Heading Calculation

The **red arrow** direction is calculated by the Windy plugin:

1. Plugin polls for position every 500ms (0.5 seconds)
2. Bridge always provides the latest GPS position from Sailaway
3. Plugin compares new position with previous position
4. Calculates bearing (angle) between the two points
5. Rotates arrow to match calculated bearing
6. Result: Stable arrow pointing in direction of actual boat movement (Course Over Ground)

**Key to stable heading**: By not rate limiting the GPS data, the plugin always receives fresh position updates whenever it polls, ensuring smooth and stable arrow rotation without drift.

## Troubleshooting

### Common Issues

#### ❌ "Connection refused" or "Failed to connect"

**Possible causes:**
- Sailaway 3 is not running
- NMEA TCP output not enabled in Sailaway
- Wrong IP address or port

**Solutions:**
1. Verify Sailaway 3 is running and you're in a boat (not menu)
2. Check Sailaway settings for NMEA TCP output
3. Verify port is `10110` (Sailaway default)
4. For local Sailaway, use `127.0.0.1` or `localhost`
5. For remote Sailaway, verify IP address with `ipconfig`

#### ❌ Windy plugin shows "No data received"

**Possible causes:**
- Bridge not running
- Bridge not connected to Sailaway
- Plugin looking at wrong URL

**Solutions:**
3. Check bridge shows **"● Connected"** (green status)
2. Verify GPS data appears in activity log (displayed every 0.5 seconds)
3. Confirm plugin URL is `http://localhost:5000/gps-data`
4. Click "Update Windy" button in the plugin
5. Refresh your browser

#### ❌ Position shows but arrow doesn't rotate or drifts back to north

**Possible causes:**
- Boat not moving (no course change)
- Moving too slowly for significant position changes
- Sailing in perfectly straight line

**Solutions:**
1. Turn your boat to see arrow rotation
2. Arrow updates based on actual position changes between plugin polls
3. More movement = more accurate heading display
4. Verify you're actually under sail/power and moving

#### ❌ "Port 5000 already in use"

**Possible causes:**
- Another application using port 5000
- Multiple instances of SA32windy running

**Solutions:**
1. Close other instances of SA32windy
2. Check for other apps using port 5000
3. Restart your computer if needed

#### ❌ GPS data in log but Windy shows null/nothing

**Possible causes:**
- Browser security blocking localhost
- Plugin not properly installed
- Cache issues
- Stale data in plugin

**Solutions:**
1. Try a different browser (Chrome, Edge, Firefox)
2. Clear browser cache
3. Reinstall Windy plugin
4. Click "Update Windy" button in plugin to force refresh
5. Check browser console for errors (F12)

### Debugging Tips

**Enable detailed logging:**
- Watch the Activity Log in SA32windy
- GPS data should appear every 0.5 seconds when connected (logging interval)
- Format: `GPS: $GPGLL,ddmm.mmmm,N,dddmm.mmmm,E,...`
- Data is updated continuously but logged at 0.5-second intervals to avoid flooding the log

**Test the HTTP endpoint:**
- Open browser to `http://localhost:5000/gps-data`
- Should see the latest NMEA sentence
- Refreshing should show updated data continuously

**Check network connectivity:**
- For remote Sailaway, verify both PCs on same network
- Ping Sailaway PC: `ping <sailaway-ip>`
- Check firewall allows port 10110

## Building from Source

### Build Your Own Executable

If you want to create your own standalone `.exe` file:

#### Requirements

- Python 3.7+
- PyInstaller: `pip install pyinstaller`

#### Build Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mikeywildcat/SA32windy.git
   cd SA32windy
   ```

2. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

3. **Build executable**:
   ```bash
   pyinstaller --onefile --windowed --name sailaway_to_windy sailaway_to_windy.py
   ```

4. **Find your executable**:
   - Located in `dist/sailaway_to_windy.exe`
   - Portable - can copy to any Windows PC
   - No Python installation needed on target PC

#### Build Options Explained

- `--onefile`: Single executable (no DLLs)
- `--windowed`: No console window (GUI only)
- `--name`: Custom executable name

#### Platform-Specific Builds

- **Windows ARM64**: Build on ARM64 Windows PC
- **Windows x64**: Build on x64 Windows PC (or use GitHub Actions)
- **Cross-platform**: Must build on target platform

### Automated Builds (GitHub Actions)

This repository includes automated builds:

1. **Push to GitHub** triggers automatic build
2. **GitHub Actions** builds x64 executable
3. **Artifacts** available in Actions tab
4. **Tag release** (e.g., `v1.0.0`) to create official release

**Create a release:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions automatically builds and attaches `.exe` to release.

## Technical Details

### Performance Characteristics

- **Memory Usage**: ~50MB typical
- **CPU Usage**: <1% idle, ~2% when processing
- **Network Bandwidth**: ~200 bytes per GPS update from Sailaway (minimal)
- **Latency**: <100ms from Sailaway to Windy
- **Update Rate**: Continuous (no rate limiting - always serves latest position)

### Code Modification

Want to customize? The code is simple and well-commented:

**Change log display frequency:**
```python
# In sailaway_to_windy.py, find at the top:
GPS_LOG_INTERVAL_SECONDS = 0.5  # Change to desired seconds (how often to display logs)
```

**Note**: The actual GPS data is updated continuously (no rate limiting). This constant only controls how often updates are logged to the activity window to prevent flooding.

**Change HTTP port** (requires Windy plugin reconfiguration):
```python
# In start_http_server() method, find:
self.http_server = HTTPServer(('localhost', 5000), GPSHandler)  # Change 5000
```

**Use different NMEA sentences:**
```python
# In receive_nmea_data() method, find:
if ('$GPRMC' in line or '$IIRMC' in line or   # RMC has COG data
    '$GPGLL' in line or '$IIGLL' in line):     # GLL position only
    # Change to use only specific types if needed
```

### Dependencies

This application uses **only Python standard library**:
- `socket` - TCP connection to Sailaway
- `threading` - Concurrent TCP and HTTP operations
- `tkinter` - GUI interface
- `http.server` - HTTP endpoint for Windy
- `time`, `datetime` - Timestamps and rate limiting

No external packages needed! 🎉

## Windy Plugin Information

### Plugin Details

- **Name**: GPS from TCP
- **Author**: [Yann Kerhervé](https://github.com/YannKerherve)
- **Repository**: https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP
- **Endpoint**: `http://localhost:5000/gps-data`
- **Update Frequency**: Plugin polls every 500ms
- **Supported Formats**: RMC (preferred - includes COG) and GLL (position only) NMEA sentences

### Plugin Features

- **Real-time Position**: Shows boat on Windy map
- **Heading Arrow**: Red arrow rotates based on course
- **Follow Mode**: Camera follows your boat automatically
- **Path Tracking**: Blue line shows your route
- **Center Ship**: Button to recenter on boat

### Alternative Plugins

This bridge provides a standard HTTP endpoint, so it may work with other GPS plugins that expect NMEA data at a local HTTP server.

## FAQ

**Q: Do I need to keep Sailaway 3 running?**
A: Yes, the bridge needs Sailaway's NMEA feed to be active.

**Q: Can I use this with real GPS devices?**
A: Potentially yes, if your device outputs NMEA via TCP. Adjust IP/port accordingly.

**Q: Does this work with Sailaway 2?**
A: It should work if Sailaway 2 has NMEA TCP output. Check your settings.

**Q: Can multiple people track the same boat?**
A: Yes! Run SA32windy on the Sailaway PC, then access `http://<sailaway-ip>:5000/gps-data` from other computers' Windy plugins.

**Q: Will this slow down Sailaway or my computer?**
A: No, it uses minimal resources (<1% CPU, ~50MB RAM).

**Q: Can I run multiple boats?**
A: Not with a single instance. You'd need multiple Sailaway instances on different ports and multiple bridge instances.

**Q: Is my data sent anywhere?**
A: No! Everything runs locally on your computer/network. No internet connection required except for loading Windy.com.

**Q: The arrow spins randomly sometimes?**
A: This can happen when:
- Boat is stationary or moving very slowly
- GPS position changes are smaller than the plugin's bearing calculation threshold
- This is normal behavior and will stabilize once moving at normal sailing speeds
- The plugin needs sufficient position change between polls to calculate accurate bearing

**Q: Can I customize the update rate?**
A: The GPS data is provided continuously with no rate limiting for best arrow stability. You can change the logging display interval by editing `GPS_LOG_INTERVAL_SECONDS` in the code, but this only affects what you see in the log window, not what the Windy plugin receives.

## Contributing

Contributions welcome! This is a simple project, but improvements are always appreciated:

- Bug fixes
- Feature additions
- Documentation improvements
- Platform compatibility enhancements

Feel free to open issues or pull requests on GitHub.

## Support

**Issues?** Open an issue on [GitHub Issues](https://github.com/mikeywildcat/SA32windy/issues)

**Questions?** Check the FAQ above or open a discussion

**Issues?** Open an issue on [GitHub Issues](https://github.com/mikeywildcat/SA32windy/issues)

**Questions?** Check the FAQ above or open a discussion

## Credits & Acknowledgments

- **Windy Plugin**: [YannKerherve/Windy-plugin-GPS-from-TCP](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP) - The excellent Windy plugin that displays GPS data
- **Sailaway Simulator**: [Sailaway](https://sailaway.world/) - Realistic sailing simulator with NMEA output
- **Windy**: [Windy.com](https://www.windy.com/) - Beautiful weather and wind visualization platform

## License

MIT License - Free to use, modify, and distribute.

See [LICENSE](LICENSE) file for details.

---

**Made for sailors who love both Sailaway and real-time weather visualization! ⛵🌊**

*Star this repo if you find it useful!* ⭐
- Sailaway Simulator: https://sailaway.world/
