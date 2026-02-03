# tools/trace/evidence_trace.py
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from llm_generation_control import evidence

@dataclass
class ObservedEvidence:

    def evidence_observability(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]],
        executor_decision: str = "retrieve",
    ):
        uuid = datetime.now(timezone.utc).isoformat()
        assessor = evidence.EvidenceAssessor()

        assessment = assessor.assess_evidence(
            query=question,
            retrieved_chunks=retrieved_chunks,
            executor_decision=executor_decision,
        )

        assessment_trace = {
            "span_id": f"evidence-{uuid}",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "evidence_present": assessment.evidence_present,
            "sufficiency": assessment.sufficiency,
            "max_similarity": assessment.max_similarity,
            "coverage_score": assessment.coverage_score,
            "conflicting_sources": assessment.conflicting_sources,
            "rationale": assessment.rationale,
        }

        return assessment, assessment_trace
