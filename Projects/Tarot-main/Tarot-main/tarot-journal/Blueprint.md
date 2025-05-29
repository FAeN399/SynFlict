Tarot Journal – Revised Developer Specification
(v2 — incorporates findings from deep-research review)

⸻

1 • Product Vision

Build a secure, offline-first desktop diary for logging tarot readings.
The app must:
	1.	Protect privacy – all journal data is locally encrypted and unlocked by a user-supplied password.
	2.	Work anywhere, anytime – no internet is required after installation; all assets ship with the app or are user-imported.
	3.	Delight tarot readers – quick to start (pre-bundled Rider–Waite deck), highly customisable field templates, rich exports, and fast search to revisit past insights.
	4.	Ship quickly on Windows, yet remain portable – the codebase should build on macOS/Linux with only packaging-level changes.

⸻

2 • Key Features (MVP Scope)

Epic	Core (v1)	Stretch (v1.x)
Security & Privacy	• AES-256 at-rest encryption via SQLCipher• Password lock screen on app launch• Automatic session lock after user-defined idle time	• Biometric unlock (Windows Hello)
Reading Workflow	• Template-based entry wizard• Drag-drop card grid, reversed toggle• Markdown notes + checklist + rating	• Voice memo & sketch pad
Deck Management	• Bundled public-domain Rider–Waite deck (78 PNGs, 300 px)• “Add Deck” folder import with validation• Placeholder image if card file missing	• Online gallery for CC-BY decks
Search & Organisation	• Global keyword search (SQLite FTS5)• Filter by date range, deck, tags, rating• Tag manager CRUD	• Saved searches & statistics dashboard
Import / Export	• Per-reading export: Markdown + images + PDF• Full-journal backup: encrypted archive (.tjbk)• Restore/import wizard (merge or replace)	• Self-contained HTML export
Print	• WYSIWYG print preview & system print	• Themeable print templates
Backup & Sync	• Local daily autobackup (rotate 3 ZIPs)	• Optional cloud-sync plugin (Dropbox/OneDrive)
Cross-Platform Readiness	• Windows installer (NSIS)• CI builds for macOS dmg & Linux AppImage (test only)	


⸻

3 • Architecture Overview

flowchart TD
  subgraph Electron Shell
    R1[Renderer<br>(React + Zustand)]
    P1[Preload<br>(contextBridge)]
    M1[Main Process<br>(Node + SQLCipher)]
  end
  R1 -- IPC -- P1
  P1 -- IPC -- M1
  M1 --> DB[(Encrypted SQLite)]
  M1 --> FS[/Deck & Export Files/]
  R1 --> TC[Toast-UI<br>Markdown]
  R1 --> Idx[Full-text Search (FTS5)]

	•	Frameworks: Electron 27, React 19, TypeScript 5.
	•	Encryption: SQLCipher (AES-256-GCM) with scrypt KDF; key stored only in memory.
	•	IPC: Secure bridge exposes whitelisted APIs (deck.import, reading.save, etc.).
	•	Security Hardening: contextIsolation: true, sandbox: true, nodeIntegration: false, strict CSP (default-src 'self').
	•	Offline Assets: Rider-Waite deck and card-meaning JSON bundled under resources/decks/default/.

⸻

4 • Data Model (SQLCipher)

Table	Fields	Notes
settings	id, key, value	encrypted application prefs
decks	id, name, folder_path, imported_at	folder_path is relative to user data dir
templates	id, name, fields_json	list & order of enabled fields
readings	id, title, spread, template_id, created_at, mood, location, rating, notes_md	
reading_cards	id, reading_id, deck_id, position, card_name, reversed, keywords_json, personal_meaning	
tags	id, label	
reading_tags	reading_id, tag_id	M-N
fts_readings	content AS notes_md	virtual FTS5 table for search


⸻

5 • Storage, Encryption & Backup Flow
	1.	Unlock: On launch, user enters password → derive encryption key via scrypt(N=2^15,r=8,p=1) → open SQLCipher DB.
	2.	Autosave: Writes occur in a transaction; on success, write is flushed to disk.
	3.	Backup: After each successful save, queue incremental backup (copy DB, zip with timestamp). Nightly cron rotates to keep the last 3.
	4.	Export (Full): Encrypt DB + decks into .tjbk (7-zip). Include manifest (version, deck hashes).
	5.	Import: User selects .tjbk → verify manifest hash → decrypt with password → merge or overwrite current DB and copy decks.

⸻

6 • Import / Export Details

Per-reading Export

Reading-2025-05-12-New-Moon/
 ├─ reading.md   # markdown + front-matter YAML
 ├─ spread.pdf   # print-ready PDF
 └─ images/
     ├─ 00-The-Fool.png
     ├─ 01-The-Magician.png
     └─ …

Full-journal Backup (.tjbk)
	•	journal.sqlcipher (encrypted)
	•	/decks (user decks)
	•	meta.json (app version, created_on)

⸻

7 • Security Considerations

Area	Measure
Electron	Disable remote module; validate all external links via shell.openExternal allow-list; frozen CSP.
Files	All user data in %APPDATA%/TarotJournal; never touch arbitrary paths.
Encryption	SQLCipher v4 with 256-bit key; in-memory key wiped on lock/quit; PBKDF param upgrades supported.
Updates	Auto-update off by default (fully offline). If enabled later, checksums & HTTPS/TLS pinning required.
Code Signing	NSIS installer signed with EV certificate (Windows SmartScreen).


⸻

8 • Testing Strategy

Level	Tool	Coverage
Unit	Vitest	crypto utils, repo classes, field logic
Component	React-Testing-Library	DeckImportModal, ReadingEditor
E2E	Playwright-Electron	Unlock → add reading → export → import round-trip
Perf	Lighthouse-desktop	Memory & FPS with 500 readings
Security	Electron Fuses audit, npm audit, dependency‐check CI	

CI: GitHub Actions → lint → test → build Win, Mac, Linux artifacts.

⸻

9 • Milestones (8 Weeks)

Week	Deliverables
1	Repo scaffold, security baseline, CI pipeline
2	SQLCipher storage, unlock screen, autobackup
3	Deck manager (default deck + import)
4	Template system & ReadingEditor MVP
5	Search/FTS5, tag filters
6	Import/Export (reading & full) + PDF print
7	E2E tests, performance profiling, UX polish
8	Signed NSIS installer, cross-platform smoke builds, release candidate


⸻

10 • Future Enhancements
	•	Cloud-sync plugin (end-to-end encrypted)
	•	Biometric unlock (Windows Hello, TouchID)
	•	Mobile companion (React Native) reusing .tjbk file format
	•	Community deck marketplace (curated CC-BY decks)

⸻

This revision integrates encryption, import workflow, search, bundled deck, and hardened security, addressing all gaps identified during deep research while retaining the original phased delivery plan.
🗂️ Tarot Journal — Play-by-Play Blueprint (File-based, Zero-Network Edition)

This blueprint aligns exactly with the revised v3 specification:
No database, no networking, every reading is a folder with reading.html + images.
The work is chunked into safe, iterative commits (≈2–4 hrs each) and mirrored with AI-prompts you can feed to a code-generation LLM in sequence.

⸻

Phase Map

Phase	Goal	Key Outcomes
0 • Environment	Repo, tooling, CI, network lockdown	Electron shell boots with all remote APIs disabled
1 • Core FS API	Secure preload & file helpers	readFile, writeFile, selectFolder, zipDir
2 • Asset Bootstrap	Rider–Waite deck, templates	Deck copied to decks/; JSON templates scaffolded
3 • Reading Wizard	Create folder ➜ HTML page	Drag-drop grid, markdown notes, per-reading save
4 • Index & Search	index.json catalog + search bar	Tag CRUD, FTS-like JS filter
5 • Backup & Restore	Zip entire journal + unzip wizard	“Backup Now” + “Restore” (merge / replace)
6 • Passphrase Lock	AES-256 encrypt index.json	Unlock screen, idle auto-lock
7 • Print & Polish	Print stylesheet, themes, UX QA	WYSIWYG Ctrl-P, dark/light CSS
8 • Packaging	Signed NSIS installer + smoke tests	TarotJournalSetup.exe, QA checklist complete


⸻

Phase-by-Phase Mini-Tasks

<details><summary>Expand task checklist</summary>


Phase 0 — Environment & Lock-Down
	•	0-1 Init git repo, .gitignore, npm init -y
	•	0-2 Add Prettier + ESLint (Airbnb/TS)
	•	0-3 Scaffold Vite + React renderer
	•	0-4 Create Electron main & preload with contextIsolation, sandbox, nodeIntegration:false
	•	0-5 Block all network via session.webRequest.onBeforeRequest (allow file:// only)
	•	0-6 Vitest sample, Playwright blank-window test
	•	0-7 GitHub Actions CI (lint → unit → build)

Phase 1 — Core File-System API
	•	1-1 Preload exposes: fs.read, fs.write, fs.mkdirp, dialog.selectFolder
	•	1-2 Main wraps Node fs/promises with try/catch + error IPC
	•	1-3 Unit tests for file helpers (tmp dir)
	•	1-4 Zip/Unzip util using adm-zip (tested)

Phase 2 — Assets Bootstrap
	•	2-1 Copy Rider–Waite images (78 PNG @300 px) into resources/decks/rider-waite
	•	2-2 On first run, copy deck to %Docs%/TarotJournal/decks
	•	2-3 Seed JSON templates (daily_draw.json, celtic_cross.json)
	•	2-4 UI DeckGallery & TemplateGallery (read-only for now)

Phase 3 — Reading Wizard MVP
	•	3-1 Wizard modal: pick template → enter title/tags
	•	3-2 Drag-drop grid (react-beautiful-dnd) loads card thumbnails
	•	3-3 Markdown editor (Toast-UI) for notes
	•	3-4 On “Save”:
	1.	Create folder readings/YYYY-MM-DD-Title/
	2.	Copy used card PNGs into /images/
	3.	Generate reading.html (inject CSS & rendered MD)
	4.	Append metadata to index.json
	•	3-5 Playwright e2e: create reading ➜ reopen file in default browser

Phase 4 — Index & Search
	•	4-1 Define index.json schema (id, title, date, tags, cards, path)
	•	4-2 CRUD tags; update index on edit/delete reading
	•	4-3 Search bar filters index locally (case-insensitive, fuzzy)
	•	4-4 Unit tests: add 500 fake records ➜ search latency <50 ms

Phase 5 — Backup & Restore
	•	5-1 “Backup Now” button → zip entire TarotJournal dir → timestamped file
	•	5-2 Auto-backup daily at 02:00 (rotate 3 zips)
	•	5-3 Restore wizard: pick zip ➜ extract to temp ➜ diff index ➜ merge/replace
	•	5-4 Playwright: backup ➜ delete journal dir ➜ restore ➜ readings visible

Phase 6 — Passphrase Lock
	•	6-1 AES-256-GCM encrypt/decrypt index.json with scrypt-derived key
	•	6-2 Unlock screen on app start; idle timer auto-locks (configurable)
	•	6-3 Unit tests: valid/invalid password, key upgrade path

Phase 7 — Print & Polish
	•	7-1 reading.css: screen + @media print styles (fit A4)
	•	7-2 Theme toggle (light/dark) via CSS variables
	•	7-3 UX details: confirm delete, unsaved prompt, drag-drop accessibility
	•	7-4 Performance audit: open 1 000 readings list under 1 s

Phase 8 — Packaging & QA
	•	8-1 Configure electron-builder NSIS (appId, icon, no auto-updates)
	•	8-2 Sign installer; SmartScreen validation
	•	8-3 Smoke builds for macOS dmg & Linux AppImage (test only)
	•	8-4 Manual QA script (print, lock, backup, restore, network check)
	•	8-5 Publish v1.0 GitHub Release with hashes + changelog

</details>



⸻

Code-Gen Prompt Sequence 🧰

Feed each prompt (one at a time) to your code-generation LLM (e.g., GPT-4 o).
Commit output before moving to the next.

# Prompt 01 – Repo & Network Lock
Create a minimal Electron + React (TypeScript) project named “tarot-journal”.

Requirements:
- Vite for renderer build
- Prettier + ESLint (Airbnb/TS)
- Electron main, preload with: contextIsolation:true, sandbox:true, nodeIntegration:false
- In main, block all HTTP/HTTPS via session.webRequest.onBeforeRequest
- One React page with “Hello Offline”
- npm scripts: dev, build, lint, test:unit, test:e2e
Return: full file tree & file contents.

# Prompt 02 – CI Workflow
Add .github/workflows/ci.yml that:
1. Checks out code
2. Uses Node 20
3. npm ci
4. npm run lint
5. npm run test:unit
6. npm run build
Cache node_modules keyed on package-lock.json.
Return diff only.

# Prompt 03 – FileSystem API Bridge
Implement secure FS IPC.
Expose in preload:
  fs.read(path) -> string
  fs.write(path, data, options)
  fs.mkdirp(dir)
  dialog.selectFolder() -> path
All in TypeScript. Add Vitest tests for mkdirp & read/write inside a tmp dir.
Return diff.

# Prompt 04 – Rider–Waite Assets & Templates
Copy public-domain Rider–Waite PNGs (78) into resources/decks/rider-waite.
On first run, copy that folder into user data dir.
Create templates/daily_draw.json and templates/celtic_cross.json.
Return diff (no binary images inline—list filenames only).

# Prompt 05 – Reading Wizard MVP
Build Wizard React component:
  1. Pick template
  2. Title/tags inputs
  3. Drag-drop card grid (react-beautiful-dnd) showing thumbnails
  4. Markdown notes editor (Toast-UI)
On save, call IPC to:
  a. mkdir readings/YYYY-MM-DD-Title
  b. copy card images into images/
  c. write reading.html (generate HTML with inline CSS link)
  d. append metadata to index.json
Return diff.

# Prompt 06 – Index & Search
Create index.json schema and TagManager.
Implement search bar (fuzzy on title, tags, cards).
Update state with Zustand.
Add tests: 500 fake records search <50 ms.
Return diff.

# Prompt 07 – Backup & Restore
Add BackupService (zipDir, unzip).
“Backup Now” button; daily cron (node-cron).
Restore wizard: compare index.json hashes; choose merge or replace.
Playwright test: backup → delete → restore.
Return diff.

# Prompt 08 – Passphrase Lock
Encrypt index.json with AES-256-GCM.
scrypt params N=2^15, r=8, p=1.
Add UnlockScreen; idle auto-lock.
Unit tests: wrong passphrase fails, upgrade scrypt cost.
Return diff.

# Prompt 09 – Print & Theme Polish
Add reading.css with screen + @media print.
Theme toggle via CSS vars.
UX confirmations, unsaved guard, drag-drop keyboard support.
Run Lighthouse desktop; fix perf issues >90 score.
Return diff.

# Prompt 10 – Packaging & Release
Configure electron-builder NSIS (no auto-updates).
Add npm run package script.
Sign with placeholder certificate config.
Generate dist/TarotJournalSetup.exe (path note in log).
Update README with install & backup instructions.
Return diff.

After Prompt 10 the app is feature-complete, packaged, and fully offline-capable.
Each prompt builds cleanly on the last, with tests ensuring no orphaned code.