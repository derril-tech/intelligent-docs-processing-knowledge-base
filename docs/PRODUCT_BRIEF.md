# Product Brief

⚠️ IMPORTANT  
This document defines the **product’s purpose, users, and goals**.  
The infrastructure plan (`INFRASTRUCTURE_PLAN.md`) must always be aligned with this brief.

---

## 1. Product Name
DocuMind™

---

## 2. Product Purpose
AI Document Intelligence & RAG Knowledge OS


---
# DocuMind™ — AI Document Intelligence & RAG Knowledge OS

**Tagline:** Turn any document corpus into an always-on, trustworthy knowledge OS with verifiable answers.

**What it is:** DocuMind™ ingests messy PDFs, slides, emails, and code docs; enriches them with OCR, structure, entities, and citations; then serves grounded answers via a production-grade RAG pipeline. Designed for regulated teams that need correctness, speed, and scale.

---

## 1) Product Snapshot

* **Core Jobs-to-be-Done**: Upload → Clean/Extract → Index (RAG) → Ask/Automate → Cite & Export.
* **Differentiators**: Evidence-linked answers, policy-aware redaction, human-in-the-loop validation, multi-tenant isolation.
* **Primary Users**: CX, Legal, Ops, RevOps, Product, and Engineering enablement.

---

## 2) Frontend Architecture (Next.js 14 + React 18 + TypeScript)

* **App Router** with **server actions**; **Edge runtime** for low-latency chat.
* **UI**: Tailwind CSS + Radix UI; shadcn component tokens; dark/light + high-contrast.
* **State**: TanStack Query (server state) + Zustand (local UX state) + React Context for auth/theme.
* **Realtime**: Socket.IO client for streaming answers & pipeline status; optimistic UI for uploads.
* **Auth**: JWT (httpOnly cookies) + silent refresh; Role/Scope guards (RBAC) on routes.
* **Accessibility**: WCAG 2.1 AA; keyboard-first flows; live-region announcements during stream.
* **Observability**: Frontend error boundary + Sentry SDK; Web Vitals to analytics.

**Key Screens**

1. **Ingest Studio**: drag/drop, source connectors (S3, GDrive, SharePoint, Confluence, Git), presigned uploads, PII toggle, OCR options.
2. **Validation Queue**: low-confidence spans, side-by-side document viewer, one-click accept/fix.
3. **Ask Workspace**: multi-turn chat with source citations, filters (space, time, entity), export to Markdown/CSV.
4. **Admin Console**: tenants, keys, quotas, retention, synonym dictionaries, stop-words.

---

## 3) Backend Architecture (FastAPI, PostgreSQL, Redis, Elasticsearch)

> **Frameworks we use (explicit):** **LangChain** (tooling & retrievers), **LangGraph** (stateful graph orchestration & retries), **CrewAI** (optional multi-agent teams for complex workflows), **RAG** pattern as the core retrieval-augmented answering strategy.

### 3.1 Services

* **API Gateway (FastAPI, async)**: REST + WebSocket; JWT auth; rate-limits (Redis sliding window).
* **Ingestion Service (Celery/Arq workers)**: presigned S3, MIME sniffing, chunking, OCR, layout parsing, metadata extraction.
* **Indexing Service**: embedding generation, hybrid rank (BM25 + vector), synonym expansion, de-dup.
* **Answering Service (LangGraph)**: graph nodes for Retrieve → Rerank → Ground → Generate → Guard → Cite.
* **Validation/Feedback Service**: HITL queue, annotation storage, model feedback loop.

### 3.2 Data & Search

* **Primary DB**: PostgreSQL 15 with **pgvector** (768/1024/3072 dims depending on model) for ANN; JSONB for metadata; row-level security.
* **Search**: **Elasticsearch 8** for BM25/keyword & aggregations; stored fields for snippet highlighting.
* **Cache/Queues**: Redis for sessions, rate limits, feature flags, idempotency keys.
* **Storage**: S3-compatible (versioned) for raw files & page images; signed URLs.

### 3.3 RAG Pipeline (Production Grade)

* **Chunking**: layout-aware (header/footers, tables); sliding windows w/ sentence-boundaries.
* **Embeddings**: OpenAI text-embedding-3-large or local (bge/multilingual) behind a provider switch.
* **Retrieval**: **LangChain** multi-retriever (dense pgvector + ES BM25) → **reciprocal-rank fusion**.
* **Rerank**: cross-encoder or lightweight LLM rerank; domain prompts.
* **Grounding & Guardrails**: schema-constrained JSON outputs; citation budget; content policy checks.
* **Generation**: **LangGraph** node calling GPT‑4 or Claude (tool-choice) with **source injection** & **context windows**.
* **Post-Gen**: factuality verifier (self-check + entailment), citation validator (must point to spans), redaction pass.

### 3.4 Multi‑Agent Orchestration (CrewAI - optional)

* **Agents**: Ingestion Agent (OCR/layout), Research Agent (query planning), Synthesis Agent (answer drafting), Compliance Agent (redaction/policy), Export Agent (reporting).
* **Coordinator**: **CrewAI** hands off to **LangGraph** nodes for deterministic steps; retries & backoff defined per edge; circuit breakers on tool errors.

### 3.5 Security & Compliance

* Tenant isolation (schema-per-tenant or row RLS), AES‑256 at rest, TLS 1.2+, KMS-managed keys.
* Secrets via environment & rotation; scoped API keys per connector.
* DLP/PII policies: regex + ML detectors; automatic hash/partial redact; audit log with immutable store.

---

## 4) Integrations

* **LLMs**: OpenAI GPT‑4, Anthropic Claude (provider router based on task: analysis vs. summarization).
* **OCR**: Tesseract + optional AWS Textract/Google Vision.
* **Connectors**: S3/GCS/Azure Blob, Google Drive, SharePoint/OneDrive, Confluence, Slack, GitHub.
* **Monitoring**: Prometheus metrics + Grafana; Sentry; OpenTelemetry traces.

---

## 5) DevOps & Deployment

* **Containers**: Docker; multi-stage images; health checks `/healthz`.
* **Environments**: Vercel (FE), Render/Kubernetes (BE); autoscale workers.
* **CI/CD**: GitHub Actions → tests (pytest + coverage), mypy, ruff, Playwright e2e → deploy.
* **Observability**: JSON logs with correlation IDs; RED metrics; alerting SLOs.

---

## 6) Success Criteria (Measurable)

* **Answer Quality**: ≥ **95%** answers contain **≥1 valid citation**; hallucination rate < **2%** (HITL sampled).
* **Latency**: P50 **<700ms** retrieval, **<2.0s** end‑to‑end streaming first token; P95 **<4s**.
* **Scale**: 10k concurrent chats; 1M docs; 10M chunks; sustained 500 rps on retrieval tier.
* **Uptime**: **99.9%** monthly; error budget tracked; zero data cross‑tenant incidents.
* **Accessibility**: Lighthouse ≥ **95**, WCAG 2.1 AA verified patterns.
* **Security**: 0 critical vulns; all secrets rotated quarterly; SOC2‑ready controls mapped.
* **Testing**: > **90%** backend unit/integration; Playwright e2e on key flows; chaos tests on graph retries.

---

## 7) Execution Prompts for Claude (Build Order)

1. **Project Setup & Architecture** – Scaffold FE/BE; envs; keys; base CI; connectors.
2. **Core Backend (LangChain + LangGraph)** – Ingestion workers, vector+BM25, graph orchestration, REST/WebSocket.
3. **Frontend Components** – Ingest Studio, Validation Queue, Ask Workspace, Admin Console.
4. **AI Integration & Features** – Provider router, rerankers, guardrails, multi‑agent (CrewAI) paths.
5. **Deployment & Optimization** – Autoscale, caching, perf budgets, monitoring, SLO alerts.

---

## 8) Roadmap (60–90 Days)

* v1: Hybrid retrieval, citations, HITL validation, exports.
* v1.1: Domain adapters (legal/finance), semantic filters, glossary.
* v1.2: Query planner (ReAct), few‑shot memory, enterprise SSO, FGAC.

> **Outcome:** A production‑ready, evidence‑driven RAG Knowledge OS built on **LangChain + LangGraph**, optionally **CrewAI** for multi‑agent workflows—meeting enterprise bar for **speed, accuracy, and trust**.
