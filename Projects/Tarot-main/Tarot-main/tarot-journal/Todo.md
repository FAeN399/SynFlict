# Tarot Journal — `todo.md`
_100 % offline, file-based edition (spec v3)_

---

## Legend  
- `[ ]` Open   `[x]` Done  
- **⬜ stretch** = optional / v1.x feature  
- **☂︎** = umbrella (contains subtasks)

---

## PHASE 0 Environment & Lock-Down

- [ ] **0-1** Init repo → `git init`, `.gitignore`, `npm init -y`
- [ ] **0-2** Add Prettier + ESLint (Airbnb + TS) configs
- [ ] **0-3** Scaffold Vite + React renderer skeleton
- [ ] **0-4** Create Electron **main** & **preload**  
  - [ ] contextIsolation `true`  
  - [ ] sandbox `true`  
  - [ ] nodeIntegration `false`
- [ ] **0-5** Block all network:  
  `session.webRequest.onBeforeRequest` → allow `file://` only
- [ ] **0-6** Vitest sample test (§ tmp dir)
- [ ] **0-7** Playwright blank-window smoke test
- [ ] **0-8** GitHub Actions CI: lint → test → build

---

## PHASE 1 Core File-System API

- [ ] **1-1** Preload exposes IPC FS bridge  
  - [ ] `fs.read(path)`  
  - [ ] `fs.write(path,data,opts)`  
  - [ ] `fs.mkdirp(dir)`  
  - [ ] `dialog.selectFolder()`
- [ ] **1-2** Main wraps Node `fs/promises` with try/catch → error IPC
- [ ] **1-3** Unit tests for read/write/mkdirp (tmp directory)
- [ ] **1-4** Zip/Unzip util (`zipDir`, `unzipToTmp`) using `adm-zip`

---

## PHASE 2 Assets Bootstrap

- [ ] **2-1** Bundle Rider–Waite deck (78 PNG @ 300 px) in `resources/decks`
- [ ] **2-2** On first run, copy deck to `.../TarotJournal/decks`
- [ ] **2-3** Seed template JSONs  
  - [ ] `daily_draw.json`  
  - [ ] `celtic_cross.json`
- [ ] **2-4** UI galleries (read-only)  
  - [ ] DeckGallery (thumbnail list)  
  - [ ] TemplateGallery

---

## PHASE 3 Reading Wizard MVP

- [ ] **3-1** Wizard modal  
  - [ ] Template picker  
  - [ ] Title + tags inputs
- [ ] **3-2** Drag-drop card grid (react-beautiful-dnd)
- [ ] **3-3** Markdown notes editor (Toast UI)
- [ ] **3-4** ☂︎ Save routine  
  - [ ] mkdir `readings/YYYY-MM-DD-Title/`  
  - [ ] copy selected card PNGs → `images/`  
  - [ ] generate `reading.html` (inline CSS link)  
  - [ ] append metadata to `index.json`
- [ ] **3-5** Playwright e2e: create reading → open in default browser

---

## PHASE 4 Index & Search

- [ ] **4-1** Define `index.json` schema (id, title, date, tags, cards, path)
- [ ] **4-2** Tag CRUD panel
- [ ] **4-3** Search bar (fuzzy filter on loaded JSON array)
- [ ] **4-4** Unit perf test: 500 records search < 50 ms

---

## PHASE 5 Backup & Restore

- [ ] **5-1** “Backup Now” → zip entire `TarotJournal` dir → `backups/YYYY-MM-DD.zip`
- [ ] **5-2** Auto-backup daily 02:00, keep latest 3 zips
- [ ] **5-3** Restore wizard  
  - [ ] Pick zip → extract to temp  
  - [ ] Diff `index.json` → choose **merge** or **replace**
- [ ] **5-4** Playwright: backup → delete journal dir → restore → readings visible

---

## PHASE 6 Passphrase Lock

- [ ] **6-1** Encrypt `index.json` with AES-256-GCM (`scrypt` key derivation)
- [ ] **6-2** Unlock screen on app start
- [ ] **6-3** Idle auto-lock (user-configurable)
- [ ] **6-4** Unit tests: correct / wrong passphrase, key-upgrade path

---

## PHASE 7 Print & Polish

- [ ] **7-1** `reading.css` screen + `@media print` (A4 fit)
- [ ] **7-2** Theme toggle (light / dark) via CSS vars
- [ ] **7-3** UX refinements  
  - [ ] Confirm delete dialogs  
  - [ ] Unsaved-changes prompt  
  - [ ] Keyboard support for drag-drop grid
- [ ] **7-4** Performance audit (≥1 000 readings list < 1 s)

---

## PHASE 8 Packaging & QA

- [ ] **8-1** Configure `electron-builder` NSIS (`appId`, icon, no auto-update)
- [ ] **8-2** Sign installer (EV cert) → SmartScreen passes
- [ ] **8-3** Cross-platform smoke builds (macOS dmg, Linux AppImage)
- [ ] **8-4** Manual QA checklist  
  - [ ] Network traffic = 0 (verify via Fiddler)  
  - [ ] Create → lock → unlock flow  
  - [ ] Backup / restore round-trip  
  - [ ] Print reading to PDF  
  - [ ] Deck import edge cases (missing images)  
  - [ ] Performance on low-spec laptop
- [ ] **8-5** Publish `v1.0` GitHub Release (+ SHA-256 hashes)

---

## BACKLOG / FUTURE ⬇️

- [ ] ⬜ Voice memo & sketch pad in readings
- [ ] ⬜ Large-image JPEG compression on import
- [ ] ⬜ Stats dashboard (card frequency, tag heat-map)
- [ ] ⬜ Biometric unlock (Windows Hello)
- [ ] ⬜ Community deck marketplace (offline zip packs)

---

_Keep this checklist at repo root and commit progress with short messages  
(e.g. “docs(todo): ✔ 3-2 Drag-drop grid”)._
