# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, cast
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import Application, AggregateNotFound
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from .domainmodel import Customer, CustomerLevelsIndex
from ..levels.domainmodel import LevelCustomersIndex
from ..levels.application import Levels
from .. import utils
import example01


class Customers(Application):
    def notify2(self, new_events) -> None:
        """"""
        example01.utils.get_logger(
            example01.system).info(f"Customer[Application].notify {self}")
        for event_obj in new_events:
            example01.utils.get_logger(
                example01.system).info(f"\t==> {event_obj}")

    def register_customer(self, login: str, collect_events=False):
        customer = Customer(login)
        if not collect_events:
            self.save(customer)
        return customer

    def add_level_to_customer(self,
                              customer_id: UUID,
                              level_id: UUID,
                              collect_events=False):
        try:
            customer_levels_index = self._get_customer_levels_index(
                customer_id)
        except AggregateNotFound:
            customer_levels_index = CustomerLevelsIndex(customer_id, [])
        if level_id not in customer_levels_index.level_ids:
            customer_levels_index.add_ref(customer_id, level_id)
            if not collect_events:
                self.save(customer_levels_index)
        return customer_levels_index

    def _get_customer_levels_index(self,
                                   customer_id: UUID) -> CustomerLevelsIndex:
        return cast(
            CustomerLevelsIndex,
            self.repository.get(CustomerLevelsIndex.create_id(customer_id)))


# NOTE: this is not used
class ProcessCustomers(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """
        """
        example01.utils.get_logger(example01.system).info(
            f"ProcessCustomers[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessCustomers[ProcessApplication] ==> {domain_event}")

    @policy.register(CustomerLevelsIndex.CustomerLevelsRefAdded)
    def _(self, domain_event, process_event):
        example01.utils.get_logger(example01.system).info(
            f"ProcessCustomers[ProcessApplication] {self}")
        example01.utils.get_logger(example01.system).info(
            f"ProcessCustomers[ProcessApplication] ==> {domain_event}")
        levels = example01.utils.get_runner(example01.system).get(Levels)
        level_customers_index = levels.add_customer_to_level(
            domain_event.level_id, domain_event.customer_id, collect_events=True)
        process_event.collect_events(level_customers_index)
