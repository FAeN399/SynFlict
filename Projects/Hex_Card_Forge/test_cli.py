"""
Simple test script for the CLI interface
"""
from cardforge.cli import app

if __name__ == "__main__":
    app(["--help"])  # Shows help message with available commands
    print("\n--- Direct title screen test ---")
    app([])  # Should show the title screen
