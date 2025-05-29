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
