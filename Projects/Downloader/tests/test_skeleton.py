"""
Basic tests to verify that the project scaffolding is correct.
"""

import subprocess
import sys
import unittest


class TestSkeleton(unittest.TestCase):
    """Test basic project structure and imports."""

    def test_import(self):
        """Verify that the grabber package can be imported."""
        result = subprocess.run(
            [sys.executable, "-c", "import grabber"], 
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, 
                        f"Failed to import grabber: {result.stderr}")
        
        # Additionally check that version is properly defined
        result = subprocess.run(
            [sys.executable, "-c", "import grabber; print(grabber.__version__)"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, 
                        f"Failed to get grabber version: {result.stderr}")
        self.assertRegex(result.stdout.strip(), r"^\d+\.\d+\.\d+$", 
                        "Version should follow semantic versioning")


if __name__ == "__main__":
    unittest.main()
