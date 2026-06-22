# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three core actions I identified are adding a pet to an owner's account,
scheduling a care task for a pet, and viewing an organized daily schedule. My
initial UML uses four classes: `Task` stores the activity details, `Pet` keeps
its own list of tasks, `Owner` manages multiple pets, and `Scheduler` retrieves
and organizes tasks. I used dataclasses so the data-focused objects have simple,
readable constructors while their behavior remains in clearly named methods.

**b. Design changes**

My first brainstorm had the `Scheduler` store its own list of tasks. During the
AI review, I noticed that this would duplicate the lists already stored by each
`Pet` and could become out of date. I changed the relationship so the
`Scheduler` keeps an `Owner` reference and retrieves the current tasks through
the owner's pets instead.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler uses task time for chronological ordering and can narrow a plan by
pet or completion status. It also considers date and time together when looking
for conflicts, and frequency determines whether completion creates a task one
day or seven days later. Priority is stored and displayed so the owner can make
decisions, but time is the main ordering rule because the project focuses on a
daily schedule. I chose these constraints because they directly affect what an
owner needs to do now and which pet needs the care.

**b. Tradeoffs**

My conflict detector only flags tasks with the exact same date and start time; it
does not calculate whether their durations overlap. This keeps the warning logic
easy to understand and avoids pretending the app knows travel or transition
time between different pet activities. Exact matches catch the clearest
scheduling mistake, while interval overlap could be added in a later version.

---

## 3. AI Collaboration

**a. How you used AI**

I used Codex to brainstorm the UML, turn the skeleton into small implementations,
connect the classes to Streamlit, and draft focused tests. Multi-file editing was
most useful when recurrence required coordinated changes to the Scheduler, CLI,
and documentation. Concrete prompts about one method or phase were more useful
than broad requests to build the entire app. Separate phase conversations kept
the UML, implementation, UI, algorithms, and tests from becoming one oversized
change and gave me a clear point to review and commit each step.

**b. Judgment and verification**

I did not use a more complex suggestion to parse times into datetime objects and
calculate every duration overlap. Since the UI always saves zero-padded `HH:MM`
strings, a lambda string sort was easier to read and still produced the correct
order. I kept exact-slot conflict detection rather than presenting partial
overlaps as more accurate than they were. I verified the decision with the CLI,
pytest cases for different dates and times, and a headless Streamlit workflow.

---

## 4. Testing and Verification

**a. What you tested**

The seven automated tests cover marking a task complete, adding a task to a pet,
sorting out-of-order times, filtering by pet and status, daily recurrence,
same-slot conflict warnings, and an owner with no tasks. Sorting, recurrence,
and conflict detection are the scheduler's main algorithms, so regressions there
would change a daily plan. The empty-owner test matters because a new user starts
without pets or tasks and the app should not crash.

**b. Confidence**

My confidence is 4 out of 5 because all seven tests, the CLI demo, and the
headless UI workflow pass. I would next test malformed time strings, three tasks
in one slot, and tasks whose durations overlap even though their start times are
different. I would also test longer recurrence chains across month and year
boundaries.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the same classes power the CLI, tests, and Streamlit UI.
Keeping the logic out of `app.py` made each scheduling behavior easier to inspect
and verify.

**b. What you would improve**

I would add edit/delete actions, persistent storage beyond one browser session,
and duration-based overlap detection. I would also validate task times inside
the logic layer so callers besides Streamlit receive the same protection.

**c. Key takeaway**

My main takeaway is that being the lead architect means deciding boundaries and
verification steps, not merely accepting generated code. AI made each phase
faster, but the small commits, CLI output, and tests are what showed that the
pieces actually fit together.
