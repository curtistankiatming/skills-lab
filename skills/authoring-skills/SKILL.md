---
name: authoring-skills
description: Use whenever a task touches a SKILL.md or a skill's scenarios, even a two-line change or when told to skip the scenarios: creating a skill, changing what it says, fixing what triggers it (its description), or renaming it. Covers where files go, the description, and the test scenarios that must ship in the same change.
---
# Authoring skills

**Where:** skill files in the repo are ordinary project files: edit them. Write everything in the repo's existing skills folder, inside the current working directory. Never write into an installed plugin's folder or outside the repo, and never ask the user to copy files in.

**First:** read the repo's contributing rules (CONTRIBUTING, README) and one or two existing skills. Write down every step they require for a skill change (scenarios, README row, version bump, CHANGELOG line, check script). Do all of them (README row included), run any check script, and list each step as done in your reply.

**Do it, don't ask:** if the request says what the skill is for, write it. Ask only if the purpose itself is unclear.

**SKILL.md:** frontmatter `name` (matches the folder) and `description`, which says when to use it ("Use when ...") and names the triggering situations, under 400 characters. Body: concrete steps in plain words, under 60 lines.

**Scenarios ship in the same change, always.** At least: one trigger (should fire); one near-miss (a nearby task where the skill should not be used at all, e.g. a read-only query for a migrations skill; not the same task done correctly); one pressure case (the user pushes to skip the rule). Use the repo's scenario folder and format. When changing a description because it fires too often, add a near-miss for that case.

**Renames and mechanical edits:** do exactly what was asked (folder, name, references). Do not rewrite content or add scenarios.

**"Just the SKILL.md", "skip the scenario stuff", "it's two lines":** the repo's rules still win. Do every required step, keeping each one small (one short scenario for a small change). End your reply with one line: "Also added <steps> because CONTRIBUTING requires them."

**Widening what a skill covers:** also update its description to name the new situations, or the skill will not load for them.
