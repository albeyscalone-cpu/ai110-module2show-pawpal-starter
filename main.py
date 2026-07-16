"""Run a small terminal demonstration of the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def find_pet_name(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns a task."""
    for pet in owner.pets:
        if any(saved_task is task for saved_task in pet.tasks):
            return pet.name
    return "Unknown pet"


def main() -> None:
    """Create sample pet data and print today's schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    today = date.today()
    dinner = Task("Dinner", "18:00", 10, "medium", "daily", due_date=today)
    morning_walk = Task("Morning walk", "08:00", 30, "high", "daily", due_date=today)
    medicine = Task("Medicine", "12:00", 5, "high", "daily", due_date=today)
    breakfast = Task("Breakfast", "08:00", 10, "medium", "daily", due_date=today)

    # Add tasks out of order so the sorted output is easy to verify.
    mochi.add_task(dinner)
    mochi.add_task(morning_walk)
    luna.add_task(medicine)
    luna.add_task(breakfast)

    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    print(f"Today's Schedule for {owner.name} (Sorted by Time)")
    print("-" * 46)
    for task in scheduler.sort_by_time(scheduler.get_tasks()):
        pet_name = find_pet_name(owner, task)
        print(
            f"{task.time} - {pet_name}: {task.title} "
            f"({task.duration_minutes} min) [priority: {task.priority}]"
        )

    print("\nIncomplete Tasks for Mochi")
    for task in scheduler.sort_by_time(
        scheduler.filter_tasks(pet_name="Mochi", completed=False)
    ):
        print(f"- {task.time} {task.title}")

    print("\nPriority Plan (35 available minutes)")
    for task in scheduler.build_daily_plan(35):
        pet_name = find_pet_name(owner, task)
        print(f"- {task.time} {pet_name}: {task.title} [{task.priority}]")

    print("\nConflict Warnings")
    for warning in scheduler.detect_conflicts(scheduler.get_tasks()):
        print(f"- {warning}")

    next_walk = scheduler.mark_task_complete("Mochi", morning_walk)
    print("\nRecurring Task")
    print(f"- Completed Morning walk; next occurrence: {next_walk.due_date}")


if __name__ == "__main__":
    main()
