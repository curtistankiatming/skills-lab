---
name: designing-before-building
description: Use before building a feature or changing existing behaviour when there are real choices to make, including changes that sound small but touch existing behaviour (soft delete, permissions, money, currencies, recurring items, notifications), and even when the user says to skip the design.
---
# Design before building

A change built on the wrong choice is expensive to undo. Agree the shape first.

1. Read the code the change touches.
2. List what else reads, lists, counts, searches, validates or bills this data. (Soft delete: do deleted items still count, show in search, or block a reused name?)
3. Reply with a short design, about 15 lines at most: the goal in one sentence; the 2-4 decisions that matter, each with your recommendation and one alternative; the interactions from step 2 and how you would handle them; what you will build first.
4. Ask the person to confirm. Do not edit code until they agree.

**"Skip the design, just build it":** build only the parts that do not depend on an open choice. Start your reply with the one or two choices you could not safely default, as questions. For money, fees and limits, always ask where the numbers come from (which exchange rates, from where, how often). Never invent data the person must supply: rates, prices, limits, thresholds, addresses.

**Skip this skill** for changes with one obvious implementation and no effect on other behaviour (a `__repr__`, a renamed variable, a clearer message).
