# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps an owner plan and track care tasks for
multiple pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks such as walks, feeding, meds, enrichment, and grooming.
- Consider constraints such as available time, priority, and owner preferences.
- Produce a daily plan and explain why it chose that plan.

This project designs the system first with UML, implements the logic in Python,
and then connects that logic to a Streamlit UI.

## Features

- Add multiple pets and keep their tasks in Streamlit session state.
- Record task time, duration, priority, due date, and once/daily/weekly frequency.
- Sort schedules chronologically and filter them by pet or completion status.
- Warn when incomplete tasks share the same date and start time.
- Complete tasks and automatically create the next daily or weekly occurrence.
- Build a priority-based plan for a limited amount of available care time.
- Save and load owner, pet, and task data with a local JSON file.
- Verify the backend independently through a CLI demo and automated tests.

The final architecture is documented in the
[Mermaid class diagram](diagrams/uml_final.mmd).

## Class Design

PawPal+ separates the Streamlit interface from the object-oriented scheduling
logic:

- `Task` stores one care item, including description, time, duration, priority,
  due date, frequency, and completion state. Its `mark_complete()` method marks
  the task finished.
- `Pet` stores a pet's name, species, and task list. It can add new tasks and
  return only incomplete tasks.
- `Owner` stores the owner's name, preferences, and pets. It can add pets and
  collect tasks across every pet.
- `Scheduler` works across the owner's pets. It sorts tasks, filters schedules,
  detects same-time conflicts, creates recurring follow-up tasks, and builds a
  priority plan for a time budget.
- `pawpal_storage.py` saves and reloads the owner graph as JSON so the app can
  persist data between runs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Run `python main.py` for a terminal-only demonstration.

## Sample Output

Run the CLI demo with `python main.py` to see the classes work together:

```text
$ python main.py
Today's Schedule for Jordan (Sorted by Time)
----------------------------------------------
08:00 - Mochi: Morning walk (30 min) [priority: high]
08:00 - Luna: Breakfast (10 min) [priority: medium]
12:00 - Luna: Medicine (5 min) [priority: high]
18:00 - Mochi: Dinner (10 min) [priority: medium]

Incomplete Tasks for Mochi
- 08:00 Morning walk
- 18:00 Dinner

Priority Plan (35 available minutes)
- 08:00 Mochi: Morning walk [high]
- 12:00 Luna: Medicine [high]

Conflict Warnings
- Conflict: Morning walk and Breakfast are both scheduled for 2026-07-15 at 08:00.

Recurring Task
- Completed Morning walk; next occurrence: 2026-07-16
```

## Testing PawPal+

The automated suite covers task completion and addition, chronological sorting,
pet/status filtering, daily recurrence, exact-time conflicts, an owner with no
tasks, priority planning with a time budget, and JSON persistence.

```bash
python -m pytest
```

```text
$ python -m pytest -p no:cacheprovider
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\AIClass\ai110-module2show-pawpal-starter-main
plugins: anyio-4.13.0
collected 9 items

tests\test_pawpal.py .........                                           [100%]

============================== 9 passed in 0.14s ==============================
```

**Confidence level:** 4/5 stars. The main scheduling behaviors are covered, but
future tests could check malformed time strings and partially overlapping tasks.

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders zero-padded `HH:MM` task times chronologically. |
| Filtering | `Scheduler.filter_tasks()` | Selects tasks by pet name, completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings for incomplete tasks in the same date and time slot. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Adds the next occurrence one day or seven days after a daily or weekly task. |
| Priority planning | `Scheduler.sort_by_priority_and_time()`, `Scheduler.build_daily_plan()` | Chooses high-priority tasks first while staying within the available minutes. |

## Persistence

The Streamlit sidebar has **Load data** and **Save data** buttons. Saving writes
the current owner, pets, and tasks to `pawpal_data.json` using
`pawpal_storage.py`. Loading rebuilds the same `Owner`, `Pet`, and `Task`
objects from that file. The JSON data file is ignored by Git because it is local
runtime data, not project source code.

## UI and Output Formatting

The app uses Streamlit sidebar controls, table output, status messages, and
warning callouts so the schedule is readable without extra dependencies. The
terminal demo uses clear headings and aligned task lines to show the same logic
outside the browser.

## Demo Walkthrough

1. Enter the owner's name, a pet name, and species, then select **Add pet**.
2. Choose that pet and enter a task title, time, duration, priority, due date,
   and frequency.
3. Select **Add task** to save a real `Task` object under the selected `Pet`.
4. Choose pet/status filters and select **Generate schedule** to see sorted rows
   plus any exact-time conflict warnings.
5. Enter available care minutes and select **Build priority plan** to pick the
   highest-value tasks that fit the time budget.
6. Select an open task and choose **Mark complete**. Daily and weekly tasks add
   their next dated occurrence automatically.
7. Use **Save data** before closing the app, then **Load data** later to restore
   the saved owner, pets, and tasks.

The same scheduler behavior is visible without a browser:

```text
Today's Schedule for Jordan (Sorted by Time)
08:00 - Mochi: Morning walk (30 min) [priority: high]
08:00 - Luna: Breakfast (10 min) [priority: medium]
12:00 - Luna: Medicine (5 min) [priority: high]
18:00 - Mochi: Dinner (10 min) [priority: medium]

Priority Plan (35 available minutes)
- 08:00 Mochi: Morning walk [high]
- 12:00 Luna: Medicine [high]

Conflict Warnings
- Conflict: Morning walk and Breakfast are both scheduled for 2026-07-15 at 08:00.
```
