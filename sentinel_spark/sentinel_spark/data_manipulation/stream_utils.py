from sentinel_common.mentions import Mention
import json


def to_mention(data_tuple):
    _, mention_raw = data_tuple
    return Mention.from_json(json.loads(mention_raw))


def clean_mention_text(mention, text_clean_func):
    return Mention(
        id=mention.id,
        text=text_clean_func(mention.text),
        url=mention.url,
        origin_date=mention.origin_date,
        download_date=mention.download_date,
        source=mention.source,
        metadata=mention.metadata,
    )
