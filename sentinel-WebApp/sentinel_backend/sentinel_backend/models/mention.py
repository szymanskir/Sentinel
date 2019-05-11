from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)


class Mention(Model):
    class Meta:
        table_name = 'mentions'
        host = "http://localhost:8000"

    id = UnicodeAttribute(hash_key=True, null=False)
    author = UnicodeAttribute(null=False)
    text = UnicodeAttribute(null=False)
    date = UTCDateTimeAttribute(null=False)
    sentimentScore = NumberAttribute(null=False)
    keyword = UnicodeAttribute(null=False)
    user = UnicodeAttribute(null=False)
