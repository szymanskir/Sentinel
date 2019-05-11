from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Keyword(Model):
    class Meta:
        table_name = "keywords"
        host = "http://localhost:8000"

    user = UnicodeAttribute(hash_key=True, null=False)
    keyword = UnicodeAttribute(range_key=True, null=False)
