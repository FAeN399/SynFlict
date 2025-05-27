# Hex Card Forge

A desktop tool for designing custom hex-shaped cards with free-form metadata and optional images.

## Project Automation Tools

This project includes automated tools to keep documentation in sync with development progress:

### 1. Project Guide Updater

The `update_project_guide.py` script automatically updates the Development Status section in PROJECT_GUIDE.md based on completed tasks in todo.md.

**How it works:**
- Scans todo.md for completed tasks (marked with [x])
- Updates the Development Status section in PROJECT_GUIDE.md
- Calculates overall project completion percentage
- Categorizes features as "Completed", "In Progress", or "Planned"

**Run manually:**
```
python update_project_guide.py
```

### 2. Automation Setup

The `setup_git_hooks.py` script configures automatic updates through various triggers:

```
python setup_git_hooks.py
```

This sets up:

1. **Git hooks** - Updates PROJECT_GUIDE.md:
   - After each commit (post-commit hook)
   - Before pushing if tests pass (pre-push hook)

2. **Pytest integration** - Updates PROJECT_GUIDE.md when tests pass

## Getting Started

1. Initialize a Git repository (if not done already):
   ```
   git init
   ```

2. Set up the automation:
   ```
   python setup_git_hooks.py
   ```

3. Start development following the TDD approach in prompt_plan.md

4. When you complete tasks in todo.md, mark them as [x] and commit your changes. The PROJECT_GUIDE.md will automatically update.

## Project Documentation

- **PROJECT_GUIDE.md** - Complete project overview and onboarding document
- **spec.md** - Detailed project specifications and requirements
- **todo.md** - Development roadmap and task checklist
- **prompt_plan.md** - Test-driven development plan

---

See the [PROJECT_GUIDE.md](PROJECT_GUIDE.md) file for detailed information about this project.
