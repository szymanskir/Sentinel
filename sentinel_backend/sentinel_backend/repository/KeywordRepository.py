from sentinel_common.db_models import Keyword
from typing import List


class KeywordRepository:
    def get_by_user(self, user: str) -> List[str]:
        keywords = Keyword.query(user)
        return [k.keyword for k in keywords]

    def get_all(self) -> List[str]:
        keywords = Keyword.scan()
        return list(set([k.keyword for k in keywords]))

    def add(self, keyword: str, user: str) -> None:
        model = Keyword(user, keyword)
        model.save()

    def delete(self, keyword: str, user: str) -> None:
        model = Keyword(user, keyword)
        model.delete()

    def update(self, old_keyword: str, current_keyword: str, user: str) -> None:
        self.delete(old_keyword, user)
        self.add(current_keyword, user)
