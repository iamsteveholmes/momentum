# Consultation Log — SQLDelight Reactive Entity Query

**Query:** `SQLDelight asFlow mapToList coroutines dispatcher requirements`
**Skill invoked:** `wiki-query`
**Date:** 2026-05-14
**Mode:** normal (full retrieval pipeline)
**Escalated:** false

---

## Routing Decision

The developer question covers SQLDelight schema setup + reactive query observation. The cmp-dev routing table maps "Query result not updating UI reactively" to `wiki-query SQLDelight asFlow mapToList coroutines dispatcher requirements`. This is a version-pinned, API-specific topic (the dispatcher parameter is a 2.x breaking change) — wiki-query is the correct mode, not a standing-rule direct answer.

---

## Step 1 — Index Pass

Read `index.md`. Identified candidate pages immediately from the Concepts section:

- `[[SQLDelight Coroutines and Flow Integration]]` — summary: "asFlow(), mapToList(), reactive vs one-shot, dispatcher requirements" — exact match
- `[[SQLDelight .sq Schema Files and Code Generation]]` — summary: "Schema definition, labeled queries, execution methods, transactions"
- `[[SQLDelight Platform Drivers]]` — summary: "Per-platform driver setup (Android, JVM desktop, iOS)"
- `[[Nornspun Kotlin KMP Conventions]]` — project-specific conventions, SQLDelight 2.3.2 section

No grep needed — index entries were precise enough. No QMD configured (env check skipped).

---

## Step 2 — Full Page Reads (4 pages)

### Page 1: `SQLDelight Coroutines and Flow Integration`

**Path:** `/Users/steve/projects/nornspun-agentic-kb/concepts/SQLDelight Coroutines and Flow Integration.md`

**Key insights:**
- `asFlow()` emits immediately with current result set, then re-emits on any table change via a registered listener
- `mapToList(dispatcher)` requires an explicit `CoroutineDispatcher` in 2.x — this is a breaking change from 1.x
- `mapToOne`, `mapToOneOrNull`, `mapToOneOrDefault` follow the same dispatcher rule
- Always use `Dispatchers.IO` for file-backed databases
- Standard `Repository` pattern: `observeAll()` returns `Flow<List<T>>`; writes use `withContext(Dispatchers.IO)`
- `awaitAs*` methods only apply when `generateAsync = true` (JS/WebWorker) — not relevant for Android/Desktop

### Page 2: `SQLDelight .sq Schema Files and Code Generation`

**Path:** `/Users/steve/projects/nornspun-agentic-kb/concepts/SQLDelight .sq Schema Files and Code Generation.md`

**Key insights:**
- `.sq` files live under `src/commonMain/sqldelight/[package]/` — one file per table by convention
- Files always describe latest schema for empty database (not migrations)
- Named query labels (`selectAll:`, `insert:`) map to generated Kotlin functions on the `*Queries` class
- Native type mappings: `INTEGER` → `Long`, `REAL` → `Double`, `TEXT` → `String`, `BLOB` → `ByteArray`
- The `AS` keyword + Kotlin type imports required for custom type mapping; needs `ColumnAdapter`
- Build task: `./gradlew generateCommonMainDatabaseInterface`

### Page 3: `SQLDelight Platform Drivers`

**Path:** `/Users/steve/projects/nornspun-agentic-kb/concepts/SQLDelight Platform Drivers.md`

**Key insights:**
- Android: `android-driver` in `androidMain`; iOS: `native-driver` in `nativeMain`; JVM Desktop: `sqlite-driver` in `jvmMain`
- `DatabaseDriverFactory` interface pattern in `commonMain` — standard KMP expect/actual approach
- JVM desktop: must call `AppDatabase.Schema.create(driver)` manually
- In-memory JVM driver: `JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)` + `Schema.create(driver)` for testing
- JVM WAL mode not enabled by default — must set manually if needed

### Page 4: `Nornspun Kotlin KMP Conventions`

**Path:** `/Users/steve/projects/nornspun-agentic-kb/project/nornspun/engineering/kotlin-kmp-conventions.md`

**Key insights:**
- Project SQLDelight version: 2.3.2 (project currently on 2.2.1 — convention doc tracks target)
- Gradle DSL: must use `.set()` (property setter) not `=` assignment — 2.x breaking change from 1.x
- Existing `ConversationRepository` pattern confirmed: `asFlow().mapToList(Dispatchers.IO)` is the project convention
- Module structure: SQLDelight goes in `shared/src/commonMain/sqldelight/com/nornspun/db/`
- `coroutines-extensions` dependency required in `commonMain`

---

## Gaps

- No wiki page covers `collectAsStateWithLifecycle` specifically (it's mentioned in the StateFlow concept page but not as a dedicated page). Applied from standing knowledge.
- No wiki page for `viewModelScope` desktop caveat — the ViewModel in CMP page exists but was not read in this retrieval (not needed to answer the schema + reactive query question).

---

## Confidence

High. The four pages consulted directly address every aspect of the question:
- Schema structure: Page 2
- Reactive query setup: Page 1
- Platform drivers and testing: Page 3
- Project conventions and version pins: Page 4
