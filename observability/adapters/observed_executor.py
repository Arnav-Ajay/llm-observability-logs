# observability/adapters/observed_executor.py
from agent_memory_systems import executor, tools # type: ignore
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass
class ObservedExecutor:

    def execute_trace_obsevability(self, plan, k, wm=None):
        uuid = datetime.now(timezone.utc).isoformat()
        executor_instance = executor.Executor()
        execution_result = executor_instance.execute(plan, wm=wm)
        execution_trace = {
            "span_id": f"planner-{uuid}",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "mode": execution_result[0].get("action", "unknown"),
            "token_budget": 1000
        }
        
        return execution_result, execution_trace