"""Core domain classes and scheduling logic for PawPal+."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta


@dataclass
class Task:
    """Represent one scheduled pet care activity."""

    title: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str = "once"
    completed: bool = False
    due_date: date | None = None

    def mark_complete(self) -> None:
        """Mark this task complete."""
        self.completed = True


@dataclass
class Pet:
    """Store a pet's details and care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)


@dataclass
class Owner:
    """Manage an owner's pets and preferences."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return tasks belonging to all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """Organize and inspect tasks retrieved through an owner."""

    owner: Owner

    def get_tasks(self) -> list[Task]:
        """Retrieve the current tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduled time."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Filter tasks by optional pet name and completion status."""
        pets = self.owner.pets
        if pet_name is not None:
            pets = [pet for pet in pets if pet.name.lower() == pet_name.lower()]

        tasks = [task for pet in pets for task in pet.tasks]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks scheduled at the same time."""
        occupied_slots: dict[tuple[date | None, str], Task] = {}
        warnings: list[str] = []

        for task in self.sort_by_time(tasks):
            if task.completed:
                continue

            slot = (task.due_date, task.time)
            if slot in occupied_slots:
                first_task = occupied_slots[slot]
                date_label = (
                    task.due_date.isoformat() if task.due_date else "the same day"
                )
                warnings.append(
                    f"Conflict: {first_task.title} and {task.title} are both "
                    f"scheduled for {date_label} at {task.time}."
                )
            else:
                occupied_slots[slot] = task

        return warnings

    def mark_task_complete(self, pet_name: str, task: Task) -> Task | None:
        """Complete a task and add its next daily or weekly occurrence."""
        pet = next(
            (pet for pet in self.owner.pets if pet.name.lower() == pet_name.lower()),
            None,
        )
        if pet is None or not any(saved_task is task for saved_task in pet.tasks):
            raise ValueError("Task does not belong to the selected pet.")

        if task.completed:
            return None

        task.mark_complete()
        repeat_days = {"daily": 1, "weekly": 7}.get(task.frequency.lower())
        if repeat_days is None:
            return None

        next_task = replace(
            task,
            completed=False,
            due_date=(task.due_date or date.today()) + timedelta(days=repeat_days),
        )
        pet.add_task(next_task)
        return next_task
