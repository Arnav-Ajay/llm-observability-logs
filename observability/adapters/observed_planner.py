# observability/adapters/observed_planner.py
from llm_generation_control import planner, decision # type: ignore
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass
class ObservedPlanner:

    def plan(self, question: str, k: int = 4, wm=None, memory_signal=None) -> planner.Plan:
        uuid = datetime.now(timezone.utc).isoformat()
        retrieval_decision = decision.decide_retrieval(question=question)
        
        planner_instance = planner.Planner()
        plan = planner_instance.generate_plan(question, k=k, wm=wm, memory_signal={"force_retrieval": False})

        query_decision = None
        if plan.steps:
            query_decision = plan.steps[0].action

        planner_trace = {
            "span_id": f"planner-{uuid}",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "decision": query_decision,
            "confidence": retrieval_decision.confidence,
            "requires_external_evidence": retrieval_decision.requires_external_evidence
        }
        
        return plan, planner_trace