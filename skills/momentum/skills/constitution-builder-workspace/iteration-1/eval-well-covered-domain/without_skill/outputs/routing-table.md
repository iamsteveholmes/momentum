## Quick Routing

> **KB coverage note:** The Nornspun KB contains no React or Next.js pages. All `wiki-query` entries below will return sparse or no results. This routing table documents intended query patterns for a React/Next.js skill; actual resolution requires ingesting React and Next.js documentation into the KB first.

### React Hooks — useState & useEffect

| Symptom | Query |
|---|---|
| Component re-renders more than expected after setState | `wiki-query React useState re-render batching stale closure` |
| State update not reflected immediately after set call | `wiki-query React useState asynchronous update closure` |
| useEffect running on every render instead of once | `wiki-query React useEffect dependency array empty mount` |
| useEffect cleanup not running / memory leak warning | `wiki-query React useEffect cleanup return function teardown` |
| Fetch inside useEffect causes race condition or stale data | `wiki-query React useEffect fetch abort controller stale closure` |
| State based on previous state is wrong | `wiki-query React useState functional update prevState` |

### React Hooks — useCallback & useMemo

| Symptom | Query |
|---|---|
| Child component re-renders even though props look the same | `wiki-query React useCallback referential equality memo child re-render` |
| useCallback or useMemo not preventing re-computation | `wiki-query React useMemo useCallback dependency array referential equality` |
| Expensive calculation running on every render | `wiki-query React useMemo expensive computation memoization` |
| Event handler recreated on every render, breaking React.memo | `wiki-query React useCallback stable reference React.memo` |
| When to use useMemo vs useCallback — decision guidance | `wiki-query React useMemo useCallback when to use tradeoffs` |

### React Hooks — Custom Hooks & Rules of Hooks

| Symptom | Query |
|---|---|
| "Hooks can only be called inside a function component" error | `wiki-query React rules of hooks conditional invalid call` |
| Extracting stateful logic into a reusable hook | `wiki-query React custom hook extract stateful logic reuse` |
| Hook dependencies cause infinite loop | `wiki-query React useEffect infinite loop dependency object function` |
| useReducer vs useState — when to choose | `wiki-query React useReducer useState complex state decision` |

### Next.js App Router — Routing & Navigation

| Symptom | Query |
|---|---|
| Link component not prefetching or navigating correctly | `wiki-query Next.js App Router Link prefetch client navigation` |
| Dynamic route segment not matching or params undefined | `wiki-query Next.js App Router dynamic segments params page` |
| Catch-all and optional catch-all route differences | `wiki-query Next.js App Router catch-all optional segments` |
| Parallel routes or intercepting routes not rendering as expected | `wiki-query Next.js App Router parallel routes intercepting modal` |
| useRouter push not triggering navigation in App Router | `wiki-query Next.js App Router useRouter navigation programmatic` |
| Route groups not affecting URL but breaking layout | `wiki-query Next.js App Router route groups layout organization` |

### Next.js App Router — Server Components

| Symptom | Query |
|---|---|
| "You're importing a component that needs useState" error in Server Component | `wiki-query Next.js server component client component boundary use client` |
| Where to draw the client/server boundary | `wiki-query Next.js server component client component boundary decision` |
| Context API not working inside Server Components | `wiki-query Next.js server component context provider workaround` |
| Third-party library breaks in Server Components | `wiki-query Next.js server component third-party library use client wrapper` |
| Server Component vs Client Component — performance tradeoffs | `wiki-query Next.js server component rendering HTML payload RSC` |
| Passing data from Server Component down to Client Component | `wiki-query Next.js server component props serialization client component` |

### Next.js App Router — Data Fetching

| Symptom | Query |
|---|---|
| fetch() response not being cached or always refetching | `wiki-query Next.js fetch cache revalidate static dynamic` |
| On-demand revalidation after a mutation | `wiki-query Next.js revalidatePath revalidateTag on-demand ISR` |
| Server Action not updating UI after form submission | `wiki-query Next.js server action form revalidation optimistic update` |
| Loading UI not showing during navigation | `wiki-query Next.js loading.tsx suspense streaming App Router` |
| Error boundary not catching errors in async Server Components | `wiki-query Next.js error.tsx error boundary async server component` |
| Waterfall fetching — parallel vs sequential data requests | `wiki-query Next.js parallel data fetching Promise.all server component` |
| Streaming long responses progressively to the client | `wiki-query Next.js streaming Suspense RSC progressive rendering` |

### Cross-Cutting Concerns

| Symptom | Query |
|---|---|
| Middleware not running or running on wrong paths | `wiki-query Next.js middleware matcher config edge runtime` |
| Environment variables not accessible in the browser | `wiki-query Next.js NEXT_PUBLIC environment variable client server` |
| Image component causing layout shift or not optimizing | `wiki-query Next.js Image component optimization layout shift priority` |
| TypeScript types for page props params and searchParams | `wiki-query Next.js TypeScript page props params searchParams types` |
