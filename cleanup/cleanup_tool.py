#!/usr/bin/env python3
"""
Cleanup Tool
Removes all persistence mechanisms added by the educational backdoor
"""

import os
import sys
import platform
import subprocess

class CleanupTool:
    def __init__(self):
        self.system = platform.system()
        
    def run(self):
        """Main cleanup routine"""
        print("="*60)
        print("EDUCATIONAL BACKDOOR CLEANUP TOOL")
        print("Removes all persistence mechanisms")
        print("="*60)
        
        # Confirm cleanup
        print("\n⚠️  This will remove all persistence mechanisms added by")
        print("the educational backdoor demonstration.")
        
        response = input("\n[*] Type 'CLEAN' to proceed: ").strip()
        
        if response != "CLEAN":
            print("[*] Cleanup cancelled.")
            return
            
        print("\n[*] Starting cleanup...")
        
        # Perform cleanup based on OS
        if self.system == "Windows":
            self.clean_windows()
        elif self.system == "Linux":
            self.clean_linux()
        else:
            print("[!] Unsupported OS for cleanup")
            
        print("\n[✓] Cleanup complete!")
        print("[*] System has been restored to original state.")
        
    def clean_windows(self):
        """Clean Windows persistence"""
        try:
            import winreg
            
            print("[*] Removing registry entries...")
            
            # Open registry key
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_READ
            )
            
            # Try to delete our value
            try:
                winreg.DeleteValue(key, "SecurityEducationBackdoor")
                print("  ✅ Removed SecurityEducationBackdoor from registry")
            except FileNotFoundError:
                print("  ℹ️  No registry entry found")
                
            winreg.CloseKey(key)
            
        except ImportError:
            print("[!] winreg module not available")
        except Exception as e:
            print(f"[!] Registry cleanup error: {e}")
            
    def clean_linux(self):
        """Clean Linux persistence"""
        # Clean crontab
        print("[*] Cleaning crontab...")
        try:
            # Get current crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Filter out our entries
                filtered_lines = [
                    line for line in lines 
                    if 'EducationalBackdoor' not in line
                ]
                
                new_cron = '\n'.join(filtered_lines)
                
                # Write back filtered crontab
                proc = subprocess.run(['crontab', '-'], input=new_cron, text=True)
                if proc.returncode == 0:
                    print("  ✅ Cleaned crontab")
                else:
                    print("  ❌ Failed to clean crontab")
            else:
                print("  ℹ️  No crontab found")
                
        except Exception as e:
            print(f"  ❌ Crontab cleanup error: {e}")
            
        # Clean autostart
        print("[*] Cleaning autostart...")
        autostart_file = os.path.expanduser("~/.config/autostart/security-education.desktop")
        
        if os.path.exists(autostart_file):
            try:
                os.remove(autostart_file)
                print("  ✅ Removed autostart entry")
            except Exception as e:
                print(f"  ❌ Failed to remove autostart: {e}")
        else:
            print("  ℹ️  No autostart entry found")
            
        # Check for other potential persistence
        self.check_other_persistence()
        
    def check_other_persistence(self):
        """Check for other common persistence locations"""
        print("\n[*] Checking other persistence locations...")
        
        # Check bashrc
        bashrc = os.path.expanduser("~/.bashrc")
        if os.path.exists(bashrc):
            with open(bashrc, 'r') as f:
                content = f.read()
                if 'security-education' in content or 'EducationalBackdoor' in content:
                    print("  ⚠️  Found suspicious entries in .bashrc")
                    print("     Manual cleanup recommended")
                    
        # Check profile
        profile = os.path.expanduser("~/.profile")
        if os.path.exists(profile):
            with open(profile, 'r') as f:
                content = f.read()
                if 'security-education' in content or 'EducationalBackdoor' in content:
                    print("  ⚠️  Found suspicious entries in .profile")
                    print("     Manual cleanup recommended")

if __name__ == "__main__":
    cleanup = CleanupTool()
    cleanup.run()