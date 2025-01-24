

from typing import List, Optional, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class SQLClient(ABC):
    @abstractmethod
    def execute_with_select_one(self, cls: Type[T], query) -> Optional[T]:
        pass

    @abstractmethod
    def execute_with_select(self, cls: Type[T], query) -> List[T]:
        pass

    @abstractmethod
    def execute_with_commit(self, query) -> None:
        pass