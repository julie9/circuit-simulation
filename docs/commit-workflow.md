# Commit Workflow

Use this as the coding agent's default workflow after completing a coherent
piece of work.

## Commit behavior

- Inspect `git status` and the diff before editing and before committing.
- Preserve unrelated user changes; never include them accidentally.
- Make a commit when the requested work is complete, unless the user asks not
  to commit.
- Keep each commit small, coherent, buildable, and easy to revert.
- Keep implementation with the focused tests that verify it.
- Keep unrelated parser, solver, viewer, and documentation work separate.
- Do not create branches or push unless the user asks.

## Commit messages

Use a short imperative subject, normally no more than 50 characters:

```text
Implement linear MNA assembly
```

Add a brief body only when the reason, constraint, or validation is not clear
from the diff. A body may mention the main test command and an intentional
scope limit. Do not write a body just to make the commit longer.

Good subjects start with a clear verb such as `Add`, `Implement`, `Fix`, or
`Document`. Avoid vague subjects such as `Changes`, `Update stuff`, or `Work
on phase 2`.

## Before finishing

1. Run the narrowest useful test, then the full suite when practical.
2. Review the staged diff and confirm only intended files are included.
3. Commit with the simple subject and optional short body.
4. Report the commit ID, subject, validation result, and any intentionally
   uncommitted files.

If Git author identity is missing, stop and ask the user to configure it. Never
guess an identity or handle credentials.
