from datetime import datetime
from typing import NamedTuple
from uuid import UUID, uuid4

class Mention:
    def __init__(self, text, url, creation_date, download_date, source, metadata):
        self.id = uuid4()
        self.text = text
        self.url = url
        self.creation_date = creation_date
        self.download_date = download_date
        self.source = source
        self.metadata = metadata

    # id: UUID
    # url: str
    # text: str
    # creation_date: datetime
    # download_date: datetime
    # source: str
    # metadata: any
