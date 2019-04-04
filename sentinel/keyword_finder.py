from typing import List
import re

# TODO Improve using:
# https://github.com/scoder/acora
# https://github.com/vi3k6i5/flashtext


class KeywordFinder:
    def __init__(self, keywords: List[str]):
        self.keywords = keywords

    def match(self, text: str) -> List[str]:
        """Finds matches of observed keywords in the given text.

        Args:
            text (str): The text to match against.

        Returns:
            List[str]: Keywords matched.
        """
        text_without_punc = re.sub(r"[^\w\s]", "", text)
        queried_text = text_without_punc.split()
        matches = list()
        for keyword in self.keywords:
            for word in queried_text:
                if word == keyword:
                    matches.append(keyword)

        return matches
