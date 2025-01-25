

from abc import ABC, abstractmethod
from typing import List, Optional, Type, TypeVar

T = TypeVar("T")

class SQLClient(ABC):
    @abstractmethod
    def execute_with_select_one(self, cls: Type[T], query: str, args: Optional[tuple]) -> Optional[T]:
        pass

    @abstractmethod
    def execute_with_select(self, cls: Type[T], query: str, args: Optional[tuple]) -> List[T]:
        pass

    @abstractmethod
    def execute_with_commit(self, query, args: Optional[tuple]) -> None:
        pass

    @abstractmethod
    def check_table_exists(self, dbname) -> bool:
        pass