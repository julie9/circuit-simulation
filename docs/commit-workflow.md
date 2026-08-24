# Commit Workflow

Use this workflow after completing a simulator phase or another coherent
feature. The goal is to keep history easy to review, bisect, and explain.

## Commit message rules

Write each commit message in this form:

```text
Short imperative subject

- State the implementation decision or behavior that changed.
- Explain the problem, constraint, or design reason behind that decision.
- Mention validation or an important scope boundary when useful.
```

Subject rules:

- Separate the subject from the body with one blank line.
- Keep the subject at 50 characters or fewer.
- Capitalize the subject.
- Use the imperative mood: `Add`, `Implement`, `Document`, `Fix`.
- Do not end the subject with a period.

The body should explain why the code was implemented this way. Reviewers can
read the patch to learn what changed; the body should preserve the reasoning
that is not obvious from the patch, such as an electrical convention, a
numerical stability choice, a compatibility constraint, or a rejected
alternative. Bullet-style body lines are preferred. Keep body lines reasonably
short for readable `git log` output.

Good subjects:

```text
Implement linear MNA assembly
Add transient capacitor history
Document diode Newton iteration
```

Avoid vague subjects:

```text
Changes
Update stuff
Work on phase 2.
```

## Split work into commits

After implementing a new phase:

1. Review `git status` and `git diff` before staging anything.
2. Keep unrelated user changes out of the commits.
3. Identify the smallest coherent responsibilities in the phase.
4. Group production code with the tests that verify it.
5. Commit documentation or project guidance separately when it has an
   independent purpose.
6. Put examples and fixtures with the feature they demonstrate.
7. Keep commits buildable and testable whenever practical.
8. Run the focused tests after each logical group, then run the full suite.
9. Review the staged diff and commit subjects before finishing.
10. Report the commit IDs, test result, and any files intentionally left out.

A typical phase may split like this:

```text
1. Define the phase's conventions and public data records
2. Implement the core algorithm and focused unit tests
3. Add integration behavior, examples, and end-to-end tests
4. Update status or learning documentation
```

Do not split a single bug fix across artificial commits just to increase the
count. Conversely, do not combine unrelated parser, solver, GUI, and document
changes when they can be reviewed independently.

## Agent request template

Use this request after finishing a phase:

```text
Review the current worktree and prepare commits for the completed phase.

- Preserve unrelated user changes.
- Split the work into the smallest coherent, testable commits.
- Keep production code with its focused tests.
- Use commit subjects of 50 characters or fewer, capitalized, imperative,
  and without a final period.
- Separate each subject from its body with one blank line.
- Use a bullet-style body explaining the implementation and why it was chosen.
- Review the staged diff before each commit.
- Run focused tests and then the full test suite.
- Do not push or create a branch unless explicitly requested.
- Report the commit IDs, subjects, tests, and final worktree status.
```

If author identity is not configured, stop before committing and ask the user
to configure the intended Git name and email. Never guess an identity.
