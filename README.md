# Genuvia Core

**The persistent intelligence layer for technical founders who can't afford to lose context.**

Small teams make fast decisions. Most of them disappear — into Slack threads, forgotten meetings, and the memory of people who later leave. Core captures decisions, detects contradictions, and surfaces forgotten context before it costs you.

Built for technical founders on 2–15 person teams. Delivered via Telegram. Deployed on Railway.

---

## The Problem

Your team decides to use PostgreSQL because your reporting queries need relational joins.

Three months later, someone proposes migrating to MongoDB to simplify scaling.

Nobody connects the two. The original reasoning is gone.

Core connects them.

---

## How It Works

**Week 1**
```
/remember We chose PostgreSQL over MongoDB because reporting queries require relational joins.
```

Core stores the decision, the rationale, the author, and the timestamp.

**Three months later**
```
/remember We should migrate to MongoDB to simplify scaling.
```

Core responds:
```
Potential contradiction detected.

On March 12 your team decided to use PostgreSQL
because reporting required relational joins.

Would you like to review that decision before proceeding?
```

That's the hook. But the value compounds.

Over time, Core becomes your team's:
- **Organisational memory** — every decision and why it was made
- **Onboarding assistant** — new hires query context instead of interrupting the team
- **Accountability system** — decisions are attributed and timestamped
- **Context engine** — surface what was decided before making the next call

---

## Why Not ChatGPT Memory?

| ChatGPT Memory | Genuvia Core |
|---|---|
| Remembers one user | Remembers an entire organisation |
| No shared team memory | Shared workspace memory across your team |
| No contradiction detection | Flags conflicting decisions automatically |
| Not structured around decisions | Built around decisions and rationale |
| No tenant isolation | Multi-tenant workspaces, isolated per team |

---

## Commands (V1)

| Command | Description |
|---|---|
| `/remember [decision]` | Stores a decision and its context |
| `/why [topic]` | Retrieves the rationale behind past decisions |
| `/search [query]` | Semantic search across your team's memory |
| `/contradictions` | Lists recently flagged contradictions |
| `/status` | Shows memory stats for your workspace |

---

## Contradiction Detection

When you log a new decision, Core doesn't just store it — it checks it.

```
New entry logged
    │
    ▼
Embed entry → search vector store for similar past decisions
    │
    ▼
If similarity above threshold:
    Send both entries to reasoning model
    Ask: "Do these contradict each other? If so, how?"
    │
    ▼
Second Telegram message with finding
(flags the conflict, not the person)
```

Confirmation arrives first. The contradiction result follows within seconds, asynchronously.

---

## Roadmap

**Phase 1 — Organisational Memory** ✓
Store decisions and rationale. Surface context on demand.

**Phase 2 — Decision Intelligence** ✓
Detect contradictions. Flag forgotten context before it causes mistakes.

**Phase 3 — Organisational Advisor**
Proactively surface relevant past decisions before new ones are made.

**Phase 4 — Autonomous Context Layer**
Become the persistent intelligence system behind the organisation — not a tool you query, but one that anticipates.

---

## Architecture

```
Telegram Bot
    │
    ▼
FastAPI Backend (Railway)
    ├── Command Router
    ├── Contradiction Detection Engine
    │       Embeds new entry → queries Qdrant for similar past decisions
    │       Sends to Claude/OpenAI for contradiction reasoning
    │       Returns result as a second message (async, non-blocking)
    │
    ├── Qdrant Cloud (vector store)
    │       Decisions stored with metadata per tenant
    │
    └── Tenant / Owner Identity Model
            Each workspace is isolated by tenant ID
```

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | Telegram Bot API |
| Backend | Python · FastAPI |
| Vector store | Qdrant Cloud |
| Reasoning | Claude API · OpenAI API |
| Deployment | Railway |

---

## Local Setup

```bash
git clone https://github.com/Sekani-27/genuvia-core
cd genuvia-core
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Required environment variables:
```
TELEGRAM_BOT_TOKEN=
QDRANT_URL=
QDRANT_API_KEY=
ANTHROPIC_API_KEY=
```

---

Built by [Ntando Miya](https://github.com/Sekani-27) · Co-founder, Genuvia (Pty) Ltd · Johannesburg

Built by [Ntando Miya](https://github.com/Sekani-27) · Co-founder, Genuvia (Pty) Ltd · Johannesburg
