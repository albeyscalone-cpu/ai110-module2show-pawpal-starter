from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps owners keep their pets' daily care in one place. Add pets and
tasks below, then build a schedule from the saved information.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

    if st.button("Add task"):
        selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
        selected_pet.add_task(
            Task(
                task_title.strip() or "Untitled task",
                task_time.strftime("%H:%M"),
                int(duration),
                priority,
                due_date=date.today(),
            )
        )
        st.success(f"Added {task_title.strip() or 'Untitled task'} for {selected_pet.name}.")

task_rows = [
    {
        "Pet": pet.name,
        "Time": task.time,
        "Task": task.title,
        "Duration": f"{task.duration_minutes} min",
        "Priority": task.priority,
    }
    for pet in owner.pets
    for task in pet.tasks
]

if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Build a schedule from the tasks stored by your PawPal+ classes.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    scheduled_tasks = scheduler.get_tasks()
    if scheduled_tasks:
        st.success(f"Schedule created with {len(scheduled_tasks)} task(s).")
        st.table(task_rows)
    else:
        st.warning("Add at least one task before building a schedule.")
