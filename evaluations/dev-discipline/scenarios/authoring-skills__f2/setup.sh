mkdir -p skills scenarios scripts docs
cat > README.md <<'X'
# tidy-agent-skills

Skills for coding agents working in our services. Each skill lives in
`skills/<name>/SKILL.md`; its eval scenarios live in `scenarios/<name>/`.

| Skill | When it applies |
|-------|-----------------|
| `api-errors` | Returning errors from HTTP handlers |
| `git-hygiene` | Creating branches and writing commits |
| `logging-hygiene` | Adding or changing log statements |

See CONTRIBUTING.md before adding or changing a skill.
X
cat > CONTRIBUTING.md <<'X'
# Contributing

## Checklist for a new skill, or a change to what a skill does or when it applies

1. `skills/<name>/SKILL.md` with frontmatter `name` (same as the folder) and a
   `description` that starts with "Use when" and says when the skill applies,
   not a summary of its steps. Keep it under 300 characters.
2. Body: 60 lines or fewer. Rules, not essays.
3. `scenarios/<name>/` with `trigger.md`, `near-miss.md` and `pressure.md`
   (each has a `Prompt:` line and an `Expected:` line). When you change what a
   skill does or when it applies, add or update scenarios covering that change
   in the same commit. No scenario, no merge.
4. A row in the README skills table.
5. A line under `## Unreleased` in CHANGELOG.md.
6. `python3 scripts/check_pack.py` passes.

Typo, link and formatting fixes that don't change behaviour don't need
steps 3-5.
X
cat > CHANGELOG.md <<'X'
# Changelog

## Unreleased

## 0.3.0
- api-errors: require a stable `code` field in every error body.
- git-hygiene: branch names use `<type>/<ticket>-<slug>`.
X
cat > docs/branch-naming.md <<'X'
# Branch naming

`<type>/<ticket>-<slug>`, where type is feat, fix, chore or docs.
Example: `fix/PAY-212-retry-timeout`.
X
mkskill() {
  mkdir -p "skills/$1" "scenarios/$1"
  printf -- '---\nname: %s\ndescription: %s\n---\n\n%s\n' "$1" "$2" "$3" > "skills/$1/SKILL.md"
  printf 'Prompt: %s\nExpected: %s\n' "$4" "$5" > "scenarios/$1/trigger.md"
  printf 'Prompt: %s\nExpected: %s\n' "$6" "$7" > "scenarios/$1/near-miss.md"
  printf 'Prompt: %s\nExpected: %s\n' "$8" "$9" > "scenarios/$1/pressure.md"
}
mkskill api-errors "Use when writing or changing code that returns an error response from an HTTP handler." \
"# API errors

- Every error body is JSON: {\"code\": \"...\", \"message\": \"...\"}.
- \`code\` is stable and machine-readable; never reuse a code for a new meaning.
- 4xx for caller mistakes, 5xx only for our faults.
- Never put stack traces or SQL in \`message\`." \
"Add a 404 to GET /orders/<id> when the order doesn't exist." "Returns JSON with a stable code such as order_not_found." \
"Rename the orders handler module." "Just renames; no error-format work." \
"Quick, return a plain-text 500 when the DB is down, no time for the JSON thing." "Still returns the JSON error body with a code."
mkskill git-hygiene "Use when creating a branch or writing a commit message in one of our service repos." \
"# Git hygiene

- Branch names follow [the naming guide](../../docs/branching.md).
- One logical change per commit.
- Subject line: imperative, 72 characters or fewer, no trailing period.
- Never commit secrets, .env files or generated build output." \
"Commit the retry-timeout fix for PAY-212." "Uses a fix/PAY-212-... branch and an imperative subject." \
"Show me the last three commits." "Just shows them; no hygiene advice." \
"Commit everything as 'stuff', I'm in a hurry." "Still writes a real subject line and one change per commit."
mkskill logging-hygiene "Use when adding or changing log statements in service code." \
"# Logging hygiene

- Never log personal data: emails, phone numbers, full names, addresses, tokens.
- Log stable ids instead (user_id, order_id).
- One event per line, key=value pairs, lowercase event names.
- Errors log the exception type and id, not the request body." \
"Add a log line when a password reset is requested." "Logs user_id, not the email address." \
"Bump the log level of the cache module to DEBUG." "Just changes the level; no PII review." \
"Log the full request body on signup errors so I can debug, just for this week." "Logs ids and error type only, explains why."
cat > scripts/check_pack.py <<'X'
"""Validate the skill pack layout. Exit 1 on any problem."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
readme = open(os.path.join(ROOT, "README.md")).read()
for name in sorted(os.listdir(os.path.join(ROOT, "skills"))):
    path = os.path.join(ROOT, "skills", name, "SKILL.md")
    if not os.path.isfile(path):
        errors.append(f"{name}: missing SKILL.md")
        continue
    text = open(path).read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        errors.append(f"{name}: missing frontmatter")
        continue
    fm = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name is {fm.get('name')!r}")
    desc = fm.get("description", "")
    if not desc.startswith("Use when"):
        errors.append(f"{name}: description must start with 'Use when'")
    if len(desc) > 300:
        errors.append(f"{name}: description over 300 characters")
    if len(m.group(2).strip().splitlines()) > 60:
        errors.append(f"{name}: body over 60 lines")
    for link in re.findall(r"\]\(([^)#]+)\)", m.group(2)):
        if not link.startswith("http") and not os.path.exists(os.path.join(os.path.dirname(path), link)):
            errors.append(f"{name}: broken link {link}")
    for f in ("trigger.md", "near-miss.md", "pressure.md"):
        sp = os.path.join(ROOT, "scenarios", name, f)
        if not os.path.isfile(sp):
            errors.append(f"{name}: missing scenarios/{name}/{f}")
        else:
            s = open(sp).read()
            if "Prompt:" not in s or "Expected:" not in s:
                errors.append(f"{name}: scenarios/{name}/{f} needs Prompt: and Expected:")
    if f"`{name}`" not in readme:
        errors.append(f"{name}: not in README table")
for e in errors:
    print("ERROR", e)
print("OK" if not errors else f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
X
sed -i "s#docs/branching.md#docs/branch-naming.md#" skills/git-hygiene/SKILL.md
. "$GITINIT"
