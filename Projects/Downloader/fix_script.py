# Script to fix the corrupted CSS/QSS in modern_gui.py
import re

# Read the file content
with open('modern_gui.py', 'r') as f:
    content = f.read()

# Look for unenclosed CSS/QSS code
pattern = r'(QScrollBar::handle:horizontal \{\{[\s\S]*?min-width: 30px;[\s\S]*?width: 0px;)'
css_match = re.search(pattern, content)

if css_match:
    # Get the problematic code
    problematic_code = css_match.group(1)
    # Remove it from the content
    fixed_content = content.replace(problematic_code, "# CSS code removed - use theme.py for styling")
    
    # Write the fixed content back to the file
    with open('modern_gui.py', 'w') as f:
        f.write(fixed_content)
    
    print("Fixed the CSS/QSS code in modern_gui.py")
else:
    print("Could not find the problematic CSS/QSS code")
