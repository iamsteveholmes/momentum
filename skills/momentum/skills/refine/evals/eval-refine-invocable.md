# Eval: Refine Skill — Independent Invocability and Backlog Presentation

## Setup
Invoke `/momentum:refine` directly (not through Impetus). Ensure `stories/index.json`
exists with at least one non-terminal story.

## Expected Behavior
1. The skill loads without error
2. The skill begins by reading `stories/index.json` to present the backlog
3. The skill does not require Impetus context, an active sprint, or any pre-existing
   sprint state to start
4. The backlog presentation groups stories by epic, excludes terminal states (done,
   dropped, closed-incomplete), and shows priority badge, status, dependency status,
   and story_file for each story
5. A summary header is shown: "N stories across M epics" with priority distribution
6. Stories within each epic are sorted: critical first, then high, medium, low;
   leaves (no unsatisfied dependencies) before stories with pending deps; alphabetical
   as tiebreaker
7. After presenting the backlog, the skill waits for the developer before proceeding
   to gap discovery
