# observability/wiring/instrumented_pipeline.py
from observability.adapters.observed_planner import ObservedPlanner
from observability.adapters.observed_retriever import ObservedRetriever
from observability.adapters.observed_executor import ObservedExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import hashlib

TRACE_FILE_OUTPUT = Path("traces/pipeline.jsonl")
TRACE_FILE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
TOP_K = 4

def main():
    question = input("Question: ").strip()
    if not question:
        print("No question provided.")
        return
    
    uuid = datetime.now(timezone.utc).isoformat()
    trace_id = f"trace-{uuid}"
    query_hash = hashlib.sha256(question.encode()).hexdigest()
    
    observed_planner = ObservedPlanner()
    plan, planner_trace = observed_planner.plan(question=question, k=TOP_K)
    print("\n\nPlan generated:", plan)

    triggered = False
    if plan.steps:
        if plan.steps[0].action == "retrieve":
            triggered = True

    if triggered:
        observed_retriever = ObservedRetriever()
        _, retrieval_trace = observed_retriever.retrieve(question=question, triggered=triggered, k=TOP_K)
    
    observed_executor = ObservedExecutor()
    _, execution_trace = observed_executor.execute_trace_obsevability(plan=plan, wm=None, k=TOP_K)

    trace_summary = {
        "trace_id": trace_id,
        "input": {
            "query": question,
            "query_hash": query_hash
        },
        "planner": planner_trace,
        "retriever": retrieval_trace if triggered else {"triggered": False},
        "executor": execution_trace
    }

    with TRACE_FILE_OUTPUT.open("a") as f:
            f.write(json.dumps(trace_summary) + "\n")

if __name__ == "__main__":
    main()