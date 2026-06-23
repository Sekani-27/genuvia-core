# Genuvia Core

An organisational memory and decision intelligence system for small technical teams. Captures decisions, detects contradictions, and surfaces context — so your team stops losing institutional knowledge between conversations.

Built for technical founders on 2–15 person teams. Delivered via Telegram. Deployed on Railway.

---

## The Problem

Your team makes a decision. Three weeks later someone makes the opposite one — without knowing. A new hire asks why you chose PostgreSQL over MongoDB. Nobody remembers. You're debugging at 2am and realise this exact failure mode was flagged in a meeting six months ago.

**Core remembers. Your team forgets.**

---

## What It Does

Genuvia Core is a Telegram bot backed by a vector store and a reasoning engine. Team members log decisions, capture context, and query organisational memory — all from Telegram, without changing how they work.

When a new entry contradicts something already in memory, Core flags it immediately, with context, without blame.

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
    │       Stores decisions, rationale, and metadata per tenant
    │
    └── Tenant / Owner Identity Model
            Each workspace is isolated by tenant ID
            Owner has admin commands; members can read and write
```

---

## Commands (V1 Scope)

| Command | Description |
|---|---|
| `/remember [decision]` | Stores a decision or piece of context into organisational memory |
| `/why [topic]` | Retrieves the rationale behind past decisions on a topic |
| `/search [query]` | Semantic search across your team's memory |
| `/contradictions` | Lists recently flagged contradictions |
| `/status` | Shows memory stats for your workspace |

---

## Contradiction Detection

The core differentiator. When you log a new decision, Core does not just store it — it checks it.

```
New entry logged
    │
    ▼
Embed entry → search Qdrant for top-k similar decisions
    │
    ▼
If similarity above threshold:
    Send both entries to reasoning model
    Ask: "Do these contradict each other? If so, how?"
    │
    ▼
Return second Telegram message with finding
(non-accusatory framing — flags the conflict, not the person)
```

This runs asynchronously. The confirmation message arrives first. The contradiction result follows within seconds.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | Telegram Bot API |
| Backend | Python · FastAPI |
| Vector store | Qdrant Cloud (free tier) |
| Reasoning | Claude API · OpenAI API |
| Deployment | Railway |
| Identity | Tenant/owner model with isolated workspaces |

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

## Roadmap

- [x] V1: Five core Telegram commands
- [x] Contradiction detection engine
- [x] Tenant isolation model
- [x] Railway deployment
- [ ] Slack integration
- [ ] Web dashboard
- [ ] Mobile app (post first paying customer)

---

## Project Context

Genuvia Core is the decision intelligence layer of the [Genuvia](https://github.com/Sekani-27) platform — positioned alongside Genuvia Edge (trading intelligence) as part of an AI infrastructure stack for small, fast-moving teams.

Built by [Ntando Miya](https://github.com/Sekani-27) · Co-founder, Genuvia (Pty) Ltd · Johannesburg
