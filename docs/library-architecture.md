# Repository Patterns — architecture map

## Purpose

This repository helps a human or LLM move from a design question to a context-specific recommendation, supported by examples and explicit trade-offs.

## Level 1 — Context

**Purpose:** This section answers “Who uses this repository, and what does it provide?”

```mermaid
flowchart LR
    Reader[Human or LLM with a design question]
    Meta[Repository Patterns]
    Example[Documented source repositories]
    Target[Target repository being considered]
    Decision[Project-specific decision]

    Reader -->|searches by need| Meta
    Meta -->|grounds ideas in| Example
    Reader -->|compares against| Target
    Meta -->|supports, not decides| Decision
    Target -->|provides context for| Decision
```

- The repository provides ideas, vocabulary, and examples.
- The target project remains the authority for its own design.
- Examples are evidence for a pattern, not instructions to reproduce the example.

## Sections in this model

| Section | Purpose |
|---|---|
| Catalog | Find a candidate by need rather than browsing every document. |
| Patterns | Understand the mechanism, fit, costs, and failure modes. |
| Case studies | See the pattern in a real repository and distinguish observation from interpretation. |
| Adoption worksheets | Translate an idea into a bounded target-repository decision. |
| Templates | Keep future additions consistent without turning them into compliance rules. |

## Level 2 — Information layers

**Purpose:** This section answers “What does each documentation layer own?”

```mermaid
flowchart TB
    Hook[README and index\npurpose and navigation]
    Catalog[Catalog\nneeds and pattern selection]
    Patterns[Pattern pages\nmechanism and trade-offs]
    Cases[Case studies\nobserved evidence and limits]
    Adoption[Worksheets and decisions\ntarget-specific application]

    Hook --> Catalog
    Catalog --> Patterns
    Patterns --> Cases
    Cases --> Adoption
```

| Layer | Owns | Does not own |
|---|---|---|
| Hook | Purpose and reading path | Full pattern prose |
| Catalog | Need-to-pattern routing | Project decisions |
| Pattern | General recommendation and trade-offs | Claim that adoption is correct |
| Case study | Source-backed example and limits | Universal guidance |
| Adoption | Target-specific reasoning | Reusable pattern definition |

## Key flow

**Purpose:** This section answers “How should a reader use one pattern?”

```mermaid
sequenceDiagram
    actor Reader
    participant Catalog
    participant Pattern
    participant Case as Case study
    participant Target as Target repository
    participant Decision

    Reader->>Catalog: State the design need
    Catalog-->>Reader: Candidate patterns
    Reader->>Pattern: Read fit and trade-offs
    Reader->>Case: Inspect concrete evidence
    Reader->>Target: Compare current structure and constraints
    Reader->>Decision: Record smallest useful adoption
    Decision-->>Reader: Keep, adapt, defer, or reject
```

## Facts and inferences

- **Observed:** The repository separates catalog, patterns, case studies, templates, and adoption material.
- **Recommended:** A reader should inspect one pattern and one example before proposing adoption.
- **Inferred:** This structure should reduce cargo-cult copying because it puts fit and trade-offs beside the example.

## Level 3 — Discovery path for agents

**Purpose:** This section answers “How does an agent in another session find what it needs, starting from nothing but the repository root?”

```mermaid
flowchart LR
    Agents[AGENTS.md\nroot of discovery]
    Index[index\nmap and evidence pins]
    Catalog[catalog\nneed to pattern]
    Pattern[pattern page\nfrontmatter + body]
    Related[related patterns]
    Case[case study\nevidence]
    Worksheet[adoption worksheet]

    Agents --> Index --> Catalog --> Pattern
    Pattern --> Related --> Pattern
    Pattern --> Case --> Worksheet
```

| Mechanism | What it guarantees | Enforced by |
|---|---|---|
| Wiki links (`[[name]]`) | A reference names its target document, independent of folders | `scripts/check_docs.py`: every wiki link resolves, including headings |
| Unique file names | Each wiki link has exactly one target | `scripts/check_docs.py`: no duplicate basenames |
| Reachability from `AGENTS.md` | Following links from the root reaches every document | `scripts/check_docs.py`: no orphaned pages |
| Pattern frontmatter | An agent can scan every pattern's need without reading bodies | `scripts/check_docs.py`: `name`, `description`, `category` on every pattern |
| Catalog coverage | Every pattern is routable by need, under its category | `scripts/check_docs.py`: catalog and pattern index list every pattern |
| One pin per source repository | All evidence for a case study comes from one commit | `scripts/check_docs.py`: one ref per external repository, recorded in the index |

The checks have their own tests (`scripts/test_check_docs.py`), and CI runs both. See [[0002-wiki-links-and-discovery]] for the decision and [[0003-self-adoption]] for which patterns this repository applies to itself.

## How to explore this map

Start with [[catalog]], then choose one pattern. Ask for a focused dive into a pattern, a case study, or an adoption worksheet rather than loading the entire repository at once.
