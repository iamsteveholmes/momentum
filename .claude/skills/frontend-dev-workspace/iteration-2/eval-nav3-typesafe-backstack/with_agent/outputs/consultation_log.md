# Consultation Log — Nav 3 Type-Safe Backstack Query

## Query

`Navigation 3 CMP NavDisplay back stack type-safe SavedStateConfiguration`

Triggered by routing table rule in cmp-dev.md:
> **Nav 3 back stack and `NavDisplay` setup** → `wiki-query Navigation 3 CMP NavDisplay back stack type-safe SavedStateConfiguration`

---

## Step 1: hot.md (instant pre-check)

**File:** `/Users/steve/projects/nornspun-agentic-kb/hot.md`

Found two directly relevant signals:

1. Key Takeaways section: "Navigation 3 CMP: back stack = user-owned `SnapshotStateList`; non-JVM needs `SavedStateConfiguration` + polymorphic serializer; `ListDetailSceneStrategy` for adaptive layouts; alpha (1.0.0-alpha05) as of May 2026"

2. Open question flagged: "MVI + Navigation 3 (CMP): Where does navigation live when back stack is user-owned `SnapshotStateList`? `Channel<Effect>` pattern uncertain"

**Key insight:** `SavedStateConfiguration` is explicitly required for non-JVM; the MVI integration with Nav 3 is documented as an unresolved open question in the wiki.

---

## Step 2: index.md pass

**File:** `/Users/steve/projects/nornspun-agentic-kb/index.md`

Located three candidate pages:
- `[[Navigation 3 CMP]]` — concept page: "Back-stack-as-list, type-safe routes, SavedStateConfiguration, adaptive layouts"
- `[[projects/nornspun-agentic-kb/references/web-kotlinlang-org-multiplatform-compose-navigation-3]]` — reference: "Navigation 3 CMP (alpha): user-owned back stack, SavedStateConfiguration, NavDisplay, adaptive layouts"
- `[[source-navigation3-cmp-johnoreilly]]` — practical walkthrough source

Also identified `[[MVI Pattern in Compose]]` as relevant for the Channel/Effect pattern question.

---

## Step 3: Full Read — Navigation 3 CMP concept page

**File:** `/Users/steve/projects/nornspun-agentic-kb/concepts/Navigation 3 CMP.md`

**Key insights:**
- Nav 3 is stable on Android (Nov 2025); CMP support since CMP 1.10
- Back stack = `rememberNavBackStack(config, HomeRoute)` — mutable list you own
- Routes: `@Serializable data object/class : NavKey`
- `SavedStateConfiguration` with `SerializersModule` polymorphic registration is required for non-JVM platforms
- Small project shortcut: sealed interface + `subclassesOfSealed<Route>()`
- Multi-module: combine `SerializersModule` with `+` operator
- Dependencies: `navigation3-ui:1.0.0-alpha05`
- Adaptive layout: `ListDetailSceneStrategy` + `NavDisplay(backStack, sceneStrategy)`
- Contradiction noted: Nav 3 is alpha; production teams should evaluate stability

---

## Step 4: Full Read — Official CMP Nav 3 reference

**File:** `/Users/steve/projects/nornspun-agentic-kb/projects/nornspun-agentic-kb/references/web-kotlinlang-org-multiplatform-compose-navigation-3.md`

**Key insights:**
- Confirms: reflection-based overload is Android/JVM-only; `SavedStateConfiguration` is the cross-platform path
- Small project pattern: sealed interface + `SnapshotStateListSerializer` — no explicit `SavedStateConfiguration` needed
- Multi-module: explicit `subclassesOfSealed<FeatureX>()` per module
- `NavDisplay(backStack = backStack, ...)` renders current destination
- Browser navigation PoC available (`navigation3-browser:0.2.0`); full support in Nav3 v1.1.0
- Only `navigation3-ui` has CMP implementation; `navigation3-common` is transitive

---

## Step 5: Source check — John O'Reilly walkthrough

**File:** `/Users/steve/projects/nornspun-agentic-kb/sources/source-navigation3-cmp-johnoreilly.md`

**Key insights:**
- Confirms same-code-on-Android-iOS-Desktop claim
- `rememberNavBackStack(config, RouteA)` with `SavedStateConfiguration` shown as the universal pattern
- `ListDetailSceneStrategy` adjusts to window dimensions without platform-specific code

---

## Step 6: Grep pass — MVI Pattern in Compose

**File:** `/Users/steve/projects/nornspun-agentic-kb/concepts/MVI Pattern in Compose.md`

Confirmed: `Channel<Effect>` is the established pattern for navigation effects. But the page contains no Nav 3 backstack content. The wiki explicitly leaves the MVI + Nav 3 integration as an open question.

---

## Summary

| Page | Step | Key Insight |
|---|---|---|
| `hot.md` | Pre-check | `SavedStateConfiguration` required for non-JVM; MVI+Nav3 = open question |
| `index.md` | Index pass | Three Nav 3 candidate pages identified |
| `concepts/Navigation 3 CMP.md` | Full read | Complete setup pattern: routes, config, NavDisplay, dependency versions |
| `references/web-kotlinlang-org-multiplatform-compose-navigation-3.md` | Full read | Two overloads clarified; reflection=JVM-only; `SavedStateConfiguration`=process-death-safe |
| `sources/source-navigation3-cmp-johnoreilly.md` | Full read | Cross-platform identical code confirmed; practical usage patterns |
| `concepts/MVI Pattern in Compose.md` | Grep pass | `Channel<Effect>` is canonical for navigation effects; Nav 3 integration not resolved |

Total pages consulted: 5 (3 full reads + grep + index pass)
Escalation: not required — index pass produced high-confidence candidates immediately
