# MUST‑Have Enhancement: Automatic Rate‑Limit Back‑Off

> **Category:** Performance & Robustness  | **Priority:** Critical (Blocker)

---

## 1 · Objective

Ensure the **Reddit Grabber** never exceeds Reddit’s API request limits, preventing 429 errors and avoiding temporary bans. The tool must dynamically throttle its request rate based on live header feedback.

---

## 2 · Functional Requirement

1. **Header Monitoring**
   Each Reddit API response includes:

   * `X-Ratelimit-Used` – requests used in current 10‑min window.
   * `X-Ratelimit-Remaining` – requests left.
   * `X-Ratelimit-Reset` – seconds until window resets.

2. **Dynamic Throttling**

   * When `remaining / reset` drops below **1.0 rps** (configurable), the grabber must **sleep** long enough to maintain a safe margin (default 80 % of allowed RPS).
   * If headers are missing (edge proxies), fall back to a fixed **max 60 req/min**.

3. **User Feedback**

   * CLI & TUI show a live “⏳ 18 / 600 req left (resets in 94 s)” indicator.
   * A WARN log is emitted whenever the back‑off sleep ≥ 5 s.

---

## 3 · Acceptance Tests (TDD)

| ID      | Scenario                                                                     | Expected                                                |
| ------- | ---------------------------------------------------------------------------- | ------------------------------------------------------- |
| **RT1** | Mock 50 consecutive API calls returning headers `(used=55, rem=5, reset=10)` | `rate_limiter.sleep()` called ≥ 4 s before next request |
| **RT2** | Headers absent for >10 requests                                              | Throttle to ≤ 60 requests/min measured by test clock    |
| **RT3** | Remaining resets mid‑run (header `rem=600, reset=600`)                       | Throttle scale increases back to default concurrency    |

*Tests will monkey‑patch `praw.Reddit._core._requestor.request` to inject synthetic headers and inspect sleep durations via `freezegun`.*

---

## 4 · Implementation Outline

1. **Module** `grabber/ratelimit.py`

   ```python
   class RateLimiter:
       def update_from_headers(self, headers: Mapping[str, str]): ...
       async def wait(): ...  # sync wrapper also exposed
   ```
2. **Patch PRAW** requestor in `reddit.py` to call `RateLimiter.update_from_headers()` after every request.
3. Replace hard‑coded `time.sleep()` with `rate_limiter.wait()` in all loops (`search.fetch_iter`, comment expansion, etc.).
4. Add CLI flag `--max-rps <float>` to override algorithm.
5. Expose stats via `rate_limiter.snapshot()` for TUI status bar.

---

## 5 · Spec Linkage

*Extends* §5.2 Search & §5.3 Download behaviour.  Adds new non‑functional bullet under **Reliability** (§7).

---

### Completion Criteria

* All RT\* tests green.
* Long‑running `sync` on a free Reddit app key completes 10 k requests/day with **0** `HTTP 429` errors.
* Visual indicator visible in both CLI (`INFO`) and TUI.

*End of must‑have file.*
