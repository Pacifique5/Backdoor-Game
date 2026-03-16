"""
Security Awareness Game Engine
Educational game about cybersecurity concepts
"""

import time
import random
import sys

class SecurityAwarenessGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.player_name = ""
        
    def run(self):
        """Main game loop"""
        self.welcome_screen()
        self.get_player_info()
        
        while self.level <= 3:
            self.play_level()
            self.level += 1
            
        self.show_final_score()
        
    def welcome_screen(self):
        """Display game welcome screen"""
        welcome = """
╔══════════════════════════════════════════════════════════╗
║     SECURITY AWARENESS TRAINING GAME                     ║
║     Learn about cybersecurity while having fun!          ║
╠══════════════════════════════════════════════════════════╣
║  This game demonstrates:                                  ║
║  • How attackers hide malware in legitimate software    ║
║  • The importance of verifying software sources         ║
║  • Why you shouldn't run unknown programs               ║
║  • Persistence mechanisms used by malware               ║
╚══════════════════════════════════════════════════════════╝
"""
        print(welcome)
        time.sleep(2)
        
    def get_player_info(self):
        """Get player information"""
        self.player_name = input("\n[*] Enter your name: ")
        print(f"\n[*] Welcome, {self.player_name}! Let's test your security knowledge.\n")
        time.sleep(1)
        
    def play_level(self):
        """Play current level"""
        print(f"\n{'='*50}")
        print(f"LEVEL {self.level}")
        print(f"{'='*50}\n")
        
        if self.level == 1:
            self.level_1_basics()
        elif self.level == 2:
            self.level_2_threats()
        else:
            self.level_3_defense()
            
    def level_1_basics(self):
        """Level 1: Security Basics"""
        questions = [
            {
                "question": "What is phishing?",
                "options": [
                    "A) A type of fishing sport",
                    "B) An attempt to steal sensitive information by pretending to be trustworthy",
                    "C) A computer virus that deletes files",
                    "D) A security software"
                ],
                "correct": 1,
                "explanation": "Phishing is a social engineering attack where attackers disguise as trusted entities."
            },
            {
                "question": "What does HTTPS stand for?",
                "options": [
                    "A) Hyper Text Transfer Protocol Secure",
                    "B) High Tech Transfer Protocol System",
                    "C) Hyper Transfer Text Protocol Secure",
                    "D) None of the above"
                ],
                "correct": 0,
                "explanation": "HTTPS encrypts data between your browser and websites."
            }
        ]
        
        for q in questions:
            self.ask_question(q)
            
    def level_2_threats(self):
        """Level 2: Common Threats"""
        questions = [
            {
                "question": "What is a backdoor?",
                "options": [
                    "A) A physical door at the back of a building",
                    "B) A hidden way to bypass normal authentication",
                    "C) A type of firewall",
                    "D) An antivirus feature"
                ],
                "correct": 1,
                "explanation": "This game demonstrates a backdoor for educational purposes."
            },
            {
                "question": "What is persistence in malware?",
                "options": [
                    "A) How long malware runs",
                    "B) Malware's ability to survive reboots",
                    "C) Malware's infection rate",
                    "D) None of the above"
                ],
                "correct": 1,
                "explanation": "Persistence mechanisms ensure malware runs after system restart."
            }
        ]
        
        for q in questions:
            self.ask_question(q)
            
    def level_3_defense(self):
        """Level 3: Defense Strategies"""
        questions = [
            {
                "question": "How can you protect against backdoors?",
                "options": [
                    "A) Download software only from official sources",
                    "B) Use antivirus software",
                    "C) Keep systems updated",
                    "D) All of the above"
                ],
                "correct": 3,
                "explanation": "Multiple layers of defense provide the best protection."
            },
            {
                "question": "What should you do if you suspect malware?",
                "options": [
                    "A) Ignore it",
                    "B) Run a security scan and seek professional help",
                    "C) Continue using the computer normally",
                    "D) Delete System32"
                ],
                "correct": 1,
                "explanation": "Always take suspected infections seriously."
            }
        ]
        
        for q in questions:
            self.ask_question(q)
            
    def ask_question(self, q_data):
        """Present a question to the player"""
        print(f"\n{q_data['question']}")
        for option in q_data['options']:
            print(option)
            
        try:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            
            # Convert letter to index
            answer_index = ord(answer) - ord('A')
            
            if answer_index == q_data['correct']:
                print("✅ Correct!")
                print(f"   {q_data['explanation']}")
                self.score += 10
            else:
                print("❌ Not quite right.")
                print(f"   Correct answer: {q_data['options'][q_data['correct']]}")
                print(f"   {q_data['explanation']}")
                
        except:
            print("[!] Invalid input. Moving to next question.")
            
        time.sleep(1)
        
    def show_final_score(self):
        """Display final score and educational message"""
        print("\n" + "="*50)
        print("GAME COMPLETE!")
        print("="*50)
        print(f"\nFinal Score: {self.score}/60")
        
        if self.score >= 50:
            print("🏆 Excellent security awareness!")
        elif self.score >= 30:
            print("👍 Good foundation, keep learning!")
        else:
            print("📚 Keep studying cybersecurity basics!")
            
        educational_message = """
════════════════════ EDUCATIONAL NOTE ════════════════════
This game demonstrated how legitimate software can hide
malicious functionality. Remember:

• Always verify software sources
• Use VMs for testing unknown applications
• Keep security software updated
• Regular backups protect your data
• Report suspicious software to IT security

The backdoor and persistence shown here are for
educational purposes only. Never deploy such
techniques without authorization.

Stay safe and ethical! 🛡️
═══════════════════════════════════════════════════════════
"""
        print(educational_message)