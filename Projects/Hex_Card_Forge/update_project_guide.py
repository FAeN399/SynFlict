#!/usr/bin/env python3
"""
Project Guide Updater

This script automatically updates the Development Status section in PROJECT_GUIDE.md
based on completed tasks in todo.md. Run this script after completing tasks to keep
the project guide in sync with development progress.
"""

import re
import datetime
from pathlib import Path
from collections import defaultdict

# File paths
PROJECT_ROOT = Path(__file__).parent
TODO_FILE = PROJECT_ROOT / "todo.md"
PROJECT_GUIDE_FILE = PROJECT_ROOT / "PROJECT_GUIDE.md"


def extract_todo_sections(todo_content):
    """Extract sections and their tasks from todo.md."""
    section_pattern = r"## (\d+) — (.+)\n((?:- \[[ x]\].+\n)+)"
    matches = re.finditer(section_pattern, todo_content)
    
    sections = []
    for match in matches:
        section_num = match.group(1)
        section_name = match.group(2)
        tasks_block = match.group(3)
        
        # Extract individual tasks
        tasks = []
        for task_line in tasks_block.strip().split('\n'):
            # Check if task is completed
            completed = "[x]" in task_line
            task_name = re.search(r"\*\*(.+?)\*\*", task_line)
            if task_name:
                tasks.append({
                    "name": task_name.group(1),
                    "completed": completed,
                    "full_text": task_line.strip()
                })
        
        sections.append({
            "number": section_num,
            "name": section_name,
            "tasks": tasks,
            "completed_count": sum(1 for t in tasks if t["completed"]),
            "total_count": len(tasks)
        })
    
    return sections


def update_project_guide(todo_sections):
    """Update the Development Status section in PROJECT_GUIDE.md."""
    with open(PROJECT_GUIDE_FILE, 'r', encoding='utf-8') as f:
        guide_content = f.read()
    
    # Prepare the updated development status section
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    status_header = "## Development Status\n\n"
    status_intro = f"The project is currently under active development. Last updated: {today}.\n\n"
    
    # Group sections by status
    completed_sections = []
    in_progress_sections = []
    not_started_sections = []
    
    for section in todo_sections:
        if section["completed_count"] == section["total_count"]:
            completed_sections.append(section)
        elif section["completed_count"] > 0:
            in_progress_sections.append(section)
        else:
            not_started_sections.append(section)
    
    # Build the status content
    status_content = status_intro
    
    if completed_sections:
        status_content += "### Completed Features\n"
        for section in completed_sections:
            status_content += f"- **{section['name']}** - All {section['total_count']} tasks completed\n"
        status_content += "\n"
    
    if in_progress_sections:
        status_content += "### In Progress\n"
        for section in in_progress_sections:
            status_content += f"- **{section['name']}** - {section['completed_count']}/{section['total_count']} tasks completed\n"
            # List completed tasks
            for task in section["tasks"]:
                if task["completed"]:
                    task_name = re.search(r"\*\*(.+?)\*\*", task["full_text"]).group(1)
                    status_content += f"  - ✅ {task_name}\n"
            # List remaining tasks
            for task in section["tasks"]:
                if not task["completed"]:
                    task_name = re.search(r"\*\*(.+?)\*\*", task["full_text"]).group(1)
                    status_content += f"  - ⏳ {task_name}\n"
        status_content += "\n"
    
    if not_started_sections:
        status_content += "### Planned Features\n"
        for section in not_started_sections:
            status_content += f"- **{section['name']}** - Not started\n"
        status_content += "\n"
    
    # If there's a repository, calculate overall progress
    total_tasks = sum(section["total_count"] for section in todo_sections)
    completed_tasks = sum(section["completed_count"] for section in todo_sections)
    if total_tasks > 0:
        progress_percentage = (completed_tasks / total_tasks) * 100
        status_content += f"Overall project completion: {completed_tasks}/{total_tasks} tasks ({progress_percentage:.1f}%)\n\n"
    
    # Replace the development status section in the guide
    pattern = r"## Development Status\n\n.*?(?=\n## |$)"
    updated_guide = re.sub(pattern, status_header + status_content.rstrip(), guide_content, flags=re.DOTALL)
    
    with open(PROJECT_GUIDE_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_guide)
    
    print(f"Updated PROJECT_GUIDE.md with current development status.")
    print(f"- Completed sections: {len(completed_sections)}")
    print(f"- In progress sections: {len(in_progress_sections)}")
    print(f"- Not started sections: {len(not_started_sections)}")


def main():
    """Main function to update the project guide."""
    print("Updating PROJECT_GUIDE.md based on todo.md...")
    
    # Check if files exist
    if not TODO_FILE.exists():
        print(f"Error: {TODO_FILE} not found.")
        return
    
    if not PROJECT_GUIDE_FILE.exists():
        print(f"Error: {PROJECT_GUIDE_FILE} not found.")
        return
    
    # Read todo.md
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        todo_content = f.read()
    
    # Extract sections and tasks
    todo_sections = extract_todo_sections(todo_content)
    
    # Update the project guide
    update_project_guide(todo_sections)


if __name__ == "__main__":
    main()
