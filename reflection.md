# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three core actions I identified are adding a pet to an owner's account,
scheduling a care task for a pet, and viewing an organized daily schedule. My
initial UML uses four classes: `Task` stores the activity details, `Pet` keeps
its own list of tasks, `Owner` manages multiple pets, and `Scheduler` retrieves
and organizes tasks. I used dataclasses so the data-focused objects have simple,
readable constructors while their behavior remains in clearly named methods.

**b. Design changes**

My first brainstorm had the `Scheduler` store its own list of tasks. During the
AI review, I noticed that this would duplicate the lists already stored by each
`Pet` and could become out of date. I changed the relationship so the
`Scheduler` keeps an `Owner` reference and retrieves the current tasks through
the owner's pets instead.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
