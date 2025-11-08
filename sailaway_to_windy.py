"""
Sailaway 3 to Windy GPS Bridge
Connects to Sailaway 3's NMEA TCP feed and serves it to the Windy GPS plugin
"""

import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
from datetime import datetime


class GPSBridge:
    """Handles connection to Sailaway and GPS data management"""
    
    def __init__(self):
        self.latest_gps_data = ""  # Current GPS data being served to plugin
        self.previous_gps_data = ""  # Track previous NMEA sentence
        self.last_sent_position = (0.0, 0.0, 0.0)  # lat, lon, timestamp
        self.is_running = False
        self.tcp_socket = None
        self.tcp_thread = None
        self.http_server = None
        self.http_thread = None
        self.log_callback = None
        self.last_update_time = 0  # Track last update time for rate limiting
        
    def set_log_callback(self, callback):
        """Set the callback function for logging"""
        self.log_callback = callback
        
    def log(self, message):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        if self.log_callback:
            self.log_callback(log_message)
        print(log_message)
        
    def start_tcp_connection(self, host, port):
        """Start TCP connection to Sailaway"""
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.settimeout(10)
            self.log(f"Connecting to {host}:{port}...")
            self.tcp_socket.connect((host, port))
            self.log(f"✓ Connected to Sailaway at {host}:{port}")
            return True
        except Exception as e:
            self.log(f"✗ Failed to connect to Sailaway: {e}")
            return False
            
    def receive_nmea_data(self):
        """Receive NMEA data from TCP connection"""
        buffer = ""
        while self.is_running:
            try:
                data = self.tcp_socket.recv(1024).decode('utf-8', errors='ignore')
                if not data:
                    self.log("Connection closed by Sailaway")
                    break
                    
                buffer += data
                lines = buffer.split('\n')
                buffer = lines[-1]  # Keep incomplete line in buffer
                
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        # Only process GLL sentences - Windy plugin can only parse GLL
                        # Plugin calculates bearing from position changes
                        # Strategy: Send positions with meaningful separation (distance OR time)
                        if '$GPGLL' in line or '$IIGLL' in line:
                            if line != self.previous_gps_data:
                                try:
                                    # Parse position from GLL: $GPGLL,ddmm.mmmm,N/S,dddmm.mmmm,E/W,...
                                    parts = line.split(',')
                                    if len(parts) >= 5 and parts[1] and parts[3]:
                                        # Convert NMEA to decimal degrees
                                        lat_str, lat_dir = parts[1], parts[2]
                                        lon_str, lon_dir = parts[3], parts[4]
                                        
                                        lat = float(lat_str[:2]) + float(lat_str[2:]) / 60.0
                                        if lat_dir == 'S':
                                            lat = -lat
                                        lon = float(lon_str[:3]) + float(lon_str[3:]) / 60.0
                                        if lon_dir == 'W':
                                            lon = -lon
                                        
                                        # Check distance and time since last update
                                        last_lat, last_lon, last_time = self.last_sent_position
                                        current_time = time.time()
                                        distance = ((lat - last_lat)**2 + (lon - last_lon)**2)**0.5
                                        time_delta = current_time - last_time
                                        
                                        # Send if: moved 0.0002° (~22m) OR 2 seconds elapsed OR first position
                                        if distance >= 0.0002 or time_delta >= 2.0 or last_lat == 0.0:
                                            self.latest_gps_data = line
                                            self.previous_gps_data = line
                                            self.last_sent_position = (lat, lon, current_time)
                                            
                                            # Log rate limited
                                            if current_time - self.last_update_time >= 0.5:
                                                self.last_update_time = current_time
                                                self.log(f"GPS: Δ{distance:.6f}° ({time_delta:.1f}s) {line[:60]}...")
                                except (ValueError, IndexError):
                                    # Parse error - use sentence as-is
                                    self.latest_gps_data = line
                                    self.previous_gps_data = line
                            
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    self.log(f"Error receiving data: {e}")
                break
                
    def start(self, host, port):
        """Start the GPS bridge"""
        if self.is_running:
            self.log("Bridge is already running")
            return False
            
        self.is_running = True
        
        # Start TCP connection
        if not self.start_tcp_connection(host, port):
            self.is_running = False
            return False
            
        # Start TCP receiver thread
        self.tcp_thread = threading.Thread(target=self.receive_nmea_data, daemon=True)
        self.tcp_thread.start()
        
        # Start HTTP server
        self.start_http_server()
        
        self.log("✓ GPS Bridge is running")
        return True
        
    def stop(self):
        """Stop the GPS bridge"""
        if not self.is_running:
            return
            
        self.log("Stopping GPS Bridge...")
        self.is_running = False
        
        # Close TCP socket
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
            except:
                pass
                
        # Stop HTTP server
        if self.http_server:
            try:
                self.http_server.shutdown()
            except:
                pass
                
        self.log("✓ GPS Bridge stopped")
        
    def start_http_server(self):
        """Start HTTP server for Windy plugin"""
        bridge = self
        
        class GPSHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/gps-data':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    # Only send data if we have valid GPS data
                    if bridge.latest_gps_data:
                        self.wfile.write(bridge.latest_gps_data.encode())
                    else:
                        # Send empty response if no data yet
                        self.wfile.write(b'')
                else:
                    self.send_response(404)
                    self.end_headers()
                    
            def log_message(self, format, *args):
                # Suppress HTTP server logs
                pass
                
        def run_server():
            try:
                self.http_server = HTTPServer(('localhost', 5000), GPSHandler)
                bridge.log("✓ HTTP server started on localhost:5000")
                self.http_server.serve_forever()
            except Exception as e:
                bridge.log(f"✗ HTTP server error: {e}")
                
        self.http_thread = threading.Thread(target=run_server, daemon=True)
        self.http_thread.start()


class BridgeGUI:
    """GUI for the GPS Bridge application"""
    
    def __init__(self):
        self.bridge = GPSBridge()
        self.window = tk.Tk()
        self.window.title("Sailaway to Windy GPS Bridge")
        self.window.geometry("700x550")
        self.window.resizable(True, True)
        
        # Set up the GUI
        self.setup_gui()
        
        # Set log callback
        self.bridge.set_log_callback(self.add_log)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_gui(self):
        """Set up the GUI components"""
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Sailaway 3 → Windy GPS Bridge", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Connection settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Sailaway Connection Settings", 
                                       padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # IP Address
        ttk.Label(settings_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_entry = ttk.Entry(settings_frame, width=20)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Port
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=5)
        self.port_entry = ttk.Entry(settings_frame, width=10)
        self.port_entry.insert(0, "10110")
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Bridge", 
                                      command=self.start_bridge, width=15)
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop Bridge", 
                                     command=self.stop_bridge, width=15, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Clear log button
        self.clear_button = ttk.Button(button_frame, text="Clear Log", 
                                      command=self.clear_log, width=15)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="● Not connected", 
                                     foreground="red", font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Info label
        info_text = "Windy plugin will connect to: http://localhost:5000/gps-data"
        ttk.Label(status_frame, text=info_text, foreground="gray").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70, 
                                                 wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add initial log message
        self.add_log("Ready to connect to Sailaway 3")
        self.add_log("Enter the IP address and port of your Sailaway NMEA TCP feed")
        
    def add_log(self, message):
        """Add a message to the log"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
    def start_bridge(self):
        """Start the GPS bridge"""
        host = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        # Validate inputs
        if not host:
            self.add_log("✗ Error: Please enter an IP address")
            return
            
        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError()
        except ValueError:
            self.add_log("✗ Error: Please enter a valid port number (1-65535)")
            return
            
        # Start the bridge
        if self.bridge.start(host, port):
            self.start_button.configure(state=tk.DISABLED)
            self.stop_button.configure(state=tk.NORMAL)
            self.ip_entry.configure(state=tk.DISABLED)
            self.port_entry.configure(state=tk.DISABLED)
            self.status_label.configure(text="● Connected", foreground="green")
        else:
            self.status_label.configure(text="● Connection failed", foreground="red")
            
    def stop_bridge(self):
        """Stop the GPS bridge"""
        self.bridge.stop()
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.ip_entry.configure(state=tk.NORMAL)
        self.port_entry.configure(state=tk.NORMAL)
        self.status_label.configure(text="● Not connected", foreground="red")
        
    def on_closing(self):
        """Handle window closing"""
        self.bridge.stop()
        self.window.destroy()
        
    def run(self):
        """Run the GUI"""
        self.window.mainloop()


def main():
    """Main entry point"""
    app = BridgeGUI()
    app.run()


if __name__ == "__main__":
    main()
