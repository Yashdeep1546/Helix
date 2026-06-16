# Vectis 🚀

### High-Throughput Async Content Engine & Secure Authentication Runtime

Vectis is a production-grade, fully asynchronous REST API built with **FastAPI**, **SQLModel**, and **Redis**. Designed to move beyond standard tutorial-tier implementations, Vectis showcases a battle-hardened architecture featuring dual-token authentication, robust cursor-based pagination, and strict database connection multiplexing.

---

## 🛰️ Animated Data Flow Architecture

The following dynamic diagram illustrates how a client request interacts with the Vectis ecosystem. The animated indicators represent real-time data streaming, cache validation, and asynchronous database execution paths.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="100%" style="background:#0d1117; border-radius:12px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <style>
    .node-text { fill: #c9d1d9; font-size: 13px; font-weight: 600; text-anchor: middle; }
    .title-text { fill: #58a6ff; font-size: 11px; font-weight: bold; letter-spacing: 1px; }
    .flow-line { stroke: #30363d; stroke-width: 2; fill: none; }
    .pulse-line { stroke-width: 2; fill: none; stroke-dasharray: 8, 12; animation: flow 2s linear infinite; }
    .client-pulse { stroke: #ff7b72; }
    .cache-pulse { stroke: #79c0ff; }
    .db-pulse { stroke: #56d364; }
    
    @keyframes flow {
      to { stroke-dashoffset: -40; }
    }
    
    .box { stroke-width: 1.5; rx: 8; }
    .box-client { fill: #21262d; stroke: #ff7b72; }
    .box-fastapi { fill: #161b22; stroke: #1f6feb; stroke-width: 2; }
    .box-redis { fill: #21262d; stroke: #79c0ff; }
    .box-db { fill: #21262d; stroke: #56d364; }
  </style>

  <!-- Title & Metadata -->
  <text x="30" y="35" class="title-text">VECTIS RUNTIME DATA FLOW MATRIX</text>

  <!-- Connections / Lines -->
  <!-- Client to FastAPI -->
  <path d="M 150 160 L 320 160" class="flow-line" />
  <path d="M 150 160 L 320 160" class="pulse-line client-pulse" />
  
  <!-- FastAPI to Redis (Cache Hit/Miss Path) -->
  <path d="M 420 130 C 470 70, 530 70, 580 130" class="flow-line" />
  <path d="M 420 130 C 470 70, 530 70, 580 130" class="pulse-line cache-pulse" />
  
  <!-- FastAPI to PostgreSQL (Async DB Path) -->
  <path d="M 420 190 C 470 250, 530 250, 580 190" class="flow-line" />
  <path d="M 420 190 C 470 250, 530 250, 580 190" class="pulse-line db-pulse" />

  <!-- Nodes / Components -->
  <!-- Client Node -->
  <g transform="translate(30, 115)">
    <rect width="120" height="90" class="box box-client" />
    <text x="60" y="45" class="node-text">HTTP Client</text>
    <text x="60" y="65" fill="#8b949e" font-size="11" text-anchor="middle">JSON Payloads</text>
  </g>

  <!-- FastAPI Core Engine -->
  <g transform="translate(320, 100)">
    <rect width="130" height="120" class="box box-fastapi" />
    <text x="65" y="45" class="node-text" fill="#58a6ff">FastAPI Core</text>
    <text x="65" y="70" fill="#8b949e" font-size="10" text-anchor="middle">Guards &amp; Throttling</text>
    <text x="65" y="90" fill="#2ea44f" font-size="11" font-family="monospace" text-anchor="middle">def async handlers</text>
  </g>

  <!-- Redis Cache Node -->
  <g transform="translate(580, 40)">
    <rect width="140" height="80" class="box box-redis" />
    <text x="70" y="35" class="node-text">Redis 7.x</text>
    <text x="70" y="55" fill="#79c0ff" font-size="11" font-family="monospace" text-anchor="middle">O(1) Read Cache</text>
  </g>

  <!-- PostgreSQL Database Node -->
  <g transform="translate(580, 190)">
    <rect width="140" height="80" class="box box-db" />
    <text x="70" y="35" class="node-text">PostgreSQL</text>
    <text x="70" y="55" fill="#56d364" font-size="11" font-family="monospace" text-anchor="middle">asyncpg Pipeline</text>
  </g>
</svg>
```

---

## ⚡ Core Architecture Breakdowns

### 📐 The Architectural Blueprint (Fundamental)

* **100% Type-Safe Contracts:** Built with comprehensive request-response segregation utilizing Pydantic schemas, guaranteeing strict validation barriers for internal business systems.
* **Cryptographic Vaulting:** Employs industry-standard cryptographic primitives via `pwdlib` to handle salt hashing alongside decoupled, stateless JSON Web Tokens (JWT).
* **Relational Integrity:** Implements native normalization patterns using SQLModel, defining programmatic database-level foreign key constraints and cascading mutations cleanly.

### 🚀 High-Concurrency Upgrades (Scalable)

* **Asynchronous I/O Multiplexing:** Completely eliminates execution-thread blocking by upgrading the database engine pipeline to run on non-blocking `asyncpg` drivers and transactional SQLAlchemy `AsyncSession` dependencies.
* **Constant-Time Pagination:** Mitigates severe horizontal scalability bottlenecks by replacing legacy, sequential offset logic with stable $O(1)$ cursor-based retrieval mechanics.
* **Redis Acceleration Layers:** Features decoupled in-memory write-through cache abstraction semantics to reduce storage engine index search pressures on heavy fetch patterns.
* **Production DevOps Controls:** Packaged neatly within containerized Docker Compose clusters and bound to structured automated GitHub Actions pipelines monitoring regression risks using `pytest`.

---

## 🛠️ Technology Stack Matrix

* **Runtime Web Framework:** FastAPI (ASGI Engine)
* **Data Models & ORM:** SQLModel & SQLAlchemy Async
* **Primary Storage Cluster:** PostgreSQL (Driven by `asyncpg`)
* **Caching & Rate Limiting Engine:** Redis 7 Cloud Stack
* **Validation Core:** Pydantic v2
* **Testing & CI Environment:** Pytest Suite + GitHub Actions Engine
* **Infrastructure Management:** Multi-Container Docker Compose Setup

---

## 📂 Code Layout

```text
app/
├── config.py          # Environment & secret settings definitions
├── database.py        # Asynchronous DB engine initialization & Session dependencies
├── main.py            # ASGI application lifecycle hooks & router mapping
├── models.py          # Relational SQLModel schemas mapped to persistent tables
├── oauth2.py          # JWT issuance, verification, and authentication interceptors
├── post_schema.py     # Pydantic data validation structures for operations
├── token_schema.py    # Schema definitions for token validation contracts
├── user_schema.py     # User registration and access token validation patterns
└── routers/
    ├── auth.py        # Identity validation & access token issuance handles
    ├── post.py        # Content mutation, caching, and async pagination handles
    └── user.py        # Identity provisioning and profile synchronization handles
```

---

## 📦 Rapid Deployment Strategy

Execute the following commands to spin up the entire isolated production-mirrored architecture stack (including application workers, PostgreSQL clusters, and active Redis pools) instantly:

```bash
# Clone the repository
git clone https://github.com/Yashdeep1546/Helix.git
cd Helix

# Fire up the entire containerized application infrastructure
docker-compose up --build -d

# Execute the integrated automated test suite across the active cluster
docker-compose exec web pytest
```
