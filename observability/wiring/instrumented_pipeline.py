# observability/wiring/instrumented_pipeline.py
from observability.adapters.observed_planner import ObservedPlanner
# from observability.adapters.observed_retriever import ObservedRetriever
from observability.adapters.observed_executor import ObservedExecutor
from observability.adapters.observed_evidence import ObservedEvidence
from observability.adapters.observed_generation import ObservedPolicyGeneration
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
    print("\nPlan Action: ", plan.steps[0].action)

    triggered = False
    if plan.steps:
        if plan.steps[0].action == "retrieve":
            triggered = True

    # if triggered:
    #     observed_retriever = ObservedRetriever()
    #     retrieval_results, retrieval_trace = observed_retriever.retrieve(question=question, triggered=triggered, k=TOP_K)

    
    
    observed_executor = ObservedExecutor()
    execution_result, execution_trace = observed_executor.execute_trace_obsevability(plan=plan, wm=None, k=TOP_K)
    # print(execution_result[0]["tool_result"])
    print("\nRetrieval Result:\n\tTop K: ", execution_result[0]["tool_result"]["k"] if plan.steps[0].action == 'retrieve' else execution_result[0]["tool_result"])
    print("\tMode: ", execution_result[0]["tool_result"]["mode"] if plan.steps[0].action == 'retrieve' else 'nan')
    print("\tReranked?: ", execution_result[0]["tool_result"]["reranked"] if plan.steps[0].action == 'retrieve' else 'nan')
    print("\tCandidate Pool Size: ", execution_result[0]["tool_result"]["candidate_pool_size"] if plan.steps[0].action == 'retrieve' else 'nan')
    
    observed_evidence = ObservedEvidence()
    chunks_for_evidence = execution_result[0].get("tool_result", {}).get("chunks", []) if plan.steps[0].action == 'retrieve' else []
    assessment, assessment_trace = observed_evidence.evidence_observability(
        question=question,
        retrieved_chunks=chunks_for_evidence,
        executor_decision=execution_result[0].get("action", "unknown")
    )
    print("\nEvidence Assessment:\n\tEvidence Present?: ", assessment.evidence_present)
    print("\tSufficiency: ", assessment.sufficiency)
    print("\tConflicting Sources Present?: ", assessment.conflicting_sources)
    print("\tRationale: ", assessment.rationale)

    observed_gen_policy = ObservedPolicyGeneration()
    policy_decision, policy_decision_trace = observed_gen_policy.decide_observability(question, assessment)
    print("\nPolicy Decision:\n\tDecision: ", policy_decision.decision)
    print("\tRationale: ", policy_decision.rationale)
    print("\tRefusal Code (if exist): ", policy_decision.refusal_code)
    print("\tHedge Code (if exist): ", policy_decision.hedge_code)

    trace_summary = {
        "trace_id": trace_id,
        "input": {
            "query": question,
            "query_hash": query_hash
        },
        "planner": planner_trace,
        # "retriever": retrieval_trace if triggered else {"triggered": False},
        "executor": execution_trace,
        "evidence": assessment_trace,
        "generation_policy_decision": policy_decision_trace,
    }

    with TRACE_FILE_OUTPUT.open("a") as f:
            f.write(json.dumps(trace_summary) + "\n")

if __name__ == "__main__":
    main()