# SQLDelight Reactive Entity Setup — Workout List Screen

*Grounded in wiki pages: [[SQLDelight .sq Schema Files and Code Generation]], [[SQLDelight Coroutines and Flow Integration]], [[SQLDelight Platform Drivers]], [[Nornspun Kotlin KMP Conventions]]*

---

## 1. Schema — `Workout.sq`

Place the file at `shared/src/commonMain/sqldelight/com/nornspun/db/Workout.sq` (matching your configured `packageName`). The `.sq` file always describes the latest schema for an empty database — it is not a migration file.

```sql
CREATE TABLE workout (
  id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name       TEXT    NOT NULL,
  started_at INTEGER NOT NULL,
  duration_s INTEGER NOT NULL DEFAULT 0
);

-- Named queries — each label becomes a function on WorkoutQueries

selectAll:
SELECT * FROM workout ORDER BY started_at DESC;

selectById:
SELECT * FROM workout WHERE id = ?;

insert:
INSERT INTO workout(name, started_at, duration_s)
VALUES (?, ?, ?);

deleteById:
DELETE FROM workout WHERE id = ?;
```

SQLDelight generates a `WorkoutQueries` class. Access it via `database.workoutQueries`.

**Type mapping reminder:**
- `INTEGER` → `Long` in Kotlin (not `Int`)
- `TEXT` → `String`

If you need a custom Kotlin type (e.g. `Instant` for `started_at`), add an `import` line and a `ColumnAdapter`. For a simple epoch-millis `Long`, no adapter is needed.

---

## 2. Adding the Dependency

In `shared/build.gradle.kts`, you need the coroutines extension in `commonMain` (no platform split needed):

```kotlin
commonMain.dependencies {
    implementation("app.cash.sqldelight:coroutines-extensions:2.3.2")
    // runtime is typically pulled transitively, but add explicitly if needed:
    // implementation("app.cash.sqldelight:runtime:2.3.2")
}
```

> **Project version note:** The project is currently pinned to SQLDelight 2.2.1. The coroutines extension version should match whatever is in your version catalog (typically `libs.sqldelight.coroutines`). The API below works for both 2.2.x and 2.3.x.

---

## 3. Gradle DSL — Register the Database

In `shared/build.gradle.kts`, use 2.x property-setter syntax:

```kotlin
sqldelight {
    databases {
        create("NornspunDatabase") {          // or AppDatabase — match your existing db name
            packageName.set("com.nornspun.db")
            dialect(libs.sqldelight.dialect.sqlite)
        }
    }
}
```

> **Breaking change from 1.x:** Do NOT use `=` assignment (`packageName = ...`). Must use `.set()`.

After adding `Workout.sq`, run:
```bash
./gradlew generateCommonMainDatabaseInterface
```
The IDE plugin triggers this automatically on file save.

---

## 4. Repository — `WorkoutRepository`

In `shared/src/commonMain/kotlin/com/nornspun/data/WorkoutRepository.kt`:

```kotlin
class WorkoutRepository(private val database: NornspunDatabase) {

    /**
     * Reactive stream — emits the full list immediately, then re-emits
     * whenever any INSERT/UPDATE/DELETE touches the workout table.
     * Collect this in the ViewModel; do NOT call executeAsList() here.
     */
    fun observeAll(): Flow<List<Workout>> =
        database.workoutQueries
            .selectAll()
            .asFlow()
            .mapToList(Dispatchers.IO)

    /** One-shot fetch — use only when reactivity is not needed. */
    suspend fun getById(id: Long): Workout? = withContext(Dispatchers.IO) {
        database.workoutQueries.selectById(id).executeAsOneOrNull()
    }

    suspend fun insert(name: String, startedAt: Long, durationSeconds: Long = 0L) =
        withContext(Dispatchers.IO) {
            database.workoutQueries.insert(name, startedAt, durationSeconds)
        }

    suspend fun delete(id: Long) = withContext(Dispatchers.IO) {
        database.workoutQueries.deleteById(id)
    }
}
```

### Critical dispatcher rule

`mapToList(Dispatchers.IO)` is **required** in SQLDelight 2.x — it is a breaking change from 1.x where the dispatcher was optional. Omitting it causes a compile error. The dispatcher controls which thread executes `executeAsList()` on each emission. Always pass `Dispatchers.IO` for file-backed SQLite.

### How reactivity works

`asFlow()` registers a query listener on the underlying SQLite table. Any write that touches `workout` (insert, update, delete) triggers a re-emission of `selectAll`. This is SQLDelight's built-in table-level invalidation — no manual refresh, no polling.

---

## 5. ViewModel — `WorkoutListViewModel`

In `composeApp/src/androidMain/kotlin/com/nornspun/ui/viewmodel/WorkoutListViewModel.kt`:

```kotlin
data class WorkoutListState(
    val workouts: List<Workout> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

sealed interface WorkoutListIntent {
    data object LoadWorkouts : WorkoutListIntent
    data class DeleteWorkout(val id: Long) : WorkoutListIntent
}

class WorkoutListViewModel(
    private val repository: WorkoutRepository
) : ViewModel() {

    private val _state = MutableStateFlow(WorkoutListState())
    val state: StateFlow<WorkoutListState> = _state.asStateFlow()

    init {
        observeWorkouts()
    }

    fun onIntent(intent: WorkoutListIntent) {
        when (intent) {
            is WorkoutListIntent.LoadWorkouts -> { /* already reactive — no-op */ }
            is WorkoutListIntent.DeleteWorkout -> deleteWorkout(intent.id)
        }
    }

    private fun observeWorkouts() {
        viewModelScope.launch {
            repository.observeAll()
                .catch { e -> _state.update { it.copy(error = e.message, isLoading = false) } }
                .collect { workouts ->
                    _state.update { it.copy(workouts = workouts, isLoading = false) }
                }
        }
    }

    private fun deleteWorkout(id: Long) {
        viewModelScope.launch {
            repository.delete(id)
            // No manual refresh needed — observeAll() re-emits automatically
        }
    }
}
```

**MVI rules applied:**
- State is a single immutable `data class` — `isLoading` and `error` are mutually exclusive by design.
- All user actions are sealed `WorkoutListIntent` members.
- The composable never writes to state.
- `viewModelScope` for all coroutines — no `GlobalScope`, no `runBlocking`.

---

## 6. Composable — `WorkoutListScreen`

```kotlin
@Composable
fun WorkoutListScreen(
    viewModel: WorkoutListViewModel = viewModel(),
    onWorkoutClick: (Long) -> Unit
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    when {
        state.isLoading -> CircularProgressIndicator()
        state.error != null -> Text("Error: ${state.error}")
        state.workouts.isEmpty() -> Text("No workouts yet.")
        else -> LazyColumn {
            items(state.workouts, key = { it.id }) { workout ->
                WorkoutRow(
                    workout = workout,
                    onClick = { onWorkoutClick(workout.id) }
                )
            }
        }
    }
}
```

`collectAsStateWithLifecycle()` stops collecting when the composable is not visible (e.g. backgrounded on Android), which is the correct lifecycle-aware pattern.

---

## 7. The Reactive Update Loop — End to End

```
INSERT INTO workout              ← repository.insert() on IO dispatcher
    │
    ▼
SQLDelight table listener fires
    │
    ▼
selectAll query re-executes     ← mapToList(Dispatchers.IO) dispatches the read
    │
    ▼
Flow<List<Workout>> emits new list
    │
    ▼
ViewModel.collect{} calls _state.update{}
    │
    ▼
StateFlow emits new WorkoutListState
    │
    ▼
collectAsStateWithLifecycle() triggers recomposition
    │
    ▼
LazyColumn renders updated list  ← UI updates reactively, zero manual refresh
```

No polling. No `notifyDataSetChanged()`. No `refresh()` calls after insert. The entire update propagates automatically.

---

## 8. Testing the Repository

Use an in-memory JVM driver in `commonTest` / `jvmTest`:

```kotlin
class WorkoutRepositoryTest : FunSpec({
    lateinit var driver: SqlDriver
    lateinit var repo: WorkoutRepository

    beforeTest {
        driver = JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)
        NornspunDatabase.Schema.create(driver)
        repo = WorkoutRepository(NornspunDatabase(driver))
    }

    afterTest {
        driver.close()
    }

    test("observeAll emits inserted workout") {
        val flow = repo.observeAll()

        flow.test {
            awaitItem() shouldBe emptyList()      // immediate emission on subscribe

            repo.insert("Morning Run", 1_700_000_000L, 3600L)

            awaitItem().also { list ->
                list shouldHaveSize 1
                list.first().name shouldBe "Morning Run"
            }
        }
    }
})
```

`flow.test { }` is Turbine's `testIn`-style block. The in-memory driver + `Schema.create()` gives you a clean database per test without any Android context.

---

## Summary of Key Rules

| Rule | Why |
|---|---|
| `mapToList(Dispatchers.IO)` is required in 2.x | Breaking change — omitting causes compile error |
| `asFlow()` gives table-level reactivity | No manual refresh needed after writes |
| Repository owns `withContext(Dispatchers.IO)` for writes | Keeps ViewModel dispatcher-agnostic |
| `viewModelScope.launch` in ViewModel | Structured concurrency; auto-cancelled on ViewModel clear |
| `collectAsStateWithLifecycle()` in Composable | Lifecycle-aware; stops collecting when app is backgrounded |
| `key = { it.id }` on LazyColumn items | Prevents item state reset on list update |

---

*Pages cited: [[SQLDelight Coroutines and Flow Integration]], [[SQLDelight .sq Schema Files and Code Generation]], [[SQLDelight Platform Drivers]], [[Nornspun Kotlin KMP Conventions]]*
