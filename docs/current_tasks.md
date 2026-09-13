# Current Tasks

This checklist tracks active implementation work. Completed milestones and stable
scope belong in `milestone_status.md`; the longer learning sequence belongs in
`implementation-roadmap.md`.

## Milestone 2: Linear MNA assembly

### Assembly structure

- [x] Map non-ground nodes to deterministic matrix indices.
- [x] Map voltage sources to deterministic branch-current indices.
- [x] Assemble dense `A` and `b` arrays with the established unknown ordering.

### Element support

- [x] Stamp resistors into the dense matrix.
- [x] Stamp voltage sources into the dense matrix and right-hand side.
- [x] Stamp current sources into the right-hand side.
- [ ] Add stamps for the retained linear element groups.
- [ ] Decide which meter records should contribute to MNA and how they should be represented.
- [ ] Add capacitor and inductor MNA tests when their stamps are implemented.

### Verification

- [x] Test matrix values and unknown ordering.
- [x] Test source direction, sign conventions, and grounded terminals.
- [x] Reject unsupported element types explicitly.
- [ ] Add hand-assembled matrix comparisons for additional small circuits.
- [ ] Verify the complete small-circuit assembly target.

### Milestone tracking

- [ ] Confirm all required Milestone 2 element stamps are implemented.
- [ ] Confirm the dense `A` and `b` systems match hand-assembled references.
- [ ] Update `milestone_status.md` to mark Milestone 2 complete.

## Milestone 3: Linear solver

- [ ] Define the solver interface and numerical conventions.
- [ ] Implement forward and backward substitution.
- [ ] Implement dense LU factorization with partial pivoting.
- [ ] Detect singular or unusable pivots.
- [ ] Report residuals and compare against independent reference results.
