from algorithm import AlgorithmStep
from worker.communication import Instruction

import json

from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class BuildInternalResponseStep(AlgorithmStep):
    """
    Builds response of type ResponseType.INTERNAL
    """
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.RESULTBUILDING
        default_logger.log_progress_event(instruction, information=instruction.response_type.name)
        return json.dumps(data)
