from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)


DB_ADDR = "http://localhost:8000"


class Mention(Model):
    class Meta:
        table_name = "mentions"
        host = DB_ADDR

    id = UnicodeAttribute(hash_key=True, null=False)
    author = UnicodeAttribute(null=False)
    text = UnicodeAttribute(null=False)
    date = UTCDateTimeAttribute(null=False)
    sentimentScore = NumberAttribute(null=False)
    keyword = UnicodeAttribute(null=False)
    user = UnicodeAttribute(null=False)


class Keyword(Model):
    class Meta:
        table_name = "keywords"
        host = DB_ADDR

    user = UnicodeAttribute(hash_key=True, null=False)
    keyword = UnicodeAttribute(range_key=True, null=False)
