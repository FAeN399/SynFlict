"""
Tests for the command-line interface.
"""

import subprocess
import sys
import unittest


class TestCLI(unittest.TestCase):
    """Test CLI functionality."""
    
    def test_help_command(self):
        """Test that 'grabber --help' exits with code 0 and displays usage."""
        result = subprocess.run(
            [sys.executable, "-m", "grabber.cli", "--help"],
            capture_output=True,
            text=True
        )
        
        # Check exit code
        self.assertEqual(result.returncode, 0, 
                         f"Help command failed with: {result.stderr}")
        
        # Check that output contains expected help text
        output = result.stdout.lower()
        self.assertIn("usage", output)
        self.assertIn("reddit", output)
        self.assertIn("grabber", output)


if __name__ == "__main__":
    unittest.main()
