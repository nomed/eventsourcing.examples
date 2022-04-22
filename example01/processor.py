# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, cast
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import Application, AggregateNotFound
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from .customers.domainmodel import Customer, CustomerLevelsIndex
from .levels.domainmodel import Level, LevelCustomersIndex
from .levels.application import Levels
import example01


class ProcessApps(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """
        """
        example01.utils.get_logger(
            example01.system).info(f"ProcessApps[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessApps[ProcessApplication] ==> {domain_event}")

    @policy.register(CustomerLevelsIndex.CustomerLevelsRefAdded)
    def _(self, domain_event, process_event):
        example01.utils.get_logger(
            example01.system).info(f"ProcessApps[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessApps[ProcessApplication] ==> {domain_event}")
        levels = example01.utils.get_runner(example01.system).get(Levels)
        level_customers_index = levels.add_customer_to_level(
            domain_event.level_id, domain_event.customer_id)
        process_event.collect_events(level_customers_index)

    @policy.register(LevelCustomersIndex.LevelCustomersRefAdded)
    def _(self, domain_event, process_event):
        example01.utils.get_logger(
            example01.system).info(f"ProcessApps[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessApps[ProcessApplication] ==> {domain_event}")
        levels = example01.utils.get_runner(example01.system).get(Levels)
        level = levels.increment_customer_count(domain_event.level_id,
                                                collect_events=True)
        process_event.collect_events(level)

    @policy.register(Level.CustomerCountIncremented)
    def _(self, domain_event, process_event):
        example01.utils.get_logger(
            example01.system).info(f"ProcessApps[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessApps[ProcessApplication] ==> {domain_event}")
        levels = example01.utils.get_runner(example01.system).get(Levels)
        level = levels.increment_customer_count(domain_event.level_id,
                                                collect_events=True)
        process_event.collect_events(level)