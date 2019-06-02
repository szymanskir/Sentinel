from sentinel_common.db_models import KeywordDb
from typing import List
from datetime import datetime


class KeywordRepository:
    def get_by_user(self, user: str) -> List[str]:
        keywords = KeywordDb.query(user)
        return [k.keyword for k in keywords]

    def get_all(self) -> List[str]:
        keywords = KeywordDb.scan()
        return list(set([k.keyword for k in keywords]))

    def add(self, keyword: str, user: str) -> None:
        model = KeywordDb(user=user, keyword=keyword, creation_date=datetime.utcnow())
        model.save()

    def delete(self, keyword: str, user: str) -> None:
        model = KeywordDb(user, keyword)
        model.delete()

    def update(self, old_keyword: str, current_keyword: str, user: str) -> None:
        self.delete(old_keyword, user)
        self.add(current_keyword, user)
