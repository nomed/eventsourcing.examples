from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.domain import Aggregate, event


@dataclass
class Customer(Aggregate):
    login: str


@dataclass
class CustomerLevelsIndex(Aggregate):
    customer_id: UUID
    ref: Optional[List[UUID]]

    class Event(Aggregate.Event):
        pass

    @staticmethod
    def create_id(customer_id: UUID) -> UUID:
        return uuid5(NAMESPACE_URL, f"/customer/levels/{customer_id}")

    @event("CustomerLevelsRefAdded")
    def add_ref(self, customer_id: UUID, ref: UUID) -> None:
        assert customer_id == self.customer_id
        if self.ref == None:
            self.ref = []
        if not ref in self.ref:
            self.ref.append(ref)