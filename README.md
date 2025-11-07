# Sailaway 3 to Windy GPS Bridge

A Python application that connects to Sailaway 3's NMEA TCP feed and forwards GPS data to the Windy GPS plugin.

## Features

- 🚢 Connects to Sailaway 3's TCP NMEA feed
- 🌐 Serves GPS data to Windy plugin via HTTP (localhost:5000)
- 🖥️ Simple GUI to configure connection settings
- 📊 Real-time activity log
- ⚡ Automatic reconnection handling
- ⏱️ Optimized updates - sends position every 2 seconds for smooth heading updates
- 🎯 Accurate data - uses GLL sentences (format expected by Windy plugin)

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)

## Installation

1. Make sure you have Python installed:
   ```bash
   python --version
   ```

2. No additional packages required! The app uses only Python standard library.

## Usage

1. **Start Sailaway 3** and ensure its NMEA TCP feed is active

2. **Run the application**:
   ```bash
   python sailaway_to_windy.py
   ```

3. **Configure connection**:
   - Enter the IP address of your Sailaway NMEA server (default: `127.0.0.1`)
   - Enter the port number (default: `10110`)

4. **Click "Start Bridge"** to connect

5. **Open Windy** in your browser and activate the GPS plugin:
   - The plugin will automatically connect to `http://localhost:5000/gps-data`

6. Your boat position should now appear on the Windy map! 🎉

## Sailaway NMEA Data Format

The application processes NMEA sentences from Sailaway, specifically:
- `$GPGLL` / `$IIGLL` - Geographic Position (Latitude/Longitude)

The Windy plugin uses position updates to calculate your boat's heading (the direction the arrow points).

Example data:
```
$GPGLL,1938.9841,N,12342.9223,W,163016.360,A,A*5C
```

Position updates are sent every 2 seconds for smooth, responsive heading updates.

## Windy Plugin

This application works with the Windy GPS from TCP plugin:
https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP

The plugin expects GPS data at `http://localhost:5000/gps-data`

## Troubleshooting

### Connection Issues

- **Can't connect to Sailaway**: 
  - Verify Sailaway's NMEA server is running
  - Check the IP address and port number
  - Try `localhost` or `127.0.0.1` if running on the same machine

- **Windy plugin shows "No data"**:
  - Ensure the bridge is running (green "Connected" status)
  - Check that you're receiving GPS data in the activity log
  - Verify the Windy plugin is looking at `localhost:5000`

### Port Already in Use

If port 5000 is already in use by another application, you'll need to:
1. Stop the other application using port 5000, or
2. Modify the code to use a different port (and update the Windy plugin accordingly)

## How It Works

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│  Sailaway   │         │   SA32windy  │         │   Windy    │
│ NMEA Server │────────▶│  127.0.0.1   │────────▶│   Plugin   │
│             │  :10110 │   :5000      │         │            │
└─────────────┘         └──────────────┘         └────────────┘
```

1. The bridge connects to Sailaway's TCP NMEA feed
2. It receives and parses NMEA sentences
3. It runs an HTTP server on localhost:5000
4. The Windy plugin fetches GPS data from the HTTP endpoint
5. Your boat appears on the Windy map with real-time updates!

## License

Free to use and modify as needed.

## Credits

- Windy Plugin: [YannKerherve/Windy-plugin-GPS-from-TCP](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP)
- Sailaway Simulator: https://sailaway.world/
