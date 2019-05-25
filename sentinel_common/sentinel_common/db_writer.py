from uuid import uuid4
from datetime import datetime
from .db_models import MentionDb, KeywordDb
from .mentions import Mention
from typing import Iterable, List, Tuple, Set
import re

AUTHOR_MAP = {
    "google-news": lambda x: x.metadata.news_source,
    "hacker-news": lambda x: x.metadata.author,
    "reddit": lambda x: x.metadata.redditor,
    "twitter": lambda x: str(x.metadata.user_id),
}


def to_db_mention(mention: Mention, keyword: str, sentiment_score: int) -> MentionDb:
    return MentionDb(
        AUTHOR_MAP[mention.source](mention),
        mention.origin_date,
        keyword=keyword,
        id=str(mention.id),
        download_date=mention.download_date,
        text=mention.text,
        url=mention.url,
        source=mention.source,
        sentiment_score=sentiment_score,
        metadata=mention.metadata.json(),
    )


def find_all_keywords(text: str, keywords: Set[str]) -> List[str]:
    text_without_punc = re.sub(r"[^\w\s]", "", text)
    queried_text = text_without_punc.split()
    found_words = [word for word in queried_text if word in keywords]

    return found_words


def save_to_db(mentionsWithScores: Iterable[Tuple[Mention, int]]) -> List[MentionDb]:
    """
    Write all items in the partition to the database. 
    Should be called with `mapPartitions`.
    """
    entities = list()
    keywords = set([x.keyword for x in KeywordDb.scan() if x.keyword])
    for mention, score in mentionsWithScores:
        for keyword in find_all_keywords(mention.text, keywords):
            entity = to_db_mention(mention, keyword, score)
            entity.save()
            entities.append(entity)
    return entities
