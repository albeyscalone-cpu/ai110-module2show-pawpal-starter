# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

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
- Conflict: Morning walk and Breakfast are both scheduled for 2026-06-21 at 08:00.

Recurring Task
- Completed Morning walk; next occurrence: 2026-06-22
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

============================== 7 passed in 0.10s ==============================
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
