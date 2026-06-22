"""Core class skeletons for the PawPal+ pet care system."""

from dataclasses import dataclass, field
from datetime import date


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
        raise NotImplementedError

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Filter tasks by optional pet name and completion status."""
        raise NotImplementedError

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks scheduled at the same time."""
        raise NotImplementedError
