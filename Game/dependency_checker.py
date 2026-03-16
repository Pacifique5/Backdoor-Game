"""
Dependency Checker Module
Checks for required applications and downloads from local server
"""

import os
import sys
import platform
import subprocess
import urllib.request
import urllib.error
import tempfile

class DependencyChecker:
    def __init__(self):
        self.system = platform.system()
        self.local_server = "http://192.168.56.1:8000"  # VM host IP
        self.required_apps = self.get_required_apps()
        
    def get_required_apps(self):
        """Get required apps based on OS"""
        if self.system == "Windows":
            return {
                'python': {
                    'check_cmd': ['python', '--version'],
                    'installer': 'python-3.9.0.exe',
                    'install_args': ['/quiet', 'InstallAllUsers=1', 'PrependPath=1']
                },
                'git': {
                    'check_cmd': ['git', '--version'],
                    'installer': 'git-2.35.0.exe',
                    'install_args': ['/SILENT']
                }
            }
        else:  # Linux
            return {
                'python3': {
                    'check_cmd': ['python3', '--version'],
                    'installer': None,  # Use package manager
                    'package': 'python3'
                },
                'git': {
                    'check_cmd': ['git', '--version'],
                    'installer': None,
                    'package': 'git'
                }
            }
            
    def check_all(self):
        """Check if all dependencies are installed"""
        print("\n[*] Checking required dependencies...")
        all_installed = True
        
        for app_name, app_info in self.required_apps.items():
            if self.check_app(app_info['check_cmd']):
                print(f"  ✅ {app_name} is installed")
            else:
                print(f"  ❌ {app_name} is NOT installed")
                all_installed = False
                
        return all_installed
        
    def check_app(self, check_cmd):
        """Check if a specific app is installed"""
        try:
            subprocess.run(check_cmd, capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def install_all(self):
        """Install all missing dependencies"""
        print("\n[*] Installing missing dependencies from local server...")
        success = True
        
        for app_name, app_info in self.required_apps.items():
            if not self.check_app(app_info['check_cmd']):
                print(f"[*] Installing {app_name}...")
                if not self.install_app(app_name, app_info):
                    print(f"[!] Failed to install {app_name}")
                    success = False
                    
        return success
        
    def install_app(self, app_name, app_info):
        """Install a specific app"""
        try:
            if self.system == "Windows":
                return self.install_windows(app_name, app_info)
            else:
                return self.install_linux(app_name, app_info)
        except Exception as e:
            print(f"[!] Installation error: {e}")
            return False
            
    def install_windows(self, app_name, app_info):
        """Windows installation from local server"""
        # Download installer
        installer_url = f"{self.local_server}/{app_info['installer']}"
        installer_path = os.path.join(tempfile.gettempdir(), app_info['installer'])
        
        print(f"[*] Downloading from {installer_url}")
        
        try:
            # Download with progress indicator
            urllib.request.urlretrieve(installer_url, installer_path)
            print(f"[*] Downloaded to {installer_path}")
            
            # Run installer silently
            install_cmd = [installer_path] + app_info['install_args']
            subprocess.run(install_cmd, check=True)
            
            print(f"[*] {app_name} installed successfully")
            return True
            
        except urllib.error.URLError:
            print(f"[!] Could not download from local server")
            print("[!] Make sure file_server.py is running")
            return False
        except Exception as e:
            print(f"[!] Installation failed: {e}")
            return False
            
    def install_linux(self, app_name, app_info):
        """Linux installation using package manager"""
        try:
            # Check if sudo is available (Linux only)
            if not hasattr(os, 'geteuid') or os.geteuid() != 0:
                print("[!] Root privileges required for installation")
                print("[!] Please run with sudo")
                return False
                
            # Use apt for Debian/Ubuntu
            subprocess.run(['apt', 'update'], check=True)
            subprocess.run(['apt', 'install', '-y', app_info['package']], check=True)
            
            print(f"[*] {app_name} installed successfully")
            return True
            
        except Exception as e:
            print(f"[!] Installation failed: {e}")
            return False