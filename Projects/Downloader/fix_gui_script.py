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

# Fix 1: Fix the QAction import issue - ensure it's only imported from QtGui not QtWidgets
old_imports = re.search(r'from PySide6\.QtWidgets import \((.+?)\)', content, re.DOTALL)
if old_imports and 'QAction' in old_imports.group(1):
    fixed_imports = old_imports.group(1).replace('QAction, ', '').replace(', QAction', '')
    content = content.replace(old_imports.group(1), fixed_imports)
    print("Fixed QAction import issue")

# Fix 2: Remove any direct CSS code that's causing syntax errors
# Lines 159 and 188 were reported as having issues with min-width and padding
line_number = 1
fixed_content = []

for line in content.splitlines():
    # Look for CSS patterns that would cause syntax errors in Python
    if re.search(r'^\s*min-width:', line) or re.search(r'^\s*padding:', line):
        print(f"Found problematic CSS at line {line_number}: {line}")
        # Skip this line or comment it out
        fixed_content.append(f"# REMOVED CSS SYNTAX ERROR: {line}")
    else:
        fixed_content.append(line)
    line_number += 1

# Write the fixed content back to the file
with open(original_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_content))

print(f"Fixed potential CSS syntax errors in {original_file}")
print(f"If the file still has issues, restore from the backup: {backup_file}")
