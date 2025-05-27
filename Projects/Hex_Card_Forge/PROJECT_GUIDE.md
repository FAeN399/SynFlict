# Hex Card Forge - Project Guide

## Project Overview

Hex Card Forge is an offline, single-user desktop tool for designing custom hex-shaped cards that carry fully free-form metadata and optional cropped hex-images. The primary purpose is to create export bundles (ZIP files) containing card data and images ready for import into downstream character-creation engines or game systems.

Key features include:
- Creation of custom cards with flexible metadata fields
- Automatic cropping of images to flat-top hexagon shape
- Export/import capabilities for individual cards and card collections ("booster packs")
- Command-line interface (CLI) with a wizard-style workflow

## Architecture Overview

### Module Structure
The project follows a modular architecture with the following key components:

```
TitleScreen → WizardController → CardModel → ZIPBundler → FileSystem
                    ↓               ↑           ↑
            ImageProcessor      Importer    BoosterTool
```

### Data Model
The core data model revolves around the `Card` entity:
```typescript
interface Card {
  uuid: string;          // v4 UUID
  title: string;         // Card title
  metadata: Meta;        // Free-form key-value pairs
  imageFile?: string;    // Optional hex-PNG filename
  created: string;       // ISO-8601 timestamp
  updated: string;       // ISO-8601 timestamp
}
```

### Key Technologies
- **Python 3.10+** - Core programming language
- **Typer** - CLI framework for interactive prompts
- **Pillow 10.x** - Image processing library for hex cropping
- **Poetry** - Dependency management
- **PyTest** - Test framework
- **Standard libraries** - uuid, zipfile, json, pathlib

## Development Status

The project is currently in the **early development stage** with a strong focus on design and planning. The repository contains:

1. **Comprehensive Specification** (`spec.md`) - Detailed requirements, architecture, and workflows
2. **Development Roadmap** (`todo.md`) - Task checklist organized into 13 implementation phases
3. **TDD Execution Plan** (`prompt_plan.md`) - Test-driven development approach for 30 implementation steps

No functional code has been implemented yet. Development will follow the Test-Driven Development methodology outlined in the prompt plan, starting with project scaffolding and progressively implementing features.

## Coding Standards

The project will follow these standards:

1. **Test-Driven Development** - Write failing tests before implementation code
2. **Modular Architecture** - Decoupled MVC modules for extensibility
3. **Type Hints** - Use Python type annotations (similar to the TypeScript-like definitions in spec)
4. **Poetry Project Structure** - Standard Python package organization with Poetry for dependency management
5. **Comprehensive Documentation** - Inline docstrings and external documentation
6. **Explicit Error Handling** - Well-defined error handling strategy with proper user feedback

## Quick Start Guide

To understand and work with this project:

1. **Read the Documentation** 
   - Start with `spec.md` to understand requirements and architecture
   - Review `todo.md` to see the development roadmap

2. **Set Up Development Environment**
   - Install Python 3.10+
   - Set up Poetry and install dependencies (once implemented)
   - Run tests to ensure everything is working properly

3. **Follow Development Steps**
   - Each feature should begin with writing a failing test
   - Implement code to pass the test
   - Move to the next feature

## Key Challenges

1. **Hex Image Cropping** - Creating an efficient algorithm for cropping images to perfect flat-top hexagons while maintaining transparency.

2. **Free-form Metadata Management** - Designing a flexible system that allows arbitrary key-value pairs while maintaining data integrity and usability.

3. **Performance Constraints** - Meeting the performance targets (e.g., ≤300ms per image crop, importing 100 cards in ≤20s with <400MB RAM usage).

4. **CLI User Experience** - Creating an intuitive wizard-style interface within the constraints of a command-line environment.

5. **Cross-platform Compatibility** - Ensuring consistent behavior across Windows, macOS, and Linux.

## AI Collaboration Context

When working on this project, AI assistants should:

1. **Adhere to the TDD Methodology** - Always write failing tests before implementation code.

2. **Follow the Development Roadmap** - Prioritize features according to the todo.md checklist.

3. **Maintain Architectural Integrity** - Keep modules decoupled and follow the defined interfaces.

4. **Balance User Experience and Technical Requirements** - Focus on making the tool intuitive while meeting all functional requirements.

5. **Consider Performance Implications** - Be mindful of the non-functional requirements like processing speed and memory usage.

6. **Keep Documentation Updated** - Ensure that changes to the code are reflected in the documentation.

## Roadmap

Immediate priorities for development (based on todo.md):

1. **Project Setup** 
   - Select CLI Stack (Typer + Pillow)
   - Scaffold repository and test harness
   
2. **Core Data Model**
   - Implement Card model (dataclass)
   - Ensure all required fields are properly typed

3. **JSON Serialization**
   - Create round-trip serialization/deserialization 
   - Ensure data integrity is maintained

4. **ZIP Export/Import**
   - Implement ZIP bundling for card data and images
   - Create import functionality with proper validation

5. **Image Handling**
   - Implement hex cropping algorithm
   - Ensure performance meets requirements

Long-term goals include completing all 13 phases outlined in the todo.md file, with a particular focus on creating a user-friendly CLI interface, supporting multiple cards in a session, and packaging the application for cross-platform distribution.

## Maintenance Strategy

To keep this guide up-to-date as the project evolves:

1. **Update After Major Milestones** - Revise this document when completing any major phase from the todo.md list.

2. **Review Before Each New Phase** - Before starting a new development phase, review and update the guide to reflect current status.

3. **Document Design Decisions** - Create a separate DECISIONS.md file to document architectural and technical choices.

4. **Track Version Changes** - Update the version information in both the code and documentation when significant changes are made.

---

This guide was created on 2025-05-27 and represents the initial planning stage of the Hex Card Forge project.
