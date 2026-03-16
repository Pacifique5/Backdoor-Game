# Educational Backdoor Game - Cybersecurity Course Project

## Project Overview
This project demonstrates cybersecurity concepts including backdoors, persistence mechanisms, and reverse shells for **educational purposes only**. All testing must be done in isolated virtual machines.

## Team Members
- [Student 1 Name]
- [Student 2 Name]
- [Student 3 Name]

## Installation & Setup

### Prerequisites
- Virtual Machine software (VirtualBox/VMware)
- Isolated VM network
- Python 3.6+ on all machines

### VM Network Setup
1. Create two VMs:
   - **Target VM**: Runs the game
   - **Attacker VM**: Runs the listener
2. Configure Host-Only Network:
   - IP Range: 192.168.56.0/24
   - Target VM IP: 192.168.56.101
   - Attacker VM IP: 192.168.56.1

### Step 1: Start Dependency Server (Attacker VM)
```bash
cd server
python file_server.py