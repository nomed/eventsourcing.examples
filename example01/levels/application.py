# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, cast
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import Application, AggregateNotFound, ProcessingEvent
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from .domainmodel import (Level, LevelCustomersIndex)
from ..customers.domainmodel import CustomerLevelsIndex
import example01


class Levels(Application):
    def notify2(self, new_events) -> None:
        example01.utils.get_logger(
            example01.system).info(f"Customer[Application].notify {self}")
        for event_obj in new_events:
            example01.utils.get_logger(example01.system).info(
                f"Customer[Application].notify\t>> {event_obj}")

    def register_level(self,
                       label: str,
                       customer_count: int = 0,
                       collect_events=False):
        level = Level(label)
        if not collect_events:
            self.save(level)
        return level

    def add_customer_to_level(self,
                              level_id: UUID,
                              customer_id: UUID,
                              collect_events=False):
        assert self._get_level_by_id(level_id).id == level_id
        try:
            level_customers_index = self._get_level_customers_index(level_id)
        except AggregateNotFound:
            level_customers_index = LevelCustomersIndex(level_id, [])
        if customer_id not in level_customers_index.customer_ids:
            level_customers_index.add_ref(level_id, customer_id)
            if not collect_events:
                self.save(level_customers_index)
        return level_customers_index

    def increment_customer_count(self, level_id: UUID, collect_events=False):
        level = self._get_level_by_id(level_id)
        assert level.id == level_id
        level.increment_customer()
        if not collect_events:
            self.save(level)
        return level

    def _get_level_by_id(self, level_id: UUID) -> Level:
        return cast(Level, self.repository.get(level_id))

    def _get_level_customers_index(self,
                                   level_id: UUID) -> LevelCustomersIndex:
        return cast(
            LevelCustomersIndex,
            self.repository.get(LevelCustomersIndex.create_id(level_id)))
