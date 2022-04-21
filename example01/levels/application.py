# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, cast
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import Application, AggregateNotFound, ProcessingEvent
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from .domainmodel import (Level, LevelCustomersIndex)
from ..customers.domainmodel import CustomerLevelsIndex


class Levels(Application):
    def register_level(self, label: str, customer_count: int = 0):
        level = Level(label)
        self.save(level)
        return level.id


class ProcessLevels(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(LevelCustomersIndex.LevelCustomersRefAdded)
    def _(self, domain_event, process_event):
        level = self.repository.get(domain_event.level_id)
        level.customer_count += 1
        self.save(level)

    @policy.register(CustomerLevelsIndex.CustomerLevelsRefAdded)
    def _(self, domain_event, process_event):

        try:
            level_customers_index_id = LevelCustomersIndex.create_id(
                domain_event.ref)
            level_customers_index = self.repository.get(
                level_customers_index_id)
        except AggregateNotFound:
            level_customers_index = LevelCustomersIndex(domain_event.ref, )
        level_customers_index.add_ref(domain_event.ref,
                                      domain_event.customer_id)
        #self.save(level_customers_index)
        process_event.collect_events(level_customers_index)