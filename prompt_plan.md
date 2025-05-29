# Incremental Implementation Plan

*(Each step is a **copy-ready prompt** for your code-generation LLM. Follow them in order; every prompt references the unified Synergy Forge ✕ Metaphysical Wrestling spec.)*

---

### 1. **Scaffold Monorepo**

```text
# Step 01 – Turborepo Init
Create a pnpm-based Turborepo with:
• apps/web  – SvelteKit + Tailwind
• apps/api  – Fastify + GraphQL Yoga
• packages/config – shared tsconfig, ESLint, Prettier
Add a Vitest sample in each app.  
Success = `pnpm turbo run build && pnpm test` both pass.
```

---

### 2. **CI Pipeline**

```text
# Step 02 – GitHub Actions
Add .github/workflows/ci.yml that:
• installs via pnpm with cache  
• runs lint → type-check → vitest  
• fails on any non-zero exit.  
Target Node 20 on ubuntu-latest + macOS-latest.
```

---

### 3. **Dev Database Container**

```text
# Step 03 – Dockerised Postgres
Provide docker-compose.yaml for Postgres 15 + pgvector.
Add .env.sample (PG variables) and Prisma schema with empty migration.
README snippet: `docker compose up db`.
Verify: `prisma migrate dev` succeeds.
```

---

### 4. **Passkey Auth Skeleton**

```text
# Step 04 – WebAuthn Routes
In apps/api:
• POST /auth/passkey/register  → `{ challenge }`
• POST /auth/passkey/verify    → JWT
Use @simplewebauthn/server + Prisma users table.
Unit test happy path with Vitest.
```

---

### 5. **Email Magic-Link Fallback**

```text
# Step 05 – Magic-Link Auth
Add POST /auth/magic to send token (use local MailHog).  
GET /auth/magic/verify?token=… completes login.  
Reuse Prisma sessions table.  
Cypress e2e covers full flow.
```

---

### 6. **GraphQL Auth Context**

```text
# Step 06 – Session Middleware
Expose `userId` in GraphQL context after JWT or session cookie.  
Add `me` query returning minimal profile stub.  
Test: unauthenticated call returns null.
```

---

### 7. **Profile Nexus CRUD**

```text
# Step 07 – Profile Schema + Pages
Prisma: profiles table per unified spec (value sliders, archetype, etc.).
GraphQL: `getProfile`, `upsertProfile`.
SvelteKit: responsive edit form with Tailwind, Lighthouse ≥ 95.
```

---

### 8. **Seed Wrestler Profiles**

```text
# Step 08 – Seed Script
Write a node script `seed:wrestlers` that inserts three starter profiles:
Repo Man, The Prince, Psychopomp (use deep fields from spec).
Run via `pnpm exec ts-node …`.
```

---

### 9. **Event-Sourcing Layer**

```text
# Step 09 – CQRS/Event Store
Implement `events` table + simple event-writer SDK (`emitEvent`, `readStream`).
Event types: PROFILE_UPDATED, MESSAGE_POSTED, QUEST_COMPLETED.
Unit tests ensure correct ordering & retrieval.
```

---

### 10. **Embedding Worker**

```text
# Step 10 – Vector Service
Create background worker (pnpm script) that:
• consumes MESSAGE_POSTED events  
• calls OpenAI embeddings  
• stores vector in `embeddings` table (pgvector) with FK to event.  
Provide retry logic & rate-limit guard.
```

---

### 11. **Polarity Vectoriser**

```text
# Step 11 – Polarity Mapping
Add polarity-axis ontology (Structure⇄Freedom, etc.).
Function `mapToAxes(embedding) -> {axis: score}`.
Store latest aggregated scores per conversation in Redis.
Unit test with dummy embeddings.
```

---

### 12. **Live Heat-Map API**

```text
# Step 12 – Heat-Map Endpoint
GraphQL subscription `conversationPolarity(convoId)` emitting {axis,score}.
Pull from Redis, update every 2 s.
WebSocket transport with GraphQL Yoga.
```

---

### 13. **Crucible Chat UI**

```text
# Step 13 – Dialectic Crucible Component
In SvelteKit:
• real-time chat pane ↑  
• connect to heat-map subscription, render canvas shader.  
• input box triggers `MESSAGE_POSTED` mutation.  
Cypress test: two browsers see synced chat & heat-map pulse.
```

---

### 14. **Quest Engine v1**

```text
# Step 14 – Quest Templates
Create quests table (JSON template, cadence).  
Cron (node-cron) assigns daily quests to profiles.  
GraphQL `currentQuests(profileId)` + `completeQuest`.
Integration test ensures ledger entry + QUEST_COMPLETED event.
```

---

### 15. **Insight Ledger UI**

```text
# Step 15 – Ledger Feed
Svelte component lists recent QUEST_COMPLETED & POLARITY_DROP milestones.  
Infinite scroll via cursor pagination.  
Accessible live region for screen readers.
```

---

### 16. **Guardian Protocols**

```text
# Step 16 – Crisis Detection
Middleware scans messages for crisis keywords array.  
On hit:  
• create MOD_ALERT event  
• email moderators & temporarily mute user.  
Add moderator dashboard route `/guard/alerts`.
```

---

### 17. **Metaphysical Wrestling Rituals**

```text
# Step 17 – Ritual Endpoint
Add `/ritual/startMatch` mutation:
• takes two profile IDs, matchType  
• emits MATCH_STARTED event  
• returns ritual script (from spec).  
Create WrestlerRole enum (Phoenix, Technician, Mirror).  
Unit test verifies event chain.
```

---

### 18. **Ritual UI Module**

```text
# Step 18 – Match Overlay
Svelte modal overlay:
• shows wrestler avatars, entrance songs, health bars (volatile score proxy).  
• “Tag” button emits TAG_EVENT.  
End ritual via MATCH_ENDED event → Insight ledger entry.  
Cypress happy-path test.
```

---

### 19. **Mobile PWA Enhancements**

```text
# Step 19 – PWA
Add SvelteKit adapter-static + Vite PWA plugin.  
Manifest: name, icons, dark theme.  
Offline fallback chat cache (indexedDB).  
Lighthouse PWA score ≥ 90.
```

---

### 20. **Edge Deployment**

```text
# Step 20 – Fly.io Apps
Provide `fly.toml` for web & api, Postgres volume.  
GitHub Action `deploy.yml` on main push.  
Health checks & rolling deploy strategy.
```

---

### 21. **Beta Feedback Instrumentation**

```text
# Step 21 – Telemetry
Integrate PostHog with anonymised distinctId = profile.id hash.  
Track: QUEST_COMPLETED, MATCH_STARTED, POLARITY_DROP > 30.  
Toggle via env flag.
```

---

### 22. **Docs & Onboarding**

```text
# Step 22 – Storybook & MDX Docs
Storybook for UI components.  
/docs route renders MDX guide “How to Use Synergy Forge & Metaphysical Wrestling.”  
Automated Chromatic snapshot tests.
```

---

### 23. **Release Candidate QA**

```text
# Step 23 – QA Suite
Run Playwright cross-browser tests:  
• Auth flows  
• Crucible chat latency < 300 ms  
• Mobile quests flow  
Generate coverage report ≥ 80 %.
```

---

### 24. **Launch & Monitor**

```text
# Step 24 – Go-Live
Toggle public registration; seed live wrestlers.  
Enable Sentry error tracking.  
Schedule weekly DB backup to S3.
```

---

> **End of execution plan.**
> Follow each prompt sequentially—every feature is traced to its spec requirement and verified before the next begins.
