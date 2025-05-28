# Comprehensive script to fix all CSS/QSS issues in modern_gui.py
import re

def fix_file():
    try:
        # Read the original file
        with open('modern_gui.py', 'r') as f:
            content = f.read()
        
        # First try to find the next problematic CSS line
        match = re.search(r'([a-zA-Z0-9:_#\-]+\s*{{\s*|[a-zA-Z0-9:_#\-]+:[^;]*;\s*|padding:\s*\d+px;|min-width:\s*\d+px;|width:\s*\d+px;)', content)
        
        if match:
            start_pos = match.start()
            # Find the beginning of the line
            line_start = content.rfind('\n', 0, start_pos) + 1
            # Find a good place to cut off - the next class definition or end of file
            good_parts = re.search(r'(class\s+[A-Za-z0-9_]+\(|def\s+[A-Za-z0-9_]+\(|if\s+__name__\s*==\s*)', content[start_pos:])
            
            if good_parts:
                cut_off = start_pos + good_parts.start()
            else:
                # If no good cut-off point found, just keep the imports
                imports_end = 0
                for match in re.finditer(r'^import\s+|^from\s+', content, re.MULTILINE):
                    imports_end = max(imports_end, match.end() + content[match.end():].find('\n') + 1)
                
                if imports_end > 0:
                    cleaned_content = content[:imports_end]
                    cleaned_content += "\n\n# Import custom modules\nfrom gui_backend import GUIBackend\nimport theme as app_theme\n\n"
                    
                    # Find any useful class definitions
                    class_defs = re.findall(r'(class\s+[A-Za-z0-9_]+\([^)]+\):[\s\S]+?(?=class\s+|\Z))', content)
                    for class_def in class_defs:
                        if 'QScrollBar' not in class_def and 'padding:' not in class_def:
                            cleaned_content += class_def + "\n\n"
                    
                    with open('modern_gui.py', 'w') as f:
                        f.write(cleaned_content)
                    
                    return "File has been comprehensively cleaned by preserving imports and class definitions"
            
            # Remove problematic CSS section
            with open('modern_gui.py', 'w') as f:
                # Keep the code before the problematic section
                f.write(content[:line_start])
                f.write("# CSS code removed - use theme.py for styling\n")
                # Keep code after the problematic section if a good cutoff was found
                if good_parts:
                    f.write(content[cut_off:])
            
            return f"Removed problematic CSS section starting at position {start_pos}"
        else:
            return "No CSS issues found in the file"
            
    except Exception as e:
        return f"Error during fix: {str(e)}"

if __name__ == "__main__":
    result = fix_file()
    print(result)
