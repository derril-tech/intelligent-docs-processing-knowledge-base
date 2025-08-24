# Product Brief

⚠️ IMPORTANT  
This document defines the **product's purpose, users, and goals**.  
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
* **Real-time Service (WebSocket)**: connection management, event routing, tenant isolation.
* **Connector Service**: external integrations (Google Drive, SharePoint, Confluence, Slack, GitHub).

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

### 3.4 Real-time Communication (WebSocket)

* **Connection Management**: Tenant-isolated WebSocket connections with JWT authentication.
* **Event Routing**: Predefined event types for document processing, validation, chat, and sync.
* **Broadcasting**: Utility functions for tenant-specific and system-wide notifications.
* **Error Handling**: Automatic reconnection with exponential backoff.
* **Integration**: Seamless integration with FastAPI router.

### 3.5 Source Connectors Framework

* **Abstract Base Class**: Common interface for all external service connectors.
* **Connector Manager**: Centralized registration and sync management.
* **OAuth2 Integration**: Secure authentication flows for external services.
* **Rate Limiting**: Intelligent rate limiting and retry logic.
* **Real-time Updates**: WebSocket notifications for sync progress.
* **Supported Services**: Google Drive, SharePoint, Confluence, Slack, GitHub.

### 3.6 Multi‑Agent Orchestration (CrewAI - optional)

* **Agents**: Ingestion Agent (OCR/layout), Research Agent (query planning), Synthesis Agent (answer drafting), Compliance Agent (redaction/policy), Export Agent (reporting).
* **Coordinator**: **CrewAI** hands off to **LangGraph** nodes for deterministic steps; retries & backoff defined per edge; circuit breakers on tool errors.

### 3.7 Security & Compliance

* Tenant isolation (schema-per-tenant or row RLS), AES‑256 at rest, TLS 1.2+, KMS-managed keys.
* Secrets via environment & rotation; scoped API keys per connector.
* DLP/PII policies: regex + ML detectors; automatic hash/partial redact; audit log with immutable store.
* WebSocket authentication: JWT token validation for real-time connections.

---

## 4) Integrations

* **LLMs**: OpenAI GPT‑4, Anthropic Claude (provider router based on task: analysis vs. summarization).
* **OCR**: Tesseract + optional AWS Textract/Google Vision.
* **Connectors**: S3/GCS/Azure Blob, Google Drive, SharePoint/OneDrive, Confluence, Slack, GitHub.
* **Real-time**: WebSocket server with tenant isolation and event routing.
* **Monitoring**: Prometheus, Grafana, Sentry, structured logging.

---

## 5) Infrastructure Status

### ✅ **Completed Infrastructure (80%)**
- **WebSocket Server**: Complete with connection management, tenant isolation, and event routing
- **Advanced RAG Pipeline**: Complete with LangGraph workflow, reranker interfaces, and hybrid retrieval
- **Source Connectors Framework**: Complete with abstract base classes, connector manager, and multiple service support
- **API Integration**: WebSocket endpoint integrated into main API router
- **Multi-tenant Security**: Row-level security and tenant isolation
- **Health Monitoring**: Comprehensive health checks for all services

### 🔄 **Claude Implementation Tasks (20%)**
- **Real-time Features**: WebSocket event handlers for document processing, chat streaming, validation notifications
- **Advanced RAG**: Cross-encoder reranking, reciprocal rank fusion, LLM generation with citations
- **External Integrations**: OAuth2 flows and API integrations for external services
- **Multi-Agent Workflows**: CrewAI agents for complex document processing

---

## 6) Performance Targets

* **RAG Query Response**: < 2s for complex queries with citations
* **File Upload**: < 5s for 50MB files
* **WebSocket Events**: < 100ms for real-time updates
* **Concurrent Users**: 10,000+ simultaneous users
* **Document Processing**: 1M+ documents per month
* **Uptime**: 99.9% availability with comprehensive monitoring

---

## 7) Success Metrics

* **Technical**: < 2s RAG response time, 99.9% uptime, zero security vulnerabilities
* **User Experience**: Intuitive interface, fast loading, seamless real-time updates
* **Business**: High adoption, significant time savings, enterprise-scale scalability
* **Compliance**: Full SOC2, GDPR compliance with comprehensive audit logging
