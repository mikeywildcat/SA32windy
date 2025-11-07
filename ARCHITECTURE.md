# 📊 System Architecture & Data Flow

## Overview

The Sailaway to Windy GPS Bridge acts as a middleware between Sailaway 3's NMEA output and the Windy GPS plugin.

## Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════╗
║                    SAILAWAY TO WINDY GPS BRIDGE                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────┐         ┌──────────────────┐         ┌──────┐ ║
║  │  Sailaway 3 │   TCP   │   Python Bridge  │  HTTP   │Windy │ ║
║  │             │────────▶│                  │────────▶│Plugin│ ║
║  │ NMEA Server │  :5555  │  TCP Receiver    │ :5000   │      │ ║
║  │             │         │       +          │         │      │ ║
║  └─────────────┘         │  HTTP Server     │         └──────┘ ║
║                          │       +          │                  ║
║                          │   Tkinter GUI    │                  ║
║                          └──────────────────┘                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Data Flow

### 1. NMEA Data Transmission (Sailaway → Bridge)

```
Sailaway 3 NMEA Output
        ↓
    TCP Socket (Port 5555)
        ↓
Python Socket Receiver
        ↓
    Buffer & Parse
        ↓
Extract GLL Sentences
        ↓
Rate Limit (2 seconds)
        ↓
Store Latest GPS Data
```

### 2. HTTP Serving (Bridge → Windy)

```
Windy Plugin Request
        ↓
GET http://localhost:5000/gps-data
        ↓
HTTP Server (Python)
        ↓
Return Latest GPS Data
        ↓
Windy Plugin Processes
        ↓
Display on Map
```

## NMEA Sentence Processing

### Input Format (from Sailaway)
```
$GPGLL,1938.9841,N,12342.9223,W,163016.360,A,A*5C
$IIGLL,1938.9841,N,12342.9223,W,163016.360,A,A*5C
$GPGGA,163016.360,1938.9841,N,12342.9223,W,1,12,0,0,M,0,M,0000,*6E
```

### Filtered Sentences (sent to Windy)
- **GPGLL/IIGLL**: Geographic Position - Latitude/Longitude only
- Updates sent every 2 seconds for smooth heading updates
- The Windy plugin calculates boat heading from consecutive position changes

### Example GPGLL Breakdown
```
$GPGLL,1938.9841,N,12342.9223,W,163016.360,A,A*5C
  │      │        │    │        │      │      │ │
  │      │        │    │        │      │      │ └─── Mode indicator
  │      │        │    │        │      │      └───── Status (A=valid)
  │      │        │    │        │      └──────────── Time (UTC)
  │      │        │    │        └─────────────────── Longitude direction
  │      │        │    └──────────────────────────── Longitude (123°42.9223')
  │      │        └───────────────────────────────── Latitude direction
  │      └────────────────────────────────────────── Latitude (19°38.9841')
  └───────────────────────────────────────────────── Sentence ID (GP=GPS, II=Integrated)
```

## Component Details

### TCP Receiver Thread
- **Purpose**: Continuously receives NMEA data from Sailaway
- **Implementation**: Threaded socket connection
- **Buffer**: Handles incomplete sentences
- **Filter**: Only processes GLL sentences (GPGLL/IIGLL)
- **Rate Limiting**: Updates every 2 seconds for optimal performance
- **Update**: Stores latest position data

### HTTP Server Thread
- **Purpose**: Serves GPS data to Windy plugin
- **Endpoint**: `/gps-data`
- **Method**: GET
- **Response**: Plain text NMEA sentence
- **CORS**: Enabled for browser access

### GUI Main Thread
- **Purpose**: User interaction and monitoring
- **Framework**: Tkinter
- **Features**:
  - Connection configuration
  - Start/Stop controls
  - Real-time activity log
  - Connection status indicator

## Threading Model

```
┌─────────────────────────────────────────────┐
│          Main Thread (GUI)                  │
│  - User Interface                           │
│  - Event Handling                           │
│  - Log Display                              │
└─────────────────────────────────────────────┘
              │
              ├─▶ Thread 1: TCP Receiver
              │   - Connect to Sailaway
              │   - Receive NMEA data
              │   - Parse and store GPS data
              │
              └─▶ Thread 2: HTTP Server
                  - Listen on port 5000
                  - Serve GPS data
                  - Handle Windy requests
```

## Error Handling

### Connection Errors
- **TCP Timeout**: 10 second timeout on socket operations
- **Connection Refused**: Retry mechanism (manual restart)
- **Data Loss**: Buffer incomplete sentences

### Recovery Strategies
- **Automatic**: Continue on temporary socket errors
- **Manual**: Restart bridge for connection failures
- **Graceful**: Clean shutdown on window close

## Performance Characteristics

- **Update Rate**: GPS position sent every 2 seconds (configurable in code)
- **Latency**: < 100ms typical
- **Memory**: < 50MB typical usage
- **Network**: Minimal bandwidth (~50 bytes per update)
- **CPU**: < 1% typical usage

## Security Considerations

### Network Exposure
- HTTP server only binds to `localhost` (127.0.0.1)
- No external network access by default
- TCP connection can be to remote host

### Data Privacy
- No data is logged to disk
- No external API calls
- All data stays local

## Extension Points

### To Add Features
1. **Data Logging**: Add file writing in TCP receiver
2. **Multiple Outputs**: Create additional HTTP endpoints
3. **Data Transformation**: Modify NMEA sentence processing
4. **Reconnection**: Add automatic retry logic
5. **Configuration File**: Save/load settings from JSON/INI

### To Modify Ports
1. **TCP Input Port**: Change in GUI or default value
2. **HTTP Output Port**: Modify line 97 in `sailaway_to_windy.py`

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| GUI | Tkinter (Python stdlib) |
| HTTP Server | http.server (Python stdlib) |
| TCP Client | socket (Python stdlib) |
| Threading | threading (Python stdlib) |
| Data Format | NMEA 0183 |

---

**No external dependencies required!** ✨
