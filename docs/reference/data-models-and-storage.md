# Data Models, Storage Schemas & Database Migrations

JARVIS stores interaction state, declarative memory, mobile pairing tokens, and telephony records in a local SQLite database (`jarvis.db`) configured in Write-Ahead Logging (`WAL`) mode ([`src/jarvis/storage/database.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/storage/database.py)).

---

## 1. Database Configuration & Engine Architecture

- **Path:** Dynamically resolved to `settings.DATABASE_PATH` (default: `jarvis/data/jarvis.db`).
- **Pragmas Applied on Connection:**
  ```sql
  PRAGMA journal_mode = WAL;
  PRAGMA synchronous = NORMAL;
  PRAGMA foreign_keys = ON;
  PRAGMA busy_timeout = 5000;
  ```
- **Thread Safety:** Python connection pools and async locks ensure transactional safety across concurrent daemons (Gateway, Telegram, WhatsApp, Cron).

---

## 2. Relational Schema & Tables

### 2.1 Interaction Sessions (`sessions`)
Tracks conversational threads across channels:
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON object storing client info, channel, voice persona
);
```

### 2.2 Conversational Turns (`turns`)
Preserves chronological dialogue history, model outputs, and tool proposals:
```sql
CREATE TABLE turns (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,           -- 'user', 'assistant', 'system', 'tool'
    content TEXT NOT NULL,
    tool_calls TEXT,              -- JSON array of proposed tool calls
    tool_results TEXT,            -- JSON array of verified tool execution outcomes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
CREATE INDEX idx_turns_session ON turns(session_id, created_at);
```

### 2.3 Long-Term Memory & Knowledge Base (`memories`)
Stores facts, observations, and learned operator preferences:
```sql
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,       -- 'preference', 'fact', 'observation', 'call_debrief'
    content TEXT NOT NULL,
    importance REAL DEFAULT 1.0,  -- Multiplier for semantic decay ranking (0.1 - 2.0)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 Full-Text Search Virtual Table (`memories_fts`)
SQLite FTS5 virtual table providing sub-millisecond BM25 keyword matching:
```sql
CREATE VIRTUAL TABLE memories_fts USING fts5(
    content,
    category,
    tokenize='porter unicode61'
);
```

### 2.5 Autonomous Task Records (`tasks`)
Tracks multi-step goals and subagent progress:
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,         -- 'QUEUED', 'IN_PROGRESS', 'COMPLETED', 'FAILED'
    plan TEXT,                    -- JSON array of execution steps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);
```

### 2.6 Telegram Paired Operators (`telegram_users`)
Stores paired smartphone identities authorized to command the PC remotely:
```sql
CREATE TABLE telegram_users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    paired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Database Migration Lifecycle

Database migrations are managed declaratively in [`src/jarvis/storage/migrations.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/storage/migrations.py):
- A dedicated tracking table (`schema_migrations`) stores applied version keys.
- On startup, `DatabaseEngine.initialize()` compares applied migrations against the code registry and executes pending migrations sequentially inside an ACID transaction.
- If a migration statement fails, the transaction is rolled back unconditionally, preventing partial or corrupted schemas.
