import json
import sys

from worker.communication import ProcessingEvent, Instruction


class LoggingCallback:
    def __init__(self, debug_call: callable, progress_call: callable):
        self.result: callable = debug_call
        self.progress: callable = progress_call

    def log_progress_event(self, instruction: Instruction, information: str = None):
        event = ProcessingEvent(instruction, information)
        self.progress(json.dumps(event.__dict__))

    def log_debug_event(self, instruction: Instruction, information: str = None):
        # TODO: Implement logging to file
        event = ProcessingEvent(instruction, information)


default_logger = LoggingCallback(print, lambda text: print(text, file=sys.stderr))
