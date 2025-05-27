# Card Forge - Technical Decisions

## CLI Stack Selection

### Decision: Typer + Pillow

Date: 2025-05-27

### Context
For the Card Forge application, we need to select a technology stack that satisfies:
- Functional Requirement FR-1 (Wizard Title Screen with 5 menu options)
- Constraint C-1 (CLI MVP in v1.1, with GUI façade postponed to v1.2)

### Options Considered

1. **argparse + prompt_toolkit**
   - Standard library for basic CLI
   - More manual work required for user interaction flow
   - Would require custom implementation for colored output and menu rendering

2. **Click**
   - Popular CLI framework
   - Good documentation and community
   - Less suited for interactive wizard-style applications

3. **Typer + rich**
   - Modern, type-annotated CLI framework built on top of Click
   - Rich REPL-like experience with proper type validation
   - Excellent for multi-step wizards with progressive disclosure
   - Built-in help text generation from type annotations

### Decision Rationale

We selected **Typer** for the CLI framework because:

1. **Type Safety** - Typer leverages Python's type hints, aligning with our development approach and making the code more maintainable.

2. **Wizard-friendly** - Typer's design is ideal for our multi-step wizard flow in FR-2, with built-in support for command groups and subcommands.

3. **Modern UX** - Provides rich command-line interaction with colorized output, proper help menus, and completion suggestions.

4. **Future-proof** - When we eventually move to a GUI in v1.2, the clean command architecture of Typer will make it easier to abstract the UI layer.

5. **Developer Experience** - Less boilerplate compared to argparse, and better structure for complex CLI apps compared to Click.

### Image Processing: Pillow 10.x

We selected **Pillow** for image processing because:

1. **Maturity** - Pillow is a well-maintained fork of PIL (Python Imaging Library) with regular updates and security fixes.

2. **Functionality** - It provides all required functionality for FR-4 (hex cropping):
   - Image opening and format conversion
   - Alpha channel manipulation for transparency
   - Geometric operations for mask application
   - High-quality resizing with Lanczos filter (as specified in C-3)

3. **Performance** - Pillow's C extensions provide near-native performance, helping meet NFR-2 (crop performance ≤ 300ms per image).

4. **Portability** - Pillow is cross-platform compatible, supporting our NFR-4 requirement (Windows, macOS, Linux).

5. **Easy Integration** - Straightforward API that will make the implementation of crop_hex() clean and maintainable.

### Conclusion

The Typer + Pillow combination provides an optimal balance of functionality, performance, and developer experience for our Card Forge CLI MVP, while ensuring we can meet all functional requirements with minimal technical debt.
