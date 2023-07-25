from threading import Thread

from worker.communication import ProcessingEvent
from queue import Queue


class QueueDistributor(Thread):
    def __init__(self, event_queue: 'Queue[ProcessingEvent]', queue_consumers: 'list[Queue[ProcessingEvent]]'):
        super().__init__()
        self.event_queue = event_queue
        self.queue_consumers = queue_consumers

    def run(self) -> None:
        while True:
            event = self.event_queue.get(block=True)
            for consumer in self.queue_consumers:
                consumer.put(event)
