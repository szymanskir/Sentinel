from sentinel.models.mentions import Mention
import json

def to_mention(data_tuple):
    _, mention_raw = data_tuple
    return json.loads(mention_raw)

def clean_mention_text(mentions, text_clean_func):
    return mentions.map(lambda x: Mention(
                             id = x.id, 
                             text = text_clean_func(x.text),
                             url = x.url,
                             creation_date = x.creation_date,
                             download_date = x.download_date,
                             source = x.source,
                             metadata = x.metadata)
                       )