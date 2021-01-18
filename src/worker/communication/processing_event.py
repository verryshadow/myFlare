from worker.communication.instruction import ExecutionState


class ProcessingEvent:
    def __init__(self, timestamp_ns: int, instruction_id: str, state: ExecutionState):
        self.timestamp_ns: int = timestamp_ns
        self.instruction_id: str = instruction_id
        self.state: str = state.name
