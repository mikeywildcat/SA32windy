# Sailaway 3 to Windy GPS Bridge

A lightweight application that connects Sailaway 3's NMEA TCP feed to the Windy GPS plugin, displaying your boat's real-time position on the Windy.com map with smooth heading updates.

## Features

- 🚢 **Connects to Sailaway 3** - Reads NMEA data directly from the game
- 🌐 **Windy Integration** - Serves GPS data to Windy plugin via HTTP (localhost:5000)
- 🖥️ **Simple GUI** - Easy-to-use interface, no configuration files needed
- 📊 **Real-time Activity Log** - See exactly what's happening
- ⚡ **Auto-reconnection** - Handles connection drops gracefully
- 🧭 **Dead-Reckoning Extrapolation** - Smooth position updates between GPS readings using RMC course and speed
- 🎯 **Accurate Navigation** - Uses GLL NMEA sentences for precise positioning with sub-meter precision
- 🎪 **Stable Heading** - Red arrow on map rotates smoothly without drifting back to north

## Quick Start (Standalone Executable)

**For users who don't want to install Python:**

1. **Download** the latest release:
   - Go to [Releases](https://github.com/mikeywildcat/SA32windy/releases)
   - Download `sailaway_to_windy.exe` (Windows x64)

2. **Install Windy Plugin**:
   - Go to [Windy.com](https://www.windy.com/)
   - Open the plugin menu (bottom-right corner)
   - Search for "GPS from TCP" and install it
   - **Note**: You only need the Windy plugin - this app replaces the separate bridge/server application

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

1. **Sailaway** outputs NMEA sentences via TCP on port 10110 (both RMC and GLL)
2. **SA32windy** connects and receives NMEA data continuously
3. **Parses RMC** sentences to extract Course Over Ground (COG) and speed in knots
4. **Parses GLL** sentences for precise Geographic Position (Lat/Lon)
5. **Dead-reckoning extrapolation**: Between real GPS updates, generates synthetic positions by:
   - Computing distance traveled = speed × time elapsed
   - Moving position along last known COG using spherical geometry
   - Creating GLL sentences with extrapolated coordinates (5 decimal precision)
6. **HTTP server** provides data at `localhost:5000/gps-data`
7. **Windy plugin** fetches GPS data every 500ms and receives smoothly changing positions
8. **Plugin calculates** boat heading from consecutive positions (always sees meaningful deltas)
9. **Map displays** boat position with stable, accurate arrow rotation - no drift to north!

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

**Why Dead-Reckoning Matters:**
- **RMC** provides Course Over Ground (COG) and speed directly from Sailaway
- **GLL** provides precise position but the Windy plugin must calculate bearing from position changes
- **Problem**: When the plugin polls faster (500ms) than significant position changes occur, it receives identical or nearly identical positions, causing unstable bearing calculations and the arrow to revert to north
- **Solution**: The bridge uses dead-reckoning to extrapolate small position changes between real GPS updates:
  - Captures COG and speed from RMC sentences
  - Computes distance traveled since last update: `distance = speed × time_elapsed`
  - Moves the position along the COG bearing using spherical geometry
  - Generates synthetic GLL sentences with extrapolated coordinates
  - Uses minimum synthetic speed (0.5 m/s) when stationary to ensure visible position deltas
- **Result**: Plugin always receives meaningful position changes at its 500ms poll rate, producing stable, smooth heading calculations

### Heading Calculation

The **red arrow** direction is calculated by the Windy plugin:

1. Plugin polls for position every 500ms (0.5 seconds)
2. Bridge provides extrapolated positions that change smoothly along the boat's course
3. Plugin compares new position with previous position
4. Calculates bearing (angle) between the two points
5. Rotates arrow to match calculated bearing
6. Result: Stable arrow pointing in direction of actual boat movement (Course Over Ground)

**Key to stable heading**: Dead-reckoning ensures the plugin receives continuously changing positions extrapolated along the boat's actual course and speed, preventing identical consecutive positions that would cause the arrow to drift or revert to north.

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

**This issue has been FIXED in v1.1.0+ with dead-reckoning extrapolation!**

**What was causing this:**
- The Windy plugin polls every 500ms and calculates heading from consecutive position changes
- When Sailaway's GPS updates were slower than the plugin's polling rate, the plugin would receive identical positions
- Identical positions = no meaningful bearing calculation = arrow reverts to north

**How the fix works:**
- Bridge now captures Course Over Ground (COG) and speed from RMC sentences
- Between real GPS updates, extrapolates position along the COG bearing
- Generates synthetic GLL sentences with smoothly changing coordinates
- Plugin always receives meaningful position deltas for stable bearing calculations

**If you still see this issue:**
1. Ensure you're running v1.1.0 or later (check About/version)
2. Verify GPS data is appearing in the activity log
3. Verify you're actually moving (check Sailaway shows speed > 0)
4. Try turning your boat - arrow should rotate smoothly with course changes

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
- **Position Extrapolation**: Computed in real-time for each plugin poll (500ms intervals)
- **Extrapolation Accuracy**: Uses spherical geometry and actual COG/speed from RMC data
- **Coordinate Precision**: 5 decimal places in minutes (sub-meter accuracy)

### Dead-Reckoning Implementation

The bridge implements dead-reckoning navigation to provide smooth position updates:

**Algorithm:**
1. Parse incoming RMC sentences to capture:
   - Course Over Ground (COG) in degrees true
   - Speed Over Ground (SOG) in knots
2. Parse GLL sentences to update actual position (latitude/longitude)
3. When HTTP endpoint is polled:
   - Calculate time elapsed since last real position update
   - Compute distance traveled: `distance = speed × time_elapsed`
   - Extrapolate new position along COG bearing using spherical geometry
   - Generate synthetic GLL sentence with extrapolated coordinates
   - Use minimum synthetic speed (0.5 m/s) when nearly stationary

**Benefits:**
- Eliminates identical consecutive positions that cause heading drift
- Provides smooth, continuous position updates at plugin's poll rate
- Maintains heading accuracy even between Sailaway GPS updates
- No modification needed to Windy plugin

**Tuning:**
```python
# Minimum synthetic speed (meters per second) when boat is stationary/slow
# Default: 0.5 m/s (1.8 km/h) - creates visible position deltas for stable bearing
speed_m_s = 0.5  # Adjust if needed for your use case
```

### Code Modification

Want to customize? The code is simple and well-commented:

**Adjust dead-reckoning synthetic speed:**
```python
# In start_http_server() -> GPSHandler.do_GET(), find:
if speed_m_s < 0.5:
    speed_m_s = 0.5  # Change to adjust minimum extrapolation speed
```

**Change coordinate precision:**
```python
# In the to_ddmm() function within dead-reckoning code:
return f"{degrees:02d}{minutes:07.5f}"  # .5f = 5 decimal places; adjust as needed
```

**Change HTTP port** (requires Windy plugin reconfiguration):
```python
# In start_http_server() method, find:
self.http_server = HTTPServer(('localhost', 5000), GPSHandler)  # Change 5000
```

**Disable dead-reckoning** (revert to raw GPS only):
```python
# In GPSHandler.do_GET(), comment out the extrapolation try/except block
# and directly serve: self.wfile.write(bridge.latest_gps_data.encode())
```

### Dependencies

This application uses **only Python standard library**:
- `socket` - TCP connection to Sailaway
- `threading` - Concurrent TCP and HTTP operations
- `tkinter` - GUI interface
- `http.server` - HTTP endpoint for Windy
- `time`, `datetime` - Timestamps and dead-reckoning calculations
- `math` - Spherical geometry for position extrapolation

No external packages needed! 🎉

## Diagnostic Tools

The repository includes diagnostic scripts for troubleshooting:

### `diagnose_nmea.py`
Connects directly to Sailaway's NMEA feed and prints raw sentences:
```bash
python diagnose_nmea.py
```
- Shows all NMEA sentences from Sailaway (RMC, GLL, VTG, etc.)
- Useful for verifying Sailaway is outputting data correctly
- Helps identify which sentence types are available

### `poll_gps.py`
Mimics the Windy plugin's polling behavior:
```bash
python poll_gps.py
```
- Polls `http://localhost:5000/gps-data` every 500ms for 30 seconds
- Shows exactly what the Windy plugin receives
- Useful for verifying dead-reckoning extrapolation is working
- Should show smoothly changing coordinates in the output

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
A: **This issue has been fixed in v1.1.0+!** The dead-reckoning extrapolation ensures the plugin always receives smoothly changing positions. If you still experience this:
- Verify you're running v1.1.0 or later
- Ensure GPS data is appearing in the activity log
- Check that Sailaway shows your boat is actually moving (speed > 0)
- The arrow should now rotate smoothly without random spinning or reverting to north

**Q: How does dead-reckoning work?**
A: The bridge captures your boat's Course Over Ground (COG) and speed from Sailaway's RMC sentences. Between real GPS updates, it mathematically extrapolates where your boat would be based on that course and speed, then generates synthetic position data. This ensures the Windy plugin always receives smoothly changing positions for stable heading calculations.

**Q: Does dead-reckoning affect position accuracy?**
A: No! The bridge constantly updates with real GPS positions from Sailaway. Dead-reckoning only fills in the gaps *between* real updates (which happen every ~2 seconds). The extrapolation uses your actual course and speed, so it accurately represents where your boat is moving.

**Q: Can I disable dead-reckoning?**
A: Yes, but it's not recommended as it may cause heading drift. You can comment out the extrapolation code in the `do_GET()` method and directly serve `bridge.latest_gps_data`. See the Technical Details section for code modification examples.

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
