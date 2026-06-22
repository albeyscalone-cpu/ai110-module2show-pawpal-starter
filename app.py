from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def find_task_pet(owner: Owner, task: Task) -> Pet | None:
    """Return the pet that owns a task instance."""
    for pet in owner.pets:
        if any(saved_task is task for saved_task in pet.tasks):
            return pet
    return None


def build_task_rows(owner: Owner, tasks: list[Task]) -> list[dict[str, str]]:
    """Convert tasks into rows that are easy to read in Streamlit."""
    rows = []
    for task in tasks:
        pet = find_task_pet(owner, task)
        rows.append(
            {
                "Pet": pet.name if pet else "Unknown",
                "Date": task.due_date.isoformat() if task.due_date else "Not set",
                "Time": task.time,
                "Task": task.title,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority.title(),
                "Frequency": task.frequency.title(),
                "Status": "Complete" if task.completed else "Open",
            }
        )
    return rows


st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps owners keep their pets' daily care in one place. Add pets and
tasks below, then build a schedule from the saved information.
"""
)

with st.expander("About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

Tasks stay connected to each pet and are organized by the scheduling logic.
"""
    )

with st.expander("Scheduling rules", expanded=False):
    st.markdown(
        """
- Tasks are ordered by their scheduled time.
- Schedule results can be filtered by pet and completion status.
- Exact date-and-time conflicts produce a warning.
- Completing a daily or weekly task creates its next occurrence.
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name.strip() or "Pet owner"

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    clean_pet_name = pet_name.strip()
    pet_exists = any(pet.name.lower() == clean_pet_name.lower() for pet in owner.pets)
    if not clean_pet_name:
        st.warning("Enter a pet name first.")
    elif pet_exists:
        st.warning(f"{clean_pet_name} is already in your pet list.")
    else:
        owner.add_pet(Pet(clean_pet_name, species))
        st.success(f"Added {clean_pet_name}.")

if owner.pets:
    st.table([{"Pet": pet.name, "Species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet. Add one before scheduling a task.")

st.markdown("### Tasks")
st.caption("Choose a pet and add a care task to its saved task list.")

if owner.pets:
    selected_pet_name = st.selectbox("Pet for this task", [pet.name for pet in owner.pets])

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.time_input("Task time", value=time(8, 0))
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
        selected_pet.add_task(
            Task(
                task_title.strip() or "Untitled task",
                task_time.strftime("%H:%M"),
                int(duration),
                priority,
                frequency,
                due_date=date.today(),
            )
        )
        st.success(f"Added {task_title.strip() or 'Untitled task'} for {selected_pet.name}.")

scheduler = Scheduler(owner)
open_tasks = scheduler.filter_tasks(completed=False)

if open_tasks:
    st.markdown("### Complete a Task")
    selected_task_index = st.selectbox(
        "Choose an open task",
        range(len(open_tasks)),
        format_func=lambda index: (
            f"{find_task_pet(owner, open_tasks[index]).name}: "
            f"{open_tasks[index].time} - {open_tasks[index].title}"
        ),
    )
    task_to_complete = open_tasks[selected_task_index]
    if st.button("Mark complete"):
        task_pet = find_task_pet(owner, task_to_complete)
        next_task = scheduler.mark_task_complete(task_pet.name, task_to_complete)
        if next_task:
            st.success(
                f"Completed {task_to_complete.title}. The next occurrence is "
                f"{next_task.due_date}."
            )
        else:
            st.success(f"Completed {task_to_complete.title}.")

all_tasks = scheduler.sort_by_time(scheduler.get_tasks())
task_rows = build_task_rows(owner, all_tasks)

if task_rows:
    st.markdown("### Current Tasks")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Filter the saved tasks, then create a chronological schedule.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in owner.pets])
with filter_col2:
    status_filter = st.selectbox("Filter by status", ["Incomplete", "Completed", "All tasks"])

if st.button("Generate schedule"):
    selected_pet = None if pet_filter == "All pets" else pet_filter
    selected_status = {"Incomplete": False, "Completed": True, "All tasks": None}[
        status_filter
    ]
    scheduled_tasks = scheduler.sort_by_time(
        scheduler.filter_tasks(pet_name=selected_pet, completed=selected_status)
    )
    if scheduled_tasks:
        st.success(f"Schedule created with {len(scheduled_tasks)} task(s).")
        st.table(build_task_rows(owner, scheduled_tasks))

        conflict_warnings = scheduler.detect_conflicts(
            scheduler.filter_tasks(completed=False)
        )
        if conflict_warnings:
            for warning in conflict_warnings:
                st.warning(warning)
        else:
            st.info("No exact-time conflicts found.")
    else:
        st.warning("No tasks match the selected filters.")
