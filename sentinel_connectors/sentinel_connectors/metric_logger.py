import threading
import time
import logging
from fluentmetrics import FluentMetric


class MetricLogger(object):
    def __init__(self, source: str):
        self.INTERVAL = 60
        self.hits_counter = AtomicCounter()
        self.data_counter = AtomicCounter()
        self._logger = logging.getLogger(MetricLogger.__name__)
        self._exit_event = threading.Event()
        self.metrics = (
            FluentMetric()
            .with_storage_resolution(60)
            .with_namespace("SentinelConnectors")
            .with_dimension("Source", source)
        )

    def start(self):
        self._logging_thread = threading.Thread(target=self._log_metrics, daemon=True)
        self._logging_thread.start()

    def _log_metrics(self):
        start_time = time.time()

        while not self._exit_event.is_set():
            self.metrics.count(MetricName="HitsCount", Value=self.hits_counter.reset())
            self.metrics.count(MetricName="DataCount", Value=self.data_counter.reset())

            self._exit_event.wait(
                self.INTERVAL - ((time.time() - start_time) % self.INTERVAL)
            )

    def increment_hits(self):
        self.hits_counter.increment()

    def increment_data(self):
        self.data_counter.increment()


class AtomicCounter:
    def __init__(self):
        self.value: int = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self.value += 1

        return self.value

    def reset(self) -> int:
        value = self.value
        with self._lock:
            self.value = 0
        return value
