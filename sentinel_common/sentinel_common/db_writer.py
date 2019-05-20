from uuid import uuid4
from datetime import datetime
import sentinel_common.db_models
from .mentions import Mention
from typing import Iterable, List, Tuple, Set
import re


def to_db_mention(
    mention: Mention, keyword: str, sentiment_score: int
) -> sentinel_common.db_models.Mention:
    return sentinel_common.db_models.Mention(
        keyword,
        str(uuid4()),
        author="authorPlaceholder",
        text=mention.text,
        date=mention.creation_date,
        sentimentScore=sentiment_score,
    )


def find_all_keywords(text: str, keywords: Set[str]) -> List[str]:
    text_without_punc = re.sub(r"[^\w\s]", "", text)
    queried_text = text_without_punc.split()
    found_words = [word for word in queried_text if word in keywords]

    return found_words


def save_to_db(
    mentionsWithScores: Iterable[Tuple[Mention, int]]
) -> List[sentinel_common.db_models.Mention]:
    """
    Write all items in the partition to the database. 
    Should be called with `mapPartitions`.
    """
    entities = list()
    keywords = set(
        [x.keyword for x in sentinel_common.db_models.Keyword.scan() if x.keyword]
    )
    for mention, score in mentionsWithScores:
        for keyword in find_all_keywords(mention.text, keywords):
            entity = to_db_mention(mention, keyword, score)
            entity.save()
            entities.append(entity)
    return entities
