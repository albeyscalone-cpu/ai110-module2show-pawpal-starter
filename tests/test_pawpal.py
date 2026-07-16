"""Automated tests for the PawPal+ core classes and scheduler."""

from datetime import date, timedelta

from pawpal_storage import load_owner, save_owner
from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_task_complete_changes_status():
    task = Task("Morning walk", "08:00", 30, "high")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "08:00", 30, "high")

    pet.add_task(task)

    assert pet.task_count() == 1


def test_sort_by_time_returns_chronological_tasks():
    scheduler = Scheduler(Owner("Jordan"))
    tasks = [
        Task("Dinner", "18:00", 10, "high"),
        Task("Morning walk", "08:00", 30, "high"),
        Task("Medicine", "12:00", 5, "high"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["08:00", "12:00", "18:00"]


def test_daily_task_completion_creates_tomorrows_task():
    today = date(2026, 6, 22)
    walk = Task("Morning walk", "08:00", 30, "high", "daily", due_date=today)
    pet = Pet("Mochi", "dog", [walk])
    scheduler = Scheduler(Owner("Jordan", [pet]))

    next_walk = scheduler.mark_task_complete("Mochi", walk)

    assert walk.completed is True
    assert next_walk is not None
    assert next_walk.due_date == today + timedelta(days=1)
    assert next_walk.completed is False
    assert next_walk in pet.tasks


def test_detect_conflicts_flags_only_matching_date_and_time():
    today = date(2026, 6, 22)
    walk = Task("Morning walk", "08:00", 30, "high", due_date=today)
    breakfast = Task("Breakfast", "08:00", 10, "high", due_date=today)
    tomorrow_walk = Task(
        "Tomorrow walk", "08:00", 30, "high", due_date=today + timedelta(days=1)
    )
    scheduler = Scheduler(Owner("Jordan"))

    warnings = scheduler.detect_conflicts([walk, breakfast, tomorrow_walk])

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Breakfast" in warnings[0]


def test_filter_tasks_by_pet_and_completion_status():
    completed_walk = Task("Morning walk", "08:00", 30, "high", completed=True)
    dinner = Task("Dinner", "18:00", 10, "high")
    breakfast = Task("Breakfast", "09:00", 10, "high")
    owner = Owner(
        "Jordan",
        [
            Pet("Mochi", "dog", [completed_walk, dinner]),
            Pet("Luna", "cat", [breakfast]),
        ],
    )
    scheduler = Scheduler(owner)

    results = scheduler.filter_tasks(pet_name="mochi", completed=False)

    assert results == [dinner]


def test_empty_scheduler_returns_empty_results():
    scheduler = Scheduler(Owner("Jordan"))

    assert scheduler.get_tasks() == []
    assert scheduler.sort_by_time([]) == []
    assert scheduler.filter_tasks() == []
    assert scheduler.detect_conflicts([]) == []


def test_daily_plan_uses_priority_and_available_minutes_across_pets():
    owner = Owner(
        "Jordan",
        [
            Pet(
                "Mochi",
                "dog",
                [
                    Task("Morning walk", "08:00", 30, "high"),
                    Task("Dinner", "18:00", 10, "medium"),
                ],
            ),
            Pet(
                "Luna",
                "cat",
                [
                    Task("Medicine", "12:00", 5, "high"),
                    Task("Breakfast", "09:00", 10, "medium"),
                ],
            ),
        ],
    )
    scheduler = Scheduler(owner)

    plan = scheduler.build_daily_plan(35)

    assert [task.title for task in plan] == ["Morning walk", "Medicine"]
    assert sum(task.duration_minutes for task in plan) == 35


def test_json_save_and_load_preserves_owner_data(tmp_path):
    due_date = date(2026, 6, 22)
    owner = Owner(
        "Jordan",
        [
            Pet(
                "Mochi",
                "dog",
                [Task("Morning walk", "08:00", 30, "high", "daily", True, due_date)],
            )
        ],
        {"quiet_hours": "21:00-07:00"},
    )
    data_file = tmp_path / "pawpal.json"

    save_owner(owner, data_file)
    loaded_owner = load_owner(data_file)

    assert loaded_owner == owner
