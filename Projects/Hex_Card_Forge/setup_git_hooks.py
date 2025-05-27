#!/usr/bin/env python3
"""
Setup Git Hooks for Hex Card Forge

This script sets up Git hooks to automatically update the PROJECT_GUIDE.md
file when commits are made or tests pass successfully.
"""

import os
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
GIT_HOOKS_DIR = PROJECT_ROOT / ".git" / "hooks"

# Hook content for post-commit
POST_COMMIT_HOOK = """#!/bin/sh
# Auto-update PROJECT_GUIDE.md after commit
echo "Running project guide updater..."
python update_project_guide.py
# If the guide was updated, offer to amend the commit
if git diff --quiet PROJECT_GUIDE.md; then
    echo "No changes to PROJECT_GUIDE.md."
else
    echo "PROJECT_GUIDE.md was updated."
    echo "Consider: git add PROJECT_GUIDE.md && git commit --amend --no-edit"
fi
"""

# Hook content for pre-push (run after successful tests)
PRE_PUSH_HOOK = """#!/bin/sh
# Auto-update PROJECT_GUIDE.md before push if tests pass
echo "Running tests before push..."
pytest
TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
    echo "Tests passed! Updating PROJECT_GUIDE.md..."
    python update_project_guide.py
    
    # Check if guide was updated
    if git diff --quiet PROJECT_GUIDE.md; then
        echo "No changes to PROJECT_GUIDE.md."
    else
        echo "PROJECT_GUIDE.md was updated. Adding to the commit..."
        git add PROJECT_GUIDE.md
        git commit --amend --no-edit
    fi
    
    exit 0
else
    echo "Tests failed. Push aborted."
    exit $TEST_STATUS
fi
"""

def setup_git_hooks():
    """Set up Git hooks to automatically update PROJECT_GUIDE.md."""
    if not (PROJECT_ROOT / ".git").exists():
        print("Error: No Git repository found. Initialize Git first with 'git init'.")
        return False
    
    # Create hooks directory if it doesn't exist
    GIT_HOOKS_DIR.mkdir(exist_ok=True)
    
    # Create post-commit hook
    post_commit_path = GIT_HOOKS_DIR / "post-commit"
    with open(post_commit_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(POST_COMMIT_HOOK)
    post_commit_path.chmod(0o755)  # Make executable
    
    # Create pre-push hook (runs after tests)
    pre_push_path = GIT_HOOKS_DIR / "pre-push"
    with open(pre_push_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PRE_PUSH_HOOK)
    pre_push_path.chmod(0o755)  # Make executable
    
    print("Git hooks installed successfully:")
    print(f"- Post-commit hook: {post_commit_path}")
    print(f"- Pre-push hook: {pre_push_path}")
    print("\nThe PROJECT_GUIDE.md will be automatically updated:")
    print("1. After each commit")
    print("2. Before push if tests pass")
    
    return True

def create_pytest_hook():
    """Create a pytest hook to update the guide after successful test runs."""
    conftest_path = PROJECT_ROOT / "conftest.py"
    
    pytest_hook = '''
"""Pytest configuration for automatic PROJECT_GUIDE.md updates."""
import subprocess
import pytest

def pytest_sessionfinish(session, exitstatus):
    """Run after all tests have completed."""
    if exitstatus == 0:
        # All tests passed, update project guide
        print("\\nTests passed! Updating PROJECT_GUIDE.md...")
        subprocess.run(['python', 'update_project_guide.py'])
    else:
        print("\\nSome tests failed. PROJECT_GUIDE.md not updated.")
'''
    
    if conftest_path.exists():
        # Append to existing conftest.py
        with open(conftest_path, 'a', encoding='utf-8') as f:
            f.write(pytest_hook)
    else:
        # Create new conftest.py
        with open(conftest_path, 'w', encoding='utf-8') as f:
            f.write(pytest_hook)
    
    print(f"Created pytest hook in {conftest_path}")
    print("The PROJECT_GUIDE.md will be updated after successful test runs.")

def main():
    """Main function to set up automation hooks."""
    print("Setting up automation for PROJECT_GUIDE.md updates...")
    
    # Setup Git hooks
    git_hooks_success = setup_git_hooks()
    
    # Create pytest hook
    create_pytest_hook()
    
    print("\nAutomation setup complete!")
    print("\nNow the PROJECT_GUIDE.md file will be automatically updated when:")
    print("1. Tests pass")
    print("2. Commits are made")
    print("3. Before pushing (if tests pass)")
    
    if not git_hooks_success:
        print("\nNote: Git hooks could not be installed. Make sure to initialize Git first.")
        print("Run 'git init' if you haven't already set up a Git repository.")

if __name__ == "__main__":
    main()
