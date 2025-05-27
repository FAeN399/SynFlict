---
title: Card Forge Development To-Do Checklist  
project: Card Forge – Hex Card Metadata Creator  
related_plan: prompt_plan.md  
related_spec: spec.md  
date: 2025-05-27  
---

## 1 — Project Setup
- [x] **Select CLI Stack** – decide on Typer + Pillow; document in DECISIONS.md (Plan #1, Spec §4 C-1)  
- [x] **Scaffold Repo & Test Harness** – initialise poetry, add pytest, failing hello-world test (Plan #2, NFR-4)  

## 2 — Core Data Model
- [x] **Card Model Test** – write failing test for Card fields (Plan #3, FR-2)  
- [x] **Card Model Implementation** – code dataclass to pass test (Plan #4, FR-2)  

## 3 — JSON Serialisation
- [x] **Round-Trip Test** – serialise/deserialise Card, expect equality (Plan #5, FR-5)  
- [x] **Serialisation Code** – implement to_json()/from_json() (Plan #6, FR-5)  

## 4 — ZIP Export / Import
- [x] **ZIP Export Test** – verify card_<uuid>.zip contains JSON only when no image (Plan #7, FR-5 §5.6)  
- [x] **ZIP Export Code** – implement export_card() (Plan #8, FR-5)  
- [x] **ZIP Import Test** – import ZIP and expect identical Card (Plan #9, FR-6 §5.6)  
- [x] **ZIP Import Code** – implement import_card() (Plan #10, FR-6)  

## 5 — Image Handling
- [x] **Hex Crop Test** – assert transparent corners & size 1024 px (Plan #11, FR-4 §5.5)  
- [x] **Hex Crop Implementation** – develop crop_hex() with Pillow (Plan #12, FR-4)  

## 6 — CLI Navigation
- [x] **Title Screen Test** – Typer root lists 5 menu options (Plan #13, FR-1)  
- [x] **Title Screen Implementation** – build root command & menu (Plan #14, FR-1)  

## 7 — Wizard / Card Editor
- [x] **Wizard Prompt Test** – `cardforge new` asks title, metadata loop (Plan #15, FR-2 §5.4)  
- [x] **Wizard Implementation** – interactive prompts to build Card (Plan #16, FR-2)  
- [x] **Free-Form Metadata Test** – ensure arbitrary key/values persist (Plan #17, FR-3)  

## 8 — Undo / Redo & History
- [ ] **History Stack Test** – sequence A→B→C→B→C (Plan #18, FR-8)  
- [ ] **History Stack Implementation** – implement undo/redo logic (Plan #19, FR-8)  

## 9 — Auto-Save & Multi-Card Session
- [ ] **Auto-Save Draft Test** – draft.json written after each step (Plan #20, FR-9 §7)  
- [ ] **Auto-Save Code** – implement save/restore draft (Plan #21, FR-9)  
- [ ] **Multi-Card Session Test** – create two cards in one run (Plan #22, FR-10 §5.2)  

## 10 — Booster Packs
- [ ] **Booster Pack Export Test** – booster ZIP contains N card ZIPs (Plan #23, FR-7 §5.7)  
- [ ] **Booster Pack Implementation** – build booster_pack.create() (Plan #24, FR-7)  

## 11 — Error Handling
- [ ] **Import Validation Test** – missing JSON raises ValidationError (Plan #25, Spec §7)  
- [ ] **Error Handling Code** – quarantine invalid bundle & log (Plan #26, Spec §7)  

## 12 — Performance
- [ ] **Benchmark Test** – 100-card import < 20 s & RAM < 400 MB (Plan #27, NFR-3 §8)  
- [ ] **Performance Optimisation** – batch DB writes / lazy image load (Plan #28, NFR-3)  

## 13 — GUI Development
- [ ] **Select GUI Framework** – evaluate and document choice of GUI framework in DECISIONS.md (Tkinter vs. PyQt vs. others)  
- [ ] **Basic GUI Layout** – implement main window with dark theme and color scheme (FR-11)  
- [ ] **Title Screen UI** – implement "The Gateway" screen with hexagonal menu design (FR-11 §5.1)  
- [ ] **Card Editor UI** – implement "The Scriptorium" with form inputs and live preview (FR-11 §5.3)  
- [ ] **Hexagonal Image Tool** – develop "The Visage Shaper" with interactive hex-cropping (FR-11 §5.5)  
- [ ] **Card Library UI** – implement "The Obsidian Library" with card thumbnails grid (FR-11 §5.2)  
- [ ] **Booster Pack UI** – implement "The Collection Forge" with card selection (FR-11 §5.7)  

## 14 — Advanced GUI Features
- [ ] **Responsive Layout** – ensure UI works across different screen sizes (NFR-5)  
- [ ] **Accessibility** – implement keyboard navigation and screen reader support (NFR-6)  
- [ ] **Animation** – add subtle transitions and hexagon-themed animations (NFR-7)  
- [ ] **Theming System** – implement CSS variables for theme customization (NFR-8)  

## 15 — Packaging & Acceptance
- [ ] **End-to-End Smoke Test** – automated UI testing for core workflows (Plan #29, §8)  
- [ ] **Package Application** – build one-file EXE with PyInstaller; smoke-test Win/macOS (Plan #30, NFR-4)  
