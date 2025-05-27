# Card Forge — TDD Execution Plan (spec.md v1.1)

1. **Select CLI Stack**  
   ```text
   Write rationale for choosing Typer + Pillow in DECISIONS.md. (covers §4 C-1, FR-1)
Project Scaffold & Test Harness

2. text
Copy
Edit
Initialise poetry project, add pytest, create failing "hello_world" test. (covers NFR-4)
Card Model — Failing Test

3. text
Copy
Edit
Test expects Card(uuid, title, metadata, imageFile?, created, updated). (covers FR-2, §5.2)
Card Model — Code

4. text
Copy
Edit
Implement Card dataclass to pass previous test. (covers FR-2, §5.2)
JSON Round-Trip — Failing Test

5. text     
Copy
Edit
Serialize Card → JSON → deserialize; assert deep-equal. (covers FR-5)
JSON Round-Trip — Code

6. text
Copy
Edit
Implement Card.to_json()/from_json(); pass round-trip test. (covers FR-5)
ZIP Export — Failing Test

7. text
Copy
Edit
Export Card without image → `card_<uuid>.zip` contains card_<uuid>.json only. (covers FR-5, §5.6)
ZIP Export — Code

8. text
Copy
Edit
Implement export_card(); ensure test passes. (covers FR-5, §5.6)
ZIP Import — Failing Test

9. text
Copy
Edit
Import previously exported ZIP; expect identical Card instance. (covers FR-6, §5.6)
ZIP Import — Code

10. text
Copy
Edit
Implement import_card(); pass import test. (covers FR-6, §5.6)
Hex Crop Mask — Failing Test

11. text
Copy
Edit
crop_hex("square.png") → PNG 1024 px, flat-top hex, transparent corners count > 0. (covers FR-4, §5.5)
Hex Crop Mask — Code

12. text
Copy
Edit
Implement crop_hex() with Pillow polygon mask; pass mask test. (covers FR-4, §5.5)
Title Screen Navigation — Failing Test

13. text
Copy
Edit
Typer CLI: running `cardforge` lists 5 menu options. (covers FR-1)
Title Screen Navigation — Code

14. text
Copy
Edit
Implement Typer root command; pass navigation test. (covers FR-1)
Wizard Flow Render — Failing Test

15. text
Copy
Edit
CLI `cardforge new` prompts for title, then metadata loop. (covers FR-2, §5.4)
Wizard Flow — Code

16. text
Copy
Edit
Implement interactive prompts & in-memory Card creation; pass render test. (covers FR-2, §5.4)
Free-Form Metadata Entry — Test

17. text
Copy
Edit
Simulate adding key=value pairs; assert Card.metadata persists exactly. (covers FR-3)
Undo / Redo History — Failing Test

18. text
Copy
Edit
Two edits, undo twice, redo once → states A→B→C→B→C. (covers FR-8)
Undo / Redo — Code

19. text    
Copy
Edit
Implement history stack; pass history test. (covers FR-8)
Auto-Save Draft — Failing Test

20. text
Copy
Edit
After each wizard step, ~/.cardforge/draft.json exists & updates timestamp. (covers FR-9, §7)
Auto-Save Draft — Code

21. text
Copy
Edit
Implement auto-save & restore on launch; pass draft test. (covers FR-9, §7)
Multi-Card Session — Failing Test

22. text
Copy
Edit
Create two cards in one session; export booster asks for both. (covers FR-10, §5.2)
Booster Pack Export — Failing Test

23. text
Copy
Edit
Select N cards → booster_<ts>.zip contains N card_ZIPs. (covers FR-7, §5.7)
Booster Pack Export — Code

24. text
Copy
Edit
Implement booster_pack.create(); pass pack test. (covers FR-7, §5.7)
Import Validation Error — Test

25. text
Copy
Edit
Import ZIP missing card.json → raises ValidationError code MISSING_JSON. (covers §7)
Error Handling — Code

26. text
Copy
Edit
Add try/except, quarantine invalid bundle; pass validation test. (covers §7)
Performance Benchmark — Test

27. text
Copy
Edit
Import 100 dummy cards; assert time < 20 000 ms, RAM < 400 MB. (covers NFR-3, §8)
Performance Optimisation — Code

28. text
Copy
Edit
Batch DB writes / lazy image load until benchmark passes. (covers NFR-3, §8)
End-to-End Smoke — Test

29. text
Copy
Edit
pexpect script: new → metadata → image → export → import → assert equality. (covers §8 integration)
Packaging

30. text
Copy
Edit
Build single-file EXE with PyInstaller; run smoke test on Win/macOS. (covers NFR-4)
Copy
Edit
