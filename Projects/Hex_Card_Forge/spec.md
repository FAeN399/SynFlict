---
title: Card Forge – Hex Card Metadata Creator  
version: 1.1            # bumped after Deep-Research Review  
date: 2025-05-27  
author: Aurum – The Builder (GPT-o3)  
related_documents:
  - prompt_plan.md
  - todo.md
---

# 1  Introduction & Objectives  
Card Forge is an **offline, single-user desktop tool** for designing custom *hex-shaped* cards that carry fully **free-form metadata** and, optionally, a cropped hex-image.  
Its sole deliverable is an **export bundle** (ZIP) ready for downstream import into a separate character-creation engine.  
Version 1.1 formalises prior brainstorming decisions and integrates clarifications from the Deep-Research Review.

---

# 2  Functional Requirements  

| ID | Requirement | Notes / Cross-refs |
|----|-------------|--------------------|
| **FR-1** | **Wizard Title Screen** with options:<br>   a) Create New Card b) Import Cards c) Create Booster Pack d) Design Card Template e) Add Image to Card | §5.3 |
| **FR-2** | **Card Editor (Wizard, CLI MVP)** collects: title → free-form metadata loop → (optional) image path → confirm | §5.4 |
| **FR-3** | **Free-form Metadata** – arbitrary key/value pairs, any categories; no enforced schema | §4 A-2 |
| **FR-4** | **Image Attachment** – accept external PNG/JPEG, auto-crop to flat-top regular hexagon (1024 px width) and save as PNG with alpha | §5.5 |
| **FR-5** | **Export Single Card** – ZIP named `card_<uuid>.zip` containing:<br>   • `card_<uuid>.json` • `card_<uuid>.png` (if image) | §5.6 |
| **FR-6** | **Import Card ZIP** – validate structure, add to in-memory library | §5.6 |
| **FR-7** | **Booster Pack Export** – bundle N cards into `booster_<timestamp>.zip` (contains N individual card ZIPs) | §5.7 |
| **FR-8** | **Undo / Redo** in editor (≥ 10 levels) | §5.4 |
| **FR-9** | **Auto-Save Draft** after each wizard step to `~/.cardforge/draft.json`; restore on next launch | §7 |
| **FR-10** | **Batch Session** – user may loop wizard to create multiple cards before final export | §5.2 |

---

# 3  Non-Functional Requirements  

| ID | NFR | Target |
|----|-----|--------|
| **NFR-1** | **Local-only** – no network I/O; all data remains on disk |
| **NFR-2** | **Crop Performance** – ≤ 300 ms per 2048×2048 px image on 3.5 GHz i7 |
| **NFR-3** | **Import Performance** – 100 cards ≤ 20 s, RAM < 400 MB |
| **NFR-4** | **Portability** – runs from source on Python 3.10+ (Win 10+, macOS 12+, Linux) |
| **NFR-5** | **Extensibility** – plugin hooks for future validators; decoupled MVC modules |

---

# 4  Assumptions & Constraints  

| ID | Statement |
|----|-----------|
| **A-1** | Single hobbyist user; no multi-user features |
| **A-2** | Metadata keys/values may differ per card; downstream tool tolerates variability |
| **C-1** | **CLI MVP** in v 1.1 (GUI façade postponed to v 1.2) |
| **C-2** | Flat-top hexagon mask; pointy-top support out-of-scope v 1.1 |
| **C-3** | Images larger than 1024 px are down-scaled with Lanczos filter |

---

# 5  System Architecture / Design  

## 5.1  High-Level Module Diagram  

```mermaid
flowchart TB
    TitleScreen --> WizardController
    WizardController -->|create/edit| CardModel
    WizardController -->|attach| ImageProcessor
    CardModel -->|serialize| ZIPBundler
    ZIPBundler --> FileSystem
    Importer -->|parse| CardModel
    BoosterTool --> ZIPBundler

5.2 Data Model (pseudo-TypeScript)
ts
Copy
Edit
type Meta = Record<string, string | number | boolean | null>;

interface Card {
  uuid: string;          // v4
  title: string;
  metadata: Meta;        // free-form
  imageFile?: string;    // hex-PNG filename
  created: string;       // ISO-8601
  updated: string;
}
5.3 CLI Title Screen
pgsql
Copy
Edit
╔════════════════════════╗
║  CARD FORGE v1.1       ║
╠════════════════════════╣
║ 1. Create New Card     ║
║ 2. Import Cards        ║
║ 3. Create Booster Pack ║
║ 4. Design Template     ║
║ 5. Add Image to Card   ║
║ 0. Exit                ║
╚════════════════════════╝
5.4 Wizard Flow (pseudo-code)
lua
Copy
Edit
while true:
    ask "Card Title?" → card.title
    repeat:
        ask "Add metadata field? (key=value) or blank to finish"
    ask "Attach image now? (y/n)"
    if y: path = file_picker(); card.imageFile = crop_hex(path)
    confirm card summary
    ask "Create another card? (y/n)"
5.5 Hex Crop Algorithm
Load image via Pillow → RGBA

Resize (max dimension = 1024 px)

Create α-mask polygon for flat-top hex (√3/2 geometry)

Image.putalpha(mask) → output PNG

5.6 Import / Export Workflows
text
Copy
Edit
export_card(card):
    json = to_json(card)
    files = [json, card.png?]
    zip_name = f"card_{card.uuid}.zip"
    zip.write(files)

import_card(zip_path):
    unzip → validate presence of card_*.json
    deserialize → CardModel
5.7 Booster Pack
python
Copy
Edit
booster_<timestamp>.zip/
    ├─ card_a.zip
    ├─ card_b.zip
    └─ …
6 Data Sources / APIs
Component	Library / API	Purpose
Image processing	Pillow 10.x	open, resize, mask, save PNG
CLI wizard	Python Typer (or argparse + prompt-toolkit)	input prompts, colored output
UUID	uuid std-lib	unique card IDs
ZIP handling	zipfile std-lib	bundle creation / extraction
Draft persistence	json + pathlib	auto-save draft.json

7 Error-Handling Strategy
Scenario	Handling
Missing image path / unreadable file	Show error, reprompt; log to stderr
Non-PNG/JPEG file	Reject → “Supported formats: PNG, JPG”
Import ZIP missing card_*.json	Abort import, display “Invalid bundle”
JSON parse failure	Print line/col; move file to ~/cardforge/quarantine/
Auto-save write error	Warn but continue; suggest manual export

8 Testing & Validation Plan
Layer	Test Type	Example Case
Unit	Model	Card round-trip JSON equality
Image	crop_hex() mask - 6 transparent corners, area ≈ 0.866×w×w
Integration	Workflow	create→crop→export→import→assert equality
CLI	Smoke	pexpect script drives wizard, verifies stdout
Performance	Benchmark	import 100 dummy cards < 20 s
User Acceptance	Checklist	Milo follows todo.md “Manual Acceptance”

9 Glossary
Term	Definition
Flat-top Hex	Regular hexagon with two horizontal edges on top/bottom.
Booster Pack	ZIP archive grouping multiple card ZIPs for distribution.
Draft.json	Auto-saved work-in-progress file re-loaded on next launch.
CLI MVP	Command-line first implementation; GUI deferred to v 1.2.

