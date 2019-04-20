from datetime import datetime
from .keyword_finder import KeywordFinder
from abc import ABC
from typing import Set
import threading
import time
import logging


class KeywordManager(ABC):
    def __init__(self, keyword_finder):
        self.keyword_finder = keyword_finder

    def any_match(self, text: str) -> bool:
        return self.keyword_finder.match(text)


class ConstKeywordManager(KeywordManager):
    def __init__(self, keywords):
        super().__init__(KeywordFinder(keywords))


class DynamicKeywordManager(KeywordManager):
    def __init__(self):
        super().__init__(KeywordFinder())
        self.SLEEP_TIME = 1
        self._current_keywords = set()
        self._logger = logging.getLogger(DynamicKeywordManager.__name__)
        self._exit_event = threading.Event()

    def run(self):
        self._update_thread = threading.Thread(
            target=self._update_keywords, daemon=True
        )
        self._update_thread.start()

    def exit(self):
        self._exit_event.set()
        self._update_thread.join()

    def _update_keywords(self):
        self.last_update = datetime.now()
        while not self._exit_event.is_set():
            new_keywords = self._get_keywords()
            if new_keywords != self._current_keywords:
                self._logger.info(f"Keywords update: {new_keywords}")
                self._current_keywords = new_keywords
                self.keyword_finder = KeywordFinder(new_keywords)

            self._wait_sleep()

    def _get_keywords(self) -> Set[str]:
        time.sleep(0.1)  # simulate redis / db call
        return set(["the"])

    def _wait_sleep(self):
        self._exit_event.wait(self.SLEEP_TIME)
