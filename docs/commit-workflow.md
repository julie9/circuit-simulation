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

## Branch, publish, and open a PR

Use these steps when the user explicitly requests a branch and pull request.

1. Check `git status --short --branch`, recent history, and the configured
   remote before changing branches.
2. Create a descriptive branch from the current base, for example:

   ```text
   git switch -c feature/linear-mna-assembly
   ```

3. Commit the work in logical, independently understandable chunks. A small
   phase commonly uses:
   - implementation and package configuration;
   - focused tests;
   - documentation or project-status updates.
4. Run the focused tests, then the full suite, before publishing.
5. Push and set the upstream branch:

   ```text
   git push -u origin feature/linear-mna-assembly
   ```

6. Open the repository's compare URL for `main...<branch>` and create the PR.
   If the GitHub CLI is unavailable, use the URL printed by `git push` or the
   compare page in the browser. Authentication must already be available;
   never request or handle credentials in the agent.
7. Confirm the final branch is clean and report the branch, commit IDs, PR URL,
   test result, and any publication step blocked by authentication.

Keep the PR title specific and imperative. Keep the body short enough to scan,
but include the motivation, concrete changes, scope limits, validation, and
the next follow-up. Use this format:

```markdown
## Why

<problem, motivation, or milestone goal>

## What changed

- <implementation change>
- <test or interface change>
- <documentation or configuration change>

## Scope

<important deferred behavior or known limitation>

## Validation

- `<focused command>`: <result>
- `<full command>`: <result>

## Follow-up

<next small milestone or intentionally deferred work>
```

Do not add generic sections such as screenshots, deployment, rollback, or
checklists unless they are relevant to the change. Do not claim that a PR was
created when the browser or CLI is unauthenticated; provide the ready compare
URL and the prepared description instead.

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

When branch and PR publication are requested, append:

```text
- Create a descriptive feature branch from the current base.
- Split the work into implementation, focused tests, and documentation
   commits when those responsibilities are independently reviewable.
- Run focused tests and then the full suite before pushing.
- Push with upstream tracking and open the compare URL for a PR.
- Use the Why / What changed / Scope / Validation / Follow-up PR format.
- If authentication blocks PR creation, do not handle credentials; report the
   compare URL and prepared description.
```

If author identity is not configured, stop before committing and ask the user
to configure the intended Git name and email. Never guess an identity.
