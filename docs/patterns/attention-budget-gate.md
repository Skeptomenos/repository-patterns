---
name: attention-budget-gate
description: The tracker receives more than maintainers can review.
category: repository-operations-and-governance
---

# Attention-budget contribution gate

## Intent

Protect maintainer attention. Close new contributions by default, and grant rights through a lightweight approval that the repository records.

## Use when

- the tracker receives more issues and pull requests than maintainers can review;
- agents can generate plausible reports at volume;
- maintainers need to review on their own schedule.

## Small shape

```text
unknown author opens an issue or PR -> auto-close + comment + "untriaged" label
maintainers review the closed queue daily -> reopen worthwhile items
maintainer reply "lgtmi" (issues) or "lgtm" (issues and PRs) -> workflow updates a registry file
gates read the registry through the API and never check out contributor code
```

## Pi example

**Observed:** The root README opens with a banner: new issues and pull requests from new contributors are auto-closed. [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/CONTRIBUTING.md) explains the gate, a quality bar ("If it does not fit on one screen, it is too long"), and a blocking policy. Its FAQ says AI can help triage but "is not trusted to make final maintainer decisions".

**Observed:** [`issue-gate.yml`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/issue-gate.yml) reads `.github/APPROVED_CONTRIBUTORS` and labels closed issues `untriaged`. [`approve-contributor.yml`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/approve-contributor.yml#L33-L34) accepts `lgtm` or `lgtmi` at the start or end of a maintainer reply, and commits the registry change. `pr-gate.yml` runs on `pull_request_target` and does not check out pull request code. A triage workflow uses a watermark label to close untriaged issues in bulk.

**Observed (drift):** `CONTRIBUTING.md` mentions two issue templates. The repository has three. The approval parser is copied into three workflows.

**Inferred:** The registry file turns a social decision into reviewable, versioned data.

**Recommended:** Write the reason for the gate in the FAQ. The gate is easier to accept when its cost to maintainers is visible.

## Benefits

- Maintainers review on their schedule instead of the tracker's.
- Trusted contributors keep a fast path.
- Agent-generated volume does not reach the review queue directly.

## Trade-offs

- New contributors can feel unwelcome.
- Good reports can wait, especially over weekends.
- Workflow logic duplicated across files drifts.

## Poor fit signals

- The project needs to attract contributors more than it needs to filter them.
- Maintainers have enough capacity to triage in real time.

## Adoption questions

- How many new issues arrive per week, and how many are actionable?
- What does a first-time contributor need to do to be heard?
- Where is the approval recorded, and who can change it?

## Related patterns

- [[repository-as-operating-system|Repository as operating system]]
- [[declared-trust-boundary|Declared trust boundary]]
- [[multi-agent-safe-worktree|Multi-agent-safe working tree]]
