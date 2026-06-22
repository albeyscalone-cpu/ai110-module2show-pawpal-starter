"""Starter tests for the PawPal+ core classes."""

from pawpal_system import Pet, Task


def test_mark_task_complete_changes_status():
    task = Task("Morning walk", "08:00", 30, "high")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "08:00", 30, "high")

    pet.add_task(task)

    assert pet.task_count() == 1
