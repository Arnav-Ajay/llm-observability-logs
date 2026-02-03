### `llm-observability-logs`

## Why this repository exists

Modern AI systems fail long **before** they produce an answer.

Failures often originate in:

* planning decisions
* retrieval gating
* evidence assessment
* policy-triggered non-actions

These failures are **invisible at the output layer** — and in many systems, outputs may not exist at all.

This repository exists to answer a stricter operational question:

> **Given a system execution, can we reconstruct *every decision that occurred* — and every decision that could not have occurred — without rerunning the system?**

If the answer is no, the system is not observable.

---

## What this repository is *not*

* Not a RAG pipeline
* Not an agent framework
* Not an LLM execution layer
* Not a tracing UI or dashboard

This repository does **not** generate answers.

It observes **decision-making boundaries** in upstream systems, without modifying their behavior.

---

## Upstream systems (required context)

This observability layer instruments existing pipelines, including:

* [**`rag-minimal-control`**](https://github.com/Arnav-Ajay/rag-minimal-control) — baseline retrieval-augmented execution
* [**`agent-tool-retriever`**](https://github.com/Arnav-Ajay/agent-tool-retriever) — retrieval as an explicit decision
* [**`agent-planner-executor`**](https://github.com/Arnav-Ajay/agent-planner-executor) — separation of planning and execution
* [**`agent-memory-systems`**](https://github.com/Arnav-Ajay/agent-memory-systems) — memory architecture *without runtime participation*
* [**`llm-generation-control`**](https://github.com/Arnav-Ajay/llm-generation-control) — generation gating and refusal policy *without text execution*
* [**`rag-failure-modes`**](https://github.com/Arnav-Ajay/rag-failure-modes) — controlled failure probes

No logic from these systems is reimplemented here.

They are treated as **black-box dependencies**.

---

## Core principle

> **Observability is not logging more.
> Observability is making agency explicit.**

Only components that possess **independent decision power** are instrumented.

If a component has no agency, its absence is recorded — not simulated.

---

## What is currently observable (and what is not)

| Layer               | Status  | Observable signal                    |
| ------------------- | ------- | ------------------------------------ |
| Planner             | Active  | Decisions, confidence, gating        |
| Retriever           | Active  | Evidence selection, score separation |
| Executor            | Passive | Execution mode, context usage        |
| Evidence Assessment | Active  | Sufficiency, coverage, conflicts     |
| Generation Policy   | Active  | Allow / Hedge / Refuse               |
| Generation          | Absent  | No text or tokens logged             |
| Memory              | Absent  | Explicitly non-participating         |

Absence is treated as a **first-class system fact**, not a missing feature.

---

## Trace model

Each execution emits **one unified trace**, written as JSONL.

The trace answers:

* Why retrieval occurred or was skipped
* Whether evidence separation was strong or ambiguous
* Whether evidence was sufficient to support generation
* Why generation was allowed, hedged, or refused
* Which behaviors were impossible by design

The trace observes generation **decisions**, but never generation **outputs**, memory effects, or retries.

---

## Repository layout (interpretation matters)

* `observability/adapters/`
  Instrumentation for components with real agency
  *(empty adapters indicate intentional absence)*

* `observability/wiring/`
  Pipeline-level observability orchestration

* `observability/schema/`
  Declared trace contracts and field rationale

* `observability/replay/`
  Reserved for future systems with divergent outcomes

* `postmortems/`
  Reserved for failures that actually occur

This layout reflects **system maturity**, not ambition.

---

## Replay vs interpretation

This repository does **not** explain reasoning.

It reconstructs **system behavior**:

* decisions taken
* actions gated
* components bypassed
* capabilities absent

Replay operates on trace files only.
No models are invoked during analysis.

---

## Why this matters

Without decision-level observability:

* failures are attributed to “model behavior”
* regressions are undetectable
* systems cannot be owned responsibly

With observability:

* responsibility is localizable
* absence is provable
* future complexity compounds safely

This repository establishes observability **before intelligence**, not after.

---

## Final invariant

If a system’s behavior cannot be explained using **only its trace** —
including why certain behaviors were impossible —
the system is not production-grade.

This repository enforces that constraint.

---