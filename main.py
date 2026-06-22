"""Run a small terminal demonstration of the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def find_pet_name(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns a task."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "Unknown pet"


def main() -> None:
    """Create sample pet data and print today's schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(
        Task("Morning walk", "08:00", 30, "high", "daily", due_date=date.today())
    )
    luna.add_task(
        Task("Breakfast", "09:00", 10, "high", "daily", due_date=date.today())
    )
    luna.add_task(
        Task("Evening medicine", "18:00", 5, "high", "daily", due_date=date.today())
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    print(f"Today's Schedule for {owner.name}")
    print("-" * 29)
    for task in scheduler.get_tasks():
        pet_name = find_pet_name(owner, task)
        print(
            f"{task.time} - {pet_name}: {task.title} "
            f"({task.duration_minutes} min) [priority: {task.priority}]"
        )


if __name__ == "__main__":
    main()
