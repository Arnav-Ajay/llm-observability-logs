from agent_memory_systems import planner, decision
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import hashlib

TRACE_FILE_OUTPUT = Path("traces/planner.jsonl")
TRACE_FILE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

@dataclass
class ObservedPlanner:

    def plan(self, question: str, k: int = 4, wm=None, memory_signal=None) -> planner.Plan:
        uuid = datetime.now(timezone.utc).isoformat()
        query_hash = hashlib.sha256(question.encode()).hexdigest()

        print("Planning started for query:", question)

        retrieval_decision = decision.decide_retrieval(question=question)
        print("Retrieval decision made:", retrieval_decision)
        
        planner_instance = planner.Planner()
        plan = planner_instance.generate_plan(question, k=k, wm=wm, memory_signal={"force_retrieval": False})
        print("Planning completed with result:", plan)

        query_decision = None
        if plan.steps:
            query_decision = plan.steps[0].action

        planner_trace = {
            "span_id": f"planner-{uuid}",
            "input": {
                "query": question,
                "query_hash": query_hash
            },
            "planner": {
                "ts_utc": datetime.now(timezone.utc).isoformat(),
                "decision": query_decision,
                "confidence": retrieval_decision.confidence,
                "requires_external_evidence": retrieval_decision.requires_external_evidence
            }
        }

        with TRACE_FILE_OUTPUT.open("a") as f:
            f.write(json.dumps(planner_trace) + "\n")
        
        return plan
    
if __name__ == "__main__":
    observed_planner = ObservedPlanner()
    sample_plan = observed_planner.plan(question="What is self attention according to attention is all you need?", k=4)
    print("Sample plan generated:", sample_plan)