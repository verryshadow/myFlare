import time

from algorithm import AlgorithmStep
from fhir import execute_fhir_query
from worker.communication import Instruction, ProcessingEvent
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class ExecuteFhirQueriesStep(AlgorithmStep):
    """
    Executes the FHIR Queries and yields the raw XML responses
    """
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        # Count number of queries and log the beginning of the execution
        instruction.state = ExecutionState.FHIREXECUTION
        query_count: int = count(data)
        executed_counter: int = 0
        callback.log_progress_event(instruction, information=f"{executed_counter}/{query_count}")

        # Iterate through CNF and execute one by one
        fhir_cnf_responses = []
        for fhir_disjunction in data:
            fhir_disjunction_res = []
            for query in fhir_disjunction:
                # Execute and put into disjunction list
                paged_query_result = execute_fhir_query(query)
                fhir_disjunction_res.append(paged_query_result)

                # Log
                executed_counter += 1
                callback.log_progress_event(instruction, information=f"{executed_counter}/{query_count}")
            # Add results of disjunction into the cnf list
            fhir_cnf_responses.append(fhir_disjunction_res)
        return fhir_cnf_responses


def count(nested_list) -> int:
    """
    Recursively counts elements of a list

    :param nested_list: list or element of the list to be counted
    :return: number of elements in list, or 1 if argument is not a list
    """
    if type(nested_list) == list:
        return sum(count(subitem) for subitem in nested_list)
    else:
        return 1
