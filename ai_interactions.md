# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Codex to work through the PawPal+ phases incrementally as if I were a
student completing the project. The main agent-mode tasks were to create the UML
design, implement the OOP classes, connect them to Streamlit, add scheduling
algorithms, add tests, and then compare the final project against the rubric.

**What did the agent do?**

The agent edited `pawpal_system.py`, `main.py`, `app.py`, `tests/test_pawpal.py`,
`diagrams/uml_final.mmd`, `README.md`, and `reflection.md`. It also added
`pawpal_storage.py` for JSON persistence and updated `.gitignore` so local saved
data is not committed. The agent ran the CLI demo, pytest, and a headless
Streamlit workflow during the phase work, then made separate commits after each
major phase.

**What did you have to verify or fix manually?**

I had to review the scope at each phase so the project looked like steady class
work instead of one giant generated change. I also checked that the final design
still matched the UML and rubric. One important correction was rejecting overly
complex duration-overlap logic for this version because the app only promises
same-time conflict warnings. Another correction was asking for rubric cleanup
after the phases so persistence, priority planning, and the AI comparison were
documented clearly.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Codex, broad all-at-once prompt | Codex, phase-by-phase prompts |
| **Prompt** | "Build the PawPal+ project from the instructions." | "Complete the current phase, stop, commit, and wait for the next phase." |
| **Response summary** | Suggested many pieces at once: classes, UI, tests, algorithms, and documentation. | Produced smaller changes focused on one project milestone at a time. |
| **What was useful** | Good for seeing the full project shape and possible stretch ideas. | Easier to review, easier to test, and matched the class workflow more closely. |
| **Problems noticed** | Too much could change at once, which makes debugging and realistic commit history harder. | Needed more prompts from me, and some later rubric details still required a final cleanup pass. |
| **Decision** | I did not use this as the final workflow. | I used this workflow for the final implementation. |

**Which approach did you use in your final implementation and why?**

I used Option B because phase-sized prompts kept the code, tests, documentation,
and commits easier to understand. The broad prompt was useful for brainstorming,
but the phase-by-phase workflow gave me better control over design decisions and
verification.
