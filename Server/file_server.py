#!/usr/bin/env python3
"""
Local HTTP Server for Dependencies
Hosts required applications for educational demonstration
"""

import http.server
import socketserver
import os
import socket

class DependencyServer:
    def __init__(self, port=8000):
        self.port = port
        self.directory = os.path.join(os.path.dirname(__file__), 'Dependencies')
        
    def start(self):
        """Start the HTTP server"""
        # Create dependencies directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print(f"[*] Created dependencies folder at: {self.directory}")
            print("[*] Place required installers here (python-3.9.0.exe, git-2.35.0.exe)")
            
        # Change to dependencies directory
        os.chdir(self.directory)
        
        # Get local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Setup HTTP server
        handler = http.server.SimpleHTTPRequestHandler
        
        print("="*60)
        print("DEPENDENCY FILE SERVER")
        print("For Cybersecurity Course - VM Only")
        print("="*60)
        print(f"[*] Server started on:")
        print(f"    - Local: http://127.0.0.1:{self.port}")
        print(f"    - Network: http://{local_ip}:{self.port}")
        print(f"[*] Serving files from: {self.directory}")
        print("[*] Available files:")
        
        # List available files
        for file in os.listdir('.'):
            if os.path.isfile(file):
                size = os.path.getsize(file) / (1024*1024)  # Convert to MB
                print(f"    - {file} ({size:.2f} MB)")
                
        print("\n[*] Press Ctrl+C to stop server")
        print("="*60)
        
        # Start server
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Shutting down file server...")
            httpd.shutdown()

if __name__ == "__main__":
    server = DependencyServer()
    server.start()