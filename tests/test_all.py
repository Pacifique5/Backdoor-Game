"""
Quick smoke tests — verifies all modules import and core logic runs.
No VMs or network required.

Run with:
    python tests/test_all.py
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Make sure Game/ and other folders are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Game'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Server'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cleanup'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ─────────────────────────────────────────────
# 1. IMPORTS — do all modules load without error?
# ─────────────────────────────────────────────
class TestImports(unittest.TestCase):

    def test_game_engine_imports(self):
        import game_engine
        self.assertTrue(hasattr(game_engine, 'SecurityAwarenessGame'))

    def test_dependency_checker_imports(self):
        import dependency_checker
        self.assertTrue(hasattr(dependency_checker, 'DependencyChecker'))

    def test_persistence_imports(self):
        import persistence
        self.assertTrue(hasattr(persistence, 'PersistenceManager'))

    def test_reverse_shell_imports(self):
        import reverse_shell
        self.assertTrue(hasattr(reverse_shell, 'ReverseShell'))

    def test_utils_imports(self):
        import utils
        self.assertTrue(hasattr(utils, 'show_disclaimer'))
        self.assertTrue(hasattr(utils, 'check_vm_environment'))

    def test_file_server_imports(self):
        import file_server
        self.assertTrue(hasattr(file_server, 'DependencyServer'))

    def test_listener_imports(self):
        import listener
        self.assertTrue(hasattr(listener, 'Listener'))

    def test_cleanup_tool_imports(self):
        import cleanup_tool
        self.assertTrue(hasattr(cleanup_tool, 'CleanupTool'))


# ─────────────────────────────────────────────
# 2. UTILS — disclaimer and VM check logic
# ─────────────────────────────────────────────
class TestUtils(unittest.TestCase):

    def test_disclaimer_accepts_correct_input(self):
        from utils import show_disclaimer
        with patch('builtins.input', return_value='I UNDERSTAND'):
            result = show_disclaimer()
        self.assertTrue(result)

    def test_disclaimer_rejects_wrong_input(self):
        from utils import show_disclaimer
        with patch('builtins.input', return_value='yes'):
            result = show_disclaimer()
        self.assertFalse(result)

    def test_vm_check_accepts_vm_input(self):
        from utils import check_vm_environment
        # Patch os.path.exists to return False (no VM drivers found)
        # then user types 'VM'
        with patch('os.path.exists', return_value=False), \
             patch('builtins.input', return_value='VM'), \
             patch('builtins.open', side_effect=OSError):
            result = check_vm_environment()
        self.assertTrue(result)

    def test_vm_check_rejects_wrong_input(self):
        from utils import check_vm_environment
        with patch('os.path.exists', return_value=False), \
             patch('builtins.input', return_value='no'), \
             patch('builtins.open', side_effect=OSError):
            result = check_vm_environment()
        self.assertFalse(result)

    def test_get_local_ip_returns_string(self):
        from utils import get_local_ip
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertGreater(len(ip), 0)


# ─────────────────────────────────────────────
# 3. DEPENDENCY CHECKER — check/install logic
# ─────────────────────────────────────────────
class TestDependencyChecker(unittest.TestCase):

    def test_check_app_returns_true_when_found(self):
        from dependency_checker import DependencyChecker
        checker = DependencyChecker()
        # python itself is definitely installed
        result = checker.check_app([sys.executable, '--version'])
        self.assertTrue(result)

    def test_check_app_returns_false_when_missing(self):
        from dependency_checker import DependencyChecker
        checker = DependencyChecker()
        result = checker.check_app(['nonexistent_binary_xyz', '--version'])
        self.assertFalse(result)

    def test_check_all_returns_bool(self):
        from dependency_checker import DependencyChecker
        checker = DependencyChecker()
        result = checker.check_all()
        self.assertIsInstance(result, bool)

    def test_required_apps_not_empty(self):
        from dependency_checker import DependencyChecker
        checker = DependencyChecker()
        self.assertGreater(len(checker.required_apps), 0)


# ─────────────────────────────────────────────
# 4. PERSISTENCE — setup doesn't crash
# ─────────────────────────────────────────────
class TestPersistence(unittest.TestCase):

    def test_windows_persistence_no_crash(self):
        from persistence import PersistenceManager
        pm = PersistenceManager()
        # Mock winreg so it doesn't actually write to registry
        mock_winreg = MagicMock()
        with patch.dict('sys.modules', {'winreg': mock_winreg}):
            with patch.object(pm, 'system', 'Windows'):
                try:
                    pm.setup_windows_persistence()
                except Exception as e:
                    self.fail(f"setup_windows_persistence raised unexpectedly: {e}")

    def test_linux_persistence_no_crash(self):
        from persistence import PersistenceManager
        pm = PersistenceManager()
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = ""
        with patch('subprocess.run', return_value=mock_proc), \
             patch('os.makedirs'), \
             patch('builtins.open', unittest.mock.mock_open()):
            with patch.object(pm, 'system', 'Linux'):
                try:
                    pm.setup_linux_persistence()
                except Exception as e:
                    self.fail(f"setup_linux_persistence raised unexpectedly: {e}")

    def test_get_persistence_locations_windows(self):
        from persistence import PersistenceManager
        pm = PersistenceManager()
        with patch.object(pm, 'system', 'Windows'):
            locs = pm.get_persistence_locations()
        self.assertIsInstance(locs, list)
        self.assertGreater(len(locs), 0)

    def test_get_persistence_locations_linux(self):
        from persistence import PersistenceManager
        pm = PersistenceManager()
        with patch.object(pm, 'system', 'Linux'):
            locs = pm.get_persistence_locations()
        self.assertIsInstance(locs, list)
        self.assertGreater(len(locs), 0)


# ─────────────────────────────────────────────
# 5. REVERSE SHELL — object creation and config
# ─────────────────────────────────────────────
class TestReverseShell(unittest.TestCase):

    def test_default_ip_and_port(self):
        from reverse_shell import ReverseShell
        import config
        shell = ReverseShell()
        self.assertEqual(shell.server_ip, config.ATTACKER_IP)
        self.assertEqual(shell.server_port, config.LISTENER_PORT)

    def test_custom_ip_and_port(self):
        from reverse_shell import ReverseShell
        shell = ReverseShell(server_ip='10.0.0.1', server_port=9999)
        self.assertEqual(shell.server_ip, '10.0.0.1')
        self.assertEqual(shell.server_port, 9999)

    def test_execute_command_returns_output(self):
        from reverse_shell import ReverseShell
        shell = ReverseShell()
        shell.sock = MagicMock()
        # Run a simple cross-platform command
        shell.execute_command('echo hello')
        shell.sock.send.assert_called_once()
        sent = shell.sock.send.call_args[0][0].decode()
        self.assertIn('hello', sent)

    def test_execute_cd_command(self):
        from reverse_shell import ReverseShell
        shell = ReverseShell()
        shell.sock = MagicMock()
        original_dir = os.getcwd()
        shell.execute_command(f'cd {original_dir}')
        shell.sock.send.assert_called_once()
        sent = shell.sock.send.call_args[0][0].decode()
        self.assertIn('Changed directory', sent)


# ─────────────────────────────────────────────
# 6. GAME ENGINE — runs without crashing
# ─────────────────────────────────────────────
class TestGameEngine(unittest.TestCase):

    def test_instantiation(self):
        from game_engine import SecurityAwarenessGame
        game = SecurityAwarenessGame()
        self.assertEqual(game.score, 0)
        self.assertEqual(game.level, 1)

    def test_ask_question_correct_answer(self):
        from game_engine import SecurityAwarenessGame
        game = SecurityAwarenessGame()
        q = {
            'question': 'Test?',
            'options': ['A) Wrong', 'B) Correct', 'C) Wrong', 'D) Wrong'],
            'correct': 1,
            'explanation': 'Because B.'
        }
        with patch('builtins.input', return_value='B'):
            game.ask_question(q)
        self.assertEqual(game.score, 10)

    def test_ask_question_wrong_answer(self):
        from game_engine import SecurityAwarenessGame
        game = SecurityAwarenessGame()
        q = {
            'question': 'Test?',
            'options': ['A) Wrong', 'B) Correct', 'C) Wrong', 'D) Wrong'],
            'correct': 1,
            'explanation': 'Because B.'
        }
        with patch('builtins.input', return_value='A'):
            game.ask_question(q)
        self.assertEqual(game.score, 0)

    def test_ask_question_invalid_input_no_crash(self):
        from game_engine import SecurityAwarenessGame
        game = SecurityAwarenessGame()
        q = {
            'question': 'Test?',
            'options': ['A) Wrong', 'B) Correct', 'C) Wrong', 'D) Wrong'],
            'correct': 1,
            'explanation': 'Because B.'
        }
        with patch('builtins.input', return_value='Z'):
            try:
                game.ask_question(q)
            except Exception as e:
                self.fail(f"ask_question crashed on invalid input: {e}")


# ─────────────────────────────────────────────
# 7. CLEANUP TOOL — removal logic
# ─────────────────────────────────────────────
class TestCleanupTool(unittest.TestCase):

    def test_instantiation(self):
        from cleanup_tool import CleanupTool
        ct = CleanupTool()
        self.assertIsNotNone(ct.system)

    def test_clean_linux_crontab_no_crash(self):
        from cleanup_tool import CleanupTool
        ct = CleanupTool()
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "# some crontab\n@reboot python3 /game/main.py # EducationalBackdoor\n"
        with patch('subprocess.run', return_value=mock_proc), \
             patch('os.path.exists', return_value=False):
            try:
                ct.clean_linux()
            except Exception as e:
                self.fail(f"clean_linux raised unexpectedly: {e}")

    def test_clean_linux_removes_backdoor_entry(self):
        from cleanup_tool import CleanupTool
        ct = CleanupTool()
        captured_input = []

        def fake_run(cmd, **kwargs):
            m = MagicMock()
            m.returncode = 0
            if '-l' in cmd:
                m.stdout = "# keep this\n@reboot python3 /game/main.py # EducationalBackdoor\n"
            else:
                # Capture what was written back to crontab
                captured_input.append(kwargs.get('input', ''))
                m.stdout = ''
            return m

        with patch('subprocess.run', side_effect=fake_run), \
             patch('os.path.exists', return_value=False):
            ct.clean_linux()

        # The EducationalBackdoor line should NOT be in the new crontab
        if captured_input:
            self.assertNotIn('EducationalBackdoor', captured_input[0])

    def test_clean_windows_no_crash_when_key_missing(self):
        from cleanup_tool import CleanupTool
        ct = CleanupTool()
        mock_winreg = MagicMock()
        mock_winreg.DeleteValue.side_effect = FileNotFoundError
        with patch.dict('sys.modules', {'winreg': mock_winreg}):
            with patch.object(ct, 'system', 'Windows'):
                try:
                    ct.clean_windows()
                except Exception as e:
                    self.fail(f"clean_windows raised unexpectedly: {e}")


# ─────────────────────────────────────────────
# 8. FILE SERVER — directory config
# ─────────────────────────────────────────────
class TestFileServer(unittest.TestCase):

    def test_dependencies_folder_path_correct_case(self):
        from file_server import DependencyServer
        server = DependencyServer()
        self.assertTrue(server.directory.endswith('Dependencies'))

    def test_default_port(self):
        from file_server import DependencyServer
        server = DependencyServer()
        self.assertEqual(server.port, 8000)

    def test_custom_port(self):
        from file_server import DependencyServer
        server = DependencyServer(port=9090)
        self.assertEqual(server.port, 9090)

    def test_dependencies_folder_exists(self):
        from file_server import DependencyServer
        server = DependencyServer()
        self.assertTrue(os.path.isdir(server.directory),
                        f"Dependencies folder not found at: {server.directory}")


# ─────────────────────────────────────────────
# 9. LISTENER — socket config
# ─────────────────────────────────────────────
class TestListener(unittest.TestCase):

    def test_default_ip_and_port(self):
        from listener import Listener
        l = Listener()
        self.assertEqual(l.ip, '0.0.0.0')
        self.assertEqual(l.port, 4444)

    def test_custom_ip_and_port(self):
        from listener import Listener
        l = Listener(ip='127.0.0.1', port=5555)
        self.assertEqual(l.ip, '127.0.0.1')
        self.assertEqual(l.port, 5555)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    