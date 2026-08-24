from tracecalib.instrumentation.schema import Stage, TraceEvent


def test_trace_event_minimal() -> None:
    event = TraceEvent(
        run_id="run-1",
        step_id=0,
        progress=0.25,
        stage=Stage.SPECIFICATION,
        event_type="model_response",
        agent_id="mini_swe_agent",
        model_id="Qwen/Qwen3-8B",
        provider="local",
        task_id="task-1",
        uncertainty={"specification": 0.4},
    )
    assert event.progress == 0.25
    assert event.stage is Stage.SPECIFICATION
