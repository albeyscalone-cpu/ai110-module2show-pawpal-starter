# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps an owner plan and track care tasks for
multiple pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- Add multiple pets and keep their tasks in Streamlit session state.
- Record task time, duration, priority, and once/daily/weekly frequency.
- Sort schedules chronologically and filter them by pet or completion status.
- Warn when incomplete tasks share the same date and start time.
- Complete tasks and automatically create the next daily or weekly occurrence.
- Verify the backend independently through a CLI demo and automated tests.

The final architecture is documented in the
[Mermaid class diagram](diagrams/uml_final.mmd).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Run `python main.py` for a terminal-only demonstration.

## 🖥️ Sample Output

Run the CLI demo with `python main.py` to see the classes work together:

```text
$ python main.py
Today's Schedule for Jordan (Sorted by Time)
----------------------------------------------
08:00 - Mochi: Morning walk (30 min) [priority: high]
08:00 - Luna: Breakfast (10 min) [priority: high]
12:00 - Luna: Medicine (5 min) [priority: high]
18:00 - Mochi: Dinner (10 min) [priority: high]

Incomplete Tasks for Mochi
- 08:00 Morning walk
- 18:00 Dinner

Conflict Warnings
- Conflict: Morning walk and Breakfast are both scheduled for 2026-06-22 at 08:00.

Recurring Task
- Completed Morning walk; next occurrence: 2026-06-23
```

## 🧪 Testing PawPal+

The automated suite covers task completion and addition, chronological sorting,
pet/status filtering, daily recurrence, exact-time conflicts, and an owner with
no tasks.

```bash
python -m pytest
```

```text
$ python -m pytest -p no:cacheprovider
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\AIClass\ai110-module2show-pawpal-starter-main
plugins: anyio-4.13.0
collected 7 items

tests\test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.20s ==============================
```

**Confidence level:** 4/5 stars. The main scheduling behaviors are covered, but
future tests could check malformed time strings and partially overlapping tasks.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders zero-padded `HH:MM` task times chronologically. |
| Filtering | `Scheduler.filter_tasks()` | Selects tasks by pet name, completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warnings for incomplete tasks in the same date and time slot. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Adds the next occurrence one day or seven days after a daily or weekly task. |

## 📸 Demo Walkthrough

1. Enter the owner's name, a pet name, and species, then select **Add pet**.
2. Choose that pet and enter a task title, time, duration, priority, and frequency.
3. Select **Add task** to save a real `Task` object under the selected `Pet`.
4. Choose pet/status filters and select **Generate schedule** to see sorted rows
   plus any exact-time conflict warnings.
5. Select an open task and choose **Mark complete**. Daily and weekly tasks add
   their next dated occurrence automatically.

The same scheduler behavior is visible without a browser:

```text
Today's Schedule for Jordan (Sorted by Time)
08:00 - Mochi: Morning walk (30 min) [priority: high]
08:00 - Luna: Breakfast (10 min) [priority: high]
12:00 - Luna: Medicine (5 min) [priority: high]
18:00 - Mochi: Dinner (10 min) [priority: high]

Conflict Warnings
- Conflict: Morning walk and Breakfast are both scheduled for 2026-06-22 at 08:00.
```
