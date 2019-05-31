from typing import Iterable, Optional
from acora import AcoraBuilder


class KeywordFinder:
    def __init__(self, keywords: Optional[Iterable[str]] = []):
        non_empty_keywords = []
        if keywords is not None:
            for w in keywords:
                if w.strip() != "":
                    non_empty_keywords.append(w)

        self._keywords = set(non_empty_keywords)

        if len(self._keywords) > 0:
            ac_builder = AcoraBuilder()
            ac_builder.update(keywords)
            self._finder = ac_builder.build()
        else:
            self._finder = None

    def match(self, text: str) -> bool:
        """Finds matches of observed keywords in the given text.

        Args:
            text (str): The text to match against.

        Returns:
            List[str]: Keywords matched.
        """
        if self._finder is not None:
            for _ in self._finder.finditer(text):
                return True

        return False
