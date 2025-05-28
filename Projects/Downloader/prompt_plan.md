---

title: Reddit Grabber – Prompt Plan (TDD)
project: reddit-grabber
related\_spec: reddit-grabber-spec.md
version: 0.9
created: 2025‑05‑28
-------------------

## Overview

This execution plan decomposes the **Reddit Grabber** functional specification into a linear, test‑first roadmap.  Each step pairs the *minimal failing test* with the code required to make it pass, following strict TDD.  Milestones map to the specification’s section numbers for easy traceability.

---

### Milestone M1 — Core CLI MVP  (§5.1, §5.3)

1. **Repo scaffold**

   * **Test 1.1** `tests/test_skeleton.py::test_import` asserts `python -c "import grabber"` exits 0.
   * **Code 1.1** Create package dir, `__init__.__version__`, and empty `cli.py`.

2. **Typer entry‑point**

   * **Test 1.2** Invoke `grabber --help` via `subprocess.run`, expect exit 0 and usage banner.
   * **Code 1.2** Implement `cli.app` with Typer scaffold.

3. **Env config loader (dotenv) (§5.6, 5.7)**

   * **Test 1.3** Mock env vars; `grabber.cli._get_config()` returns expected dict.
   * **Code 1.3** Create `config.py` with precedence logic.

4. **`grab` command: submission URL validation (§5.1.1)**

   * **Test 1.4** `grab https://redd.it/abc123 --dry-run` prints “submission id=abc123”.
   * **Code 1.4** Regex parse + stub `reddit.fetch_submission()`.

5. **Manifest JSON write (§5.4)**

   * **Test 1.5** Run grabber with a fixture submission; assert `manifest.json` schema keys exist.
   * **Code 1.5** Implement Manifest dataclass & writer.

---

### Milestone M2 — Search & Sync  (§5.2, §5.5)

6. **SearchParams dataclass**

   * **Test 2.1** `SearchParams.parse_args(["--query","corgi","--min-score","100"])` populates fields.
   * **Code 2.1** `search.py` with parser + validation.

7. **Subreddit iterator**

   * **Test 2.2** Mock PRAW; iterator yields N submissions ≤ `limit`.
   * **Code 2.2** `search.fetch_iter()` implementing filters.

8. **`sync` CLI command**

   * **Test 2.3** `sync r/test --limit 2 --dry-run` logs two submissions.
   * **Code 2.3** CLI wiring + pagination loop.

9. **SQLite cache layer (§5.5)**

   * **Test 2.4** Insert duplicate hash, run `sync` twice, second run downloads 0.
   * **Code 2.4** `database.py` with `posts`, `files` tables + helper methods.

10. **Resumable logic**

    * **Test 2.5** Interrupt download mid‑run; resume flag continues from last saved id.
    * **Code 2.5** Transaction checkpoint + resume cursor.

---

### Milestone M3 — Downloader Engine  (§5.3)

11. **Image download (requests)**

    * **Test 3.1** Download mock HTTP server file; file size > 0.
    * **Code 3.1** `downloader.save_image()` with retries.

12. **Video download (yt‑dlp)**

    * **Test 3.2** Patch `subprocess.run`; ensure correct command assembled.
    * **Code 3.2** `save_video()` supporting `v.redd.it`, Imgur GIFV, etc.

13. **De‑duplication by SHA‑1 (§5.5)**

    * **Test 3.3** Two different URLs of same file produce single saved copy.
    * **Code 3.3** Hash after download; consult `files` table before save.

14. **Output template paths**

    * **Test 3.4** `--template "{sub}/{id}"` places file under correct tree.
    * **Code 3.4** Path renderer in `utils.py`.

---

### Milestone M4 — Textual TUI  (§6.1)

15. **UI launcher flag**

    * **Test 4.1** `--ui textual` imports `textual`; raises ImportError if missing.
    * **Code 4.1** Conditional import in `ui/__init__.py`.

16. **Table model & fetch thread**

    * **Test 4.2** Mock iterator; rows appear in table within 1 s.
    * **Code 4.2** `ui/tui.py` with LiveData + Rich progress.

17. **Queue interaction**

    * **Test 4.3** Simulate keypress; selected row pushed to download queue.
    * **Code 4.3** Key‑binding handlers + event bus.

---

### Milestone M5 — Packaging & CI  (§11, §12)

18. **pyproject metadata & entry‑point**

    * **Test 5.1** `pipx install . && reddit-grabber --version` prints semver.
    * **Code 5.1** Complete `pyproject.toml`, `grabber.__main__`.

19. **Docker image**

    * **Test 5.2** `docker run reddit-grabber grab https://redd.it/...` exits 0.
    * **Code 5.2** `Dockerfile` based on python\:slim.

20. **GitHub Actions matrix**

    * **Test 5.3** Workflow passes on 3.9–3.12 and Ubuntu/Windows.
    * **Code 5.3** Add `ci.yml` + badge in README.

---

### Milestone M6 — Optional PySide6 GUI (stretch)

21. **Qt stub window**

    * **Test 6.1** `--ui pyside` opens `MainWindow` without error (mock `QApplication`).
    * **Code 6.1** Create `desktop.py` with basic MVC wiring.

22. **Drag‑and‑drop output chooser**

    * **Test 6.2** Simulated drop updates config path.
    * **Code 6.2** FolderDialog + settings persistence.

---

## Completion Criteria

* All milestone tests green (`pytest -q`).
* README quick‑start commands succeed on clean machine.
* MIT license header present in every source file.
* Semantic version tag `v1.0.0` created & published on GitHub.

---

*End of Prompt Plan*
