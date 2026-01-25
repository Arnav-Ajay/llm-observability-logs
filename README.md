## `llm-observability-logs`

### Why this repository exists

Modern LLM systems fail in ways that are **not visible from outputs alone**.

An answer can be:

* fluent
* confident
* even correct

…and still represent a system failure.

This repository exists to answer a single operational question:

> **Given a model output, can we reconstruct the exact decision path that produced it — without rerunning the system?**

If the answer is no, the system is not observable.

---

## What this repository is *not*

* Not a RAG pipeline
* Not an agent framework
* Not a tracing UI
* Not an LLM-based explanation layer

All generation, retrieval, planning, and memory logic lives **upstream**.

This repository observes those systems without modifying them.

---

## Upstream systems (required context)

This observability layer instruments existing agent pipelines, including:

* **[`rag-minimal-control`](https://github.com/Arnav-Ajay/rag-minimal-control)**: Baseline end-to-end retrieval-augmented generation
* **[`agent-tool-retriever`](https://github.com/Arnav-Ajay/agent-tool-retriever)**: Explicit retrieval as a decision, not a default
* **[`agent-planner-executor`](https://github.com/Arnav-Ajay/agent-planner-executor)**: Separation of planning and execution responsibilities
* **[`agent-memory-systems`](https://github.com/Arnav-Ajay/agent-memory-systems)**: Episodic and semantic memory with persistence and decay
* **[`rag-failure-modes`](https://github.com/Arnav-Ajay/rag-failure-modes)**: Intentionally broken behaviors used as observability test cases

No logic from these systems is reimplemented here.

They are treated as **black-box dependencies**.

---

## Core principle

> **Observability is not logging more.
> Observability is logging the right boundaries.**

Each system layer is responsible for emitting **only the facts it owns**:

| Layer     | Emits                                 | Never Emits        |
| --------- | ------------------------------------- | ------------------ |
| Planner   | decisions, alternatives, reason codes | tool outputs       |
| Retriever | candidate IDs, scores, drops          | generated text     |
| Executor  | context usage, token budgets          | planner rationale  |
| Memory    | reads, writes, evictions              | planning decisions |

This preserves causal attribution.

---

## Trace model

All executions emit a **single structured trace**, written as JSONL.

A trace is sufficient to answer:

* Why retrieval occurred (or didn’t)
* Why specific evidence was selected
* Whether memory influenced the outcome
* Where failure entered the system

No trace requires replaying the model.

---

## Repository layout

* `observability/schema/`
  Canonical trace schema and field rationale

* `observability/adapters/`
  Wrappers around upstream components (planner, retriever, executor, memory)

* `observability/wiring/`
  Composition of an instrumented pipeline from unmodified dependencies

* `observability/replay/`
  Deterministic reconstruction of decision paths from traces

* `traces/`
  Captured executions (successes, failures, ambiguous cases)

* `postmortems/`
  Failure analyses grounded entirely in trace evidence

---

## Replay, not interpretation

This repository does **not** attempt to explain model reasoning.

Instead, it reconstructs **system behavior**:

* decisions taken
* alternatives rejected
* information accessed
* resources consumed

Replay tools operate on trace files only.
No models are invoked during analysis.

---

## Why this matters

Without observability:

* failures are anecdotal
* regressions are invisible
* correctness is inferred from vibes

With observability:

* failures are localizable
* responsibility is attributable
* systems become ownable

This repository turns opaque LLM pipelines into debuggable systems.

---

## Final invariant

If a system answer cannot be explained using **only a trace file**,
the system is not production-grade.

This repository enforces that constraint.

---