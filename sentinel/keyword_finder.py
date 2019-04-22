from typing import Iterable, Optional
import re


class KeywordFinder:
    def __init__(self, keywords: Optional[Iterable[str]] = None):
        self._keywords = set(keywords) if keywords is not None else set()

    def match(self, text: str) -> bool:
        """Finds matches of observed keywords in the given text.

        Args:
            text (str): The text to match against.

        Returns:
            List[str]: Keywords matched.
        """
        text_without_punc = re.sub(r"[^\w\s]", "", text)
        queried_text = text_without_punc.split()
        for word in queried_text:
            if word in self._keywords:
                return True

        return False
