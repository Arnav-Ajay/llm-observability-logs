# observability/adapters/observed_retriever.py
from typing import Dict
from agent_memory_systems import tools # type: ignore
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

INPUT_PDF_DIR = Path("data/input_pdfs/")

@dataclass
class ObservedRetriever:
    def retrieve(self, question: str, k: int = 4, chunking_strategy: str = "fixed", enable_rerank: bool = False, triggered: bool = False) -> Dict:
        uuid = datetime.now(timezone.utc).isoformat()

        print("Retrieval started for query:", question)
        retrieval_decision = tools.retrieve_tool(question=question, k=k, pdf_dir=INPUT_PDF_DIR, chunking_strategy=chunking_strategy, enable_rerank=enable_rerank)    
        
        raw_scores = [
            chunk.get("score")
            for chunk in retrieval_decision.get("chunks", [])
            if chunk.get("score") is not None
        ]

        numeric_scores = [
            s for s in raw_scores
            if isinstance(s, (int, float))
        ]

        score_spread = None
        if len(numeric_scores) >= 2:
            sorted_scores = sorted(numeric_scores, reverse=True)
            score_spread = sorted_scores[0] - sorted_scores[1]


        retriever_trace = {
            "span_id": f"retriever-{uuid}",
            "triggered": triggered,
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "top_k": k,
            "top_k_chunk_ids": [chunk["chunk_id"] for chunk in retrieval_decision["chunks"] if chunk.get("chunk_id") is not None][:k],
            "top_k_chunk_scores": [chunk["score"] for chunk in retrieval_decision["chunks"] if chunk.get("score") is not None][:k],
            "score_spread":score_spread
        }
        
        return retrieval_decision, retriever_trace