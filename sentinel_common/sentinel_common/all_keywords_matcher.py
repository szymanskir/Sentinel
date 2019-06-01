import re
from typing import Set, List
from nltk.tokenize import MWETokenizer


class AllKeywordsMatcher:
    def __init__(self, keywords: Set[str]):
        keywords_tuples = [tuple(k.split()) for k in keywords]
        self.keywords = keywords
        self._mwe_tokenizer = MWETokenizer(keywords_tuples, separator=" ")
        self._punc_regex = re.compile(r"[^\w\s]")

    def all_occurring_keywords(self, text: str) -> List[str]:
        text_without_punc = self._punc_regex.sub("", text)
        queried_text = self._mwe_tokenizer.tokenize(text_without_punc.split())
        found_words = [word for word in queried_text if word in self.keywords]

        return found_words
