"""JSON persistence helpers for PawPal+ owner data."""

import json
from datetime import date
from pathlib import Path

from pawpal_system import Owner, Pet, Task


def save_owner(owner: Owner, path: str | Path) -> None:
    """Save an owner, pets, and tasks to a JSON file."""
    data = {
        "name": owner.name,
        "preferences": owner.preferences,
        "pets": [
            {
                "name": pet.name,
                "species": pet.species,
                "tasks": [
                    {
                        "title": task.title,
                        "time": task.time,
                        "duration_minutes": task.duration_minutes,
                        "priority": task.priority,
                        "frequency": task.frequency,
                        "completed": task.completed,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                    }
                    for task in pet.tasks
                ],
            }
            for pet in owner.pets
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_owner(path: str | Path) -> Owner:
    """Load an owner, pets, and tasks from a JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    owner = Owner(data["name"], preferences=data.get("preferences", {}))

    for pet_data in data.get("pets", []):
        pet = Pet(pet_data["name"], pet_data["species"])
        for task_data in pet_data.get("tasks", []):
            due_date_text = task_data.get("due_date")
            pet.add_task(
                Task(
                    task_data["title"],
                    task_data["time"],
                    task_data["duration_minutes"],
                    task_data["priority"],
                    task_data.get("frequency", "once"),
                    task_data.get("completed", False),
                    date.fromisoformat(due_date_text) if due_date_text else None,
                )
            )
        owner.add_pet(pet)

    return owner
