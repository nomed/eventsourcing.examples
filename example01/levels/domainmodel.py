from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.domain import Aggregate, event




@dataclass
class Level(Aggregate):
    label: str
    customer_count: int = 0


@dataclass
class LevelCustomersIndex(Aggregate):
    level_id: UUID
    customer_ids: Optional[List[UUID]] = None

    @staticmethod
    def create_id(level_id: UUID) -> UUID:
        return uuid5(NAMESPACE_URL, f"/level/customers/{level_id}")

    @event("LevelCustomersRefAdded")
    def add_ref(self, level_id: UUID, ref: UUID) -> None:
        assert level_id == self.level_id
        if self.customer_ids == None:
            self.customer_ids = []
        if not ref in self.customer_ids:
            self.customer_ids.append(ref)