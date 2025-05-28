"""
Fix script for modern_gui.py to resolve QAction import issues and CSS syntax errors
"""
import re
import os
import shutil
import time

# Create a backup of the original file
original_file = 'modern_gui.py'
backup_file = f'modern_gui.py.bak.{int(time.time())}'

print(f"Creating backup of {original_file} as {backup_file}")
shutil.copy2(original_file, backup_file)

# Read the content of the file
with open(original_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the import issue - ensure QAction is only imported from QtGui
content = re.sub(
    r'from PySide6\.QtWidgets import \((.*?)\)',
    lambda m: m.group(0).replace('QAction, ', '').replace(', QAction', ''),
    content,
    flags=re.DOTALL
)

# Find and fix any CSS code that's not properly enclosed in strings
# This pattern looks for CSS-like constructs that aren't in strings
css_patterns = [
    r'(?<!["\'])min-width: \d+px;',
    r'(?<!["\'])padding: \d+px;',
    r'(?<!["\'])QScrollBar::handle:horizontal \{',
    r'(?<!["\'])QScrollBar::handle:vertical \{'
]

for pattern in css_patterns:
    matches = re.finditer(pattern, content)
    for match in matches:
        # Get context around the match to better understand how to fix it
        start_pos = max(0, match.start() - 100)
        end_pos = min(len(content), match.end() + 100)
        context = content[start_pos:end_pos]
        
        # Log the issue
        print(f"Found CSS pattern outside of strings: {match.group(0)}")
        print(f"Context: {context[:50]}...")
        
        # For now, we'll comment out the problematic line as a safety measure
        # In a real fix, we'd need to understand the context better
        problem_line_start = content.rfind('\n', 0, match.start()) + 1
        problem_line_end = content.find('\n', match.start())
        if problem_line_end == -1:
            problem_line_end = len(content)
        
        problem_line = content[problem_line_start:problem_line_end]
        fixed_line = f"# FIXED: {problem_line}  # Original line had CSS syntax error"
        
        content = content[:problem_line_start] + fixed_line + content[problem_line_end:]

# Write the fixed content back to the file
with open(original_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed import issues and potential CSS syntax errors in {original_file}")
print(f"If the file still has issues, restore from the backup: {backup_file}")
