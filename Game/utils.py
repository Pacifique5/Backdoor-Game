"""
Utility Functions
Helper functions for the educational backdoor game
"""

import sys
import platform
import os
import socket

def show_disclaimer():
    """Display ethical disclaimer and get consent"""
    disclaimer = """
╔══════════════════════════════════════════════════════════════════╗
║                    ETHICAL DISCLAIMER                            ║
╠══════════════════════════════════════════════════════════════════╣
║  This program is part of a CYBERSECURITY COURSE ASSIGNMENT      ║
║  at Rwanda Coding Academy.                                       ║
║                                                                  ║
║  By proceeding, you acknowledge:                                 ║
║                                                                  ║
║  1. This is for EDUCATIONAL PURPOSES ONLY                        ║
║  2. You are running this in an ISOLATED VIRTUAL MACHINE          ║
║  3. You will NOT deploy this on any real system                  ║
║  4. You understand the ethical implications                      ║
║  5. You will use this knowledge for DEFENSIVE purposes only      ║
║                                                                  ║
║  This program demonstrates:                                      ║
║  • How attackers hide malware in legitimate software            ║
║  • Persistence mechanisms used by malware                        ║
║  • Reverse shell functionality (in controlled environment)       ║
║                                                                  ║
║  Legal Note: Unauthorized use of these techniques is ILLEGAL    ║
║  and violates computer fraud laws.                               ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(disclaimer)
    
    response = input("\n[*] Type 'I UNDERSTAND' to proceed: ").strip()
    return response == "I UNDERSTAND"

def check_vm_environment():
    """Check if running in a VM (basic checks for educational safety)"""
    # This is a basic check - not foolproof
    vm_indicators = []
    
    # Check for VM-specific files/drivers
    if platform.system() == "Windows":
        vm_files = [
            "C:\\windows\\System32\\Drivers\\VBoxGuest.sys",
            "C:\\windows\\System32\\Drivers\\vmmouse.sys",
            "C:\\windows\\System32\\Drivers\\vm3dgl.dll"
        ]
        
        for file in vm_files:
            if os.path.exists(file):
                vm_indicators.append(True)
                
    elif platform.system() == "Linux":
        # Check for VM processes
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                if "hypervisor" in cpuinfo or "QEMU" in cpuinfo:
                    vm_indicators.append(True)
        except:
            pass
            
    # If no VM indicators found, show warning but don't block
    # (since this is educational, we want students to be aware)
    if not vm_indicators:
        print("\n[!] WARNING: No clear VM indicators detected!")
        print("[!] This program should ONLY be run in a virtual machine.")
        print("[!] Are you sure you want to continue?")
        
        response = input("[*] Type 'VM' to confirm you're in a VM: ").strip()
        return response == "VM"
        
    return True

def get_local_ip():
    """Get local IP address"""
    try:
        # Create temporary socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"