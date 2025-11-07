# 🚢 Sailaway to Windy GPS Bridge

[![Build Executables](https://github.com/YOUR_USERNAME/SA32windy/actions/workflows/build.yml/badge.svg)](https://github.com/YOUR_USERNAME/SA32windy/actions/workflows/build.yml)

A Python application that bridges Sailaway 3's NMEA TCP feed to the Windy GPS plugin, allowing you to see your boat's real-time position on the Windy weather map!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

## ✨ Features

- 🖥️ **User-friendly GUI** - Simple interface to configure connection settings
- 🌐 **HTTP Server** - Serves GPS data to Windy plugin on localhost:5000
- 📡 **TCP Client** - Connects to Sailaway's NMEA feed
- 📊 **Real-time Monitoring** - Activity log shows connection status and GPS data
- 🚀 **Standalone Executable** - No Python required for end users (x64 build available)
- 🔄 **Auto-updates** - Refresh every 500ms for smooth tracking

## 📥 Downloads

### Latest Release

[**Download Latest Release**](https://github.com/YOUR_USERNAME/SA32windy/releases/latest)

Choose the version for your system:
- **SailawayWindyBridge_x64.exe** - For most Windows PCs (Intel/AMD) ⭐ Recommended
- **Python Script** - Universal version (requires Python 3.7+)
- **ARM64 users** - Build locally on your ARM64 device

## 🚀 Quick Start

### Option 1: Use the Executable (Easy)

1. Download `SailawayWindyBridge_x64.exe` from [releases](https://github.com/YOUR_USERNAME/SA32windy/releases)
2. Double-click to run
3. Enter your Sailaway connection details (default: `127.0.0.1:10110`)
4. Click "Start Bridge"
5. Open [Windy](https://www.windy.com/) and activate the GPS plugin
6. Your boat appears on the map! 🎉

### Option 2: Run the Python Script

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SA32windy.git
cd SA32windy

# Run the application (no installation needed - uses Python stdlib only!)
python sailaway_to_windy.py
```

## 📋 Requirements

### For Executable Version
- Windows 10/11 (x64)
- Sailaway 3 with NMEA TCP output enabled
- [Windy GPS from TCP plugin](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP)

### For Python Script
- Python 3.7 or higher
- tkinter (usually included with Python)
- Standard library only - no pip install needed!

## 🎮 How It Works

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│  Sailaway   │         │   SA32windy  │         │   Windy    │
│ NMEA Server │────────▶│  127.0.0.1   │────────▶│   Plugin   │
│             │  :10110 │   :5000      │         │            │
└─────────────┘         └──────────────┘         └────────────┘
```

1. The bridge connects to Sailaway's TCP NMEA feed (default port 10110)
2. Parses GPS position from NMEA GLL sentences (latitude/longitude)
3. Sends position updates every 2 seconds for smooth heading display
4. Serves data via HTTP on `localhost:5000/gps-data`
5. Windy plugin fetches data, calculates heading, and displays your boat in real-time

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) - Step-by-step setup instructions
- [Configuration Guide](CONFIGURATION.md) - Advanced configuration options
- [Architecture](ARCHITECTURE.md) - Technical details and data flow
- [Standalone Version](STANDALONE.md) - Building your own executable
- [Distribution Guide](DISTRIBUTION.md) - How to share with others

## 🔧 Configuration

Default settings:
- **Sailaway IP**: `127.0.0.1` (change if Sailaway runs on another PC)
- **Sailaway Port**: `10110` (default NMEA TCP port)
- **HTTP Server**: `localhost:5000` (fixed - required by Windy plugin)

## 🛠️ Building from Source

### Build the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build for your platform
pyinstaller --onefile --windowed --name "SailawayWindyBridge" sailaway_to_windy.py

# Executable will be in dist/ folder
```

Or use the build script:
```bash
build_standalone.bat
```

### GitHub Actions

This repository uses GitHub Actions to automatically build the x64 executable on every push:
- Builds are available in the [Actions tab](https://github.com/YOUR_USERNAME/SA32windy/actions)
- Tagged releases (e.g., `v1.0.0`) automatically create GitHub releases

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is free to use and distribute. See [LICENSE](LICENSE) for details.

## 🙏 Credits

- **Windy Plugin**: [YannKerherve/Windy-plugin-GPS-from-TCP](https://github.com/YannKerherve/Windy-plugin-GPS-from-TCP)
- **Sailaway Simulator**: [sailaway.world](https://sailaway.world/)

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/SA32windy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/SA32windy/discussions)

## 🗺️ Screenshot

_Coming soon - screenshot of boat on Windy map_

---

**Happy Sailing!** ⛵

Made with ❤️ for the Sailaway community
