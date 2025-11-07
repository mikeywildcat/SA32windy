# Configuration Examples for Sailaway to Windy GPS Bridge

## Common Sailaway TCP Configurations

### Local Sailaway Instance
```
IP Address: localhost (or 127.0.0.1)
Port: 5555
```

### Remote Sailaway Instance (same network)
```
IP Address: 192.168.1.100 (replace with your Sailaway PC's IP)
Port: 5555
```

### Custom Port
If Sailaway is configured to use a different port:
```
IP Address: localhost
Port: [Your custom port number]
```

## Windy Plugin Configuration

The bridge always serves data on:
```
URL: http://localhost:5000/gps-data
```

If you need to change the HTTP server port (5000), you'll need to modify line 97 in `sailaway_to_windy.py`:
```python
self.http_server = HTTPServer(('localhost', 5000), GPSHandler)
```

Change `5000` to your desired port, then update the Windy plugin to match.

## Finding Your Sailaway NMEA Port

1. Open Sailaway 3
2. Go to Settings
3. Look for NMEA or TCP settings
4. Note the port number (usually 5555)

## Network Setup

### Same Computer
- Use `localhost` or `127.0.0.1`
- No firewall configuration needed

### Different Computers (LAN)
- Find Sailaway computer's IP address:
  - Windows: Open CMD and type `ipconfig`
  - Look for "IPv4 Address"
- Use that IP address in the bridge
- May need to allow port through firewall

## Firewall Configuration (Windows)

If connecting from another computer:

1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port 5555 → Next
6. Allow the connection → Next
7. Apply to all profiles → Next
8. Name it "Sailaway NMEA" → Finish
