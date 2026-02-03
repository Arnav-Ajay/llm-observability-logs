# observability/adapters/observed_generation.py
from typing import Dict
from dataclasses import dataclass
from datetime import datetime, timezone
from llm_generation_control import generator
from llm_generation_control import evidence as ev
from llm_generation_control import policies

@dataclass
class ObservedPolicyGeneration:
    def decide_observability(self, question: str, evidence_summary: dict):
        uuid = datetime.now(timezone.utc).isoformat()
        evidence = ev.models.EvidenceAssessment(
            evidence_present=evidence_summary.evidence_present,
            sufficiency=evidence_summary.sufficiency,
            max_similarity=evidence_summary.max_similarity,
            coverage_score=evidence_summary.coverage_score,
            conflicting_sources=evidence_summary.conflicting_sources,
            rationale=evidence_summary.rationale
            )
        # Apply generation policy (no logic change)
        policy_decision = policies.GenerationPolicy().decide(
            evidence=evidence
        )

        if policy_decision.refusal_code:
            outcome = {
                "type": "refusal",
                "code": policy_decision.refusal_code,
            }
        elif policy_decision.hedge_code:
            outcome = {
                "type": "hedge",
                "code": policy_decision.hedge_code,
            }
        else:
            outcome = {
                "type": "allowed"
            }

        policy_decision_trace = {
            "span_id": f"generation-policy-{uuid}",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "decision": policy_decision.decision,
            "refusal_code": policy_decision.refusal_code,
            "hedge_code": policy_decision.hedge_code,
            "outcome": outcome["type"]
        }

        return policy_decision, policy_decision_trace
