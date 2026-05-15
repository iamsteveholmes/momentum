# Adding a reactive `Workout` entity to nornspun-client

## 1. Define the schema — `Workout.sq`

Place at `shared/src/commonMain/sqldelight/nornspun/Workout.sq` (one `.sq` per table, matching the existing `Conversations.sq` convention):

```sql
CREATE TABLE workout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    created_at INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s','now') AS INTEGER))
);

CREATE INDEX idx_workout_created_at ON workout(created_at);

selectAll:
SELECT * FROM workout ORDER BY created_at DESC;

selectById:
SELECT * FROM workout WHERE id = ?;

insert:
INSERT INTO workout(name, duration_seconds)
VALUES (?, ?);

deleteById:
DELETE FROM workout WHERE id = ?;
```

Notes:
- `INTEGER → Long`, `TEXT → String` map natively — no `AS` adapters needed for this entity, so no `import` lines at the top.
- Every labeled statement (`selectAll:`, `insert:`, ...) generates a typed Kotlin function on `WorkoutQueries`.
- This file describes the **latest** schema; if you later evolve it, that's a `.sqm` migration, not an edit here.
- IDE plugin re-runs codegen on save; CLI is `./gradlew generateCommonMainDatabaseInterface`.

## 2. Confirm the coroutines extension is on the classpath

In `shared/build.gradle.kts` (commonMain), make sure this is present alongside `sqldelight.runtime`:

```kotlin
implementation("app.cash.sqldelight:coroutines-extensions:<version>")
```

No platform-specific dep — the extension is multiplatform.

## 3. Repository — expose a `Flow<List<Workout>>`

`shared/src/commonMain/kotlin/.../data/WorkoutRepository.kt`:

```kotlin
class WorkoutRepository(
    private val queries: WorkoutQueries,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO,
) {
    // Reactive — re-emits whenever the `workout` table changes
    fun observeAll(): Flow<List<Workout>> =
        queries.selectAll()
            .asFlow()
            .mapToList(ioDispatcher)

    suspend fun add(name: String, durationSeconds: Long) =
        withContext(ioDispatcher) { queries.insert(name, durationSeconds) }

    suspend fun delete(id: Long) =
        withContext(ioDispatcher) { queries.deleteById(id) }
}
```

How the reactivity actually works:
- `asFlow()` turns `Query<T>` into `Flow<Query<T>>`. It **emits immediately with the current result set**, then **re-emits whenever the underlying table changes** because SQLDelight registers a listener on the query against the driver.
- `mapToList(dispatcher)` calls `executeAsList()` on each emission on the given dispatcher. **The dispatcher is mandatory in SQLDelight 2.x** — `Dispatchers.IO` for a file-backed SQLite driver.
- Use `mapToOneOrNull(dispatcher)` for a single-row observation (e.g., `selectById`). `mapToOne` throws on empty — only when you've guaranteed a row exists.
- The trigger is **any write through the same driver/transacter that targets the watched table**. Calling `queries.insert(...)` causes every active `selectAll().asFlow()` collector to re-fire automatically. No manual invalidation, no event bus.

## 4. ViewModel — own the state machine

State, intent, and effect per the MVI rules:

```kotlin
data class WorkoutListUiState(
    val workouts: List<Workout> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null,
)

sealed interface WorkoutListIntent {
    data class Add(val name: String, val durationSeconds: Long) : WorkoutListIntent
    data class Delete(val id: Long) : WorkoutListIntent
}

sealed interface WorkoutListEffect {
    data class ShowError(val message: String) : WorkoutListEffect
}

class WorkoutListViewModel(
    private val repo: WorkoutRepository,
) : ViewModel() {

    private val _effects = Channel<WorkoutListEffect>(Channel.BUFFERED)
    val effects: Flow<WorkoutListEffect> = _effects.receiveAsFlow()

    val state: StateFlow<WorkoutListUiState> =
        repo.observeAll()
            .map { WorkoutListUiState(workouts = it, isLoading = false) }
            .catch { e ->
                emit(WorkoutListUiState(isLoading = false, error = e.message))
                _effects.send(WorkoutListEffect.ShowError(e.message ?: "unknown"))
            }
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = WorkoutListUiState(),
            )

    fun onIntent(intent: WorkoutListIntent) {
        when (intent) {
            is WorkoutListIntent.Add ->
                viewModelScope.launch { repo.add(intent.name, intent.durationSeconds) }
            is WorkoutListIntent.Delete ->
                viewModelScope.launch { repo.delete(intent.id) }
        }
    }
}
```

Key points:
- The `Flow<List<Workout>>` from SQLDelight is the **single source of truth**. The ViewModel just `map`s it into UI state and converts the cold flow into a `StateFlow` via `stateIn(WhileSubscribed)`.
- After `repo.add(...)`, you do **not** update state yourself. SQLDelight fires the table listener, `asFlow()` re-emits, `map` rebuilds the UI state, and the composable recomposes.
- `Channel(BUFFERED).receiveAsFlow()` for effects — never `StateFlow` for navigation/toasts (they'd replay on resubscription).

## 5. Composable — observe and emit intents

```kotlin
@Composable
fun WorkoutListScreen(viewModel: WorkoutListViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.effects.collect { effect ->
            when (effect) {
                is WorkoutListEffect.ShowError -> { /* show snackbar */ }
            }
        }
    }

    Column {
        if (state.isLoading) CircularProgressIndicator()
        LazyColumn {
            items(state.workouts, key = { it.id }) { workout ->
                WorkoutRow(
                    workout = workout,
                    onDelete = { viewModel.onIntent(WorkoutListIntent.Delete(workout.id)) },
                )
            }
        }
        AddWorkoutButton(
            onAdd = { name, secs ->
                viewModel.onIntent(WorkoutListIntent.Add(name, secs))
            },
        )
    }
}
```

Why this updates reactively without you doing anything special:
- `collectAsStateWithLifecycle` keeps the UI subscribed to `state` while the screen is alive.
- The subscription keeps `asFlow().mapToList(...)` collecting in the ViewModel scope.
- Any `INSERT`/`DELETE`/`UPDATE` against `workout` — from this screen, from another screen, from a background sync — flows back through SQLDelight's listener → `mapToList` → ViewModel `map` → `StateFlow` → recomposition.
- Use `key = { it.id }` on `LazyColumn.items` so rows preserve state across re-emissions (don't recompose every row on every list change).

## 6. Test — Turbine + in-memory driver

```kotlin
class WorkoutRepositoryTest : FunSpec({
    coroutineTestScope = true

    lateinit var driver: SqlDriver
    lateinit var repo: WorkoutRepository

    beforeTest {
        driver = inMemorySqlDriver()  // your shared test helper
        AppDatabase.Schema.create(driver)
        repo = WorkoutRepository(
            AppDatabase(driver).workoutQueries,
            ioDispatcher = UnconfinedTestDispatcher(testScheduler),
        )
    }

    test("observeAll emits initial empty list then updates on insert") {
        repo.observeAll().test {
            awaitItem() shouldBe emptyList()
            repo.add("Run", 1800)
            awaitItem().single().name shouldBe "Run"
            cancelAndIgnoreRemainingEvents()
        }
    }
})
```

Per the standing rules: `coroutineTestScope = true` is non-negotiable for any test touching suspend functions or virtual time, and Turbine's `awaitItem()` is how you exercise the emission rather than assuming it fires.

---

## Gotchas

- 2.x **requires** an explicit dispatcher on every `mapTo*` operator (1.x default was implicit). Don't copy old snippets.
- The listener fires on **table** changes via the **same driver**. If a sync layer ever bypasses the SQLDelight driver (e.g., raw `execSQL` from elsewhere), the flow won't re-emit — keep all writes funneled through `WorkoutQueries`.
- Don't `mapToOne` a list-shaped query; and don't `mapToOne` a possibly-empty single-row query — it throws.

## Wiki sources

- `concepts/SQLDelight Coroutines and Flow Integration.md`
- `concepts/SQLDelight .sq Schema Files and Code Generation.md`
